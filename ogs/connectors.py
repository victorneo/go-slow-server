from typing import Optional
import os
import requests
from django.core.cache import cache
from django.utils import timezone
from users.models import User
from .models import OGSUser, OGSGame


OGS_OAUTH_URL = 'https://online-go.com/oauth2/token/'
OGS_USER_GAMES_URL = 'https://online-go.com/api/v1/ui/overview'
OGS_USER_VITALS_URL = 'https://online-go.com/api/v1/me'
OGS_CLIENT_ID = os.environ.get('OGS_CLIENT_ID')
OGS_CLIENT_SECRET = os.environ.get('OGS_CLIENT_SECRET')


class OGSConnector(object):
    def login(self, username, password, user) -> Optional[User]:
        data = {
            'username': username,
            'password': password,
            'client_id': OGS_CLIENT_ID,
            'grant_type': 'password',
        }

        resp = requests.post(
            OGS_OAUTH_URL,
            data=data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
        )

        if not resp.ok:
            return None

        resp = resp.json()

        try:
            ogs_user = OGSUser.objects.select_related('user').get(username=username)
        except OGSUser.DoesNotExist:
            if not user.is_authenticated:
                # Generate a random username for this user
                user = User.objects.create(
                    username='ogs_' + username,
                    email=username + '@online-go.com',
                )

            user_resp = requests.get(
                OGS_USER_VITALS_URL,
                headers={
                    'Authorization': 'Bearer ' + resp['access_token'],
                },
            )
            user_resp = user_resp.json()

            ogs_user = OGSUser.objects.create(
                username=username,
                user=user,
                access_token=resp['access_token'],
                refresh_token=resp['refresh_token'],
                ogs_user_id=user_resp['id'],
            )
        else:
            user = ogs_user.user

        return user

    def refresh_token(self, ogs_user):
        now = timezone.now()
        if ogs_user.token_expiry > now:
            return

        data = {
            'username': ogs_user.username,
            'refresh_token': ogs_user.refresh_token,
            'client_id': OGS_CLIENT_ID,
            'grant_type': 'refresh_token',
        }

        resp = requests.post(
            OGS_OAUTH_URL,
            data=data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
        )

        ogs_user.access_token = resp.json()['access_token']
        ogs_user.refresh_token = resp.json()['refresh_token']
        ogs_user.save()

    def show_games(self, ogs_user):
        cache_key = f'running_games_{ogs_user.username}'
        games = cache.get(cache_key)

        if games:
            return games

        self.refresh_token(ogs_user)

        headers = {
            'Authorization': 'Bearer ' + ogs_user.access_token,
            'Content-Type': 'application/json',
        }

        resp = requests.get(OGS_USER_GAMES_URL, headers=headers)

        games = resp.json()['active_games']
        game_ids = [g['id'] for g in games]

        ogs_games = {
            g.game_id: g for g in OGSGame.objects.filter(game_id__in=game_ids).all()
        }

        to_be_updated = []
        all_games = []
        for g in games:
            if g['black']['id'] == ogs_user.ogs_user_id:
                opponent = g['white']
                my_time_remaining = g['json']['clock']['black_time']['thinking_time']
                opponent_time_remaining = g['json']['clock']['white_time'][
                    'thinking_time'
                ]
            else:
                opponent = g['black']
                my_time_remaining = g['json']['clock']['white_time']['thinking_time']
                opponent_time_remaining = g['json']['clock']['black_time'][
                    'thinking_time'
                ]

            my_turn = False
            if g['json']['clock']['current_player'] == ogs_user.ogs_user_id:
                my_turn = True

            game = ogs_games.get(g['id'], None)
            if not game:
                game = OGSGame(
                    ogs_user=ogs_user,
                    game_id=g['id'],
                    handicap=g['json']['handicap'],
                    komi=g['json']['komi'],
                    width=g['width'],
                    height=g['height'],
                    name=g['name'],
                    rules=g['json']['rules'],
                    opponent_id=opponent['id'],
                    opponent_name=opponent['username'],
                    my_turn=my_turn,
                    my_time_remaining=my_time_remaining,
                    opponent_time_remaining=opponent_time_remaining,
                )
                game.save()
                all_games.append(game)
            else:
                game.my_turn = my_turn
                game.my_time_remaining = my_time_remaining
                game.opponent_time_remaining = opponent_time_remaining
                to_be_updated.append(game)
                all_games.append(game)

        OGSGame.objects.bulk_update(
            to_be_updated, ['my_turn', 'my_time_remaining', 'opponent_time_remaining']
        )

        cache.set(cache_key, all_games, 900)

        return all_games
