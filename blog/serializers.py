from rest_framework import serializers
from blog.models import BlogPost, User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'bio', 'is_active', 'password']


class ListUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class BlogPostSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    author_id = serializers.UUIDField(write_only=True, required=True)
    author = ListUserSerializer(read_only=True)
    created_at = serializers.DateTimeField(format="%d/%m/%Y", read_only=True)
    updated_at = serializers.DateTimeField(format="%d/%m/%Y", read_only=True)

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'author', 'author_id',
                  'created_at', 'updated_at']