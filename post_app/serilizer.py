from .models import *
from rest_framework import serializers


class PostModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = ('id','title', 'body', 'author')
        extra_kwargs = {'title': {'required': True}, 'body': {'required': True}}