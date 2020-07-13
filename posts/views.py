from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from posts.models import Post, Group, Follow
from users.models import LogoutTime, User
from posts.forms import PostForm, CommentForm, GroupForm


def index(request):
    last_logout = request.user.logout_time
    post_list = Post.objects.order_by('-pub_date').all()
    paginator = Paginator(post_list, 5) 
    page_number = request.GET.get('page') 
    page = paginator.get_page(page_number) 
    return render(request, 'index.html', {'page': page, 'paginator': paginator, 'last_logout': last_logout})

def group_posts(request, slug):
    last_logout = request.user.logout_time
    group = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.filter(group = group).order_by('-pub_date').all()
    paginator = Paginator(post_list, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'group.html', {'group':group, 'post_list':post_list, 'page':page, 'paginator': paginator, 'last_logout': last_logout})

@login_required
def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST or None)
        if form.is_valid():
            form.save()
            redirect_slug = form.cleaned_data['slug']
            return redirect('group', slug=redirect_slug)
        return render (request, 'create_group.html', {'form': form})
    form = GroupForm()
    return render (request, 'create_group.html', {'form': form})

@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST or None, files=request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
        return render(request, 'new.html', {'form':form})
    form = PostForm()
    return render(request, 'new.html', {'form':form})

def profile(request, username):
    last_logout = request.user.logout_time
    author = get_object_or_404(User, username=username)
    current_user = request.user
    following = current_user.is_authenticated and Follow.objects.filter(user=current_user, author=author).exists()
    post_list = author.posts.order_by('-pub_date')
    last_post = post_list.first()
    paginator = Paginator(post_list, 5)
    page_number = request.GET.get('page') 
    page = paginator.get_page(page_number) 
    return render(request, 'profile.html', {'author':author, 'page':page, 'paginator': paginator, 'last_post':last_post, 'following':following, 'last_logout': last_logout})
     

def post_view(request, username, post_id):
    post = get_object_or_404(Post, id=post_id)
    if not post.is_read.filter(id=request.user.id).exists() and request.user.is_authenticated:
        post.is_read.add(request.user)      
    comments = post.comments.all()
    form = CommentForm()
    group = post.group
    author = get_object_or_404(User, username=username)
    return render(request, 'post.html', {'post':post, 'author':author, 'comments':comments, 'group':group, 'form':form})

@login_required
def post_edit(request, username, post_id):
    update_indicator = True
    post = get_object_or_404(Post, id=post_id)
    current_user = request.user
    context = {
        'form':PostForm(),
        'update_indicator':update_indicator,
        'post':post
        }
    if current_user != post.author:
        return redirect('post', username=username, post_id=post.id )
    if request.method == 'POST':
        form = PostForm(request.POST or None, files=request.FILES or None, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post', username=username, post_id=post.id)
        return render(request, 'new.html', context=context)
    form = PostForm(instance=post)
    context['form'] = form
    return render(request, 'new.html', context=context)
    
def page_not_found(request, exception):
    return render(request, 'misc/404.html', {'path': request.path}, status=404)

def server_error(request):
    return render(request, 'misc/500.html', status=500)

@login_required
def add_comment(request, username, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            form.save()
            return redirect('post', username=username, post_id=post.id)
        return render(request, 'comments.html', {'form':form, 'comments':comments, 'post':post})
    form = CommentForm()
    return render(request, 'comments.html', {'form':form, 'comments':comments, 'post':post})

def post_delete(request, username, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect('post', username=username, id=post_id)
    post.delete()
    return redirect('profile', username=username)

@login_required
def follow_index(request):
    last_logout = request.user.logout_time
    current_user = request.user
    posts = Post.objects.filter(author__following__user=current_user).order_by('-pub_date')
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page') 
    page = paginator.get_page(page_number)
    return render(request, 'follow.html', {'page':page, 'paginator':paginator, 'last_logout': last_logout})

@login_required
def profile_follow(request, username):
    current_user = request.user
    author = get_object_or_404(User, username=username)
    if Follow.objects.filter(user=current_user, author=author).exists():
        return redirect('profile', username=username)
    if current_user != author:
        Follow.objects.create(user=current_user, author=author)
    return redirect('profile', username=author.username)

@login_required
def profile_unfollow(request, username):
    current_user = request.user
    author = get_object_or_404(User, username=username)
    relation = Follow.objects.filter(user=current_user, author=author)
    relation.delete()
    return redirect('profile', username=author.username)