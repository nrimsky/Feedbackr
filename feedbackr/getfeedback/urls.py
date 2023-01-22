from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload, name='upload'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('myqs/', views.my_qs, name='myqs'),
    path('answer/<int:id>/', views.answer, name='answer'),
    path('details/<int:id>/', views.details, name='details'),
    path('yes/', views.vote_yes, name='voteyes'),
    path('no/', views.vote_no, name='voteno'),
]