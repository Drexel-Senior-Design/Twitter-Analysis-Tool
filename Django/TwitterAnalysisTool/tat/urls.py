from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = "tat"
urlpatterns = [
    path('search/', views.search, name='search'),
    path('about/', views.about, name='about'),
    path('', views.index, name='index'),
]