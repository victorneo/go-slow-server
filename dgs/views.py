import requests
from bs4 import BeautifulSoup
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from users.models import User
from .models import DGSUser, DGSGame


DGS_LOGIN_URL = 'https://dragongoserver.net/login.php'
DGS_SHOW_GAMES_URL = 'https://www.dragongoserver.net/show_games.php?userid={}'


def dgs_login(request):
    if request.method == 'GET':
        return render(request, 'dgs_login.html')

    # We only use the userid and passwd to login, and we do not store the password
    userid = request.POST.get('userid')
    passwd = request.POST.get('passwd')

    s = requests.Session()
    resp = s.post(DGS_LOGIN_URL, {'userid': userid, 'passwd': passwd})

    if 'Sorry' in resp.text:
        return render(request, 'dgs_login.html', {'userid': userid, 'failed': True})

    cookie_sessioncode = s.cookies['cookie_sessioncode']
    cookie_handle = s.cookies['cookie_handle']

    try:
        dgs_user = DGSUser.objects.select_related('user').get(userid=userid)
    except DGSUser.DoesNotExist:
        # Generate a random username for this user
        username = 'dgs_' + userid
        user = User.objects.create(
            username=username,
            email=username + '@dragongoserver.net',
        )
        dgs_user = DGSUser.objects.create(
            userid=userid,
            cookie_sessioncode=cookie_sessioncode,
            cookie_handle=cookie_handle,
            user=user,
        )
    else:
        user = dgs_user.user

    login(request, user)
    return redirect('/dgs/dashboard')


@login_required
def dgs_dashboard(request):
    # Fetch games if the user is logged in
    dgs_user = request.user.dgsuser
    url = DGS_SHOW_GAMES_URL.format(dgs_user.userid)

    resp = requests.get(
        url.format(dgs_user.userid),
        cookies={
            'cookie_sessioncode': dgs_user.cookie_sessioncode,
            'cookie_handle': dgs_user.cookie_handle,
        },
    )

    soup = BeautifulSoup(resp.content, 'html.parser')
    table = soup.find('table', {'id': 'runningTable'})
    running_games = []

    if table:
        games = table.select('tr[class*="Row"]')
        for g in games:
            game_data = [d for d in g.contents if d != '\n']
            my_turn = False
            turn = game_data[10].find('img').attrs['src']
            if 'w_w' in turn or 'b_b' in turn:
                my_turn = True
            running_games.append(
                {
                    'game_id': game_data[0].text,
                    'opponent_name': game_data[5].text,
                    'opponent_userid': game_data[6].text,
                    'my_turn': my_turn,
                    'ruleset': game_data[12].text,
                    'size': int(game_data[13].text),
                    'handicap': int(game_data[14].text),
                    'komi': float(game_data[15].text),
                    'moves': int(game_data[16].text),
                    'is_rated': game_data[17].text == 'Yes',
                    'my_time_remaining': game_data[24].text,
                    'opp_time_remaining': game_data[25].text,
                }
            )

        game_ids = [g['game_id'] for g in running_games]
        records = {
            g.game_id: g for g in dgs_user.dgs_games.filter(game_id__in=game_ids).all()
        }

        to_be_updated = []
        to_be_created = []

        for g in running_games:
            if g['game_id'] in records:
                record = records[g['game_id']]
                record.moves = g['moves']
                record.my_time_remaining = g['my_time_remaining']
                record.opponent_time_remaining = g['opp_time_remaining']
                record.my_turn = g['my_turn']
                to_be_updated.append(record)
            else:
                record = DGSGame(dgs_user=dgs_user)
                record.game_id = g['game_id']
                record.opponent_name = g['opponent_name']
                record.opponent_userid = g['opponent_userid']
                record.ruleset = g['ruleset']
                record.size = g['size']
                record.handicap = g['handicap']
                record.komi = g['komi']
                record.is_rated = g['is_rated']
                record.moves = g['moves']
                record.my_turn = g['my_turn']
                record.my_time_remaining = g['my_time_remaining']
                record.opponent_time_remaining = g['opp_time_remaining']
                to_be_created.append(record)

        DGSGame.objects.bulk_create(to_be_created)
        DGSGame.objects.bulk_update(
            to_be_updated,
            fields=['moves', 'my_time_remaining', 'opponent_time_remaining'],
        )

    return render(request, 'dgs_dashboard.html', {'running_games': running_games})
