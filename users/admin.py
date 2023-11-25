from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile

# admin.StackedInline 클래스를 상속받아 profile 모델을 세로로 스택된 형태로 표현
class ProfileInline(admin.StackedInline):
    model = Profile
    # profile 삭제할 수 없도록
    can_delete = False
    # 복수형 표현
    verbose_name_plural = "profile"

class UserAdmin(BaseUserAdmin):
    # UserAdmin 클래스에 ProfileInline을 추가해서 User 관리자 패널에 profile 정보 표시
    inlines = (ProfileInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)