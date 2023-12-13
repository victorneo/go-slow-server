from django.contrib.auth import login
from django.shortcuts import render, redirect
from .connectors import DGSConnector


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
