from django.db import models
from django.conf import settings


class Post(models.Model):
    """Посты"""
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.TextField(max_length=150)
    text = models.TextField(max_length=1000)


class UserSubscription(models.Model):
    """Подписки"""
    class Meta:
        unique_together = ("owner", "author")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='subscriptions', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='subscribers', on_delete=models.CASCADE)


class NotViewedPost(models.Model):
    """Непросмотренные посты"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)



