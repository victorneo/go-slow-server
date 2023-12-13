import os
import requests
from django.contrib.auth import login
from django.shortcuts import render, redirect
from users.models import User
from .models import OGSUser


OGS_LOGIN_URL = 'http://online-go.com/oauth2/access_token'
OGS_CLIENT_ID = os.getenv('OGS_CLIENT_ID')
OGS_CLIENT_SECRET = os.getenv('OGS_CLIENT_SECRET')


def ogs_login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    # We only use the username and password to login, and we do not store the password
    username = request.POST.get('username')
    password = request.POST.get('password')

    resp = requests.post(
        OGS_LOGIN_URL,
        {
            'username': username,
            'password': password,
            'grant_type': 'password',
            'client_id': OGS_CLIENT_ID,
            'client_secret': OGS_CLIENT_SECRET,
        },
    )

    if not resp.ok:
        return render(request, 'login.html', {'username': username, 'failed': True})

    resp = resp.json()

    try:
        ogs_user = OGSUser.objects.select_related('user').get(username=username)
    except OGSUser.DoesNotExist:
        # User is already logged in
        if request.user:
            user = request.user
        else:
            username = 'ogs_' + username
            user = User.objects.create(
                username=username,
                email=username + '@online-go.com',
            )

        ogs_user = OGSUser.objects.create(
            username=username,
            user=user,
            access_token=resp['access_token'],
            refresh_token=resp['refresh_token'],
        )
    else:
        user = ogs_user.user

    login(request, user)
    return redirect('/dashboard')
