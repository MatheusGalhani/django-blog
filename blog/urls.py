from django.urls import path, include
from rest_framework import routers
from blog.views import CreateUserView

router = routers.DefaultRouter()
router.register(r'register', CreateUserView, basename='register')

urlpatterns = [
    path('', include(router.urls)),
]
