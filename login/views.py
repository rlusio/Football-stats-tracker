from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login/register.html', {'form': form}, status=400)
    else:
        form = UserCreationForm()
    return render(request, 'login/register.html', {'form':form})

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')
    return render(request, 'login/register.html', {})