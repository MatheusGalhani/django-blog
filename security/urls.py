from django.urls import path
from rest_framework import routers

from security.views import CustomTokenRefreshView, EmailTokenObtainPairView

router = routers.DefaultRouter()


urlpatterns = [
    path('token/', EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]
