from django.urls import path
from . import views

urlpatterns = [
    path('contact/', views.contact, name='contact'),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('projects/', views.projects, name='projects'),
]
