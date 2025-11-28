from django.db import models
from accounts.models import CustomUser

class Category(models.Model):
    '''
    投稿のカテゴリを管理するモデル
    '''
    title = models.CharField(
        verbose_name='カテゴリ',
        max_length=20
    )

    def __str__(self):
        '''
        オブジェクトを文字列に変換して返す
        '''
        return self.title
    
class MoodPost(models.Model):
    '''
    投稿されたデータを管理するモデル
    '''
    user = models.ForeignKey(
        CustomUser,
        verbose_name='ユーザー',
        on_delete=models.CASCADE
        )
    category = models.ForeignKey(
        Category,
        verbose_name='カテゴリ',
        on_delete=models.PROTECT
    )
    title = models.CharField(
    verbose_name='タイトル', # フィールドのタイトル
    max_length=200        # 最大文字数は200
    )
    comment = models.TextField(
    verbose_name='相談',  # フィールドのタイトル
    )
    posted_at = models.DateTimeField(
    verbose_name='投稿日時', # フィールドのタイトル
    auto_now_add=True       # 日時を自動追加
    )
    def __str__(self):
        return self.title
    
