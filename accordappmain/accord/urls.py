from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginpage, name='login'),
    path('logout/', views.logoutuser, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('', views.mainmenu, name='menu'),

    path('home/', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('tasks/', views.tasks, name='tasks'),
    path('lobby/<str:pk>/', views.lobby, name='lobby'),
    path('user_profile/<str:pk>', views.user_profile, name='user-profile'),
    path('order_list', views.order_list, name='order-list'),
    path('update_user/', views.update_user, name="update-user"),
    path('update_order/<str:pk>', views.update_order, name="update-order"),

    path('topics/', views.topics, name='topics'),
    path('pages/', views.pages, name='pages'),
    path('activity/', views.activity, name='activity'),
    path('create_lobby/', views.create_lobby, name='create-lobby'),
    path('create_order/', views.create_order, name='create-order'),
    path('create_product/', views.create_product, name='create-product'),
    path('create_task/', views.create_task, name='create-task'),
    path('update_lobby/<str:pk>/', views.update_lobby, name='update-lobby'),
    path('delete_lobby/<str:pk>/', views.deleteLobby, name='delete-lobby'),
    path('delete_post/<str:pk>/', views.deletePost, name='delete-post'),


    path('coinshophome', views.coinShopHome, name='coinshophome'),
]
