from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Planet(models.Model):
  firstname = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)
  phone = models.IntegerField(null=True)
  dob = models.DateField(null=True)

  def __str__(self):
    return f"{self.firstname} {self.lastname}"

class Post(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    content = models.TextField()
    image = models.ImageField(null=True)
    date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('blog')

class Post1(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    audio = models.FileField(upload_to='madia/music', null=True)
    def __str__(self):
        return self.title