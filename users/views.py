from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ProfileUpdateForm, UserRegistrationForm, UserUpdateForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            message = f'{username}, your account has been created! You are now able to login.'
            messages.success(request, message)
            return redirect('login')
    else:
        form = UserRegistrationForm()

    context = {
        'form' : form
    }
    return render(request, 'users/register.html', context)


@login_required
def profile(request):
    user = request.user 
    profile = user.profile

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = ProfileUpdateForm(request.POST, 
                                         request.FILES, 
                                         instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            if 'image' in request.FILES:
                # delete olf profile pic and reset forms variables with user and profile instances
                # may need to set form variables without instances above - check validation - example: username already exists
                pass
            user_form.save()
            profile_form.save()

            message = 'Your account has been updated!'
            messages.success(request, message)
            return redirect('profile')

    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = ProfileUpdateForm(instance=profile)

    context = {
        'user_form' : user_form,
        'profile_form' : profile_form
    }

    return render(request, 'users/profile.html', context)
