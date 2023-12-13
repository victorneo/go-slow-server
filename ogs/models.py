from django.db import models
from users.models import User


class OGSUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    ogs_user_id = models.IntegerField()
    username = models.CharField(max_length=255)
    access_token = models.TextField()
    refresh_token = models.TextField()
    token_expiry = models.DateTimeField(null=True, blank=True, auto_now_add=True)


class OGSGame(models.Model):
    ogs_user = models.ForeignKey(OGSUser, on_delete=models.CASCADE)

    game_id = models.IntegerField()
    name = models.CharField(max_length=255)
    opponent_id = models.IntegerField()
    opponent_name = models.CharField(max_length=255)

    width = models.PositiveSmallIntegerField(default=9)
    height = models.PositiveSmallIntegerField(default=9)

    handicap = models.PositiveSmallIntegerField(default=0)
    komi = models.FloatField(default=6.5)
    rules = models.CharField(max_length=255)

    my_turn = models.BooleanField(default=True)
    my_time_remaining = models.IntegerField(default=0)
    opponent_time_remaining = models.IntegerField(default=0)

    def _time_remaining_display(self, time):
        my_time = time
        days = int(my_time // (24 * 60 * 60))
        hours = int((my_time - (days * 24 * 60 * 60)) // (60 * 60))
        minutes = int((my_time - (days * 24 * 60 * 60) - (hours * 60 * 60)) // 60)
        return f'{days}d {hours}h {minutes}m'

    def my_time_remaining_display(self):
        return self._time_remaining_display(self.my_time_remaining)

    def opponent_time_remaining_display(self):
        return self._time_remaining_display(self.opponent_time_remaining)
