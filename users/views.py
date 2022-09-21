from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from users.forms import LoginUserForm, RegisterUserForm, CustomUserForm
from users.models import CustomUser


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login_user.html'
    success_url = '/'


class UsersListView(ListView):
    model = CustomUser


class UserCreateView(CreateView):
    model = CustomUser
    form_class = CustomUserForm
    context_object_name = 'users'
    success_url = reverse_lazy('users:users')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['label_suffix'] = ''
        return kwargs

    def post(self, request, *args, **kwargs):
        print(request.POST)
        form = self.form_class(request.POST)
        print(form.is_valid(), form.errors)
        return super().post(self, request, *args, **kwargs)



# class RegisterUser(CreateView):
#     form_class = RegisterUserForm
#     template_name = 'users/register.html'
#     success_url = '/'

#
# def logouts(requerst):
#         logout(requerst)
#         return redirect('/')


