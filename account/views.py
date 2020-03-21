from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RegistrationForm, UserProfileForm


# 通过自写视图函数实现登陆
def user_login_view(request):
    if request.method == 'GET':
        login_form = LoginForm()
        return render(request, 'account/login_view.html', {'form': login_form})
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
        profile_form = UserProfileForm(request.POST)  # 补充一个表
        if reg_form.is_valid() * profile_form.is_valid():  # 相当于and逻辑
            user = reg_form.save(commit=False)  # 获验证后的表单，创立变量但不提交
            user.set_password(reg_form.cleaned_data['password'])  # 设定用户密码
            user.save()  # 最后保存注册的用户
            profile = profile_form.save(commit=False)
            profile.user = user  # 模型里UserProfile字段对应
            profile.save()
            return HttpResponse('恭喜，注册成功。')
        else:
            return HttpResponse('对不起，注册失败。')
