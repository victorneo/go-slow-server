from django.urls import path
from .views import dgs_login, dgs_dashboard


urlpatterns = [
    path('dgs/login/', dgs_login, name='dgs-login'),
    path('dgs/dashboard/', dgs_dashboard, name='dgs-dashboard'),
]
