from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from .models import UserProfile, UserInfo
from .forms import LoginForm, RegistrationForm, UserProfileForm, UserForm, UserInfoForm
from django.contrib.auth.decorators import login_required


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


# 显示个人信息
@login_required
def myself(request):
    userprofile = UserProfile.objects.get(user=request.user) if hasattr(request.user,
                                                                        'userprofile') else UserProfile.objects.create(
        user=request.user)
    userinfo = UserInfo.objects.get(user=request.user) if hasattr(request.user,
                                                                  'userinfo') else UserInfo.objects.create(
        user=request.user)
    return render(request, 'account/myself.html',
                  {'user': request.user, 'userinfo': userinfo, 'userprofile': userprofile})


# 修改个人信息
@login_required(login_url='/account/login')
def myself_edit(request):
    userprofile = UserProfile.objects.get(user=request.user) if hasattr(request.user,
                                                                        'userprofile') else UserProfile.objects.create(
        user=request.user)
    userinfo = UserInfo.objects.get(user=request.user) if hasattr(request.user,
                                                                  'userinfo') else UserInfo.objects.create(
        user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        userinfo_form = UserInfoForm(request.POST)
        if user_form.is_valid() * userprofile_form.is_valid() * userinfo_form.is_valid():
            user_cd = user_form.cleaned_data
            userprofile_cd = userprofile_form.cleaned_data
            userinfo_cd = userinfo_form.cleaned_data
            request.user.email = user_cd['email']
            userprofile.phone = userprofile_cd['phone']
            userinfo.company = userinfo_cd['company']
            userinfo.profession = userinfo_cd['profession']
            userinfo.aboutme = userinfo_cd['aboutme']
            request.user.save()
            userprofile.save()
            userinfo.save()
        return HttpResponseRedirect('/account/aboutme/')
    else:
        user_form = UserForm(instance=request.user)
        userprofile_form = UserProfileForm(initial={'phone': userprofile.phone})
        userinfo_form = UserInfoForm(
            initial={'company': userinfo.company, 'profession': userinfo.profession, 'aboutme': userinfo.aboutme})
        return render(request, 'account/myself_edit.html',
                      {'user_form': user_form, 'userprofile_form': userprofile_form, 'userinfo_form': userinfo_form})


def my_image(request):
    return render(request, 'account/imagecrop.html', )
