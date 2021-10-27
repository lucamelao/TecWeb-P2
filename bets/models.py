from django.db import models

class Bet(models.Model):
    user = models.CharField(max_length=100)

    def __str__(self):
        return '%d' % (self.user)

class Round(models.Model):
    number = models.CharField(max_length=2)
    bet = models.ForeignKey(Bet, on_delete=models.CASCADE, related_name='rounds')

    def __str__(self):
        return '%d' % (self.number)

class Fixture(models.Model):
    home_team = models.CharField(max_length=100)
    away_team = models.CharField(max_length=100)
    round = models.ForeignKey(Round, on_delete=models.CASCADE, related_name='fixtures')

    def __str__(self):
        return '%d x %s' % (self.home_team, self.away_team)

class Score(models.Model):
    home_score = models.CharField(max_length=2)
    away_score = models.CharField(max_length=2)
    fixture = models.OneToOneField(Fixture, on_delete=models.CASCADE, related_name= 'score')

    def __str__(self):
        return '%d x %s' % (self.home_score, self.away_score)