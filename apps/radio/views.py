from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *



class MusicViewSet(viewsets.ModelViewSet):
    queryset = Music.objects.all()
    serializer_class = MusicSerializer
    http_method_names = ['get', 'head', 'options']

# pagination qilib qoiyldi oldindan


    # @action(detail=True, methods=['get', 'head', 'options'])
    # def posts(self, request, slug=None):
    #     category = self.get_object()
    #     if not category:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    #     pagination = self.paginate_queryset(category.post_set.all())
    #     if pagination is not None:
    #         serializer = MusicSerializer(pagination, many=True)
    #         return self.get_paginated_response(serializer.data)
    #     queryset = category.post_set.all()
    #     serializer = MusicSerializer(queryset, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)


class ProgramViewSet(viewsets.ModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    http_method_names = ['get', 'head', 'options']