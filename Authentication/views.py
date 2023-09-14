from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from Authentication.models import CusUser
from Authentication.forms import UserLoginForm, UserRegisterForm
from Authentication.forms import UserChangePasswordForm
from django.contrib.auth import update_session_auth_hash


# Create your views here.
def UserLoginView(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            OneEmailOrUsername = form.cleaned_data.get('OneEmailOrUsername')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=OneEmailOrUsername, password=password)
            if user is not None:
                login(request, user)
                CusUser.objects.filter(id=user.id).update(is_status=True)
                return redirect(reverse('home'))
            else:
                messages.error(request, 'Sai tài khoản hoặc mật khẩu.')
                return redirect(reverse('login'))
        else:
            messages.error(request, 'Vui lòng kiểm tra lại thông tin.')
            return redirect(reverse('login'))
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'registration/login.html', context)


def UserLogoutView(request):
    if request.user.is_authenticated:
        user = CusUser.objects.get(username=request.user.username)
        CusUser.objects.filter(id=user.id).update(is_status=False)
        logout(request)
    return redirect(reverse('home'))


def UserRegisterView(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Đăng ký thành công.')
            return redirect(reverse('login'))
        else:
            messages.error(request, 'Vui lòng kiểm tra lại thông tin.')
    else:
        form = UserRegisterForm()
    context = {'form': form}
    return render(request, 'registration/register.html', context)

# def PasswordChangeView(request):
#     return render(request, 'features/_password_changes/_password_change_form.html', {})
# def PasswordChangeDoneView(request):
#     return render(request, 'features/_password_changes/_password_change_done.html', {})
