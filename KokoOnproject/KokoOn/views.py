from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from django.views.generic import CreateView, DetailView
from django.urls import reverse_lazy
from .forms import MoodPostForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import MoodPost, Comment
from django.views.generic import DetailView
from django.views.generic import DeleteView
from .forms import CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(ListView):
    template_name = 'index.html'
    queryset = MoodPost.objects.order_by('-posted_at')
    paginate_by = 9

@method_decorator(login_required, name='dispatch')
class CreateMoodView(CreateView):
    '''
    写真投稿ページのビュー
    MoodPostFormで定義されているモデルとフィールドと連携して
    投稿データをデータベースに登録する
    '''
    form_class = MoodPostForm
    template_name = "post_mood.html"
    success_url = reverse_lazy('KokoOn:post_done')

    def form_valid(self, form):
        postdata = form.save(commit=False)
        postdata.user = self.request.user
        postdata.save()
        return super().form_valid(form)
    
class PostSuccessView(TemplateView):
    '''
    投稿完了ページのビュー
    '''
    template_name = 'post_success.html'

class CategoryView(ListView):
    template_name ='index.html'
    paginate_by = 9

    def get_queryset(self):
        category_id = self.kwargs['category']
        categories = MoodPost.objects.filter(
            category=category_id).order_by('-posted_at')
        return categories
    
class UserView(ListView):
    template_name = 'index.html'
    paginate_by = 9

    def get_queryset(self):
        user_id = self.kwargs['user']
        user_list = MoodPost.objects.filter(
            user=user_id).order_by('-posted_at')
        return user_list
    

class MypageView(ListView):
    template_name = 'mypage.html'
    paginate_by = 9

    def get_queryset(self):
        queryset = MoodPost.objects.filter(   
        user=self.request.user).order_by('-posted_at')
        return queryset
    
class MoodDeleteView(DeleteView):
    model = MoodPost
    template_name = 'mood_delete.html'
    success_url = reverse_lazy('KokoOn:mypage')

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
    
class MoodDetailView(DetailView):
    model = MoodPost
    template_name = 'detail.html'
    
    # GETリクエスト（ページ表示）とPOSTリクエスト（フォーム送信）の両方を処理する
    def get_context_data(self, **kwargs):
        # ページを表示する際のコンテキスト（変数のセット）を作成
        context = super().get_context_data(**kwargs)
        # コメントフォームをコンテキストに追加
        context['comment_form'] = CommentForm()
        # 投稿に紐づくコメントを最新のものから取得してコンテキストに追加
        # related_name='comments_for_post' を使ってコメントを取得
        context['comments'] = self.object.comments_for_post.all().order_by('-posted_at')
        return context

    # POSTリクエスト（フォーム送信時）の処理
    def post(self, request, *args, **kwargs):
        # ログインしていない場合はログインページへ
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        
        self.object = self.get_object() # 現在の投稿（MoodPost）を取得
        comment_form = CommentForm(request.POST) # 送信されたデータをフォームに入れる

        if comment_form.is_valid():
            # フォームのインスタンスをまだ保存しない（commit=False）
            comment = comment_form.save(commit=False)
            
            # 必須項目（comment_userとmood）を手動でセットする
            comment.comment_user = request.user # ログイン中のユーザー
            comment.mood = self.object  # 現在の投稿
            
            # save()を実行すると、models.pyで定義した youtube_id 抽出ロジックが実行されます
            comment.save()
            
            # 処理後に詳細ページにリダイレクトする（リロードと同じ）
            return redirect('KokoOn:mood_detail', pk=self.object.pk)
        
        # フォームが無効だった場合、元のページとエラー情報でレンダリングし直す
        context = self.get_context_data(**kwargs)
        context['comment_form'] = comment_form # エラー情報を持ったフォーム
        return self.render_to_response(context)
    
class CommentDeleteView(DeleteView):
    model = Comment
    template_name = 'comment_delete.html'
    success_url = reverse_lazy('KokoOn:mypage')

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)