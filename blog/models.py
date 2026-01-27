from django.db import models
from django.contrib.auth.models import AbstractUser
from core.models import UUIDBaseModel

# Create your models here.
class User(AbstractUser, UUIDBaseModel):
    AUTHOR = 'author'
    READER = 'reader'

    BLOG_ROLE = (
        (AUTHOR, 'Autor'),
        (READER, 'Leitor'),
    )
    role = models.CharField(max_length=10, choices=BLOG_ROLE, default=READER)
    bio = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True, db_index=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self._metas = dict()
    
    def __str__(self):
        return self.get_full_name() or self.email
    
    class Meta:
        db_table = 'users'
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
