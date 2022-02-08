# Create your models here.
from datetime import date

from django.db import models


# class Users(models.Model):
#     email = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=32)
#     password = models.CharField(max_length=32)
#     course = models.AutoField(max_length=32)
#     birthday = models.DateField()


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=50)  # student account
    nickname = models.CharField(max_length=50)  # student nickname
    email = models.EmailField()
    birthday = models.DateField(default=date.today)
    password_hash = models.CharField(max_length=100)  # hash password
    password_salt = models.CharField(max_length=50)  # password salt
    course = models.CharField(max_length=32)
    status = models.IntegerField(default=1)  # status:1 normal/2 disable/9 deleted
    # create_at = models.DateTimeField(auto_now_add=True)  # create time
    # update_at = models.DateTimeField(auto_now_add=True)  # update time

    # def toDict(self):
    #     return {'id': self.id, 'username': self.username, 'nickname': self.nickname, 'email': self.email, 'birthday': self.birthday.strftime('%Y-%m-%d %H:%M:%S'), 'password_hash': self.password_hash,
    #             'password_salt': self.password_salt, 'course': self.course, 'status': self.status, 'create_at': self.create_at.strftime('%Y-%m-%d %H:%M:%S'),
    #             'update_at': self.update_at.strftime('%Y-%m-%d %H:%M:%S')}

#
# class Avatar(models.Model):
#     name = models.CharField(max_length=32)
#     collar = models.CharField(max_length=32)
#     colour = models.CharField(max_length=32)
#     mood = models.CharField(max_length=32)
#     health = models.CharField()
#
#
#
# class Calendar(models.Model):
#     name = models.CharField(max_length=32)
#
#
# class Events(models.Model):
#     name = models.CharField(max_length=32)
#     start = models.CharField(max_length=32)
#     end = models.AutoField(max_length=32)
#     date = models.DateField()
#
#
# class Goals(models.Model):
#     status = models.CharField()
#     goal = models.CharField(max_length=32)
#     description = models.AutoField(max_length=32)
#     deadline = models.DateField()
#     recurring = models.AutoField(max_length=32)
#     category = models.AutoField(max_length=32)
#
#
# class Rewards(models.Model):
#     name = models.CharField(max_length=32)
#     coins = models.CharField(max_length=32)
#     awards = models.AutoField(max_length=32)
#     price = models.CharField()
#     redeemtime = models.DateField()
#     redeemcode = models.CharField()
#     coderedemptions = models.CharField()
#
#
# class Notifications(models.Model):
#     name = models.CharField(max_length=32)
#     Admin = models.CharField(max_length=32)
#     email = models.AutoField(max_length=32)
#     userid = models.CharField()
#     password = models.CharField()
