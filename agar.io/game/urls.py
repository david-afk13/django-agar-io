from django.urls import path
from . import views

urlpatterns = [
    path('api/return_best_players', views.return_best_players),
    path('best_players', views.ListView_best_players.as_view()),
    path('api/register/', views.register, name='register'),
    path('api/login/', views.login, name='login'),
    path('api/player/<int:player_id>/update/', views.update_state, name='update_state'),
    path('api/player/<int:player_id>/logout/', views.logout, name='logout'),
    path('', views.index, name='index'),
    path('game/', views.game_view, name='game'), # Новий маршрут
]