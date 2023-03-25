from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.blog.views import CategoryViewSet, PostViewSet

router = DefaultRouter()

router.register('categories', CategoryViewSet, basename='categories')
router.register('posts', PostViewSet, basename='posts')


urlpatterns = [
    path('', include(router.urls)),
]