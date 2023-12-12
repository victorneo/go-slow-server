# Generated by Django 5.0 on 2023-12-12 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dgs', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dgsgame',
            name='handicap',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='dgsgame',
            name='my_time_remaining',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='dgsgame',
            name='opponent_time_remaining',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='dgsgame',
            name='moves',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='dgsgame',
            name='opponent_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='dgsgame',
            name='opponent_userid',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='dgsgame',
            name='sgf',
            field=models.FileField(blank=True, null=True, upload_to='sgf'),
        ),
    ]
