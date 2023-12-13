from django.urls import path
from .views import (
    dashboard,
    dashboard_login,
    ogs_login,
    dgs_login,
    logout_user,
    accounts,
)


urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('login/', dashboard_login, name='dashboard_login'),
    path('logout/', logout_user, name='dashboard_logout'),
    path('accounts/', accounts, name='accounts'),
    path('ogs/login/', ogs_login, name='ogs_login'),
    path('dgs/login/', dgs_login, name='dgs_login'),
]
