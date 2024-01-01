from django.urls import path
from Palindrome import views

urlpatterns = [
    path('crud-user/', views.crud_user, name='crud-user'),
    path('user-login/', views.user_login, name='user-login'),
    path('user-logout/', views.user_logout, name='user-logout'),
    path('get-board/', views.get_board, name='get-board'),
    path('update-board/', views.update_board, name='update-board'),
    path('game-list/', views.game_id_list, name='game-list'),
]