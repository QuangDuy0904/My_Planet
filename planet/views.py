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
from .models import Planet, Post1, Comment
from .models import SupportMessage
from django.contrib.auth.models import User
from django.http import JsonResponse


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


@login_required(login_url='login')
def add_blog(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Tự động gán người đăng là tài khoản hiện tại
            post.save()
            return redirect('post_detail', id=post.id)
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
    post = get_object_or_404(Post1, id=id)

    # Xử lý gửi bình luận
    if request.method == 'POST' and 'comment_submit' in request.POST:
        if not request.user.is_authenticated:
            return redirect('login')
        content = request.POST.get('content', '').strip()
        if content:
            Comment.objects.create(
                post=post,
                user=request.user,
                content=content
            )
        return redirect('post_detail', id=post.id)

    # Kiểm tra xem user hiện tại đã thả tim bài này chưa
    is_liked = False
    if request.user.is_authenticated:
        is_liked = post.likes.filter(id=request.user.id).exists()

    comments = post.comments.all()

    context = {
        'post': post,
        'comments': comments,
        'is_liked': is_liked,
    }
    return render(request, 'post_detail.html', context)

# View xử lý bấm Tim/Bỏ tim
@login_required(login_url='login')
def like_post(request, id):
    post = get_object_or_404(Post1, id=id)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    # Trả về JSON để cập nhật giao diện mà không reload trang
    return JsonResponse({
        'liked': liked,
        'total_likes': post.total_likes
    })

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
                user=request.user,
                sender=request.user,
                message=msg,
                is_read=False
            )
        return redirect('user_chat')

    # Đánh dấu các tin nhắn của Admin gửi cho User là đã đọc khi User mở khung chat
    SupportMessage.objects.filter(user=request.user).exclude(sender=request.user).update(is_read=True)

    messages_list = SupportMessage.objects.filter(user=request.user)
    return render(request, 'user_chat.html', {'messages_list': messages_list})

# View Danh sách người chat (Admin)
@login_required(login_url='login')
def admin_chat_list(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('user_chat')

    user_ids = SupportMessage.objects.values_list('user', flat=True).distinct()
    users = User.objects.filter(id__in=user_ids)

    # Đếm số tin nhắn chưa đọc từ từng thành viên
    chat_list_data = []
    for u in users:
        unread_count = SupportMessage.objects.filter(user=u, sender=u, is_read=False).count()
        chat_list_data.append({
            'user': u,
            'unread_count': unread_count
        })

    return render(request, 'admin_chat_list.html', {'chat_list_data': chat_list_data})

# View Chi tiết khung chat (Admin)
@login_required(login_url='login')
def admin_chat_detail(request, user_id):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('user_chat')

    chat_user = get_object_or_404(User, id=user_id)

    # Đánh dấu toàn bộ tin nhắn của người này gửi là ĐÃ ĐỌC
    SupportMessage.objects.filter(user=chat_user, sender=chat_user, is_read=False).update(is_read=True)

    if request.method == 'POST':
        msg = request.POST.get('message', '').strip()
        if msg:
            SupportMessage.objects.create(
                user=chat_user,
                sender=request.user,
                message=msg,
                is_read=False
            )
        return redirect('admin_chat_detail', user_id=chat_user.id)

    messages_list = SupportMessage.objects.filter(user=chat_user)
    return render(request, 'admin_chat_detail.html', {'chat_user': chat_user, 'messages_list': messages_list})

@login_required(login_url='login')
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Tự động gán người đăng là tài khoản đang đăng nhập
            post.save()
            return redirect('post_detail', id=post.id)
    else:
        form = PostForm()
    
    return render(request, 'create_post.html', {'form': form})