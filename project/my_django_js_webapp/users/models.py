# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # 이메일 필드를 유니크로 설정
    id = models.CharField(unique=True,primary_key=True,max_length=20)  # 이메일 필드를 유니크로 설정
    username = models.CharField(max_length=150, unique=True)  # 유저이름 필드는 유니크 제약 해제

    USERNAME_FIELD = 'username'  # 이메일을 유저네임 필드로 설정
    REQUIRED_FIELDS = []  # 이메일 외에 필수 필드가 없다면 비워 둠

    def __str__(self):
        return self.email
