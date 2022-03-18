# Generated by Django 4.0.2 on 2022-03-18 22:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0006_delete_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recommendation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coin', models.IntegerField(verbose_name='Recommend Coin')),
                ('name', models.CharField(max_length=20, verbose_name='Recommend Name')),
                ('image', models.CharField(blank=True, max_length=256, verbose_name='Image')),
            ],
        ),
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coin', models.IntegerField(verbose_name='Reward Coin')),
                ('name', models.CharField(max_length=20, verbose_name='Reward Name')),
                ('image', models.CharField(blank=True, max_length=256, verbose_name='Image')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('orderID', models.IntegerField(blank=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recomID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.recommendation', verbose_name='Recommend')),
                ('rewardID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.reward', verbose_name='Reward')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
        migrations.CreateModel(
            name='Goals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goal', models.CharField(max_length=50, verbose_name='Goal')),
                ('location', models.CharField(max_length=30, verbose_name='Location')),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='Data')),
                ('start', models.TimeField(verbose_name='Start Time')),
                ('end', models.TimeField(verbose_name='End Time')),
                ('status', models.CharField(choices=[('0', 'Undo'), ('1', 'Done')], max_length=1, verbose_name='Status')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Goals',
            },
        ),
        migrations.CreateModel(
            name='Coins',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coin', models.IntegerField(default=0, verbose_name='User Coins')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name_plural': 'Coins',
            },
        ),
    ]
