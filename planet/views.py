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
from .models import SupportMessage
from django.contrib.auth.models import User


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
            auth_login(request, user)
            return redirect('main')
        else:
            messages.error(request, "Tài khoản hoặc mật khẩu không chính xác!")

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

@login_required(login_url='login')
def post_list(request):
    # Code xem danh sách bài viết của bạn...
    posts = Post1.objects.all()
    return render(request, 'post_list.html', {'posts': posts})

@login_required(login_url='login')
def post_detail(request, id):
    # Code xem chi tiết 1 bài viết của bạn...
    post = get_object_or_404(Post1, id=id)
    return render(request, 'post_detail.html', {'post': post})

@user_passes_test(lambda u: u.is_staff or u.is_superuser, login_url='login')
def edit_post(request, id):
    post = get_object_or_404(Post1, id=id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'edit_post.html', {'form': form, 'post': post})

@user_passes_test(lambda u: u.is_staff or u.is_superuser, login_url='login')
def delete_post(request, id):
    post = get_object_or_404(Post1, id=id)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'delete_post.html', {'post': post})

@login_required(login_url='login')
def user_chat(request):
    if request.user.is_staff or request.user.is_superuser:
        return redirect('admin_chat_list')

    if request.method == 'POST':
        msg = request.POST.get('message', '').strip()
        if msg:
            SupportMessage.objects.create(
                user=request.user,       # Cuộc trò chuyện thuộc về user này
                sender=request.user,     # Người gửi là chính user
                message=msg
            )
        return redirect('user_chat')

    messages_list = SupportMessage.objects.filter(user=request.user)
    return render(request, 'user_chat.html', {'messages_list': messages_list})

@login_required(login_url='login')
def admin_chat_list(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('user_chat')

    # Lấy danh sách các User đã từng nhắn tin
    user_ids = SupportMessage.objects.values_list('user', flat=True).distinct()
    users = User.objects.filter(id__in=user_ids)
    return render(request, 'admin_chat_list.html', {'chat_users': users})

@login_required(login_url='login')
def admin_chat_detail(request, user_id):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('user_chat')

    chat_user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        msg = request.POST.get('message', '').strip()
        if msg:
            SupportMessage.objects.create(
                user=chat_user,          # Thuộc cuộc trò chuyện của user đó
                sender=request.user,     # Người gửi là Admin
                message=msg
            )
        return redirect('admin_chat_detail', user_id=chat_user.id)

    messages_list = SupportMessage.objects.filter(user=chat_user)
    return render(request, 'admin_chat_detail.html', {'chat_user': chat_user, 'messages_list': messages_list})