from django.forms import ModelForm, Textarea
from .models import MoodPost, Comment

class MoodPostForm(ModelForm):
    '''
    ModelFormのサブクラス
    '''
    class Meta:
        model = MoodPost
        fields = ['category','title', 'comment']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text':Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'コメント（YouTube URLも可）を入力...'})
        }