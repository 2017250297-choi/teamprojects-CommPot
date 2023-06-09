from .models import Profile
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
import re
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
# User_app/views.py


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
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, "User/signup.html")
    elif request.method == "POST":  # POST 메서드로 요청이 들어 올 경우
        input_dictionary = {
            'username': request.POST.get("username", "").strip(),
            'email': request.POST.get("email", "").strip(),
            'password': request.POST.get("password", "").strip(),
            'password2': request.POST.get("password2", "").strip(),
        }
        if get_user_model().objects.filter(username=input_dictionary['username']).exists():

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
        new_user = get_user_model().objects.create(
            username=input_dictionary['username'],
            email=input_dictionary['email'],
        )
        try:
            new_user.set_password(input_dictionary['password'])
            new_user.save()
            new_profile = Profile.objects.create(
                username=new_user, description='')
            new_profile.save()
        except:
            return render(request, "User/signup.html", {'error': 'Invalid PW. Too common or similar with your ID or e-mail'})
        return redirect('/api/user/login')


def sign_in_view(request) -> HttpResponse:
    """username과 password를 받아 로그인"""
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, "user/signin.html")
    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if not user:

            return render(request, "user/signin.html", {'error': 'Invalid ID or PW.'})
        login(request, user)

        return redirect('/api/posts')


# def profile_view(request, id: int) -> HttpResponse or HttpResponseRedirect:


@login_required
def logout_view(request) -> HttpResponseRedirect:
    '''로그인한 회원이 로그아웃'''

    logout(request)
    return redirect('/api/posts')


def profile_view(request, path_username: str) -> HttpResponse:
    '''
    모든 사용자가 프로필 페이지를 조회할 수 있습니다. 프로필과 프로필 소유자의 글 목록이 주어집니다.
    오직 프로필 소유자 일때만 프로필의 수정을 할 수 있습니다.
    '''
    # 프로필 가져오기
    try:
        opened_profile = Profile.objects.get(username=path_username)
    except:
        return render(request, 'no_user.html')
    if request.method == 'GET':
        # 역참조로 지정된 사용자의 글만 가져오기
        posts = opened_profile.username.posting_set.order_by('-created_at')
        return render(request, 'User/profile.html', {'profile': opened_profile, 'posts': posts})
    if request.method == 'POST':
        if request.user != opened_profile.username:
            return redirect('/')
        locate = request.POST.get('locate', '')
        description = request.POST.get('description', '')
        opened_profile.locate = locate
        opened_profile.description = description
        to_default = request.POST.get('default', False)
        if (img := request.FILES.get('img', None)) or to_default == 'on':
            try:
                opened_profile.image.delete(save=False)
            except:
                pass
            opened_profile.image = img
            if to_default == 'on':
                opened_profile.image = None
        opened_profile.save()
        return redirect('/api/profile/'+path_username)


@login_required
def user_follow_view(request, path_username):
    me = request.user
    try:
        click_user = get_user_model().objects.get(username=path_username)
    except:
        return render(request, 'no_user.html')
    if me in click_user.followee.all():
        print('unfollow')
        click_user.followee.remove(request.user)
    else:
        print('follow')
        click_user.followee.add(request.user)
    return HttpResponseRedirect(request.GET.get('from', '/'))


@login_required
def delete_account_view(request):
    if request.method == 'POST':
        password = request.POST.get('password', '')
        my_account = get_user_model().objects.get(username=request.user.username)
        user = authenticate(
            request, username=request.user.username, password=password)
        if user:
            logout(request)
            my_account.delete()
            return redirect('/')
        return render(request, 'User/delete_account.html', {'error': 'Worng Password.'})
    else:
        return render(request, 'User/delete_account.html')
