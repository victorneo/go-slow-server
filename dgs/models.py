from django.db import models
from users.models import User


class DGSUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    userid = models.CharField(max_length=255, unique=True)

    cookie_sessioncode = models.TextField(null=True, blank=True)
    cookie_handle = models.TextField(null=True, blank=True)


class DGSGame(models.Model):
    status_choices = [
        ('running', 'Running'),
        ('finished', 'Finished'),
    ]

    game_id = models.CharField(max_length=255)
    dgs_user = models.ForeignKey(
        DGSUser, on_delete=models.CASCADE, related_name='dgs_games'
    )

    sgf = models.FileField(upload_to='sgf', null=True, blank=True)
    opponent_name = models.CharField(max_length=255, null=True, blank=True)
    opponent_userid = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, choices=status_choices, default='running')
    rated = models.BooleanField(default=True)
    size = models.SmallIntegerField(default=9)
    handicap = models.SmallIntegerField(default=0)
    komi = models.FloatField(default=6.5)
    ruleset = models.CharField(max_length=255)
    is_rated = models.BooleanField(default=True)
    my_turn = models.BooleanField(default=True)

    my_time_remaining = models.CharField(max_length=255, null=True, blank=True)
    opponent_time_remaining = models.CharField(max_length=255, null=True, blank=True)
    moves = models.IntegerField(default=0)

    def __init__(self, *args, **kwargs):
        super(DGSGame, self).__init__(*args, **kwargs)
