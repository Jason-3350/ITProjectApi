from django.contrib import admin

from api.models import Goals, Recommendation, Reward, Coins, Notices, Order, UserICal


# Register your models here.


class GoalsManager(admin.ModelAdmin):
    list_display = ['goal', 'location', 'date', 'start', 'end', 'status', 'user']


class RecommendationManager(admin.ModelAdmin):
    list_display = ['coin', 'name', 'image']


class RewardManager(admin.ModelAdmin):
    list_display = ['coin', 'name', 'image']


class OrderManager(admin.ModelAdmin):
    list_display = ['coin', 'rewards', 'qr', 'status', 'user']


class CoinsManager(admin.ModelAdmin):
    list_display = ['coin', 'user']


class UserICalManager(admin.ModelAdmin):
    list_display = ['summary', 'date', 'start', 'end', 'location', 'status', 'icsName', 'user']


class NoticesManager(admin.ModelAdmin):
    list_display = ['notice', 'user']


# 注册模型在后台能显示
admin.site.register(Goals, GoalsManager)
admin.site.register(Recommendation, RecommendationManager)
admin.site.register(Reward, RewardManager)
admin.site.register(Order, OrderManager)
admin.site.register(Coins, CoinsManager)
admin.site.register(UserICal, UserICalManager)
admin.site.register(Notices, NoticesManager)
