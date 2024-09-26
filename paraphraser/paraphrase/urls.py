# paraphrase/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.paraphrase_view, name='paraphrase'),
    path('download_txt/', views.download_txt, name='download_txt'),
]
