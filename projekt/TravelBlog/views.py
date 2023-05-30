from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.http import JsonResponse
from django.utils import timezone
from .models import Post, User, Comment
from .forms import RegistrationForm, CommentForm, PostForm

# Create your views here.
def base(request):
    posts = Post.objects.all()
    user_group = 'Blogger' if request.user.groups.filter(name='Blogger').exists() else ''
    context = {
        'posts': posts,
        'user_group': user_group
    }
    return render(request, 'base.html', context)

def registration(request):
    if request.method == 'POST':
        clearMessageStorage(request)
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            if User.objects.filter(Q(username=username) | Q(email=email)).exists():
                messages.error(request, 'Użytkownik o podanym adresie email / nazwie użytkownika, już istnieje.')
            else:
                # Create the new user object and save it to the database
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                return redirect('base')
        else:
            print(form.errors)
    else:
        form = RegistrationForm()

    context = {
        'form': form,
        'messages': messages.get_messages(request),
    }
    return render(request, 'registration.html', context=context)

def login_view(request):
    clearMessageStorage(request)
    if request.method == 'POST':
        print("inside login POST")
        username = request.POST['username']
        password = request.POST['password']
        print(f"username: {username}, password: {password}")
        user = authenticate(request, username=username, password=password)
        print(f"inside login user: {user}")
        if user is not None:
            login(request, user)
            print(f"user: {username} is logged in")
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': 'Nieprawidłowa nazwa użytkownika, lub hasło.'}, status=401)
    else:
        redirect('base')

def logout_view(request):
    logout(request)
    return redirect('base')

def clearMessageStorage(request):
    storage = messages.get_messages(request)
    if storage.used:
        storage.clear()

def post_detail(request, pk):
    post = get_object_or_404(Post, post_id=pk)
    form = comment(request, pk, post)
    user_group = 'Blogger' if request.user.groups.filter(name='Blogger').exists() else ''
    print(request.user.groups.filter(name='Blogger').exists())
    return render(request, 'post_detail.html', {'post': post, 'form': form, 'user_group': user_group})

@login_required
def comment(request, pk, post):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            print(post)
            print(request.user)
            print(form.cleaned_data['content'])
            print(timezone.now().date())
            comment = Comment(
                post=post,
                author=request.user,
                content=form.cleaned_data['content'],
                created_at=timezone.now()
            )
            comment.save()
            messages.success(request, 'Dodano komentarz.')
            form = CommentForm()
    else:
        form = CommentForm()

    return form

def blogger_required(view_func):
    @user_passes_test(lambda user: user.groups.filter(name='Blogger').exists(), login_url='login')
    def wrapper(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    return wrapper

@blogger_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()

    # Redirect back to the post detail page
    return redirect('post_detail', pk=comment.post.pk)

def post_list(request):
    # posts = Post.objects.all()
    # num_posts = len(posts)
    # context = {'posts': posts, 'num_posts': num_posts}
    # return render(request, 'new_post.html', context)
    users = User.objects.all()
    num_users = len(users)
    context = {'users': users, 'num_users': num_users}
    return render(request, 'new_post.html', context)

def new_post(request):
    print(request.method)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, request=request)
        if form.is_valid():
            post = form.save(commit=False)
            # post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(request=request)

    return render(request, 'new_post.html', {'form': form})
