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
    
