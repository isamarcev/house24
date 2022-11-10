import datetime


from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Sum
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import CreateView, ListView, DetailView, UpdateView, \
    DeleteView, TemplateView
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.contrib.auth import logout as auth_logout

from crm_accounting.models import Invoice, status_invoice
from crm_accounting import views as account_views
from crm_home.models import TariffService
from houses.models import House, Flat, Section, Floor
from users.forms import LoginUserForm, CustomUserForm, \
    OwnerUserForm, RequestForm, MessageForm, RequestUserForm, RegisterUserForm
from users.models import CustomUser, Role, Request, Message, MessageUsers
from users.utilites import send_activation_notification, signer


def handler403(request, exception):
    response = render(request, 'error403.html', context={}, status=403)
    return response


def handlers404(request, exception):
    response = render(request, 'error404.html', context={}, status=404)
    print(response)

    return response


class CabinetPermissionMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = reverse_lazy('users:login')
    redirect_field_name = 'redirect_to'

    def test_func(self):
        if self.request.user.is_anonymous:
            return False
        elif not self.request.user.role:
            return True

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        elif self.request.user.role:
            return HttpResponseRedirect(reverse_lazy('houses:statistics'))


def check_remember_me_answer(self, form):
    remember_me = form.cleaned_data.get('remember_me')
    if not remember_me:
        self.request.session.set_expiry(0)
        self.request.session.modified = True


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login_user.html'

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return HttpResponseRedirect(reverse_lazy('users:message_list'))
        elif self.request.user.is_authenticated and not self.request.user.is_staff:
            return HttpResponseRedirect(reverse_lazy('users:user_profile'))
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('users:user_profile')

    def form_valid(self, form):
        ''' Check remember me checkbox from form'''
        check_remember_me_answer(self, form)
        return super(LoginUser, self).form_valid(form)


class RegisterUserView(CreateView):
    model = CustomUser
    form_class = RegisterUserForm
    template_name = 'users/registration_user.html'
    success_url = reverse_lazy('users:register_done')

    def get_context_data(self, **kwargs):
        context = super(RegisterUserView, self).get_context_data()
        confirmation = self.request.GET.get('notconfirm')
        if confirmation:
            context['confirm'] = 'Почта не подтверждена, поскольку ' \
                                 'использован нерпавильный ключ. ' \
                                 'Попробуйте еще раз'
        return context

    def post(self, request):
        form_class = self.form_class(request.POST)
        if form_class.is_valid():
            form_class.save()
            return HttpResponseRedirect(self.success_url)
        else:
            return render(request, self.template_name,
                          context={'form': form_class})


class RegisterDoneView(TemplateView):
    template_name = 'users/register_done.html'


class LoginAdminUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login_admin_user.html'

    # redirect_authenticated_user = reverse_lazy('users:layout')

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return HttpResponseRedirect(reverse_lazy('users:message_list'))
        elif self.request.user.is_authenticated and not self.request.user. \
                is_staff:
            return HttpResponseRedirect(reverse_lazy('users:user_profile'))
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('users:users')

    def form_valid(self, form):
        ''' Check remember me checkbox from form'''
        check_remember_me_answer(self, form)
        return super(LoginAdminUser, self).form_valid(form)


class LogoutUser(LogoutView):

    def get_success_url(self):
        return reverse_lazy('content:main')

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        """Logout may be done via POST."""
        auth_logout(request)
        return HttpResponseRedirect(reverse_lazy('content:main'))


class UsersListView(account_views.AdminPermissionMixin, ListView):
    model = CustomUser
    queryset = CustomUser.objects.filter(~Q(role=None)).order_by('id'). \
        select_related('role')
    context_object_name = 'users'
    check_permission_name = 'users'

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
        users = CustomUser.objects.filter(Q(first_name__icontains=user)
                                          | Q(last_name__icontains=user),
                                          Q(role__name__icontains=role_name),
                                          Q(phone__contains=phone),
                                          Q(email__icontains=email),
                                          Q(status__contains=status_value)). \
            order_by('id')
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


