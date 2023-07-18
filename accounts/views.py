from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignupForm

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('verification_sent.html')
    else:
        form = SignupForm()
    
    param = {
        'form': form
    }
    return render(request, 'signup.html', param)
