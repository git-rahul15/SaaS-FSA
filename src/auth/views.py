from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model

# Create your views here.

User = get_user_model()

def login_view(request):
    if request.method == 'POST':
        username = request.POST["username"] or None
        password = request.POST["password"] or None
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print(user.is_authenticated)
            return redirect ('/', {"user":user})
    return render(request, "auth/login.html", {})


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"] or None
        password = request.POST["password"] or None
        confirm_password = request.POST["confirm-password"] or None
        email = request.POST['email'] or None
        # user_exists_qs = User.objects.filter(username__iexact=username).exists()
        # email_exists_qs = User.objects.filter(email__iexact=username).exists()
        try:
            User.objects.create_user(username, email=email, password=password)
        except:
            pass
    return render(request, "auth/register.html",{})