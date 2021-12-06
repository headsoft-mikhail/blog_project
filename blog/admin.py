from django.contrib import admin
from .models import Post, UserSubscription


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass

@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    pass

