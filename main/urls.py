from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tests/', views.tests, name='tests'),
    path('test/<int:test_id>/', views.test_detail, name='test_detail'),
    path('videos/', views.videos, name='videos'),
    path('formulas/', views.formulas, name='formulas'),
    path('library/', views.library, name='library'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
]