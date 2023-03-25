from rest_framework import serializers
from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField
from .models import *


class MusicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Music
        fields = '__all__'


class ProgramSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Program)
    
    class Meta:
        model = Program
        fields = '__all__'