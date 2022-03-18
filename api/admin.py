from django.contrib import admin

from api.models import Goals, Recommendation, Reward, Order, Coins


# Register your models here.
# Testing user: abc adc@gmail.com mopup123456

class GoalsManager(admin.ModelAdmin):
    list_display = ['goal', 'location', 'start', 'end', 'status', 'user']


# recomID和rewardID是Recommendation和Reward的外部键，所以有外部参考的关系。
# 默认的页面显示中，将两者分离开来，无法体现出两者的从属关系。
# 使用内联显示，让 Order 附加在Recommendation和Reward的编辑页面上显示。

class OrderInline(admin.TabularInline):
    model = Order


class RecommendationManager(admin.ModelAdmin):
    inlines = [OrderInline]
    list_display = ['coin', 'name', 'image']


class RewardManager(admin.ModelAdmin):
    inlines = [OrderInline]
    list_display = ['coin', 'name', 'image']


class OrderManager(admin.ModelAdmin):
    list_display = ['orderID', 'recomID', 'rewardID', 'user']
    # 自定义显示：栏目分Main和Advance两部分
    # classes 说明它所在的部分的CSS格式，这里让Auto部分隐藏
    fieldsets = (
        ['Main', {
            'fields': ('recomID', 'rewardID', 'user'),
        }],
        ['Auto', {
            'classes': ('collapse',),  # CSS
            'fields': ('orderID',),
        }]
    )


class CoinsManager(admin.ModelAdmin):
    list_display = ['coin', 'user']


# 注册模型在后台能显示
admin.site.register(Goals, GoalsManager)
admin.site.register(Recommendation, RecommendationManager)
admin.site.register(Reward, RewardManager)
admin.site.register(Order, OrderManager)
admin.site.register(Coins, CoinsManager)
