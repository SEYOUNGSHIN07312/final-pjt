from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        login_id = validated_data.get('login_id')
        username = validated_data.get('username')
        password = validated_data.get('password')
        user = User(
            login_id=login_id,
            username=username
        )
        user.set_password(password)
        user.save()
        return user
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'