from rest_framework import serializers
from .models import TodoList
from django.contrib.auth.models import User


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoList
        fields = ("title", "body", "userid")

    def __init__(self, *args, **kwargs):
        super(TodoSerializer, self).__init__(*args, **kwargs)
        self.fields["userid"] = serializers.HiddenField(default="")


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "email")

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["username"], validated_data["email"], validated_data["password"]
        )
        return user
