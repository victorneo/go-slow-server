# Generated by Django 5.0 on 2023-12-12 10:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dgs', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='dgsuser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='dgsgame',
            name='dgs_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dgs_games', to='dgs.dgsuser'),
        ),
    ]
