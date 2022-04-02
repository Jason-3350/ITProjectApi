# Generated by Django 4.0.2 on 2022-04-02 23:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0009_delete_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coin', models.IntegerField(verbose_name='Coin')),
                ('rewards', models.CharField(max_length=20, verbose_name='Rewards')),
                ('qr', models.CharField(max_length=200, verbose_name='QRInfo')),
                ('status', models.IntegerField(choices=[(0, 'Delete'), (1, 'Show')], default=1, verbose_name='Status')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
    ]
