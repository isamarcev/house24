from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Q
# Create your views here.
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DetailView, UpdateView

from users.forms import LoginUserForm, RegisterUserForm, CustomUserForm
from users.models import CustomUser, Role


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login_user.html'
    success_url = '/'


class UsersListView(ListView):
    model = CustomUser
    queryset = CustomUser.objects.all().order_by('id')
    context_object_name = 'users'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['roles'] = Role.objects.all()
        users1 = CustomUser.objects.filter(Q(first_name__icontains='') | Q(last_name__icontains="мыаршмы"))
        print(users1, 'fsadf')
        print(context)
        return context


class AjaxUsersListView(View):
        @staticmethod
        def get(request, *args, **kwargs):
            user = request.GET['user']
            role_name = request.GET['role']
            phone = request.GET['phone']
            email = request.GET['email']
            status_value = request.GET['status']
            users = CustomUser.objects.filter(Q(first_name__icontains=user) | Q(last_name__icontains=user),
                                              Q(role__name__icontains=role_name), Q(phone__contains=phone),
                                              Q(email__icontains=email), Q(status__contains=status_value)).order_by('id')
            user_list = []
            for user in users:
                instance = {
                    'id': user.id,
                    'user': f'{user.first_name} {user.last_name}',
                    'role': str(user.role.name).title(),
                    'phone': user.phone,
                    'email': user.email,
                    'status': user.status
                }
                user_list.append(instance)
            return JsonResponse({'users': user_list})


class UserCreateView(CreateView):
    model = CustomUser
    form_class = CustomUserForm
    context_object_name = 'users'
    success_url = reverse_lazy('users:users')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['label_suffix'] = ''
        return kwargs


class UserDetailView(DetailView):
    model = CustomUser


class UserUpdateView(UpdateView):
    pass

