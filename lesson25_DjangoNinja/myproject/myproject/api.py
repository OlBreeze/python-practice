from ninja_extra import NinjaExtraAPI
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.controller import NinjaJWTDefaultController
from user_auth.api import auth_router
from tasks.api import router as tasks_router
from store.api import router as ecommerce_router
from movies.api import router as movies_router
from blog.api import router as blog_router
from server_monitor.api import router as server_router
from library.api import router as library_router
from institute.api import router as institute_router

# api = NinjaExtraAPI(auth=JWTAuth())
api = NinjaExtraAPI(
    title="Library API (Created by Olga and Swagger)",
    description="API для демонстрации NinjaExtraAPI",
    version="3.3.3",
    auth=JWTAuth(),
)
# api = NinjaAPI(auth=django_auth) - простой


# JWT endpoints: /api/token/pair, /api/token/refresh, /api/token/verify
api.register_controllers(NinjaJWTDefaultController)

# Кастомная аутентификация (без auth по умолчанию)
api.add_router("/auth/", tags=["Auth"], router=auth_router)

# Tasks API (защищено JWT по умолчанию)
api.add_router("/tasks", tags=["Tasks"], router=tasks_router)
api.add_router("/store", tags=["E-commerce"], router=ecommerce_router)
api.add_router("/movies", tags=["Movies Collection"], router=movies_router)
api.add_router("/blog", tags=["Blog"], router=blog_router)
api.add_router("/server", tags=["Server minitoring"], router=server_router)
api.add_router("/library", tags=["Library"], router=library_router)
api.add_router("/institute", tags=["Student Course Management"], router=institute_router)

# api = NinjaAPI(auth=django_auth)
#           Тогда всё API будет требовать аутентификацию, кроме тех маршрутов, где ты явно укажешь: auth=None
#
# @router.get("/public", auth=None)
# def public_endpoint(request):
#     return {"message": "Hello"}
