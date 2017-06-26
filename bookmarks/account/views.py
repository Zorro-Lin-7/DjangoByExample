from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required


# Create your views here.


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

# to create a new view to display a dashboard to the user when he logs in their account.
@login_required
def dashboard(request):
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard'}) # define a section variable. 
                                            # We are going to use this variable to track which section of the site the user is watching.
                                            # Multiple views may correspond to the same section. 

def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        
        if user_form.is_valid():
            new_user = user_form.save(commit=False) #Create a new user object but avoid saving it yet
            new_user.set_password(user_form.cleaned_data['password']) #Set the chosen password
            new_user.save()  # Save the User object
            return render(request, 'account/register_done.html',{'new_user': new_user})
    else:                     # 此处犯过错，多了个缩进
        user_form = UserRegistrationForm()
    return render(request,'account/register.html',{'user_form': user_form})    