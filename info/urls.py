from django.urls import path
from . import views

app_name = 'info'

urlpatterns = [
    path('', views.index, name='index'),
    path('news/', views.news_list, name='news_list'),  # ← добавь эту строку
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
    path('documents/', views.documents, name='documents'),
    path('announcements/', views.announcements, name='announcements'),
]
