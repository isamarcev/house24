from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
# Create your views here.
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from houses.models import House
from users.forms import LoginUserForm, RegisterUserForm, CustomUserForm, OwnerUserForm
from users.models import CustomUser, Role


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login_user.html'
    success_url = reverse_lazy('crm_home:roles')


class UsersListView(ListView):
    model = CustomUser
    queryset = CustomUser.objects.filter(role=True).order_by('id').select_related('role')
    context_object_name = 'users'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['roles'] = Role.objects.all()
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
    model = CustomUser
    form_class = CustomUserForm
    context_object_name = 'users'
    success_url = reverse_lazy('users:users')
    template_name = 'users/customuser_update_form.html'


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['label_suffix'] = ''
        return kwargs

    def post(self, request, *args, **kwargs):
        form_class = self.form_class(request.POST, instance=self.get_object())
        print(form_class.is_valid(), form_class.errors)
        if form_class.is_valid():
            form_class.save(commit=False)
            if len(request.POST.get('password')) == 0:
                del form_class.instance.password
            form_class.save()
            return HttpResponseRedirect(reverse_lazy('users:users'))
        return render(request, self.template_name, self.get_context_data())


def delete_user(request, pk):
    user = CustomUser.objects.get(pk=pk)
    if not user.is_superuser:
        user.delete()
        return HttpResponseRedirect(reverse_lazy('users:users'))


class OwnerListView(ListView):
    model = CustomUser
    context_object_name = 'users'
    queryset = CustomUser.objects.filter(role=None).prefetch_related('house_set',
                                                                      'flat_set__house__personalaccount_set',
                                                                     'flat_set__personal_account').order_by('date_joined')
    template_name = 'users/owners_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['houses'] = House.objects.all()
        return context


class OwnerCreateView(CreateView):
    model = CustomUser
    form_class = OwnerUserForm
    context_object_name = 'users'
    success_url = reverse_lazy('users:owner_list')
    template_name = 'users/owner_create_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['label_suffix'] = ''
        return kwargs

    def post(self, request, *args, **kwargs):
        form_class = self.form_class(request.POST, request.FILES)
        if form_class.is_valid():
            messages.success(request, 'Владелец успешно добавлен')
        return super().post(self, request, *args, **kwargs)


class OwnerUpdateView(UpdateView):
    model = CustomUser
    form_class = OwnerUserForm
    context_object_name = 'users'
    success_url = reverse_lazy('users:owner_list')
    template_name = 'users/owner_update_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['label_suffix'] = ''
        return kwargs

    def post(self, request, *args, **kwargs):
        form_class = self.form_class(request.POST, request.FILES, instance=self.get_object())
        if form_class.is_valid():
            form_class.save(commit=False)
            if len(request.POST.get('password')) == 0:
                del form_class.instance.password
            form_class.save()
            messages.success(request, 'Владелец успешно обновлен')
            return HttpResponseRedirect(reverse_lazy('users:owner_list'))
        return render(request, self.template_name, self.get_context_data())


class OwnerDetailView(DetailView):
    model = CustomUser
    template_name = 'users/owner_detail.html'

    def get_queryset(self):
        return CustomUser.objects.all().prefetch_related('flat_set__house__personalaccount_set')




