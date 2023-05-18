from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'accounts'
urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('auth/', AuthAPIView.as_view()),
    path('auth/refresh/', TokenRefreshView.as_view()),
]