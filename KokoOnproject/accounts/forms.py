from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    '''
    UserCreationFormのサブクラス
    '''
    class Meta:
        '''
        UserCreationFormのインナークラス
        '''
        model = CustomUser #連携するUserモデルを設定
        fields = ('username', 'email', 'password1', 'password2') #フォームで使用するフィールドを設定