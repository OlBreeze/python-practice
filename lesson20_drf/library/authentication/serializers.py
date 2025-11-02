from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator


class RegisterSerializer(serializers.ModelSerializer):
    """
    Серіалізатор для реєстрації нових користувачів.

    Fields:
        username: Унікальне ім'я користувача
        email: Унікальна email адреса
        password: Пароль (тільки для запису)
        password2: Підтвердження пароля (тільки для запису)
        first_name: Ім'я користувача (опціонально)
        last_name: Прізвище користувача (опціонально)
    """
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        label='Підтвердження пароля'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name']
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False}
        }

    def validate(self, attrs):
        """
        Перевірка співпадіння паролів.

        Args:
            attrs: Словник з атрибутами

        Returns:
            Валідовані атрибути

        Raises:
            ValidationError: Якщо паролі не співпадають
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "password": "Паролі не співпадають"
            })
        return attrs

    # ⬇️ ЦЕЙ МЕТОД ВІДСУТНІЙ У ВАШОМУ КОДІ!
    def create(self, validated_data):
        """
        Створення нового користувача.

        Args:
            validated_data: Валідовані дані

        Returns:
            Створений об'єкт User
        """
        # Видаляємо password2, оскільки воно не є полем моделі User
        validated_data.pop('password2')

        # Використовуємо create_user для правильного хешування пароля
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Серіалізатор для відображення інформації про користувача.
    """
    books_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'books_count', 'is_staff']
        read_only_fields = ['id', 'is_staff']

    def get_books_count(self, obj):
        """
        Отримує кількість книг користувача.

        Args:
            obj: Об'єкт User

        Returns:
            Кількість книг користувача
        """
        return obj.books.count()


class ChangePasswordSerializer(serializers.Serializer):
    """
    Серіалізатор для зміни пароля.
    """
    old_password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    new_password2 = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        """
        Перевірка співпадіння нових паролів.
        """
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({
                "new_password": "Нові паролі не співпадають"
            })
        return attrs