from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Task


authors_name = serializers.ReadOnlyField(source='owner.username')


'''class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')
'''


class UserSerializer(serializers.ModelSerializer):
    #snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Task.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'password')


class TaskSerializer(serializers.ModelSerializer):
    authors_name = UserSerializer()
    class Meta:
        model = Task
        fields = ('slug1', 'intro_text', 'authors_name', 'pub_date', 'end_date', 'id')
