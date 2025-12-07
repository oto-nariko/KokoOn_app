from django.urls import path
from . import views

app_name = 'KokoOn'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('post/', views.CreateMoodView.as_view(), name='post'),
    path('post_done/',
         views.PostSuccessView.as_view(),
         name='post_done'),
    path('moods/<int:category>',
         views.CategoryView.as_view(),
         name = 'mood_cat'),
    path('user-list/<int:user>',
         views.UserView.as_view(),
         name = 'user_list'),
     path('mood-dital/<int:pk>',
          views.MoodDetailView.as_view(),
          name = 'mood_detail'),
     path('mypage/', views.MypageView.as_view(), name = 'mypage'),
     path('mood/<int:pk>/delete/',
          views.MoodDeleteView.as_view(),
          name = 'mood_delete'),
]
