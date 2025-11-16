# blog/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import re
from .models import Article, Comment, CustomUser, Tag


# ========== ЗАВДАННЯ 10: Кастомні поля форм ==========
class HexColorField(forms.CharField):
    """Кастомне поле для перевірки HEX-коду кольору"""

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 7
        super().__init__(*args, **kwargs)
        self.widget.attrs.update({'placeholder': '#RRGGBB'})

    def validate(self, value):
        super().validate(value)
        if value and not re.match(r'^#[0-9A-Fa-f]{6}$', value):
            raise ValidationError(
                'Введіть правильний HEX-код кольору (наприклад, #FF5733)'
            )


class PhoneNumberFormField(forms.CharField):
    """Кастомне поле форми для телефонного номера"""

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 13
        super().__init__(*args, **kwargs)
        self.widget.attrs.update({'placeholder': '+380XXXXXXXXX'})

    def validate(self, value):
        super().validate(value)
        if value and not re.match(r'^\+380\d{9}$', value):
            raise ValidationError(
                'Телефон повинен бути у форматі +380XXXXXXXXX'
            )


# ========== ЗАВДАННЯ 2: Кастомні віджети ==========
class ColorPickerWidget(forms.TextInput):
    """Кастомний віджет для вибору кольору"""

    input_type = 'color'

    def __init__(self, attrs=None):
        default_attrs = {'class': 'color-picker'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)


class TagSelectWidget(forms.SelectMultiple):
    """Кастомний віджет для вибору тегів з пошуком"""

    template_name = 'widgets/tag_select.html'

    def __init__(self, attrs=None):
        default_attrs = {
            'class': 'tag-select',
            'data-placeholder': 'Виберіть теги...'
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)


class RichTextWidget(forms.Textarea):
    """Кастомний віджет для богатого текстового редактора"""

    def __init__(self, attrs=None):
        default_attrs = {
            'class': 'rich-text-editor',
            'rows': 10,
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)


# ========== ЗАВДАННЯ 2: Кастомні валідатори ==========
def validate_no_profanity(value):
    """Валідатор для перевірки на нецензурну лексику"""
    profanity_words = ['badword1', 'badword2', 'badword3']  # Додайте реальні слова
    for word in profanity_words:
        if word.lower() in value.lower():
            raise ValidationError(
                f'Текст містить недопустимі слова. Будь ласка, перефразуйте.'
            )


def validate_min_words(min_words=10):
    """Валідатор для перевірки мінімальної кількості слів"""

    def validator(value):
        word_count = len(value.split())
        if word_count < min_words:
            raise ValidationError(
                f'Текст повинен містити принаймні {min_words} слів. '
                f'Зараз: {word_count} слів.'
            )

    return validator


def validate_slug_unique(value):
    """Валідатор для перевірки унікальності slug"""
    if Article.objects.filter(slug=value).exists():
        raise ValidationError('Стаття з таким URL вже існує.')


