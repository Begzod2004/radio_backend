from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
router = DefaultRouter()

router.register('music', MusicViewSet, basename='musics')
router.register('program', ProgramViewSet, basename='Programs')


urlpatterns = [
    path('', include(router.urls)),
]