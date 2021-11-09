from django.urls import include, path
from . import views

urlpatterns = [
  path('get_all', views.get_bets),
  path('get_scores', views.get_total_scores),
  path('post_bet', views.post_bet),
  path('get_user_bet/<int:bet_id>', views.get_user_bet),
  path('calculate_scores/<int:round_number>', views.calculate_scores),
]