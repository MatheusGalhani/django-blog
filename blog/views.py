from django.shortcuts import render
from rest_framework import viewsets, permissions, mixins, status
from rest_framework.response import Response

from blog.models import User
from blog.serializers import UserSerializer

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
        
        serializer = self.get_serializer(data=data, many=False, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
