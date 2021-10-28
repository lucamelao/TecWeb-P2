from django.urls import include, path
from . import views

urlpatterns = [
  path('get_all', views.get_bets),
  path('post_bet', views.post_bet),
  path('get_user_bet/<int:bet_id>', views.get_user_bet),
  path('get_round/<int:round_number>', views.get_round),
]