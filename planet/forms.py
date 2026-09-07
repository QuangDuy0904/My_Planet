from django import forms
import re
from django.contrib.auth.models import User
from .models import Post, Post1  # Thêm Post1

class RegistrationForm(forms.Form):
    username = forms.CharField(label='Tài khoản')
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Nhập lại mật khẩu', widget=forms.PasswordInput())

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError("Tên tài khoản không được chứa kí tự đặc biệt")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Tài khoản đã tồn tại")
        return username

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error('password2', "Mật khẩu nhập lại không khớp!")
        return cleaned_data

    def save(self):
        return User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1']
        )

# Form dùng cho trang đăng bài Post1 hiển thị ra web
class PostForm(forms.ModelForm):
    class Meta:
        model = Post1
        fields = ['title', 'body', 'image', 'audio']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập tiêu đề bài viết'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Nhập nội dung bài viết'}),
        }

# Giữ nguyên nếu bạn có dùng ở nơi khác
class BlogPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'description', 'content', 'image', 'audio')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title of the Blog'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Copy the title with no space and a hyphen in between'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Content of the Blog'}),
        }