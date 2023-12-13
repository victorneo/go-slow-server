from django.urls import path
from .views import ogs_login


urlpatterns = [
    path('ogs/login/', ogs_login, name='ogs-login'),
]
