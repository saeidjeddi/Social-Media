from django.shortcuts import render,redirect
from django.views import View
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.


class RegisterView(View):
    form_class = RegisterForm
    template_name = 'account/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):

        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'], cd['email'], cd['password1'])
            messages.success(request, 'your registered.', 'success')
            return redirect('home:index')
        return render(request, self.template_name, {'form': form})


class LoginView(View):
    form_class = LoginForm
    templates_name = 'account/login.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):

        form = self.form_class()
        return render(request, self.templates_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'you login in account.', 'success')
                return redirect('home:index')
            messages.warning(request,'username or password is wrong', 'warning')
            return render(request, self.templates_name, {'form': form})


def logouts(request):
    user = request.user.username
    logout(request)
    messages.success(request, f'bye {user} 	👋', 'primary')
    return redirect("home:index")
