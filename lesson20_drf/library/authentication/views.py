from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import RegisterSerializer, UserSerializer, ChangePasswordSerializer


class RegisterView(generics.CreateAPIView):
    """
    API ендпоінт для реєстрації нових користувачів.

    POST /api/auth/register/

    Не вимагає аутентифікації. Приймає дані нового користувача та створює акаунт.
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    @swagger_auto_schema(
        operation_description="Реєстрація нового користувача",
        responses={
            201: openapi.Response(
                description="Користувач успішно зареєстрований",
                schema=UserSerializer
            ),
            400: "Помилка валідації"
        }
    )
    def post(self, request, *args, **kwargs):
        """
        Створює нового користувача.

        Args:
            request: HTTP запит з даними користувача

        Returns:
            Response з даними створеного користувача
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'message': 'Користувач успішно зареєстрований'
        }, status=status.HTTP_201_CREATED)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    API ендпоінт для перегляду та оновлення профілю користувача.

    GET /api/auth/profile/ - отримати інформацію про поточного користувача
    PUT /api/auth/profile/ - оновити інформацію про користувача
    PATCH /api/auth/profile/ - частково оновити інформацію
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Повертає поточного користувача.

        Returns:
            Об'єкт User поточного користувача
        """
        return self.request.user

    @swagger_auto_schema(
        operation_description="Отримати профіль поточного користувача"
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Оновити профіль користувача"
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Частково оновити профіль користувача"
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class ChangePasswordView(APIView):
    """
    API ендпоінт для зміни пароля користувача.

    POST /api/auth/change-password/
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Зміна пароля користувача",
        request_body=ChangePasswordSerializer,
        responses={
            200: openapi.Response(
                description="Пароль успішно змінено",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            ),
            400: "Невірний старий пароль або помилка валідації"
        }
    )
    def post(self, request):
        """
        Змінює пароль користувача.

        Args:
            request: HTTP запит зі старим та новим паролем

        Returns:
            Response з повідомленням про успішну зміну або помилку
        """
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user

            # Перевірка старого пароля
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({
                    'old_password': ['Невірний пароль']
                }, status=status.HTTP_400_BAD_REQUEST)

            # Встановлення нового пароля
            user.set_password(serializer.validated_data['new_password'])
            user.save()

            return Response({
                'message': 'Пароль успішно змінено'
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
