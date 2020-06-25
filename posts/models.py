from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Group(models.Model):
    title = models.CharField(max_length = 200)
    slug = models.SlugField(unique=True)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class Post(models.Model):
    text = models.TextField(blank=False)
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    group = models.ForeignKey(Group, blank=True, null=True, on_delete=models.CASCADE, related_name="posts")
    image = models.ImageField(upload_to='posts/', blank=True)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField(blank=False)
    created = models.DateTimeField(auto_now_add=True)

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")