# Generated by Django 4.0.2 on 2022-02-08 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=50)),
                ('nickname', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('birthday', models.DateField()),
                ('password_hash', models.CharField(max_length=100)),
                ('password_salt', models.CharField(max_length=50)),
                ('course', models.CharField(max_length=32)),
                ('status', models.IntegerField(default=1)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
