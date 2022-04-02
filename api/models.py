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
        (0, 'Undo'),
        (1, 'Done'),
    )
    status = models.IntegerField(verbose_name='Status', choices=STATUS_CHOICES, default=0)
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
    coin = models.IntegerField(verbose_name='Coin')
    rewards = models.CharField(verbose_name='Rewards', max_length=20)
    qr = models.CharField(verbose_name='QRInfo', max_length=200)
    STATUS_CHOICES = (
        (0, 'Delete'),
        (1, 'Show'),
    )
    status = models.IntegerField(verbose_name='Status', choices=STATUS_CHOICES, default=1)
    user = models.ForeignKey(verbose_name='User', to=User, on_delete=models.CASCADE)

    def __str__(self):
        return '%s-%s-%s-%s' % (self.coin, self.rewards, self.qr, self.user)


class Coins(models.Model):
    coin = models.IntegerField(verbose_name='User Coins', default=0)
    user = models.ForeignKey(verbose_name='User', to=User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Coins'

    def __str__(self):
        return '%s-%s' % (self.coin, self.user)


class UserICal(models.Model):
    summary = models.CharField(verbose_name='Summary', max_length=30)
    date = models.DateField(verbose_name='Date', default=timezone.now)
    start = models.TimeField(verbose_name='Start Time')
    end = models.TimeField(verbose_name='End Time')
    location = models.CharField(verbose_name='Location', max_length=30)
    STATUS_CHOICES = (
        (0, 'Undo'),
        (1, 'Done'),
    )
    status = models.IntegerField(verbose_name='Status', choices=STATUS_CHOICES, default=0)
    icsName = models.CharField(verbose_name='ICalendar', max_length=200, blank=True)
    user = models.ForeignKey(verbose_name='User', to=User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'UserICal'

    def __str__(self):
        return '%s-%s-%s-%s-%s-%s-%s-%s' % (self.summary, self.date, self.start, self.end, self.location, self.status, self.icsName, self.user)


class Notices(models.Model):
    notice = models.CharField(verbose_name='Notices', max_length=200)
    user = models.ForeignKey(verbose_name='User', to=User, on_delete=models.CASCADE, default=4)

    class Meta:
        verbose_name_plural = 'Notices'

    def __str__(self):
        return '%s-%s' % (self.notice, self.user)
