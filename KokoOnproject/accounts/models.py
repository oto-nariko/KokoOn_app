from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    '''
    Userモデルを継承したカスタムユーザーモデル
    '''
    pass


