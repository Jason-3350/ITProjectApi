from rest_framework import serializers

from api.models import User


class UserSerializer(serializers.ModelSerializer):
    # createdTime = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")
    # birthday = serializers.DateField(format="%d-%m-%Y %H:%M:%S")
    # create_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")  # create time
    # update_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")  # update time

    class Meta:
        model = User
        fields = '__all__'
