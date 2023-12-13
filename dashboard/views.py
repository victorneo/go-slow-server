from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.shortcuts import render, redirect
from dgs.models import DGSUser
from dgs.connectors import DGSConnector
from ogs.models import OGSUser


@login_required
def dashboard(request):
    dgs_games = []
    ogs_games = []

    # Fetch DGS games if the user is logged in
    try:
        dgs_user = request.user.dgsuser
    except DGSUser.DoesNotExist:
        pass
    else:
        dgs_connector = DGSConnector()
        dgs_games = dgs_connector.show_games(dgs_user)

    # Fetch OGS games if the user is logged in
    try:
        dgs_user = request.user.ogsuser
    except OGSUser.DoesNotExist:
        pass
    else:
        dgs_connector = DGSConnector()
        dgs_games = dgs_connector.show_games(dgs_user)

    return render(request, 'dashboard.html', {'dgs_games': dgs_games})


def dashboard_login(request):
    return render(request, 'login.html')


def dgs_login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    # We only use the userid and passwd to login, and we do not store the password
    userid = request.POST.get('userid')
    passwd = request.POST.get('passwd')

    dgs_connector = DGSConnector()

    user = dgs_connector.login(userid, passwd)

    if not user:
        return render(request, 'login.html', {'userid': userid, 'failed': True})
    else:
        login(request, user)

    return redirect('/dashboard')


def ogs_login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    # We only use the username and password to login, and we do not store the password
    username = request.POST.get('username')
    password = request.POST.get('password')

    return render(request, 'login.html', {'username': username, 'failed': True})
