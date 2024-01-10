from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView, PasswordResetConfirmView
from .forms import RegistrationForm, LoginForm, UserPasswordResetForm, UserSetPasswordForm, UserPasswordChangeForm
from django.contrib.auth import logout
from apps.utils import all_sales
from apps.models import Order
from django.contrib.auth.decorators import user_passes_test

# Create your views here.

# Pages


def is_staff_or_superuser(user):
    return user.is_staff or user.is_superuser


@user_passes_test(is_staff_or_superuser)
def index(request):
    return render(request, 'pages/index.html', {'segment': 'index', })


@user_passes_test(is_staff_or_superuser)
def billing(request):
    order = Order.objects.all()
    return render(request, 'pages/billing.html', {'segment': 'billing', "orders": order})


@user_passes_test(is_staff_or_superuser)
def tables(request):
    return render(request, 'pages/tables.html', {'segment': 'tables'})


@user_passes_test(is_staff_or_superuser)
def vr(request):
    return render(request, 'pages/virtual-reality.html', {'segment': 'vr'})


@user_passes_test(is_staff_or_superuser)
def rtl(request):
    return render(request, 'pages/rtl.html', {'segment': 'rtl'})


@user_passes_test(is_staff_or_superuser)
def notification(request):
    return render(request, 'pages/notifications.html', {'segment': 'notification'})


@user_passes_test(is_staff_or_superuser)
def profile(request):
    return render(request, 'pages/profile.html', {'segment': 'profile'})


# Authentication
class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            print('Account created successfully!')
            return redirect('/accounts/login/')
        else:
            print("Register failed!")
    else:
        form = RegistrationForm()

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def logout_view(request):
    logout(request)
    return redirect('/accounts/login/')


class UserPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    form_class = UserPasswordResetForm


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    form_class = UserSetPasswordForm


class UserPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    form_class = UserPasswordChangeForm
