from django.contrib.auth.models import User # User 모델
from django.contrib.auth.password_validation import validate_password # 장고 기본 pw 검증 도구
from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework.authtoken.models import Token # Token 모델
from rest_framework.validators import UniqueValidator # 이멜 중복 방지 검증 도구

from .models import Profile

class RegisterSerializer(serializers.ModelSerializer):
    # 이멜 중복 검증
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    # 비번 검증
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
    )
    # 비번 확인 위한 필드
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email')

    # 추가적으로 비번 일치 여부 확인
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return data
    
    # create 요청에 대해 create 메소드를 오버라이딩
    # user 생성하고 token 생성
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        # 시리얼라이저에서 받은 data
        user = authenticate(**data)
        if user:
            # 토큰에서 유저 찾아서 반환!
            token = Token.objects.get(user=user)
            return token
        raise serializers.ValidationError(
            {"error": "Unable to log in with provided credentials."}
        )
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("nickname", "position", "subjects", "image")