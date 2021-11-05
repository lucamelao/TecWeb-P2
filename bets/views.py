from .models import Bet, Round, Score, Fixture
from .serializer import BetSerializer, RoundSerializer, FixtureSerializer, ScoreSerializer
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework import status
import json
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from .api_futebol import get_results

@api_view(["GET"])
def get_bets(request):
    bets = Bet.objects.all()
    serializer = BetSerializer(bets, many=True)
    return JsonResponse({'bets': serializer.data}, safe=False, status=status.HTTP_200_OK)

@api_view(["GET"])
def get_user_bet(request, bet_id):
    user_bet = Bet.objects.get_object_or_404(id = bet_id)
    serializer = BetSerializer(user_bet, many=True)
    return JsonResponse({'bets': serializer.data}, safe=False, status=status.HTTP_200_OK)

@api_view(["GET"])
def get_round(request, round_number):
    round = Round.objects.filter(number = round_number)
    serializer = RoundSecondSerializer(round, many=True)
    return JsonResponse({'round': serializer.data}, safe=False, status=status.HTTP_200_OK)

@api_view(["POST"])
def post_bet(request):
    payload = json.loads(request.body)
    user_bet = Bet.objects.filter(user = payload["user"])

    if len(user_bet) == 0:
        bet = Bet(user = payload["user"], total_score = 0)
        bet.save()
    else:
        # bet = user_bet[0]
        return JsonResponse({'status': "user has already made a bet"}, safe=False, status=status.HTTP_401_UNAUTHORIZED)

    fixtures = payload["fixtures"]
    new_round = Round(number =  payload["round"], bet=bet, round_score=0)
    new_round.save()

    for i in fixtures:

        fixture = Fixture(home_team = i["home"], away_team = i["away"] , round=new_round, fixture_score=0, slug=i["slug"])
        fixture.save()
        score = Score(home_score = i["score"]["home"], away_score = i["score"]["away"], fixture=fixture)
        score.save()
       

    return JsonResponse({'status': "ok"}, safe=False, status=status.HTTP_200_OK)

def calculate_round_scores():
    all_rounds = Round.objects.all()
    all_fixtures = Fixture.objects.all()
    for i in all_rounds:
        round = Round.objects.filter(id=i.id)
        round_score = 0
        for j in all_fixtures:
            if j.round == i:
                round_score += j.fixture_score
        round.update(round_score = round_score)

def calculate_bet_scores():
    all_rounds = Round.objects.all()
    all_bets = Bet.objects.all()
    for i in all_bets:
        bet = Bet.objects.filter(id=i.id)
        for j in all_rounds:
            total_score = 0
            if j.bet == i:
                total_score += j.round_score
        bet.update(total_score = total_score)




@api_view(["GET"])
def calculate_scores(request, round_number):
    partidas = get_results(round_number)
    scores = Score.objects.filter(fixture__round__number = round_number)
    for i in scores:
        fix = Fixture.objects.filter(id=i.fixture.id)
        for j in partidas:
            if i.fixture.slug == j["slug"]:
                if i.home_score == j["placar_mandante"] and i.away_score == j["placar_visitante"]:
                    fix.update(fixture_score = 5)
                elif i.home_score > i.away_score and j["placar_mandante"] > j["placar_visitante"]:
                    fix.update(fixture_score = 3)
                elif i.home_score < i.away_score and j["placar_mandante"] < j["placar_visitante"]:
                    fix.update(fixture_score = 3)
                elif i.home_score == i.away_score and j["placar_mandante"] == j["placar_visitante"]:
                    fix.update(fixture_score = 3)
                else:
                    fix.update(fixture_score = 0)
                

    calculate_round_scores()
    calculate_bet_scores()
    bets = Bet.objects.all()
    serializer = BetSerializer(bets, many=True)
    return JsonResponse({'all': serializer.data}, safe=False, status=status.HTTP_200_OK)

