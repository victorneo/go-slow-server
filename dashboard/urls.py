from django.urls import path
from .views import dashboard, dashboard_login, ogs_login, dgs_login


urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('login/', dashboard_login, name='dashboard_login'),
    path('ogs/login/', ogs_login, name='ogs_login'),
    path('dgs/login/', dgs_login, name='dgs_login'),
]
