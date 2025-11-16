# ========== ЗАВДАННЯ 7: REST API та DRF ==========
# blog/serializers.py

from rest_framework import serializers
from .models import Article, Comment, Tag, CustomUser


class UserSerializer(serializers.ModelSerializer):
    """Серіалізатор користувача"""

    article_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'phone_number',
            'bio', 'avatar', 'article_count', 'date_joined'
        ]
        read_only_fields = ['id', 'date_joined']


class TagSerializer(serializers.ModelSerializer):
    """Серіалізатор тегу"""

    article_count = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ['id', 'name', 'article_count']

    def get_article_count(self, obj):
        return obj.articles.filter(status='published').count()


class CommentSerializer(serializers.ModelSerializer):
    """Серіалізатор коментаря"""

    author = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id', 'article', 'author', 'content',
            'parent', 'is_approved', 'created_at', 'replies'
        ]
        read_only_fields = ['id', 'author', 'created_at']

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(
                obj.replies.filter(is_approved=True),
                many=True
            ).data
        return []


class ArticleListSerializer(serializers.ModelSerializer):
    """Серіалізатор для списку статей (без контенту)"""

    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comment_count = serializers.IntegerField(read_only=True)
    reading_time = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'slug', 'author', 'status',
            'tags', 'views_count', 'comment_count',
            'reading_time', 'created_at', 'updated_at'
        ]

    def get_reading_time(self, obj):
        return obj.get_reading_time()


class ArticleDetailSerializer(serializers.ModelSerializer):
    """Серіалізатор для деталей статті з вкладеними полями"""

    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comments = serializers.SerializerMethodField()
    statistics = serializers.SerializerMethodField()
    related_articles = serializers.SerializerMethodField()

    # Додаткові поля для створення/оновлення
    tag_names = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'slug', 'author', 'content',
            'status', 'metadata', 'tags', 'tag_names',
            'views_count', 'comments', 'statistics',
            'related_articles', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'author', 'views_count', 'created_at', 'updated_at']

    def get_comments(self, obj):
        """Отримати коментарі першого рівня"""
        comments = obj.comments.filter(
            parent=None,
            is_approved=True
        ).select_related('author')
        return CommentSerializer(comments, many=True).data

    def get_statistics(self, obj):
        """Отримати статистику статті"""
        return obj.get_statistics()

    def get_related_articles(self, obj):
        """Отримати схожі статті"""
        article_tags = obj.tags.all()
        if not article_tags:
            return []

        from django.db.models import Count
        related = Article.objects.filter(
            tags__in=article_tags,
            status='published'
        ).exclude(id=obj.id).annotate(
            same_tags=Count('tags')
        ).order_by('-same_tags', '-views_count')[:3]

        return ArticleListSerializer(related, many=True).data

    def create(self, validated_data):
        """Створення статті з тегами"""
        tag_names = validated_data.pop('tag_names', [])
        article = Article.objects.create(**validated_data)

        # Створення/додавання тегів
        for tag_name in tag_names:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            article.tags.add(tag)

        return article

    def update(self, instance, validated_data):
        """Оновлення статті з тегами"""
        tag_names = validated_data.pop('tag_names', None)

        # Оновлення полів статті
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Оновлення тегів
        if tag_names is not None:
            instance.tags.clear()
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                instance.tags.add(tag)

        return instance
