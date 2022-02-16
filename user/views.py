from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.models import User

from .models import Profile

from .forms import SignUpForm, LoginForm, UserUpdateForm, ProfileUpdateForm

# Create your views here.

def login_view(request):
    if request.method=='POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None :
                login(request,user)
                return redirect('admin-dashboard')
            else:
                messages.error(request,"Invalid username or password")
        else:
                messages.error(request,"Invalid username or password")
    return render(request, 'user/login.html',
    context={'form':LoginForm()})

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            #user = form.save()
            # group = Group.objects.get(name='Users')
            # user.groups.add(group)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account {username} has been created')
            return redirect('login')
    else:
        form = SignUpForm()
    context = {
        'form': form
    }
    return render(request, 'user/register.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')

def profile(request):
    return render(request, 'user/profile.html')

def profile_update(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'user/profile_update.html', context)

def settings_account(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('settings-account')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'settings/settings.html', context)

def settings_pass(request):
    return render(request, 'settings/settings_pass.html')

def analytics_view(request):
    users = User.objects.all()
    # users_count = users.count()
    users_count = User.objects.all().count()
    admin_count = Profile.objects.filter(role='Administrator').count()
    student_count = Profile.objects.filter(role='Student').count()
    staff_count = Profile.objects.filter(role='STAFF').count()
    faculty_count = Profile.objects.filter(role='FACULTY').count()
    # foot_traffic = RoomReservation.objects.filter(date=date.today()).count()
    
    context = {
        'users': users,
        'users_count': users_count,        
        'admin_count': admin_count,
        'student_count': student_count,
        'staff_count': staff_count,
        'faculty_count': faculty_count,
        # 'foot_traffic': foot_traffic,
    }
    return render(request, 'analytics.html', context)