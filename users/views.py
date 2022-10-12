import datetime

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
from django_datatables_view.base_datatable_view import BaseDatatableView

from houses.models import House, Flat
from users.forms import LoginUserForm, RegisterUserForm, CustomUserForm, \
    OwnerUserForm, RequestForm
from users.models import CustomUser, Role, Request


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
        return CustomUser.objects.all().\
            prefetch_related('flat_set__house__personalaccount_set')


class RequestsCreateView(CreateView):
    model = Request
    success_url = reverse_lazy('users:requests_list')
    form_class = RequestForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['masters'] = CustomUser.objects.filter(~Q(role=None))
        return context


class AjaxUserFlatsList(View):

    @staticmethod
    def get(request, *args, **kwargs):
        owner_id = request.GET.get('owner_id')
        query_flats = Flat.objects.filter(owner=owner_id)
        flat_list = list()
        for flat in query_flats:
            item = {
                'id': flat.id,
                'number': flat.number,
                'house': flat.house.title
            }
            flat_list.append(item)
        return JsonResponse({'flats': flat_list})


class RequestListView(ListView):
    model = Request
    queryset = model.objects.all().select_related('flat__house', 'owner')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['owners'] = CustomUser.objects.filter(role=None)
        context['masters'] = CustomUser.objects.filter(~Q(role=None)).\
            select_related('role')
        return context


class RequestGetViewAjax(BaseDatatableView):
    model = Request
    columns = ['id', 'date', 'time', 'type_master',
               'description', 'flat', 'flat.house', 'flat.id',
               'owner', 'owner.id', 'owner.phone', 'master',
               'master.id', 'status']
    order_columns = ['id', 'date', 'type_master']

    def get_initial_queryset(self):
        return self.model.objects.all().select_related('flat__house',
                                                       'owner')

    def filter_queryset(self, qs):
        id = self.request.GET.get('id')
        date_range = self.request.GET.get('date_range')
        type_master = self.request.GET['type_master']
        description = self.request.GET.get('description')
        flat = self.request.GET.get('flat')
        owner = self.request.GET.get('owner')
        phone = self.request.GET.get('phone')
        master = self.request.GET.get('master')
        status = self.request.GET.get('status')
        if date_range:
            date_start = datetime.datetime.strptime(date_range.split(' - ')[0],
                                                    '%m/%d/%Y')
            date_end = datetime.datetime.strptime(date_range.split(' - ')[1],
                                                    '%m/%d/%Y')
            qs = qs.filter(Q(date__gt=date_start), Q(date__lt=date_end))
        if id:
            qs = qs.filter(id=id)
        if type_master:
            qs = qs.filter(type_master=type_master)
        if description:
            qs = qs.filter(description__contains=description)
        if flat:
            qs = qs.filter(Q(flat__contains=flat)|Q(flat__house__contains=flat))
        if owner:
            qs = qs.filter(owner=owner)
        if phone:
            qs = qs.filter(flat__owner__phone__contains=phone)
        if master:
            qs = qs.filter(master=master)
        if status:
            qs = qs.filter(status=status)
        return qs


class RequestDeleteAjax(DeleteView):

    def post(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_staff:
            request_id = request.POST.get('id')
            request_instance = get_object_or_404(Request, id=request_id)
            request_instance.delete()
            return JsonResponse({'success': 'success'})
        else:
            return JsonResponse(
                {'success': "У Вас недостаточно прав для удаления."}
            )


class RequestDetailView(DetailView):
    model = Request

    def get_queryset(self):
        return self.model.objects.all().select_related('flat__house',
                                                       'owner', 'master')


class RequestUpdateView(UpdateView):
    model = Request
    template_name = 'users/request_update_form.html'
    success_url = reverse_lazy('users:requests_list')
    form_class = RequestForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['masters'] = CustomUser.objects.filter(~Q(role=None))
        return context