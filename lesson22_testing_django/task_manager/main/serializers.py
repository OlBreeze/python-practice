from datetime import date

from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'user']
        read_only_fields = ['id']

    def validate_due_date(self, value):
        if value < date.today():
            raise serializers.ValidationError(
                "Дата виконання не може бути в минулому"
            )
        return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class TaskWithUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'user']

    def validate_due_date(self, value):
        if value < date.today():
            raise serializers.ValidationError(
                "Дата виконання не може бути в минулому"
            )
        return value

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        task = Task.objects.create(user=user, **validated_data)
        return task
