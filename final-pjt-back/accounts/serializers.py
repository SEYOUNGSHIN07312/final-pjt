from rest_framework import serializers
from django.contrib.auth import get_user_model
from datetime import date

User = get_user_model()
class UserJWTSignupSerializer(serializers.ModelSerializer):
    id = serializers.CharField(
        required=True,
        write_only=True,
        max_length=20
    )

    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    
    birth = serializers.DateField(
        required=True,
        write_only=True,
    )

    class Meta(object):
        model = User
        fields = ['id', 'password', 'birth']

    def save(self, request):
        user = super().save()

        user.id = self.validated_data['id']
        user.birth = self.validated_data['birth']

        user.set_password(self.validated_data['password'])
        user.save()

        return user

    def validate(self, data):
        id = data.get('id', None)

        if User.objects.filter(id=id).exists():
            raise serializers.ValidationError("user already exists")

        data['subscription_date'] = date.today()

        return data