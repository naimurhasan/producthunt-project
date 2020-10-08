from django.shortcuts import render

def login(request):
    return render(request, 'accounts/login.html')

def signup(request):
    pass

def logout(request):
    pass