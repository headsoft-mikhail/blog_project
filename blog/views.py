from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django.contrib.auth.models import User
from blog.models import Post, UserSubscription
from blog.serializers import PostsSerializer, UserSerializer, SubscriptionsSerializer
from blog.permissions import IsOwnerOrAdmin
from blog.filters import PostsFilter
from django_filters import rest_framework as filters


class PostsViewSet(ModelViewSet):
    """ViewSet для постов."""
    queryset = Post.objects.select_related('owner').order_by('-created_at')
    serializer_class = PostsSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = PostsFilter

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create"]:
            return [IsAuthenticated()]
        elif self.action in ["update", "partial_update", "destroy"]:
            return [IsOwnerOrAdmin()]
        else:
            return []


class UsersViewSet(ReadOnlyModelViewSet):
    """ViewSet для пользователей."""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SubscriptionsViewSet(ModelViewSet):
    """ViewSet для подписок."""
    serializer_class = SubscriptionsSerializer
    queryset = UserSubscription.objects.none()

    def get_queryset(self):
        user = self.request.user
        if user.id is None:  # AnonymousUser
            return UserSubscription.objects.none()
        else:
            queryset = UserSubscription.objects.filter(owner=user).order_by('id')
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create"]:
            return [IsAuthenticated()]
        elif self.action in ["destroy"]:
            return [IsOwnerOrAdmin()]
        else:
            return []


class FeedViewSet(ReadOnlyModelViewSet):
    """Получение ленты."""
    serializer_class = PostsSerializer
    queryset = Post.objects.none()

    def get_queryset(self):
        user = self.request.user
        if user.id is None:  # AnonymousUser
            return Post.objects.none()
        else:
            authors = UserSubscription.objects.filter(owner=user).values_list('author', flat=True)
            queryset = Post.objects.none()
            for author_id in authors:
                queryset = queryset | (Post.objects.filter(owner=author_id))
            queryset = queryset.order_by('-created_at')
            return queryset

