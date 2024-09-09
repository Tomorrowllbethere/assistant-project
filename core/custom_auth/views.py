from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin

from django.urls import reverse_lazy
from custom_auth.forms import RegisterForm, LoginForm, ProfileForm

def signupuser(request):
    if request.user.is_authenticated:
        return redirect(to='features:main')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            print(form['username'], form['password1'])
            form.save()
            return redirect(to='custom_auth:login')
        else:
            return render(request, 'custom_auth/signup.html', context={"form": form})

    return render(request, 'custom_auth/signup.html', context={"form": RegisterForm()})

def loginuser(request):
    if request.user.is_authenticated:

        return redirect(to='features:main')

    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is None:
            messages.error(request, 'Username or password didn\'t match')
            return redirect(to='custom_auth:login')

        login(request, user)
        return redirect(to='features:main')

    return render(request, 'custom_auth/login.html', context={"form": LoginForm()})


@login_required
def logoutuser(request):
    logout(request)
    return redirect(to='features:welcome')


@login_required
def profile(request):
    # return render(request, 'users/profile.html')
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='custom_auth:profile')

    profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'custom_auth/profile.html', context={'profile_form': profile_form})


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'custom_auth/password_reset.html'
    email_template_name = 'custom_auth/password_reset_email.html'
    html_email_template_name = 'custom_auth/password_reset_email.html'
    success_url = reverse_lazy('custom_auth:password_reset_done')
    success_message = "An email with instructions to reset your password has been sent to %(email)s."
    subject_template_name = 'custom_auth/password_reset_subject.txt'

