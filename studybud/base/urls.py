from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("register/", views.registerUser, name="register"),
    
    # Home 
    path("", views.home, name="home"),
    
    # Room 
    path("room/<str:pk>", views.room, name="room"), 
    path("create-room/", views.createRoom, name="create-room"),
    path("update-room/<str:pk>", views.updateRoom, name="update-room"),
    path("delete-room/<str:pk>", views.deleteRoom, name="delete-room"),
    path("delete-message/<str:pk>", views.deleteMessage, name="delete-message"),
    
    # User Profile
    path("profile/<str:pk>", views.userProfile, name="user-profile"),
]