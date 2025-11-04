from django.urls import path
from . import views

app_name = 'info'

urlpatterns = [
    path('', views.index, name='index'),
    path('news/', views.news_list, name='news_list'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
    path('documents/', views.documents, name='documents'),
    path('documents/download/<int:pk>/',
         views.download_document, name='download_document'),
    path('announcements/', views.announcements, name='announcements'),
    # временно:
    path('create-admin/', views.create_admin, name='create_admin'),
    path('documents/', views.documents_list, name='documents_list'),
    path('documents/download/<int:document_id>/',
         views.download_document, name='download_document'),
]
