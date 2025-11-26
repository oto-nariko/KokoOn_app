from django.shortcuts import render
from django.views.generic import CreateView, TemplateView
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy

class SignUpView(CreateView):
    '''
    サインアップページのビュー
    '''
    form_class = CustomUserCreationForm #forms.pyで定義したフォームクラス
    template_name = "signup.html" #レンダリングするテンプレート
    success_url = reverse_lazy('accounts:signup_success') #サインアップ完了後のリダイレクト先のURLパターン

    def form_valid(self, form):
        '''
        CreateViewクラスのform_valid()をオーバーライド
        フォームのバリエーションを通過したときに呼ばれる
        フォームデータの登録を行う
        '''
        #formオブジェクトのフィールドの値をデータベースに保存
        user = form.save()
        self.object = user
        #戻り値はスーパークラスのform_valid()の戻り値(HttpResponseRedirect)
        return super().form_valid(form)

class SignUpSuccessView(TemplateView):
    '''
    サインアップ完了ページのビュー
    '''
    template_name = "signup_success.html" #レンダリングするテンプレート