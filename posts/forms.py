from django import forms
from posts.models import Post, Group, Comment
from sorl.thumbnail import ImageField

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'