from django.contrib import admin
from .models import Category, MoodPost, Comment

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')

class MoodPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')

class CommentAdmin(admin.ModelAdmin):
    # 管理画面の一覧画面で表示するフィールド
    list_display = ('comment_user', 'mood', 'text', 'youtube_id', 'posted_at')
    
    # 管理画面の編集フォームで編集可能にするフィールド
    # ここに 'youtube_id' を追加して、手動で確認・編集できるようにします。
    fields = ('comment_user', 'mood', 'text', 'youtube_id') 
    
    # 検索可能なフィールド
    search_fields = ('user__username', 'text', 'youtube_id')

admin.site.register(Category, CategoryAdmin)
admin.site.register(MoodPost, MoodPostAdmin)
admin.site.register(Comment, CommentAdmin)