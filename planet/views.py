from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Post1
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .forms import PostForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
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
    if request.user.is_authenticated:
        return redirect('main')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Bạn đã đăng ký tài khoản thành công!")
            form = RegistrationForm()  # Làm sạch các ô sau khi lưu
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('main')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)  # Dùng auth_login ở đây
            return redirect('main')
        else:
            messages.error(request, "Tài khoản hoặc mật khẩu không chính xác.")

    return render(request, 'login.html')

def logout_view(request):
    auth_logout(request)
    return redirect('main')


@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def add_blogs(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'add_blog.html', {'form': form})

@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def add_blogs(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'add_blog.html', {'form': form})

def post_list(request):
    posts = Post1.objects.all().order_by('-date')
    return render(request, 'post_list.html', {'posts': posts})

def post_detail(request, id):
    post = get_object_or_404(Post1, id=id)
    return render(request, 'post_detail.html', {'post': post})