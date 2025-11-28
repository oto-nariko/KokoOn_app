from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import MoodPostForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import MoodPost
from django.views.generic import DetailView
from django.views.generic import DeleteView


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
    
class DetailView(DetailView):
    template_name = 'detail.html'
    model = MoodPost

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