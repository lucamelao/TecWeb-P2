from .models import Bet, Round, Score, Fixture
from .serializer import BetSerializer, ScoreSerializer
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework import status
import json
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

@api_view(["GET"])
def get_bets(request):
    bets = Bet.objects.all()
    serializer = BetSerializer(bets, many=True)
    return JsonResponse({'bets': serializer.data}, safe=False, status=status.HTTP_200_OK)

@api_view(["GET"])
def get_user_bet(request, bet_id):
    user_bet = Bet.objects.filter(id = bet_id)
    serializer = BetSerializer(user_bet, many=True)
    return JsonResponse({'bets': serializer.data}, safe=False, status=status.HTTP_200_OK)

@api_view(["POST"])
def post_bet(request):
    payload = json.loads(request.body)
    user_bet = Bet.objects.filter(user = payload["user"])

    if len(user_bet) == 0:
        bet = Bet(user = payload["user"])
        bet.save()
    else:
        bet = user_bet[0]

    fixtures = payload["fixtures"]
    round_number = payload["round"]
    new_round = Round(number = round_number, bet=bet)
    new_round.save()

    for i in fixtures:

        fixture = Fixture(home_team = i["home"], away_team = i["away"] , round=new_round)
        fixture.save()
        score = Score(home_score = i["score"]["home"], away_score = i["score"]["away"], fixture=fixture)
        score.save()
       

    return JsonResponse({'status': "ok"}, safe=False, status=status.HTTP_200_OK)
        

