from django.urls import path

from . import views


urlpatterns = [
    # profile 페이지 조회,수정
    path('api/profile/<int:id>', views.profile_view, name='profile'),
    path("api/user/signup/", views.sign_up_view, name="sign-up"),
    path("api/user/login/", views.sign_in_view, name="login"),
    path("api/user/logout/", views.logout_view, name="logout"),
]
