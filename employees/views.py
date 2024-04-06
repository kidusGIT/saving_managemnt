from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.

# LOGIN
def login_employee(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        password = request.POST.get('password')

        user = authenticate(request, username=employee_id, password=password)

        if user is not None:
            login(request, user)
            return redirect('home-page')
        
        else:
            messages.info(request, 'Invalid username or password')
        

    return render(request, 'login.html')

# LOGOUT
@login_required
def logout_employee(request):
    logout(request)
    return redirect('login-employee')
