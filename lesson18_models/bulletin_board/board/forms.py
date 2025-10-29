"""
Форми для додатку board.

Містить ModelForm для створення та редагування оголошень.
"""

from django import forms
from django.core.exceptions import ValidationError
from .models import Ad, Category, Comment


class AdForm(forms.ModelForm):
    """
    Форма для створення та редагування оголошення.
    """

    class Meta:
        model = Ad
        fields = ['title', 'description', 'price', 'category', 'is_active']

        # Локалізовані назви полів
        labels = {
            'title': 'Заголовок',
            'description': 'Опис',
            'price': 'Ціна (грн)',
            'category': 'Категорія',
            'is_active': 'Активне оголошення',
        }

        # Текст підказок
        help_texts = {
            'title': 'Введіть короткий і зрозумілий заголовок (максимум 200 символів)',
            'description': 'Детально опишіть товар або послугу',
            'price': 'Вкажіть ціну в гривнях',
            'category': 'Оберіть відповідну категорію',
            'is_active': 'Зніміть галочку, щоб приховати оголошення',
        }

        # Тексти помилок
        error_messages = {
            'title': {
                'required': 'Заголовок є обов\'язковим полем',
                'max_length': 'Заголовок занадто довгий (максимум 200 символів)',
            },
            'description': {
                'required': 'Опис є обов\'язковим полем',
            },
            'price': {
                'required': 'Ціна є обов\'язковим полем',
                'invalid': 'Введіть коректну ціну',
            },
            'category': {
                'required': 'Оберіть категорію',
            },
        }

        # Віджети (стилізація полів)
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Наприклад: iPhone 15 Pro 256GB',
                'maxlength': '200',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Опишіть стан, комплектацію, особливості...',
                'rows': 5,
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'min': '0',
                'step': '0.01',
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }

    def __init__(self, *args, **kwargs):
        """
        Ініціалізація форми з додатковими налаштуваннями.
        """
        super().__init__(*args, **kwargs)

        # Встановити is_active=True за замовчуванням для нових оголошень
        if not self.instance.pk:
            self.initial['is_active'] = True

        # Додати порожній варіант для категорії
        self.fields['category'].empty_label = '-- Оберіть категорію --'

        # Зробити всі поля обов'язковими (крім is_active)
        for field_name, field in self.fields.items():
            if field_name != 'is_active':
                field.required = True

    def clean_title(self):
        """
        Валідація заголовку.
        """
        title = self.cleaned_data.get('title')

        # Перевірка на мінімальну довжину
        if len(title) < 5:
            raise ValidationError(
                'Заголовок занадто короткий (мінімум 5 символів)'
            )

        # Перевірка на заборонені слова (приклад)
        forbidden_words = ['спам', 'обман', 'шахрайство']
        if any(word in title.lower() for word in forbidden_words):
            raise ValidationError(
                'Заголовок містить заборонені слова'
            )

        return title

    def clean_price(self):
        """
        Валідація ціни.
        """
        price = self.cleaned_data.get('price')

        # Перевірка на мінімальну ціну
        if price is not None and price < 0:
            raise ValidationError('Ціна не може бути від\'ємною')

        # Перевірка на максимальну ціну
        if price is not None and price > 1000000:
            raise ValidationError('Ціна занадто велика (максимум 1,000,000 грн)')

        return price

    def clean(self):
        """
        Загальна валідація форми.
        """
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        description = cleaned_data.get('description')

        # Перевірка: опис не повинен дублювати заголовок
        if title and description and title.lower() == description.lower():
            raise ValidationError(
                'Опис не може повністю дублювати заголовок'
            )

        return cleaned_data


class AdCreateForm(AdForm):
    """
    Форма для створення нового оголошення (розширена версія).
    """

    class Meta(AdForm.Meta):
        fields = ['title', 'description', 'price', 'category']
        # is_active не включаємо - буде True автоматично

    def save(self, commit=True, user=None):
        """
        Зберегти оголошення з прив'язкою до користувача.
        """
        instance = super().save(commit=False)

        # Встановити користувача
        if user:
            instance.user = user

        # Встановити is_active=True
        instance.is_active = True

        if commit:
            instance.save()

        return instance


class AdUpdateForm(AdForm):
    """
    Форма для редагування існуючого оголошення.
    """

    class Meta(AdForm.Meta):
        # Включаємо всі поля, включно з is_active
        fields = ['title', 'description', 'price', 'category', 'is_active']


class AdSearchForm(forms.Form):
    """
    Форма для пошуку оголошень.
    """

    query = forms.CharField(
        label='Пошук',
        required=False,
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введіть ключові слова...',
        })
    )

    category = forms.ModelChoiceField(
        label='Категорія',
        queryset=Category.objects.all(),
        required=False,
        empty_label='Всі категорії',
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )

    min_price = forms.DecimalField(
        label='Мін. ціна',
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'від',
        })
    )

    max_price = forms.DecimalField(
        label='Макс. ціна',
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'до',
        })
    )

    only_active = forms.BooleanField(
        label='Тільки активні',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        })
    )

    def clean(self):
        """
        Валідація форми пошуку.
        """
        cleaned_data = super().clean()
        min_price = cleaned_data.get('min_price')
        max_price = cleaned_data.get('max_price')

        # Перевірка: мінімальна ціна не більша за максимальну
        if min_price and max_price and min_price > max_price:
            raise ValidationError(
                'Мінімальна ціна не може бути більшою за максимальну'
            )

        return cleaned_data


class CommentForm(forms.ModelForm):
    """
    Форма для додавання коментаря до оголошення.
    """

    class Meta:
        model = Comment
        fields = ['content']

        labels = {
            'content': 'Ваш коментар',
        }

        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Напишіть свій коментар...',
                'rows': 3,
            }),
        }

    def clean_text(self):
        """
        Валідація тексту коментаря.
        """
        text = self.cleaned_data.get('content')

        # Перевірка на мінімальну довжину
        if len(text) < 3:
            raise ValidationError(
                'Коментар занадто короткий (мінімум 3 символи)'
            )

        # Перевірка на максимальну довжину
        if len(text) > 1000:
            raise ValidationError(
                'Коментар занадто довгий (максимум 1000 символів)'
            )

        return text


class CategoryForm(forms.ModelForm):
    """
    Форма для створення/редагування категорії (для адміністраторів).
    """

    class Meta:
        model = Category
        fields = ['name', 'description']

        labels = {
            'name': 'Назва категорії',
            'description': 'Опис категорії',
        }

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Наприклад: Електроніка',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Опис категорії...',
                'rows': 3,
            }),
        }

    def clean_name(self):
        """
        Валідація назви категорії.
        """
        name = self.cleaned_data.get('name')

        # Перевірка на унікальність (якщо це нова категорія)
        if not self.instance.pk:
            if Category.objects.filter(name__iexact=name).exists():
                raise ValidationError(
                    f'Категорія "{name}" вже існує'
                )

        return name