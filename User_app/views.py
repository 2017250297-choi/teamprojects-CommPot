
from .models import Profile, UserModel
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
import re
# Create your views here.
# User_app/views.py


def sign_up_view(request):
    username_regex = '^[A-Za-z][A-Za-z0-9_]{7,29}$'
    if request.method == "GET":  # GET 메서드로 요청이 들어 올 경우
        return render(request, "User/signup.html")
    elif request.method == "POST":  # POST 메서드로 요청이 들어 올 경우
        input_dictionary = {
            'username': request.POST.get("username", "").trim(),
            'email': request.POST.get("email", "").trim(),
            'password': request.POST.get("password", "").trim(),
            'password2': request.POST.get("password2", "").trim(),
        }

        if not all(input_dictionary.values()):
            return render(request, "User/signup.html", {'error': 'please input every field.'})
        if re.match(username_regex, input_dictionary['username']) is None:
            return render(request, "User/signup.html", {'error': 'Wrong ID. Use alphabets, numbers, and "_". Start with alphabet, 8~30 letters.'})
        if re.match('^[\w\.-]+@+([\w-]+\.)+[\w-]{2,4}$', input_dictionary['email']) is None:
            return render(request, "User/signup.html", {'error': 'Invalid email address'})
        if re.match('^[0-9]*$', input_dictionary['password']) or len(input_dictionary['password']) < 8:
            return render(request, "User/signup.html", {'error': 'Invalid PW. 8 or more letters, no only numbers.'})
        if input_dictionary['password'] != input_dictionary['password2']:
            return render(request, "User/signup.html", {'error': 'password confirmation doesn\'t match.'})
        new_user = UserModel.objects.create(
            username=input_dictionary['username'],
            email=input_dictionary['email'],
        )
        try:
            new_user.set_password(input_dictionary['password'])
            new_user.save()
        except:
            return render(request, "User/signup.html", {'error': 'Invalid PW. Too common or similar with your ID or e-mail'})
        return redirect('/api/user/login')


def sign_in_view(request):
    if request.method == 'GET':
        return render(request, "user/signin.html")
    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if not user:
            return render(request, "user/signin.html", {'error': 'Invalid ID or PW.'})
        login(request, user)
        return redirect('/')


def profile_view(request, id: int) -> HttpResponse | HttpResponseRedirect:
    '''
    모든 사용자가 프로필 페이지를 조회할 수 있습니다. 프로필과 프로필 소유자의 글 목록이 주어집니다.
    오직 프로필 소유자 일때만 프로필의 수정을 할 수 있습니다.
    '''
    # 프로필 가져오기
    opened_profile = Profile.objects.get(id=id)
    if request.method == 'GET':
        # 역참조로 지정된 사용자의 글만 가져오기
        posts = opened_profile.username.posting_set.order_by('-created_at')
        return render('', {'profile': opened_profile, 'posts': posts})
    if request.method == 'POST':
        if request.user != opened_profile.username:
            return redirect('/')
        locate = request.POST.get('locate', '')
        description = request.POST.get('description', '')
        opened_profile.locate = locate
        opened_profile.description = description
        opened_profile.save()
        return redirect('/api/proflie/'+str(id))
