from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponse
from .models import Post, User
from .forms import RegistrationForm

# Create your views here.
def base(request):
    return render(request, 'base.html')

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
    #post = get_object_or_404(Post, pk=pk)
    post = Post.objects.get(pk=pk)
    return render(request, 'post_detail.html')
