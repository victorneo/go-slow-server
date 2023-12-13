from django.db import models
from users.models import User


class OGSUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    username = models.CharField(max_length=255)
    access_token = models.TextField()
    refresh_token = models.TextField()
