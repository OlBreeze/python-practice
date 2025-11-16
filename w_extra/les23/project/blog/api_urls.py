from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import ArticleViewSet, CommentViewSet, TagViewSet, UserViewSet

router = DefaultRouter()
router.register(r'articles', ArticleViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'tags', TagViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]