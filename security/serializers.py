
from datetime import datetime

from config.settings import SIMPLE_JWT
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as JwtTokenObtainPairSerializer, TokenRefreshSerializer

class EmailTokenObtainPairSerializer(JwtTokenObtainPairSerializer):
    username_field = get_user_model().USERNAME_FIELD
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['role'] = user.role
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            'id': self.user.id,
            'email': self.user.email,
            'role': self.user.role,
        }
        
        access_token_lifetime = SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
        access_token_exp = datetime.now() + access_token_lifetime
        data['expires'] = access_token_exp.isoformat()
        return data


class CustomTokenRefreshSerializer(TokenRefreshSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        access_token_lifetime = SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
        access_token_exp = datetime.now() + access_token_lifetime
        data['expires'] = access_token_exp.isoformat()
        return data
