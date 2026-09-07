from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import RegistrationForm, BlogPostForm
from .models import Planet, Post1

def planet(request):
    myplanet = Planet.objects.all().values()
    template = loader.get_template('all_planet.html')
    context = {
        'myplanet': myplanet,
    }
    return HttpResponse(template.render(context, request))

def details(request, id):
    myplanet = Planet.objects.get(id=id)
    template = loader.get_template('details.html')
    context = {
        'myplanet': myplanet,
    }
    return HttpResponse(template.render(context, request))

def main(request):
    # Dùng render để truyền session user chuẩn xác vào template
    return render(request, 'main.html')

def testing(request):
    template = loader.get_template('template.html')
    mydata = Planet.objects.values_list('firstname')
    context = {
        'myplanets': mydata, 
        'fruits': ['Apple', 'Banana', 'Cherry'],  
    }
    return HttpResponse(template.render(context, request))

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Đăng ký tài khoản thành công! Hãy đăng nhập ngay.")
            return HttpResponseRedirect('/login/')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def Login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return HttpResponseRedirect("/")
        else:
            messages.error(request, "Invalid Credentials")
            return render(request, 'login.html')
    return render(request, "login.html")

def Logout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return HttpResponseRedirect('/login')

@login_required(login_url='/login')
def add_blogs(request):
    if request.method == "POST":
        form = BlogPostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            blogpost = form.save(commit=False)
            blogpost.author = request.user
            blogpost.save()
            obj = form.instance
            alert = True
            return render(request, "add_blog.html", {'obj': obj, 'alert': alert})
    else:
        form = BlogPostForm()
    return render(request, "add_blog.html", {'form': form})