from django.contrib import messages
from django.db.models import Q
from django.db.models.aggregates import Sum
from django.forms import modelformset_factory
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, \
    ListView, DeleteView, View
from django_datatables_view.base_datatable_view import BaseDatatableView
from datetime import datetime
from crm_home.models import PaymentState, TariffService
from houses.models import Section, Flat, House
from users.models import CustomUser
from . import models
from . import forms
from .models import get_next_transaction, PersonalAccount


# Create your views here.


def main_page(request, pk):
    pass


def get_statistics(context):
    """Balance personal accounts, depts and cahsbox`s state """
    income = models.Transaction.objects. \
        filter(payment_state__type='in').aggregate(Sum('amount'))
    outcome = models.Transaction.objects. \
        filter(payment_state__type='out').aggregate(Sum('amount'))
    cashbox_state = income['amount__sum'] - outcome['amount__sum']
    sum_personal_accounts = models.PersonalAccount.objects.all().aggregate(
        Sum('balance'))
    context['cashbox_state'] = cashbox_state
    context['sum_accounts_balance'] = sum_personal_accounts.get('balance__sum')
    invoices_dopts = models.Invoice.objects.filter(
        payment_state=True,status__in=['Неоплачена', 'Частично оплачена']). \
        aggregate(Sum('amount'))
    context['invoices_dobts'] = invoices_dopts.get('amount__sum')
    return context



class AccountCreateView(CreateView):
    model = models.PersonalAccount
    form_class = forms.PersonalAccountForm
    success_url = reverse_lazy('crm_accounting:account_list')
    template_name = 'crm_accounting/personalaccount_form.html'

    def post(self, request, *args, **kwargs):
        form_class = self.form_class(request.POST or None)
        if form_class.is_valid():
            flat = request.POST.get('flat')
            form_class.save()
            if flat:
                flat = Flat.objects.get(pk=flat)
                flat.personal_account = form_class.instance
            return HttpResponseRedirect(self.success_url)
        else:
            return render(request, self.template_name,
                          context={'form': form_class})


