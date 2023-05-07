from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    post_id = models.CharField(max_length=10, primary_key=True)
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)