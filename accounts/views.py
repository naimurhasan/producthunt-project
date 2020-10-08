from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User

def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {'error':'Username or password didn\'t match'})

    return render(request, 'accounts/login.html')

def signup(request):
    if request.method == 'POST':
        # verify confirm pass
        if request.POST['password1'] == request.POST['password2']:
            try:
                # check if username taken
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'accounts/signup.html', {'error':'Username already taken'})
            except User.DoesNotExist:
                # create uuser
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                auth.login(request, user)
                return redirect('home')
        else:
            return render(request, 'accounts/signup.html', {'error':'Password Doesn\'t math.'})

    return render(request, 'accounts/signup.html')

def logout(request):
    auth.logout(request)
    return redirect('home')