class UserCreateView(account_views.AdminPermissionMixin, CreateView):
    model = CustomUser
    form_class = CustomUserForm
    context_object_name = 'users'
    success_url = reverse_lazy('users:users')
    check_permission_name = 'users'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['label_suffix'] = ''
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(UserCreateView, self).get_context_data()
        user_id = self.request.GET.get('user_id')
        if user_id:
            user = get_object_or_404(CustomUser, id=user_id)
            initial = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role,
                'phone': user.phone
            }
            context['form'] = self.form_class(initial=initial)
        return context


class UserDetailView(account_views.AdminPermissionMixin, DetailView):
    model = CustomUser
    check_permission_name = 'users'


class UserUpdateView(account_views.AdminPermissionMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserForm
    context_object_name = 'users'
    success_url = reverse_lazy('users:users')
    template_name = 'users/customuser_update_form.html'
    check_permission_name = 'users'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['label_suffix'] = ''
        return kwargs

    def post(self, request, *args, **kwargs):
        form_class = self.form_class(request.POST, instance=self.get_object())
        if form_class.is_valid():
            form_class.save(commit=False)
            form_class.save()
            return HttpResponseRedirect(reverse_lazy('users:users'))
        return render(request, self.template_name, self.get_context_data())


def delete_user(request, pk):
    user = CustomUser.objects.get(pk=pk)
    if not user.is_superuser:
        user.delete()
    else:
        messages.error(request, 'Вы не можете удалть суперпользователя')
    return HttpResponseRedirect(reverse_lazy('users:users'))


class OwnerListView(account_views.AdminPermissionMixin, ListView):
    model = CustomUser
    context_object_name = 'users'
    queryset = CustomUser.objects.filter(role=None).prefetch_related(
        'house_set',
        'flat_set__house__personalaccount_set',
        'flat_set__personal_account').order_by('date_joined')
    template_name = 'users/owners_list.html'
    check_permission_name = 'owner'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['houses'] = House.objects.all()
        return context


class OwnerCreateView(account_views.AdminPermissionMixin, CreateView):
    model = CustomUser
    form_class = OwnerUserForm
    context_object_name = 'users'
    success_url = reverse_lazy('users:owner_list')
    template_name = 'users/owner_create_form.html'
    check_permission_name = 'owner'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['label_suffix'] = ''
        return kwargs

    def post(self, request, *args, **kwargs):
        form_class = self.form_class(request.POST, request.FILES)
        if form_class.is_valid():
            messages.success(request, 'Владелец успешно добавлен')
        return super().post(self, request, *args, **kwargs)


class OwnerUpdateView(account_views.AdminPermissionMixin, UpdateView):
    model = CustomUser
    form_class = OwnerUserForm
    context_object_name = 'users'
    success_url = reverse_lazy('users:owner_list')
    template_name = 'users/owner_update_form.html'
    check_permission_name = 'owner'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['label_suffix'] = ''
        return kwargs

    def post(self, request, *args, **kwargs):
        form_class = self.form_class(request.POST, request.FILES,
                                     instance=self.get_object())
        if form_class.is_valid():
            form_class.save(commit=False)
            form_class.save()
            messages.success(request, 'Владелец успешно обновлен')
            return HttpResponseRedirect(reverse_lazy('users:owner_list'))
        return render(request, self.template_name,
                      context={'form': form_class})


class OwnerDetailView(account_views.AdminPermissionMixin, DetailView):
    model = CustomUser
    template_name = 'users/owner_detail.html'
    check_permission_name = 'owner'
    queryset = CustomUser.objects.all(). \
        prefetch_related('flat_set__house__personalaccount_set')


class RequestsCreateView(account_views.AdminPermissionMixin, CreateView):
    model = Request
    success_url = reverse_lazy('users:requests_list')
    form_class = RequestForm
    check_permission_name = 'application'

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


class RequestListView(account_views.AdminPermissionMixin, ListView):
    model = Request
    queryset = model.objects.all().select_related('flat__house', 'owner')
    check_permission_name = 'application'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['owners'] = CustomUser.objects.filter(role=None)
        context['masters'] = CustomUser.objects.filter(~Q(role=None)). \
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
            qs = qs.filter(
                Q(flat__contains=flat) | Q(flat__house__contains=flat))
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


class RequestDetailView(account_views.AdminPermissionMixin, DetailView):
    model = Request
    check_permission_name = 'application'
    queryset = model.objects.all().select_related('flat__house',
                                                  'owner', 'master')


class RequestUpdateView(account_views.AdminPermissionMixin, UpdateView):
    model = Request
    template_name = 'users/request_update_form.html'
    success_url = reverse_lazy('users:requests_list')
    form_class = RequestForm
    check_permission_name = 'application'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['masters'] = CustomUser.objects.filter(~Q(role=None))
        return context


class MessageListView(account_views.AdminPermissionMixin, ListView):
    model = Message
    check_permission_name = 'message'

    def get_context_data(self, *, object_list=None, **kwargs):
        return {}


class MessageAjaxList(BaseDatatableView):
    model = Message
    columns = ['id', 'title', 'text', 'date',
               'message_address_house_id',
               'message_address_section_id', 'message_address_floor_id',
               'message_address_flat_id']

    def get_initial_queryset(self):
        return self.model.objects.all().order_by('-date')

    def filter_queryset(self, qs):
        search_field = self.request.GET.get('search')
        if search_field:
            qs = qs.filter(Q(title__icontains=search_field)
                           | Q(text__icontains=search_field))
        return qs


class MessageCreateView(account_views.AdminPermissionMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'users/message_form.html'
    check_permission_name = 'message'

    def post(self, request, *args, **kwargs):
        form_class = self.form_class(request.POST or None)
        if form_class.is_valid():
            form_class.save(commit=False)
            form_class.instance.sender = request.user
            form_class.save()
            users = CustomUser.objects.all().prefetch_related(
                'owner__personal_account__account_flat')
            message_for_deptors = request.POST.get('message_for_deptors')
            if message_for_deptors:
                users = users.filter(flat__personalaccount__balance__lt=0)
            house = request.POST.get('message_address_house_id')
            if house:
                users = users.filter(flat__house=house)
                section = request.POST.get('message_address_section_id')
                if section:
                    users = users.filter(flat__section=section)
                    floor = request.POST.get('message_address_floor_id')
                    if floor:
                        users = users.filter(flat__floor=floor)
                        flat = request.POST.get('message_address_flat_id')
                        if flat:
                            users = users.filter(flat=flat)
            MessageUsers.objects.bulk_create([MessageUsers(
                user=user, message=form_class.instance) for user in users])
            messages.success(request, 'Сообщение отправлено!')
            return HttpResponseRedirect(reverse_lazy('users:message_list'))
        else:
            return render(request, self.template_name, context={
                'form': form_class
            })


class MessageAjaxHouseInfo(View):
    @staticmethod
    def get(request):
        house = request.GET.get('house')
        sections = Section.objects.filter(house_id=house)
        floors = Floor.objects.filter(house_id=house)
        flats = Flat.objects.filter(house_id=house)
        section_list = list()
        floor_list = list()
        flat_list = list()
        for section in sections:
            instance = {
                'id': section.id,
                'title': section.title
            }
            section_list.append(instance)
        for floor in floors:
            instance = {
                'id': floor.id,
                'title': floor.title
            }
            floor_list.append(instance)
        for flat in flats:
            instance = {
                'id': flat.id,
                'title': flat.number
            }
            flat_list.append(instance)
        return JsonResponse({'section': section_list,
                             'floor': floor_list,
                             'flat': flat_list})


class MessageAjaxSectionInfo(View):
    @staticmethod
    def get(request):
        section = request.GET.get('section')
        floor = request.GET.get('floor')
        flats = Flat.objects.filter(section=section)
        if floor:
            flats = flats.filter(floor=floor)
        flat_list = list()
        for flat in flats:
            instance = {
                'id': flat.id,
                'title': flat.number
            }
            flat_list.append(instance)
        return JsonResponse({'flat': flat_list})


class MessageDetailView(account_views.AdminPermissionMixin, DetailView):
    model = Message
    check_permission_name = 'message'

    def get_queryset(self):
        return self.model.objects.filter(sender=self.request.user)


class MessageAjaxDelete(DeleteView):
    model = Message

    def post(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_staff:
            if request.POST.get('id'):
                message = get_object_or_404(Message, id=request.POST.get('id'))
                message.delete()
                return JsonResponse({'success': 'success'})
            messages_id = request.POST.get('deleted_list').split(',')
            messages = self.model.objects.filter(id__in=messages_id)
            messages.delete()
            return JsonResponse({'success': 'success'})
        else:
            return JsonResponse(
                {'success': "У Вас недостаточно прав для удаления."}
            )


class CabinetStatisticView(CabinetPermissionMixin, TemplateView):
    template_name = 'users/cabinet/statistics_for_flat.html'

    def get_context_data(self, **kwargs):
        context = dict()
        flat = get_object_or_404(Flat.objects.filter(owner=self.request.user).
                                 select_related('personal_account'),
                                 id=self.request.GET.get('flat_id'))
        context['personal_account'] = flat.personal_account
        context['flat'] = flat
        month_list = [number for number in range(1, 13)]
        payed_per_month = [Invoice.objects.
                           filter(flat=flat,
                                  date__month=number,
                                  status='Оплачена').
                           aggregate(Sum('amount'))
                           for number in month_list]
        payed_per_month_value = []
        for month in payed_per_month:
            if month.get('amount__sum'):
                payed_per_month_value.append(int(month.get('amount__sum')))
        if payed_per_month_value:
            context['average_per_month'] = sum(payed_per_month_value) / \
                                           len(payed_per_month_value)
        return context


class CabinetInvoicesListView(CabinetPermissionMixin, ListView):
    model = Invoice
    template_name = 'users/cabinet/invoice_users.html'

    def get_queryset(self):
        return self.model.objects.filter(flat__owner=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = dict()
        context['status'] = status_invoice
        if self.request.GET.get('flat_id'):
            context['flat_id'] = self.request.GET.get('flat_id')
        return context


class CabinetInvoicesAjaxList(BaseDatatableView):
    model = Invoice
    columns = ['id', 'number', 'date', 'status', 'amount']
    order_columns = ['date']

    def get_initial_queryset(self):
        flat_id = self.request.GET.get('flat')
        user_id = self.request.GET.get('user')
        qs = self.model.objects.filter(flat__owner=self.request.user)
        if flat_id:
            qs = qs.filter(flat_id=flat_id)
        if user_id:
            qs = qs.filter(flat__owner__id=user_id)
        return qs

    def filter_queryset(self, qs):
        date = self.request.GET.get('date')
        status = self.request.GET.get('status')
        if status:
            qs = qs.filter(status=status)
        if date:
            date_formatting = datetime.datetime.strptime(date, '%m/%d/%Y')
            qs = qs.filter(date=date_formatting)
        return qs


class CabinetInvoicesDetail(CabinetPermissionMixin, DetailView):
    model = Invoice
    template_name = 'users/cabinet/invoice_users_detail.html'

    def get_queryset(self):
        return Invoice.objects.filter(flat__owner=self.request.user). \
            prefetch_related('invoiceservice_set__service__unit')


class CabinetTariffForFlatView(CabinetPermissionMixin, TemplateView):
    model = TariffService
    template_name = 'users/cabinet/tariff_for_flat.html'

    def get_queryset(self):
        qs = get_object_or_404(
            TariffService.objects
            .filter(tariff__flat__owner=self.request.user)
            .select_related(''),
            tariff=self.request.GET.get('flat_id'))
        return qs

    def get_context_data(self, **kwargs):
        context = dict()
        context['object'] = \
            get_object_or_404(Flat.objects.filter(owner=self.request.user)
                              .select_related('house'),
                              id=self.request.GET.get('flat_id'))
        context['tariff_services'] = \
            self.model.objects. \
                filter(tariff__flat=self.request.GET.get('flat_id')). \
                select_related('service__unit')
        return context


class MessageUserList(CabinetPermissionMixin, TemplateView):
    template_name = 'users/cabinet/message_users_list.html'


class MessageUserAjaxList(BaseDatatableView):
    model = MessageUsers
    columns = ['id', 'message.text', 'message.title', 'message.date',
               'message.sender', 'read']

    def get_initial_queryset(self):
        return self.model.objects.filter(user=self.request.user). \
            select_related('message').order_by('-message_id')

    def filter_queryset(self, qs):
        search_field = self.request.GET.get('search')
        if search_field:
            qs = qs.filter(Q(message__title__icontains=search_field)
                           | Q(message__text__icontains=search_field))
        return qs


class MessageUserAjaxDelete(CabinetPermissionMixin, DeleteView):
    model = MessageUsers

    def post(self, request, *args, **kwargs):
        if request.POST.get('id'):
            message = get_object_or_404(MessageUsers.objects
                                        .filter(user=self.request.user),
                                        id=request.POST.get('id'))
            if message.user is request.user:
                message.delete()
                return JsonResponse({'success': 'success'})
            else:
                return JsonResponse({'success': 'Это не ваше сообщение'})
        messages_id = request.POST.get('deleted_list').split(',')
        messages = self.model.objects.filter(id__in=messages_id)
        for message in messages:
            if message.user is request.user:
                message.delete()
        return JsonResponse({'success': 'success'})


class MessageUserDetailView(CabinetPermissionMixin, DetailView):
    template_name = 'users/cabinet/message_user_detail.html'

    def get_queryset(self):
        qs = MessageUsers.objects.filter(user=self.request.user). \
            select_related('message')
        return qs

    def get_context_data(self, **kwargs):
        message = self.object
        if not message.read:
            message.read = True
            message.save()
        return super().get_context_data()


class RequestUserListView(CabinetPermissionMixin, TemplateView):
    template_name = 'users/cabinet/request_user_list.html'


class RequestUserAjaxListView(BaseDatatableView):
    model = Request
    columns = ['id', 'type_master', 'description', 'date', 'time',
               'status']

    def get_initial_queryset(self):
        return self.model.objects.filter(owner_id=self.request.user.id) \
            .order_by('-id')


class RequestUserAjaxDelete(CabinetPermissionMixin, DeleteView):
    model = Request

    def post(self, request, *args, **kwargs):
        master_request_id = request.POST.get('id')
        master_request = get_object_or_404(Request, id=master_request_id)
        if any([master_request.owner is request.user,
                request.user.is_superuser]):
            master_request.delete()
            return JsonResponse({'success': 'success'})
        else:
            return JsonResponse({'success': 'Это не ваш запрос!'})


class RequestUserCreateView(CabinetPermissionMixin, CreateView):
    model = Request
    template_name = 'users/cabinet/request_user_form.html'
    form_class = RequestUserForm

    def post(self, request, *args, **kwargs):
        form_class = self.form_class(request.POST or None)
        if form_class.is_valid():
            form_class.save(commit=False)
            form_class.instance.owner = request.user
            form_class.save()
            return HttpResponseRedirect(
                reverse_lazy('users:request_user_view'))
        else:
            return render(request, self.template_name,
                          context={'form': form_class})


class ProfileUserView(CabinetPermissionMixin, TemplateView):
    template_name = 'users/cabinet/profile_user_view.html'

    def get_context_data(self, **kwargs):
        context = dict()
        context['flats'] = Flat.objects.filter(owner=self.request.user). \
            select_related('floor', 'house', 'section')
        return context


class ProfileUserUpdate(CabinetPermissionMixin, UpdateView):
    template_name = 'users/cabinet/profile_user_update_form.html'
    form_class = OwnerUserForm
    success_url = reverse_lazy('users:user_profile')

    def get_object(self, queryset=None):
        return self.request.user


def confirm_register(request, sign):
    email = signer.unsign((sign))
    user = CustomUser.objects.filter(email=email)
    if user.exists():
        user = user.first()
        user.is_active = True
        user.status = 'Новый'
        user.save()
        return HttpResponseRedirect(reverse_lazy('users:login'))
    else:
        return HttpResponseRedirect(
            f"{reverse_lazy('users:register')}?notconfirm=True")
