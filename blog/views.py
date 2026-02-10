from django.shortcuts import render
from rest_framework import viewsets, permissions, mixins, status
from rest_framework.response import Response

from blog.models import BlogPost, User
from blog.serializers import BlogPostSerializer, UserSerializer
from core.throttling import FivePerMinuteRateThrottle, PaginationMinuteUserRateThrottle

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
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [PaginationMinuteUserRateThrottle]
