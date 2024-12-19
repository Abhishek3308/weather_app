from django.shortcuts import render,redirect
from .models import CustomUser
from django.contrib import messages
import requests
import datetime
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
import os
from dotenv import load_dotenv
load_dotenv()
# Create your views here.

def sign_up(request):
    errors={}
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if CustomUser.objects.filter(email=email).exists():
            errors['email']="email is already exist"
            # messages.error(request, 'Email is already taken')
            # print('email already taken')
            # return redirect('signup') 
        if CustomUser.objects.filter(username=username).exists():
            errors['username']="username is already exists"

        if password!=confirm_password:
            errors['confirm_password']="Password doesn't match"

        if errors:
            return render(request,"signup.html",{'errors':errors})
        
        
        user= CustomUser.objects.create_user(
        email=email,
        username=username)
        user.set_password(password)
        user.save()
        messages.success(request, 'Account created successfully. Please log in.')
        return redirect('signin')
        
        # messages.error(request, 'Email is already taken')
    return render(request,'signup.html')

def sign_in(request):
    if request.method == 'POST':
        errors={}
        username = request.POST.get('username')
        password = request.POST.get('password')
        user= authenticate(request,username=username,password=password)
        print(user,"user")
        if user :
            login(request,user)
            return redirect('weather')
        else:
            errors['user']="user is not found"
            # messages.error(request,"invalid username or password")
           
            
        
    return render(request,'signin.html')

def home_view(request):
    
    user=request.user
    print(user,'uuuuuserrr')

    return render(request,'home.html',{'user':user})
def sign_out(request):
    logout(request)
    return redirect('home')
    # return render(request,'home.html')

@login_required(login_url='signin')
def weather(request):
    errors={}
    if 'city' in request.POST:
        city= request.POST.get('city')
        print(city,"nnnnnnn")
    else:
        city='calicut'
    APP_ID=os.getenv('APP_ID')

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={APP_ID}"
    PARAMS = {'units':'metric'}
   

    try:
        data=requests.get(url, params=PARAMS).json()
        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        temp = data['main']['temp']
        day=datetime.date.today()
        

        return render(request, 'weather.html',{
            'description': description,
            'icon': icon,
            'temp': temp,
            'day': day,
            'city':city,
            'exception_occured':False,
        })
        
    except KeyError:
        exception_occured = True
        errors['weather']="Enter date is not valid to API"
        # messages.error(request,'Enter date is not valid to API')
        day=datetime.date.today()
        
    return render(request,'weather.html',{
        'description':'clear sky',
        'icon':'01d',
        'temp':25,
        'day': day,
        'city': 'calicut',
        'exception_occured':exception_occured,
    })




