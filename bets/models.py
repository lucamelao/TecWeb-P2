from django.db import models

class Bet(models.Model):
    user = models.CharField(max_length=100)
    total_score = models.IntegerField()

    def __str__(self):
        return '%d' % (self.user)

class Round(models.Model):
    number = models.IntegerField()
    bet = models.ForeignKey(Bet, on_delete=models.CASCADE, related_name='rounds')
    round_score = models.IntegerField()

    def __str__(self):
        return '%d' % (self.number)

class Fixture(models.Model):
    home_team = models.CharField(max_length=100)
    away_team = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    round = models.ForeignKey(Round, on_delete=models.CASCADE, related_name='fixtures')
    fixture_score = models.IntegerField()

    def __str__(self):
        return self.home_team + " " + self.away_team + " " + "points" + ":" + str(self.fixture_score)

class Score(models.Model):
    home_score = models.IntegerField()
    away_score = models.IntegerField()
    fixture = models.OneToOneField(Fixture, on_delete=models.CASCADE, related_name= 'score')

    def __str__(self):
        return '%d x %s' % (self.home_score, self.away_score)