# ========== ЗАВДАННЯ 2 та 6: Форми з кастомною валідацією ==========
class ArticleForm(forms.ModelForm):
    """Форма створення/редагування статті"""

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=TagSelectWidget(),
        label="Теги"
    )

    theme_color = HexColorField(
        required=False,
        label="Колір теми статті"
    )

    class Meta:
        model = Article
        fields = ['title', 'slug', 'content', 'status', 'metadata']
        widgets = {
            'content': RichTextWidget(),
            'slug': forms.TextInput(attrs={'class': 'slug-field'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Додаємо кастомні валідатори
        self.fields['content'].validators.append(validate_no_profanity)
        self.fields['content'].validators.append(validate_min_words(50))

        if not self.instance.pk:
            self.fields['slug'].validators.append(validate_slug_unique)

    def clean_title(self):
        """Кастомна валідація заголовку"""
        title = self.cleaned_data.get('title')
        if title and len(title) < 10:
            raise ValidationError(
                'Заголовок повинен містити принаймні 10 символів.'
            )

        # Перевірка на дублікати заголовків
        if Article.objects.filter(title__iexact=title).exclude(
                pk=self.instance.pk if self.instance else None
        ).exists():
            raise ValidationError(
                'Стаття з таким заголовком вже існує.'
            )

        return title

    def clean_slug(self):
        """Валідація slug"""
        slug = self.cleaned_data.get('slug')
        if slug:
            # Перевірка формату slug
            if not re.match(r'^[-\w]+$', slug):
                raise ValidationError(
                    'URL може містити тільки літери, цифри, дефіси та підкреслення.'
                )
        return slug

    def clean(self):
        """Загальна валідація форми"""
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        content = cleaned_data.get('content')

        # Перевірка що опубліковані статті мають достатньо контенту
        if status == 'published' and content and len(content) < 100:
            raise ValidationError(
                'Опубліковані статті повинні містити принаймні 100 символів.'
            )

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Обробка metadata з theme_color
        theme_color = self.cleaned_data.get('theme_color')
        if theme_color:
            if not instance.metadata:
                instance.metadata = {}
            instance.metadata['theme_color'] = theme_color

        if commit:
            instance.save()
            self.save_m2m()

            # Зберігаємо теги
            tags = self.cleaned_data.get('../templates/blog/tags', [])
            instance.tags.set(tags)

        return instance


class CustomUserRegistrationForm(UserCreationForm):
    """Форма реєстрації з кастомною валідацією"""

    email = forms.EmailField(
        required=True,
        label="Email"
    )
    phone_number = PhoneNumberFormField(
        required=False,
        label="Номер телефону"
    )
    birth_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Дата народження"
    )
    terms_accepted = forms.BooleanField(
        required=True,
        label="Я погоджуюсь з умовами використання"
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'birth_date',
                  'password1', 'password2', 'terms_accepted']

    def clean_email(self):
        """Валідація email на унікальність"""
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError(
                'Користувач з таким email вже зареєстрований.'
            )
        return email

    def clean_username(self):
        """Валідація username"""
        username = self.cleaned_data.get('username')

        # Перевірка довжини
        if len(username) < 3:
            raise ValidationError(
                'Ім\'я користувача повинно містити принаймні 3 символи.'
            )

        # Перевірка на спеціальні символи
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise ValidationError(
                'Ім\'я користувача може містити тільки літери, цифри та підкреслення.'
            )

        return username

    def clean_password2(self):
        """Додаткова валідація паролю"""
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError('Паролі не співпадають.')

        # Перевірка складності паролю
        if password2:
            if len(password2) < 8:
                raise ValidationError(
                    'Пароль повинен містити принаймні 8 символів.'
                )
            if not any(char.isdigit() for char in password2):
                raise ValidationError(
                    'Пароль повинен містити принаймні одну цифру.'
                )
            if not any(char.isupper() for char in password2):
                raise ValidationError(
                    'Пароль повинен містити принаймні одну велику літеру.'
                )

        return password2

    def clean_birth_date(self):
        """Валідація дати народження"""
        from datetime import date
        birth_date = self.cleaned_data.get('birth_date')

        if birth_date:
            today = date.today()
            age = today.year - birth_date.year - (
                    (today.month, today.day) < (birth_date.month, birth_date.day)
            )

            if age < 13:
                raise ValidationError(
                    'Вам повинно бути принаймні 13 років для реєстрації.'
                )
            if age > 120:
                raise ValidationError(
                    'Будь ласка, введіть правильну дату народження.'
                )

        return birth_date


class CommentForm(forms.ModelForm):
    """Форма коментаря"""

    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Напишіть ваш коментар...'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].validators.append(validate_no_profanity)

    def clean_content(self):
        """Валідація контенту коментаря"""
        content = self.cleaned_data.get('content')

        if len(content) < 3:
            raise ValidationError(
                'Коментар повинен містити принаймні 3 символи.'
            )

        if len(content) > 1000:
            raise ValidationError(
                'Коментар не може перевищувати 1000 символів.'
            )

        return content