from rest_framework import serializers
from .models import Bet, Round, Fixture, Score

class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ['home_score', 'away_score']

class FixtureSerializer(serializers.ModelSerializer):
    score = ScoreSerializer(many=False)
    class Meta:
        model = Fixture
        fields = ['home_team', 'away_team', 'score', 'slug', 'fixture_score']

class RoundSerializer(serializers.ModelSerializer):
    fixtures = FixtureSerializer(many=True)

    class Meta:
        model = Round
        fields = ['number', 'fixtures', 'round_score']

class BetSerializer(serializers.ModelSerializer):
    rounds = RoundSerializer(many=True) 

    class Meta:
        model = Bet
        fields = ['user','rounds', 'total_score']

class BetSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Bet
        fields = ['user', 'total_score', 'id']