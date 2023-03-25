# models
from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.text import slugify


class Category(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=255, verbose_name=_('Name')),
    )
    slug = models.SlugField(max_length=255, verbose_name=_('Slug'))

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class Post(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=300, verbose_name=_('Sarlavha')),
        description = models.CharField(max_length=1000, verbose_name=_('Maqola haqida qisqacha')),
        content = models.TextField(verbose_name=_('Maqola')),
    )
    categories = models.ManyToManyField(Category, verbose_name=_('Kategoriyalar'))
    image = models.ImageField(upload_to='post_images', verbose_name=_('Rasm'))
    created_at = models.DateTimeField(verbose_name=_('Created at'))
    updated_at = models.DateTimeField(verbose_name=_('Updated at'))
    is_featured = models.BooleanField(default=False, verbose_name=_('Maxus post'))
    slug = models.SlugField(max_length=255, verbose_name=_('Slug'))
    views = models.IntegerField(default=0, verbose_name=_('Ko\'rilganlar soni'))

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = _('Maqola')
        verbose_name_plural = _('Maqolalar')
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            super(Post, self).save(*args, **kwargs)

# serializer

from rest_framework import serializers
from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField
from apps.blog.models import Category, Post


class CategorySerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Category)

    class Meta:
        model = Category
        fields = '__all__'
        ref_name = 'CategorySerializer'


class PostSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Post)
    categories = CategorySerializer(many=True)
    
    class Meta:
        model = Post
        fields = '__all__'
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        for lang in data['translations']:
            data['translations'][lang]['content'] = ''
        return data


class PostRetrieveSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Post)
    categories = CategorySerializer(many=True)

    
    class Meta:
        model = Post
        fields = '__all__'

# viows


from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from apps.blog.models import Category, Post
from apps.blog.serializers import CategorySerializer, PostSerializer, PostRetrieveSerializer
from apps.blog.filters import PostFilter


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    http_method_names = ['get', 'head', 'options']
    lookup_field = 'slug'

    @action(detail=True, methods=['get', 'head', 'options'])
    def posts(self, request, slug=None):
        category = self.get_object()
        if not category:
            return Response(status=status.HTTP_404_NOT_FOUND)
        pagination = self.paginate_queryset(category.post_set.all())
        if pagination is not None:
            serializer = PostSerializer(pagination, many=True)
            return self.get_paginated_response(serializer.data)
        queryset = category.post_set.all()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-updated_at')
    serializer_class = PostSerializer
    http_method_names = ['get', 'head', 'options']
    filterset_class = PostFilter

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PostRetrieveSerializer
        return super().get_serializer_class()
    
    def retrieve(self, request, *args, **kwargs):
        saved_views = request.session.get('views', [])
        post = self.get_object()
        if post.id not in saved_views:
            post.views += 1
            post.save()
            saved_views.append(post.id)
            request.session['views'] = saved_views
        return super().retrieve(request, *args, **kwargs)
    

# urls


from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.blog.views import CategoryViewSet, PostViewSet

router = DefaultRouter()

router.register('categories', CategoryViewSet, basename='categories')
router.register('posts', PostViewSet, basename='posts')


urlpatterns = [
    path('', include(router.urls)),
]
    



