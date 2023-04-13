
from .models import Profile, UserModel
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
import re
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
# User_app/views.py


@csrf_exempt  # 추후 템플릿에 토큰 추가해서 제거필요
def sign_up_view(request) -> HttpResponse:
    """
    회원가입 기능. username, email, password, password confirm을 입력받는다.
    아이디: 8~30자, 알파벳으로 시작, 알파벳과 숫자, _ 이용가능
    이메일: 형식 갖춰야함
    비밀번호: 8자 이상, 전부 숫자면 안됨

    아이디 중복은 안됨
    """
    username_regex = '^[A-Za-z][A-Za-z0-9_]{7,29}$'
    if request.method == "GET":  # GET 메서드로 요청이 들어 올 경우
        return render(request, "User/signup.html")
    elif request.method == "POST":  # POST 메서드로 요청이 들어 올 경우
        input_dictionary = {
            'username': request.POST.get("username", "").strip(),
            'email': request.POST.get("email", "").strip(),
            'password': request.POST.get("password", "").strip(),
            'password2': request.POST.get("password2", "").strip(),
        }
        if UserModel.objects.filter(username=input_dictionary['username']).exists():

            return render(request, "User/signup.html", {'error': 'Already exist ID. Try others.'})

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


@csrf_exempt
def sign_in_view(request) -> HttpResponse:
    """username과 password를 받아 로그인"""
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
