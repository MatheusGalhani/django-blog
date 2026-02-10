from django.urls import path, include
from rest_framework import routers
from blog.views import BlogPostViewSet, CreateUserView

router = routers.DefaultRouter()
router.register(r'register', CreateUserView, basename='register')
router.register(r'blog-post', BlogPostViewSet, basename='posts')

urlpatterns = [
    path('', include(router.urls)),
]
