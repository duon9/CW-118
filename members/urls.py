from django.urls import path
from . import views

urlpatterns  = [
    path('members/', views.members, name = 'members'),
    path('', views.home, name = "home"),
    path('members/detail/<int:id>', views.detail, name='details'),
    path('player/<int:id>', views.player, name = "player"),
    path('movies/', views.movies, name = 'movies'),
    path('signin/', views.signin, name = "signin"),
    path('signup/', views.signup, name = "signup"),
    path('logout', views.logout, name = "logout"),
    path('tvseries', views.tvseries, name = 'tvseries'),
    path('tvseries/<int:id>', views.tvseries_detail, name = 'tvseries_detail'),
    path('watch/<int:id>', views.watch, name = 'watch'),
    path('proxy-file/', views.file_proxy, name='file_proxy'),
    path('profile', views.profile, name='profile'),
    path('change_avatar', views.change_avatar, name = "change_avatar"),
    path("test/", views.test, name = "test")
]