from django.contrib.auth.models import User
from rest_framework import serializers

# from api.models import User
from api.models import Goals, Recommendation, Reward, Coins, Notices, Order, UserICal


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class GoalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goals
        fields = '__all__'


class RecommendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = '__all__'


class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class CoinsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coins
        fields = '__all__'


class UserICalSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserICal
        fields = '__all__'


class NoticesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notices
        fields = '__all__'
