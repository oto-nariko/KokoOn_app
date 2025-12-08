from django.db import models
from accounts.models import CustomUser
import re

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
    
class Comment(models.Model):
    user = models.ForeignKey(
        CustomUser,
        verbose_name='ユーザー',
        on_delete=models.CASCADE
    )

    mood = models.ForeignKey(
        'MoodPost', # 同じファイル内にあるMoodPostモデルを参照
        verbose_name='対象投稿',
        on_delete=models.CASCADE,
        related_name='comments_for_post'
    )
    
    text = models.TextField(verbose_name="コメント内容")

    posted_at = models.DateTimeField(
        verbose_name='投稿日時',
        auto_now_add=True
    )

    youtube_id = models.CharField(max_length=20, null=True, blank=True)

# YouTube URLの正規表現
    # 例: https://www.youtube.com/watch?v=xxxxxxxxxxx や https://youtu.be/xxxxxxxxxxx に対応
    YOUTUBE_RE = re.compile(
        r'(?:youtu\.be\/|v=)([a-zA-Z0-9_-]{11})'
    )

    def save(self, *args, **kwargs):
        # コメントテキストからYouTube IDを抽出
        match = self.YOUTUBE_RE.search(self.text)
        if match:
            self.youtube_id = match.group(1)
        else:
            self.youtube_id = None
            
        super().save(*args, **kwargs)

    # コメントテキストからURLを取り除くメソッド (オプション)
    def clean_text(self):
        return self.YOUTUBE_RE.sub('', self.text).strip()

    # 動画が存在するか確認するプロパティ (テンプレートで使う)
    @property
    def has_youtube(self):
        return self.youtube_id is not None and self.youtube_id != ''
    
    def __str__(self):
        return f'{self.user.username} - {self.mood.title[:10]}...'