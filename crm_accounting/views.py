from django.db.models import Q
from django.forms import modelformset_factory
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, \
    ListView, DeleteView
from django_datatables_view.base_datatable_view import BaseDatatableView
from datetime import datetime
from crm_home.models import PaymentState
from houses.models import Section, Flat, House
from users.models import CustomUser
from . import models
from . import forms
from .models import get_next_transaction


# Create your views here.


def main_page(request, pk):
    pass


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
        if instance_id:
            transaction = models.Transaction.objects.select_related('manager', 'owner').\
                get(pk=instance_id)
            initial = {
                # 'number': get_next_transaction,
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
        else: context['form'] = self.form_class()
        if type_of_transaction == 'in':
            context['type'] = 'приходная ведомость'
        elif type_of_transaction == 'out':
            context['type'] = 'расходная ведомость'
        context['payment_states'] = PaymentState.objects.filter(
            type=type_of_transaction)
        print(context)
        return context


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
        return context


class TransactionListViewAjax(BaseDatatableView):
    model = models.Transaction
    columns = ['number', 'date', 'completed', 'payment_state',
               'owner', 'personal_account', 'payment_state.type',
               'amount', 'id']
    order_columns = ['date']

    def get_initial_queryset(self):
        return self.model.objects.all().select_related('payment_state').\
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
            date_start = datetime.strptime(date.split(' - ')[0],
                                           '%m-%d-%Y')
            date_end = datetime.strptime(date.split(' - ')[1],
                                         '%m-%d-%Y')
            qs = qs.filter(Q(date__gt=date_start), Q(date__lt=date_end))
        return qs


class DeleteTransaction(DeleteView):
    model = models.Transaction

    def get(self, request, *args, **kwargs):
        transaction = self.model.objects.get(
            pk=request.GET.get('transaction')
        )
        transaction.delete()
        return HttpResponseRedirect(reverse_lazy('crm_accounting:transaction_list'))

    def post(self, request, *args, **kwargs):
        transaction = self.model.objects.get(
            pk=request.POST.get('account'))
        if request.user.is_superuser:
            transaction.delete()
            return JsonResponse({'success': 'success'})
        else:
            return JsonResponse({'success': 'Удаление счета доступно только старшему персоналу!'})


class TransactionUpdateView(UpdateView):
    model = models.Transaction
    form_class = forms.TransactionForm
    success_url = reverse_lazy('crm_accounting:transaction_list')
    template_name = 'crm_accounting/transaction_update_form.html'

    def get_context_data(self, **kwargs):
        instance = self.get_object()
        context = dict()
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


class TransactionDetailView(DetailView):
    model = models.Transaction

    def get_queryset(self):
        return self.model.objects.all().\
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


class InvoiceCreateView(CreateView):
    model = models.Invoice
    # service_formset = modelformset_factory(models.InvoiceService)


class InvoiceDetailView(CreateView):
    model = models.Invoice


class InvoiceUpdateView(CreateView):
    model = models.Invoice


class InvoiceDeleteView(CreateView):
    model = models.Invoice
