from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import User
from .serializers import UserJWTSignupSerializer
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
# Create your views here.

@api_view(['POST'])
class JWTSignupView(APIView):
    serializer_class = UserJWTSignupSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=False):
            user = serializer.save(request)

            token = RefreshToken.for_user(user)
            refresh = str(token)
            access = str(token.access_token)

            return JsonResponse({'user': user,
                                 'access': access,
                                 'refresh': refresh})