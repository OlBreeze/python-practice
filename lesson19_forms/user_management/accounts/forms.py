from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import UserProfile


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="Мінімум 8 символів"
    )
    password_confirm = forms.CharField(
        label="Підтвердження паролю",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label="Електронна пошта",
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        required=True
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        labels = {
            'username': "Ім'я користувача",
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

    #  Валидация полей (методы clean_...)
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Користувач з таким ім'ям вже існує.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Користувач з такою електронною поштою вже існує.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        try:
            validate_password(password)  # Использует стандартную
            # Django-функцию validate_password(),
            # которая проверяет длину, простоту, повторяемость и т.д.
        except ValidationError as e:
            raise ValidationError(e.messages)
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise ValidationError("Паролі не співпадають.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            # Створюємо профіль для нового користувача
            UserProfile.objects.create(user=user)
        return user


# Здесь важное поведение:
# super().save(commit=False) создаёт объект User, но не сохраняет его.
# user.set_password() хэширует пароль (Django хранит пароли не в открытом виде).
# Если commit=True — пользователь сохраняется в БД.
# После сохранения создаётся связанный UserProfile (вторая модель с дополнительной информацией).

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'birth_date', 'location', 'avatar']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Розкажіть про себе...'
            }),
            'birth_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Місто, країна'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            # Перевірка розміру файлу (2 МБ)
            if avatar.size > 2 * 1024 * 1024:
                raise ValidationError("Розмір зображення не повинен перевищувати 2 МБ.")

            # Перевірка типу файлу
            if not avatar.content_type.startswith('image/'):
                raise ValidationError("Завантажити можна лише зображення.")

        return avatar


class PasswordChangeForm(forms.Form):
    current_password = forms.CharField(
        label="Поточний пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password = forms.CharField(
        label="Новий пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="Мінімум 8 символів"
    )
    new_password_confirm = forms.CharField(
        label="Підтвердження нового паролю",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')
        if not self.user.check_password(current_password):
            raise ValidationError("Поточний пароль введено невірно.")
        return current_password

    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        try:
            validate_password(new_password, self.user)
        except ValidationError as e:
            raise ValidationError(e.messages)
        return new_password

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get('current_password')
        new_password = cleaned_data.get('new_password')
        new_password_confirm = cleaned_data.get('new_password_confirm')

        # Перевірка, що новий пароль відрізняється від поточного
        if current_password and new_password and current_password == new_password:
            raise ValidationError("Новий пароль повинен відрізнятися від поточного.")

        # Перевірка, що паролі співпадають
        if new_password and new_password_confirm and new_password != new_password_confirm:
            raise ValidationError("Нові паролі не співпадають.")

        return cleaned_data

    def save(self):
        self.user.set_password(self.cleaned_data['new_password'])
        self.user.save()
        return self.user
