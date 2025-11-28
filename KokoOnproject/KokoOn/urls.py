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
]
