from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm, UserForm
from django.contrib.auth.models import Group
from .decorators import group_required

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name=form.cleaned_data.get('group'))
            user.groups.add(group)
            username = form.cleaned_data.get('username')
            messages.success(request, f'{username}, your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserForm()

    return render(request, 'users/register.html', context={'form': form, 'title': 'sign up'})


@login_required
@group_required('Copy editor')
def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name=form.cleaned_data.get('group'))
            user.groups.add(group)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account with username "{username}" and role "{group}" has been created! You are now able to give it to your new worker!')
            return redirect('profile')
    else:
        form = UserForm()

    return render(request, 'users/register.html', context={'form': form, 'title': 'sign up'})


@login_required
def profile(request):
    # If user want to change smth
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        # Check forms for correctness
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            # Say user that all things are succedeed and show fresh profile
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    if isUserInGroup(request.user, "Default user") or isUserInGroup(request.user, "Copy editor"):
        return render(request, 'users/profile.html', context)
    else:
        return render(request, 'users/profile_workers.html', context)


def isUserInGroup(user, groupname):
    return user.groups.filter(name=groupname).exists()