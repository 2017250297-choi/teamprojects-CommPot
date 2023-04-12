from django.contrib import admin


from .models import UserModel,Profile

# 나의 UserModel을 Admin에 추가
admin.site.register(UserModel)
admin.site.register(Profile)
