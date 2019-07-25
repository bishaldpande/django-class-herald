# serializers.py

from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Blog


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class BlogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Blog
        fields = ('id', 'url', 'title', 'description', 'created_date', 'author')