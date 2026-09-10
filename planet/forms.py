from django import forms
import re
from django.contrib.auth.models import User
from .models import Post, Post1  # Thêm Post1

class RegistrationForm(forms.Form):
    username = forms.CharField(
        label='Username:',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập tên đăng nhập'})
    )
    email = forms.EmailField(
        label='Email:',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Nhập địa chỉ email'})
    )
    password1 = forms.CharField(
        label='Password:',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nhập mật khẩu'})
    )
    password2 = forms.CharField(
        label='Confirm Password:',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nhập lại mật khẩu'})
    )

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
        fields = ['title', 'body', 'image', 'audio', 'youtube_url']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập tiêu đề bài viết...'
            }),
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Viết nội dung bài viết của bạn tại đây...'
            }),
            'youtube_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://www.youtube.com/watch?v=...'
            }),
        }
        labels = {
            'title': 'Tiêu đề',
            'body': 'Nội dung',
            'image': 'Ảnh minh họa',
            'audio': 'File âm thanh (MP3)',
            'youtube_url': 'Link video YouTube',
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