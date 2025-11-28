from django.forms import ModelForm
from .models import MoodPost

class MoodPostForm(ModelForm):
    '''
    ModelFormのサブクラス
    '''
    class Meta:
        model = MoodPost
        fields = ['category','title', 'comment']