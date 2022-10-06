from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, \
    ListView, DeleteView
from django_datatables_view.base_datatable_view import BaseDatatableView

from houses.models import Section, Flat
from .models import PersonalAccount
from .forms import *

# Create your views here.


def main_page(request, pk):
    pass


class AccountCreateView(CreateView):
    model = PersonalAccount
    form_class = PersonalAccountForm
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
    model = PersonalAccount
    template_name = 'crm_accounting/personalaccount_update_form.html'
    form_class = PersonalAccountForm
    success_url = reverse_lazy('crm_accounting:account_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        account = self.get_object()
        context['sections'] = Section.objects.filter(house=account.house)
        context['flats'] = Flat.objects.filter(section=account.section).\
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
    model = PersonalAccount
    queryset = None

    def get_context_data(self, *, object_list=None, **kwargs):
        context = dict()
        context['houses'] = House.objects.all()
        context['owner'] = CustomUser.objects.all()
        return context


class AccountListViewAjax(BaseDatatableView):
    model = PersonalAccount
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
    model = PersonalAccount

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
    model = PersonalAccount
    template_name = 'crm_accounting/personalaccount_detail.html'


def get_flats(request):
    if request.GET:
        flat_list = list()
        if request.GET.get('section'):
            section = request.GET.get('section')
            flats = Flat.objects.filter(section=section).\
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
