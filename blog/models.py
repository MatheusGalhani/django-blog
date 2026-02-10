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
    REQUIRED_FIELDS = ['username']
    
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self._metas = dict()
    
    def __str__(self):
        return self.get_full_name() or self.email
    
    class Meta:
        db_table = 'users'
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'


class BlogPost(UUIDBaseModel):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'blog_posts'
        verbose_name = 'Postagem do Blog'
        verbose_name_plural = 'Postagens do Blog'