class PersonalAccountUpdateView(UpdateView):
    model = models.PersonalAccount
    template_name = 'crm_accounting/personalaccount_update_form.html'
    form_class = forms.PersonalAccountForm
    success_url = reverse_lazy('crm_accounting:account_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        account = self.get_object()
        context['sections'] = Section.objects.filter(house=account.house)
        context['flats'] = Flat.objects.filter(section=account.section). \
            order_by('number')
        print(context)
        return context

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        form_class = self.form_class(request.POST or None, instance=instance)
        if form_class.is_valid():
            flat = request.POST.get('flat')
            form_class.save()
            if flat:
                flat = Flat.objects.get(pk=flat)
                flat.personal_account = form_class.instance
            return HttpResponseRedirect(self.success_url)
        else:
            return render(request, self.template_name,
                          context={'form': form_class})


class AccountListView(ListView):
    model = models.PersonalAccount
    queryset = None

    def get_context_data(self, *, object_list=None, **kwargs):
        context = dict()
        context['houses'] = House.objects.all()
        context['owner'] = CustomUser.objects.all()
        context = get_statistics(context)
        return context


class AccountListViewAjax(BaseDatatableView):
    model = models.PersonalAccount
    columns = ['account_number', 'status', 'flat.number',
               'house', 'section', 'flat.owner', 'balance', 'id']
    order_columns = ['account_number', 'status', 'flat.number',
                     'house', 'section', 'flat.owner', 'balance', 'id']

    def get_initial_queryset(self):
        return self.model.objects.all().select_related('house', 'section',
                                                       'flat__owner')

    def filter_queryset(self, qs):
        number = self.request.GET.get('number')
        house = self.request.GET.get('house')
        section = self.request.GET.get('section')
        flat = self.request.GET.get('floor')
        status = self.request.GET.get('status')
        owner = self.request.GET.get('owner')
        dolg = self.request.GET.get('dolg')
        if number:
            qs = qs.filter(account_number__icontains=number)
        if house:
            qs = qs.filter(house=house)
        if section:
            qs = qs.filter(section=section)
        if flat:
            qs = qs.filter(flat=flat)
        if owner:
            qs = qs.filter(flat__owner=owner)
        if dolg:
            if dolg == 'false':
                qs = qs.filter(balance__gt=0)
            elif dolg == 'true':
                qs = qs.filter(balance__lt=0)
        if status:
            qs = qs.filter(status=status)
        return qs


class DeletePersonalAccount(DeleteView):
    model = models.PersonalAccount

    def post(self, request, *args, **kwargs):
        personal_account = self.model.objects.get(
            pk=request.POST.get('account'))
        if request.user.is_superuser:
            personal_account.delete()
            return JsonResponse({'success': 'success'})
        else:
            return JsonResponse(
                {'success': 'Удаление счета доступно только Директору'})


class PersonalAccountDetailView(DetailView):
    model = models.PersonalAccount
    template_name = 'crm_accounting/personalaccount_detail.html'


def get_flats(request):
    if request.GET:
        flat_list = list()
        if request.GET.get('section'):
            section = request.GET.get('section')
            flats = Flat.objects.filter(section=section). \
                select_related('owner')
            for flat in flats:
                element = {
                    'flat_id': flat.id,
                    'flat_number': flat.number,
                }
                flat_list.append(element)
        return JsonResponse({'flats': flat_list}, status=200)


def get_users(request):
    if request.GET:
        owner_info = dict()
        if request.GET.get('flat'):
            flat = request.GET.get('flat')
            try:
                owner = CustomUser.objects.get(flat=flat)
                owner_info['name'] = \
                    f'{owner.first_name} {owner.last_name} {owner.father_name}'
                owner_info['phone'] = owner.phone
                owner_info['id'] = owner.id
            finally:
                pass
        return JsonResponse({'owner': owner_info}, status=200)


def calculate_balance(form_class, **kwargs):
    """Check the form Transaction for checkbox and calculate account balance"""
    form_class.save(commit=False)
    form_type = kwargs.get('type')
    payment_state = form_class.instance.payment_state.type

    if form_type == 'update' and payment_state == 'in':
        completed_instance = kwargs.get('completed')
        completed_instance_form = form_class.instance.completed
        account = models.PersonalAccount.objects.get(
            id=form_class.instance.personal_account.id)
        if completed_instance == completed_instance_form:
            pass
        elif completed_instance_form:
            operation = account.balance + form_class.instance.amount
            account.balance = operation
            account.save()
        elif not completed_instance_form:
            operation = account.balance - form_class.instance.amount
            account.balance = operation
            account.save()
    elif form_type == 'create' and payment_state == 'in':
        account = models.PersonalAccount.objects.get(
            id=form_class.instance.personal_account.id)
        if form_class.instance.completed:
            operation = account.balance + form_class.instance.amount
            account.balance = operation
            account.save()
    form_class.save()


class TransactionCreateView(CreateView):
    model = models.Transaction
    form_class = forms.TransactionForm
    success_url = reverse_lazy('crm_accounting:transaction_list')

    def get_context_data(self, **kwargs):
        context = dict()
        context['manager_list'] = CustomUser.objects.filter(~Q(role=None)). \
            select_related('role')
        type_of_transaction = self.request.GET.get('type')
        context['manager'] = self.request.user
        instance_id = self.request.GET.get('transaction_id')
        if kwargs.get('form'):
            context['form'] = kwargs['form']
        else:
            context['form'] = self.form_class()
        if instance_id:
            transaction = models.Transaction.objects.select_related('manager',
                                                                    'owner'). \
                get(pk=instance_id)
            initial = {
                'payment_state': transaction.payment_state,
                'comment': transaction.comment,
                'owner': transaction.owner,
                'personal_account': transaction.personal_account,
                'amount': transaction.amount,
                'manager': transaction.manager,
                'completed': transaction.completed
            }
            context['form'] = self.form_class(initial=initial)
            type_of_transaction = transaction.payment_state.type
            context['manager'] = transaction.manager
        if type_of_transaction == 'in':
            context['type'] = 'приходная ведомость'
        elif type_of_transaction == 'out':
            context['type'] = 'расходная ведомость'
        context['payment_states'] = PaymentState.objects.filter(
            type=type_of_transaction)
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.form_class(request.POST or None)
        if form_class.is_valid():
            calculate_balance(form_class, type='create')
            return HttpResponseRedirect(self.success_url)
        else:
            return render(request, 'crm_accounting/transaction_form.html',
                          context={'form': form_class})


def get_personal_accounts_ajax(request):
    owner_id = request.GET.get('owner_id')
    accounts = models.PersonalAccount.objects.filter(
        account_flat__owner_id=owner_id)
    account_list = list()
    for i in accounts:
        account = {
            'id': i.id,
            'account_number': i.account_number
        }
        account_list.append(account)
    return JsonResponse({'accountList': account_list})


class TransactionListView(ListView):
    model = models.Transaction
    queryset = None

    def get_context_data(self, *, object_list=None, **kwargs):
        context = dict()
        context['owners'] = CustomUser.objects.filter(role=None)
        context['payment_states'] = PaymentState.objects.all()
        context = get_statistics(context)
        return context


def filter_qs_daterange(date, qs):
    date_start = datetime.strptime(date.split(' - ')[0],
                                   '%m-%d-%Y')
    date_end = datetime.strptime(date.split(' - ')[1],
                                 '%m-%d-%Y')
    qs = qs.filter(Q(date__gt=date_start), Q(date__lt=date_end))
    return qs



class TransactionListViewAjax(BaseDatatableView):
    model = models.Transaction
    columns = ['number', 'date', 'completed', 'payment_state',
               'owner', 'personal_account', 'payment_state.type',
               'amount', 'id']
    order_columns = ['date']

    def get_initial_queryset(self):
        return self.model.objects.all().select_related('payment_state'). \
            order_by('-number')

    def filter_queryset(self, qs):
        number = self.request.GET.get('number')
        date = self.request.GET.get('date')
        owner = self.request.GET.get('owner')
        personal_account = self.request.GET.get('personal_account')
        completed = self.request.GET.get('completed')
        payment_state = self.request.GET.get('paymentstate')
        type_of_payment = self.request.GET.get('type_of_payment')
        if type_of_payment:
            qs = qs.filter(payment_state__type=type_of_payment)
        if number:
            qs = qs.filter(number__contains=number)
        if owner:
            qs = qs.filter(owner=owner)
        if personal_account:
            qs = qs.filter(personal_account__contains=personal_account)
        if completed:
            if completed == 'completed':
                qs = qs.filter(completed=True)
            elif completed == 'not_completed':
                qs = qs.filter(completed=False)
        if payment_state:
            qs = qs.filter(payment_state=payment_state)
        if date:
            qs = filter_qs_daterange(date, qs)
        return qs


class DeleteTransaction(DeleteView):
    model = models.Transaction

    def get(self, request, *args, **kwargs):
        transaction = self.model.objects.get(
            pk=request.GET.get('transaction')
        )
        transaction.delete()
        return HttpResponseRedirect(
            reverse_lazy('crm_accounting:transaction_list'))

    def post(self, request, *args, **kwargs):
        transaction = self.model.objects.get(
            pk=request.POST.get('account'))
        if request.user.is_superuser:
            transaction.delete()
            return JsonResponse({'success': 'success'})
        else:
            return JsonResponse({'success': 'Удаление счета доступно '
                                            'только старшему персоналу!'})


class TransactionUpdateView(UpdateView):
    model = models.Transaction
    form_class = forms.TransactionForm
    success_url = reverse_lazy('crm_accounting:transaction_list')
    template_name = 'crm_accounting/transaction_update_form.html'

    def get_context_data(self, **kwargs):
        instance = self.get_object()
        context = dict()
        if kwargs.get('form'):
            context['form'] = kwargs['form']
        else:
            context['form'] = self.form_class(instance=instance)
        context['object'] = instance
        instance = context['form'].instance
        type_of_transaction = instance.payment_state.type
        if type_of_transaction == 'in':
            context['type'] = 'Приходная ведомость'
        elif type_of_transaction == 'out':
            context['type'] = 'Расходная ведомость'
        context['payment_states'] = PaymentState.objects.filter(
            type=type_of_transaction)
        context['manager_list'] = CustomUser.objects.filter(~Q(role=None)). \
            select_related('role')
        return context

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        completed_instance = instance.completed
        form_class = self.form_class(request.POST or None, instance=instance)
        if form_class.is_valid():
            calculate_balance(form_class, type='update',
                              completed=completed_instance)
            return HttpResponseRedirect(self.success_url)
        else:
            return render(request,
                          'crm_accounting/transaction_update_form.html',
                          context={'form': form_class})


class TransactionDetailView(DetailView):
    model = models.Transaction

    def get_queryset(self):
        return self.model.objects.all(). \
            select_related('personal_account__flat__owner', 'payment_state')

    def get_context_data(self, **kwargs):
        context = super(TransactionDetailView, self).get_context_data()
        if self.object.payment_state.type == 'in':
            context['type'] = 'Приходная ведомость'
        else:
            context['type'] = 'Расходная ведомость'
        return context


class InvoiceListView(ListView):
    model = models.Invoice

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(InvoiceListView, self).get_context_data()
        context = get_statistics(context)
        return context


class InvoiceListViewAjax(BaseDatatableView):
    model = models.Invoice
    columns = ['number', 'status', 'date', 'flat',
               'house', 'flat.owner', 'payment_state',
               'amount', 'id']
    order_columns = ['date']

    def get_initial_queryset(self):
        return self.model.objects.all().select_related('house', 'section',
                                                       'flat__owner').\
            order_by('-id')

    def filter_queryset(self, qs):
        number = self.request.GET.get('number')
        status = self.request.GET.get('status')
        date = self.request.GET.get('date')
        month = self.request.GET.get('month')
        month_list = [
            'January', 'February', 'March', 'April', 'May', 'June', 'July',
            'August', 'September', 'October', 'November', 'December'
        ]
        if month:
            filter_month = month.split(' ')[0]
            qs = qs.filter(date__month=int(month_list.index(filter_month) + 1))
        if date:
            qs = filter_qs_daterange(date, qs)
        flat = self.request.GET.get('flat')
        owner = self.request.GET.get('owner')
        payment_state = self.request.GET.get('payment_state')
        if number:
            qs = qs.filter(account_number__icontains=number)
        if status:
            qs = qs.filter(status=status)
        if flat:
            qs = qs.filter(flat__owner_id=owner)
        if payment_state:
            qs = qs.filter(payment_state=payment_state)
        x = self.model.objects.filter()
        return qs


class InvoiceCreateView(CreateView):
    model = models.Invoice
    service_formset = forms.InvoiceServiceFormset
    form_class = forms.InvoiceForm

    def get_context_data(self, **kwargs):
        context = super(InvoiceCreateView, self).get_context_data()
        date_service = {'form-TOTAL_FORMS': '0',
                        'form-INITIAL_FORMS': '0',
                        }
        context['service_formset'] = self.service_formset(data=date_service)
        context['services'] = forms.Service.objects.all()
        context['units'] = forms.Unit.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.form_class(request.POST or None)
        service_formset = self.service_formset(request.POST or None)
        if form_class.is_valid():
            form_class.save()
            if service_formset.is_valid():
                service_formset.save(commit=False)
                for service in service_formset.new_objects:
                    if service.total:
                        service.invoice = form_class.instance
                        service.save()
            form_class.calculate_invoice(form_class, type='create')
            return HttpResponseRedirect(reverse_lazy
                                        ('crm_accounting:invoice_list'))
        return render(request, 'crm_accounting/invoice_form.html',
                      context={'form':form_class,
                               'service_formset':service_formset})


class InvoiceDetailView(DetailView):
    model = models.Invoice

    def get_queryset(self):
        queryset = models.Invoice.objects.all().\
            select_related('flat__personal_account', 'flat__owner', ).\
            prefetch_related('invoiceservice_set__service__unit')
        return queryset


class InvoiceUpdateView(UpdateView):
    model = models.Invoice
    template_name = 'crm_accounting/invoice_update_form.html'
    service_formset = forms.InvoiceServiceFormset
    form_class = forms.InvoiceForm
    queryset = model.objects.all().select_related('flat__section__house')

    def get_context_data(self, **kwargs):
        # context = super().get_context_data()
        context = dict()
        if kwargs.get('form'):
            context['form'] = kwargs['form']
            self.object = kwargs['form'].instance

        else:
            context['form'] = self.form_class(instance=self.object)
        context['object'] = self.object
        context['sections'] = Section.objects.filter(house=self.object.house)
        context['flats'] = Flat.objects.filter\
            (section_id=self.object.section.id)
        context['service_formset'] = self.service_formset(
            queryset=models.InvoiceService.objects.filter(
                invoice=self.object))
        context['services'] = forms.Service.objects.all()
        context['units'] = forms.Unit.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        status = instance.status
        payment_state = instance.payment_state
        form_class = self.form_class(request.POST or None,
                                     instance=instance)
        service_formset = self.service_formset(
            request.POST or None,
            queryset=models.InvoiceService.objects.filter(invoice=instance))
        print(form_class.is_valid(), form_class.errors)
        print(service_formset.is_valid(), service_formset.errors)
        if all([form_class.is_valid(), service_formset.is_valid()]):
            form_class.save()
            service_formset.save(commit=False)
            for service in service_formset.new_objects:
                if service.total:
                    service.invoice = form_class.instance
                    service.save()
            for service in service_formset.deleted_objects:
                service.delete()
            for service in service_formset.changed_objects:
                if all([service[0].total, service[0].service]):
                    service[0].save()
            service_formset.save()
            form_class.calculate_invoice(form_class, type='update',
                                         status=status,
                                         payment_state=payment_state)
            messages.success(request, "Квитанция изменена")
            return HttpResponseRedirect(reverse_lazy
                                        ('crm_accounting:invoice_list'))
        return render(request, self.template_name,
                      self.get_context_data(form=form_class,
                                            service_formset=service_formset))


class InvoiceDeleteView(DeleteView):
    model = models.Invoice

    def post(self, request, *args, **kwargs):
        delete_list = request.POST.get('deleted_list').split(',')
        if request.user.is_superuser:
            self.model.objects.filter(id__in=delete_list).delete()
            return JsonResponse({'success': 'success'})
        else:
            return JsonResponse({'success': 'У Вас нет прав для удаления!'})


class SectionAjaxView(View):
    @staticmethod
    def get(request):
        house_id = request.GET.get('house_id')
        sections = list()
        if house_id:
            query_sections = Section.objects.filter(house_id=house_id)
            for section in query_sections:
                instance = {'section_id': section.id,
                            'section_title': section.title}
                sections.append(instance)
        return JsonResponse({'data': sections})


class FlatAjaxList(View):
    @staticmethod
    def get(request):
        section_id = request.GET.get('section_id')
        flats = list()
        if section_id:
            query_flats = Flat.objects.filter(section_id=section_id)
            for flat in query_flats:
                instance = {'flat_id': flat.id,
                            'flat_title': flat.number}
                flats.append(instance)
        print(flats)
        return JsonResponse({'flats': flats})


class FlatAjaxInfo(View):
    @staticmethod
    def get(request):
        flat_id = request.GET.get('flat_id')
        data = dict()
        flat = get_object_or_404(Flat, id=flat_id)
        data['owner'] = {'owner': f'{flat.owner.first_name} '
                                  f'{flat.owner.last_name}',
                         'phone': flat.owner.phone,
                         'id': flat.owner.id}
        if flat.personal_account:
            data['personal_account'] = flat.personal_account.account_number

        return JsonResponse({'data': data})


def tariff_ajax_info(request):
    tariff_id = request.GET.get('tariff')
    services = TariffService.objects.filter(tariff_id=tariff_id).\
        select_related('service__unit')
    services_list = list()
    for service in services:
        instance = {
            'service_id': service.service.id,
            'unit_id': service.service.unit.id,
            'price': service.price
        }
        services_list.append(instance)
    return JsonResponse({'services': services_list})
