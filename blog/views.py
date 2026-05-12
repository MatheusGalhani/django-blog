from django.shortcuts import render
from rest_framework import viewsets, permissions, mixins, status
from rest_framework.response import Response

from blog.keys import get_blogpost_cache_key
from blog.models import BlogPost, User
from blog.serializers import BlogPostSerializer, UserSerializer
from core.throttling import FivePerMinuteRateThrottle, PaginationMinuteUserRateThrottle
from utils.cache import get_cache, set_cache

# Create your views here.


class CreateUserView(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        from utils.random import get_random_key
        data = request.data.copy()
        if 'username' not in data or not data['username']:
            data['username'] = f"{data['first_name'].lower()}-{get_random_key()}"

        serializer = self.get_serializer(
            data=data, many=False, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogPostViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, 
                      mixins.CreateModelMixin, mixins.RetrieveModelMixin, 
                      mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = BlogPost.objects.select_related('author').all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [PaginationMinuteUserRateThrottle]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['author_id'] = request.user.id
        serializer = self.get_serializer(
            data=data, many=False, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        if instance.author_id != request.user.id:
            return Response({'detail': 'You do not have permission to edit this post.'}, status=status.HTTP_403_FORBIDDEN)
        
        data = request.data.copy()
        data['author_id'] = request.user.id
        serializer = self.get_serializer(
            instance, data=data, partial=partial, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            key = get_blogpost_cache_key(kwargs['pk'])
            set_cache(key, serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, *args, **kwargs):
        key = get_blogpost_cache_key(kwargs['pk'])
        if (cached_data := get_cache(key)) is not None:
            return Response(cached_data, status=status.HTTP_200_OK)
        
        instance = self.get_object()
        serializer = self.serializer_class(instance)
        cached_data = serializer.data
        set_cache(key, cached_data)
        return Response(cached_data, status=status.HTTP_200_OK)