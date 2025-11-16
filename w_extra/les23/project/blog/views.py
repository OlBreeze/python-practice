from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.db.models import Q, Count
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Article, Comment, Tag
from .forms import ArticleForm, CommentForm


class ArticleListView(ListView):
    """Кастомне відображення списку статей"""

    model = Article
    template_name = 'blog/article_list.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        queryset = Article.objects.filter(status='published').select_related(
            'author'
        ).prefetch_related('tags', 'comments')

        # Пошук
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query)
            )

        # Фільтр за тегом
        tag = self.request.GET.get('tag')
        if tag:
            queryset = queryset.filter(tags__name=tag)

        # Сортування
        sort = self.request.GET.get('sort', '-created_at')
        allowed_sorts = ['-created_at', 'created_at', '-views_count', 'views_count']
        if sort in allowed_sorts:
            queryset = queryset.order_by(sort)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['current_tag'] = self.request.GET.get('tag', '')
        context['current_sort'] = self.request.GET.get('sort', '-created_at')
        return context


class ArticleDetailView(FormMixin, DetailView):
    """Кастомне відображення деталей статті з формою коментарів"""

    model = Article
    template_name = 'blog/article_detail.html'
    context_object_name = 'article'
    form_class = CommentForm

    def get_queryset(self):
        return Article.objects.filter(
            status='published'
        ).select_related('author').prefetch_related(
            'tags',
            'comments__author',
            'comments__replies'
        )

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Збільшуємо лічильник переглядів
        obj.increment_views()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.get_object()

        # Коментарі першого рівня
        context['comments'] = article.comments.filter(
            parent=None,
            is_approved=True
        ).select_related('author').prefetch_related('replies')

        # Статистика
        context['statistics'] = article.get_statistics()

        # Схожі статті
        context['related_articles'] = self.get_related_articles(article)

        # Хлібні крихти
        context['breadcrumbs'] = [
            {'title': 'Головна', 'url': '/'},
            {'title': 'Статті', 'url': '/articles/'},
            {'title': article.title, 'url': ''},
        ]

        return context

    def get_related_articles(self, article, count=3):
        """Отримати схожі статті за тегами"""
        article_tags = article.tags.all()
        if not article_tags:
            return Article.objects.none()

        related = Article.objects.filter(
            tags__in=article_tags,
            status='published'
        ).exclude(id=article.id).annotate(
            same_tags=Count('tags')
        ).order_by('-same_tags', '-views_count')[:count]

        return related

    def post(self, request, *args, **kwargs):
        """Обробка POST запиту (додавання коментаря)"""
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Необхідна авторизація'}, status=401)

        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        """Збереження коментаря"""
        comment = form.save(commit=False)
        comment.article = self.get_object()
        comment.author = self.request.user

        # Перевірка на відповідь до іншого коментаря
        parent_id = self.request.POST.get('parent_id')
        if parent_id:
            comment.parent_id = parent_id

        comment.save()

        return redirect(self.get_object().get_absolute_url())


class ArticleCreateView(LoginRequiredMixin, CreateView):
    """Створення нової статті"""

    model = Article
    form_class = ArticleForm
    template_name = 'blog/article_form.html'
    success_url = reverse_lazy('blog:article_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Редагування статті"""

    model = Article
    form_class = ArticleForm
    template_name = 'blog/article_form.html'

    def test_func(self):
        """Перевірка що користувач є автором"""
        article = self.get_object()
        return self.request.user == article.author or self.request.user.is_staff

    def get_success_url(self):
        return self.object.get_absolute_url()


class TaggedArticlesView(ListView):
    """Відображення статей за тегом"""

    model = Article
    template_name = 'blog/tagged_articles.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, name=self.kwargs['tag_name'])
        return Article.objects.filter(
            tags=self.tag,
            status='published'
        ).select_related('author').order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        context['tag_article_count'] = self.tag.get_article_count()
        return context


class SearchView(ListView):
    """Пошук статей"""

    model = Article
    template_name = 'blog/search_results.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q', '')

        if not query:
            return Article.objects.none()

        return Article.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__username__icontains=query),
            status='published'
        ).select_related('author').distinct().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['result_count'] = self.get_queryset().count()
        return context


class UserArticlesView(ListView):
    """Відображення статей конкретного автора"""

    model = Article
    template_name = 'blog/user_articles.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        from .models import CustomUser
        self.author = get_object_or_404(CustomUser, username=self.kwargs['username'])

        queryset = Article.objects.filter(
            author=self.author,
            status='published'
        ).select_related('author').order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.author
        context['author_article_count'] = self.get_queryset().count()
        return context