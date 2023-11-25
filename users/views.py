from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Profile

from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        # serializer_class 이용해 데이터를 직렬화 함.
        serializer = self.get_serializer(data=request.data)
        # 시리얼라이저가 유효한지 확인.
        serializer.is_valid(raise_exception=True)
        # 시리얼라이저의 validated_data 속성 사용해서 token 추출
        token = serializer.validated_data
        return Response({"token": token.key}, status=status.HTTP_200_OK)
    
class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer