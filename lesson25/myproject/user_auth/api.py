from ninja import Router
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from ninja_jwt.tokens import RefreshToken
from .schemas import RegisterSchema, LoginSchema, TokenSchema, ErrorSchema

auth_router = Router()


@auth_router.post("/register", response={200: TokenSchema, 400: ErrorSchema}, auth=None)
def register(request, data: RegisterSchema):
    """
    Регистрация нового пользователя
    """
    if User.objects.filter(username=data.username).exists():
        return 400, {"error": "Пользователь уже существует"}

    if User.objects.filter(email=data.email).exists():
        return 400, {"error": "Email уже используется"}

    user = User.objects.create(
        username=data.username,
        email=data.email,
        password=make_password(data.password),
        first_name=data.first_name,
        last_name=data.last_name
    )

    refresh = RefreshToken.for_user(user)

    return 200, {
        "access": str(refresh.access_token),
        "refresh": str(refresh)
    }


@auth_router.post("/login", response={200: TokenSchema, 401: ErrorSchema}, auth=None)
def login(request, data: LoginSchema):
    """
    Вход пользователя
    """
    user = authenticate(
        username=data.username,
        password=data.password
    )

    if user is None:
        return 401, {"error": "Неверные учетные данные"}

    refresh = RefreshToken.for_user(user)

    return 200, {
        "access": str(refresh.access_token),
        "refresh": str(refresh)
    }