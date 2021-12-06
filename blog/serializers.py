from rest_framework import serializers
from blog.models import Post, UserSubscription
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'subscriptions', 'subscribers')


class PostsSerializer(serializers.ModelSerializer):
    """Serializer для постов."""
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('owner', 'title', 'text', 'created_at')


class SubscriptionsSerializer(serializers.ModelSerializer):
    """Serializer для подписок."""
    owner = UserSerializer(read_only=True)

    class Meta:
        model = UserSubscription
        fields = ['owner', 'author']


