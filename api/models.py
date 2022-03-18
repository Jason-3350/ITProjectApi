from django.contrib.auth.models import AbstractUser, User
from django.db import models

# Create your models here.
from django.utils import timezone


class Goals(models.Model):
    goal = models.CharField(verbose_name='Goal', max_length=50)
    location = models.CharField(verbose_name='Location', max_length=30)
    date = models.DateField(verbose_name='Data', default=timezone.now)
    start = models.TimeField(verbose_name='Start Time')
    end = models.TimeField(verbose_name='End Time')
    STATUS_CHOICES = (
        ('0', 'Undo'),
        ('1', 'Done'),
    )
    status = models.CharField(verbose_name='Status', max_length=1, choices=STATUS_CHOICES)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    # 写了返回才能通过list_display显示字段名，否则显示的是一个对象
    def __str__(self):
        return '%s-%s-%s-%s-%s-%s' % (self.goal, self.location, self.start, self.end, self.start, self.user)

    class Meta:
        verbose_name_plural = 'Goals'  # 后台管理界面的’Goalss‘改为复数形式’Goals‘


class Recommendation(models.Model):
    coin = models.IntegerField(verbose_name='Recommend Coin')
    name = models.CharField(verbose_name='Recommend Name', max_length=20)
    image = models.CharField(verbose_name="Image", max_length=256, blank=True)  # save url

    def __str__(self):
        return '%s-%s-%s' % (self.coin, self.name, self.image)


class Reward(models.Model):
    coin = models.IntegerField(verbose_name='Reward Coin')
    name = models.CharField(verbose_name='Reward Name', max_length=20)
    image = models.CharField(verbose_name='Image', max_length=256, blank=True)  # save url

    def __str__(self):
        return '%s-%s-%s' % (self.coin, self.name, self.image)


class Order(models.Model):
    # orederID, It is impossible to add a non-nullable field 'orderID' to order without specifying a default.
    # This is because the database needs something to populate existing rows.
    # 设置 blank = True 解决
    orderID = models.IntegerField(verbose_name='ID', primary_key=True, blank=True)
    recomID = models.ForeignKey(verbose_name='Recommend', to=Recommendation, on_delete=models.CASCADE, null=True, blank=True)
    rewardID = models.ForeignKey(verbose_name='Reward', to=Reward, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(verbose_name='User', to=User, on_delete=models.CASCADE)

    def __str__(self):
        return '%s-%s-%s' % (self.recomID, self.rewardID, self.user)


class Coins(models.Model):
    coin = models.IntegerField(verbose_name='User Coins', default=0)
    user = models.ForeignKey(verbose_name='User', to=User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Coins'

    def __str__(self):
        return '%s-%s' % (self.coin, self.user)
