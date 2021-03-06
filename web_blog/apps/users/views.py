from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User

def register(request):
    """Register of a new user"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,\
                f'{username}, your account has been created!\
                    Now you are able to log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    """Profile view of logged in users"""
    if request.method == 'POST':
        user_form = UserUpdateForm(
            request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES,
            instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        
    forms = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'users/profile.html', forms)


def users_list(request):
    """List of all blog memebers"""
    members = User.objects.all().order_by('username')

    return render(request, 'users/users_list.html',
        {'members': members}
    )
