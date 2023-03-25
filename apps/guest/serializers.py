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


class PostRetrieveSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Post)
    categories = CategorySerializer(many=True)

    
    class Meta:
        model = Post
        fields = '__all__'
        