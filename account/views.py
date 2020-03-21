from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RegistrationForm, UserProfileForm


# 通过自写视图函数实现登陆
def user_login_view(request):
    if request.method == 'GET':
        login_form = LoginForm()
        return render(request, 'account/login.html', {'form': login_form})
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user:
                login(request, user)
                return HttpResponse('Welcome you. You have logined the website.')
            else:
                return HttpResponse('Sorry, your username or password is wrong.')
        else:
            return HttpResponse('Invalid login.')


def register(request):
    if request.method == 'GET':
        reg_form = RegistrationForm()
        profile_form = UserProfileForm()
        return render(request, 'account/register.html', {'reg_form': reg_form, 'profile_form': profile_form})
    if request.method == 'POST':
        reg_form = RegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if reg_form.is_valid() * profile_form.is_valid():
            user = profile_form.save(commit=False)
            user.set_password(reg_form.cleaned_data['password'])
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return HttpResponse('恭喜，注册成功。')
        else:
            return HttpResponse('对不起，注册失败。')
