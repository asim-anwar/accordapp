from django.urls import path
from . import views
from .views import Userlogin

urlpatterns = [
    path('', views.getRouts),
    path('lobbys/', views.getLobbys),
    path('users/', views.getUsers),
    path('lobbys/<str:pk>/', views.getLobby),
    path('login/', Userlogin.as_view(), ),

]