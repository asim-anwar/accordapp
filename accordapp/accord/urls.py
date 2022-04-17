from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginpage, name='login'),
    path('logout/', views.logoutuser, name='logout'),
    path('signup/', views.signup, name='signup'),

    path('', views.home, name='home'),
    path('lobby/<str:pk>/', views.lobby, name='lobby'),
    path('user_profile/<str:pk>', views.user_profile, name='user-profile'),
    path('update_user/', views.update_user, name="update-user"),

    path('topics/', views.topics, name='topics'),
    path('activity/', views.activity, name='activity'),
    path('create_lobby/', views.create_lobby, name='create-lobby'),
    path('update_lobby/<str:pk>/', views.update_lobby, name='update-lobby'),
    path('delete_lobby/<str:pk>/', views.deleteLobby, name='delete-lobby'),
    path('delete_post/<str:pk>/', views.deletePost, name='delete-post')
]
