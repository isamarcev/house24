from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.forms import modelformset_factory
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django_datatables_view.base_datatable_view import BaseDatatableView

from houses.models import House, Flat
from users.forms import RoleForm
from users.models import Role
from . import forms
from .models import *
from django.views.generic import DetailView, UpdateView, DeleteView, FormView,\
    ListView, CreateView, TemplateView
from crm_accounting import views as account_views


class ServiceSettings(account_views.AdminPermissionMixin,
                      FormView, SuccessMessageMixin):
    formset_service = modelformset_factory(Service, forms.ServiceForm,
                                           extra=0, can_delete=True,
                                           fields=('name', 'show', 'unit'))
    template_name = 'crm_home/system_settings/services.html'
    queryset = Service.objects.all().prefetch_related('invoiceservice_set').\
        select_related('unit')
    formset_units = modelformset_factory(Unit, forms.UnitForm, extra=0,
                                         can_delete=True, fields=('title',))
    check_permission_name = 'service'

    def get_context_data(self, **kwargs):
        context = {'formset_service': self.formset_service(
            queryset=self.queryset, prefix='service'),
                   'formset_units': self.formset_units(
                       queryset=Unit.objects.all().
                       prefetch_related('service_set').all(), prefix='unit')}
        return context

    def post(self, request, *args, **kwargs):
        formset_service = self.formset_service(request.POST,
                                               queryset=Service.objects.all(),
                                               prefix='service')
        formset_units = self.formset_units(request.POST,
                                           queryset=Unit.objects.all(),
                                           prefix='unit')
        if all([formset_service.is_valid(), formset_units.is_valid()]):
            formset_service.save(commit=False)
            formset_units.save(commit=False)
            for form_service in formset_service.deleted_objects:
                form_service.delete()
            for form_service in formset_service.new_objects:
                if form_service.name:
                    form_service.save()
            formset_service.save()
            for form_unit in formset_units.deleted_objects:
                form_unit.delete()
            formset_units.save()
            messages.success(request, 'Выполнено успешно.')
            return HttpResponseRedirect(reverse_lazy('crm_home:set_services'))
        messages.error(request, 'Неправильно заполнены поля')
        return render(request, self.template_name,
                      context={'formset_service': formset_service,
                               'formset_units': formset_units})


class TariffListView(account_views.AdminPermissionMixin, ListView):
    queryset = Tariff.objects.all().order_by('-updated_at')
    template_name = 'crm_home/system_settings/tariff/tariff_list.html'
    check_permission_name = 'tariff'


class TariffDetailView(account_views.AdminPermissionMixin, DetailView):
    model = Tariff
    template_name = 'crm_home/system_settings/tariff/tariff_detail_view.html'
    check_permission_name = 'tariff'

    def get_context_data(self, **kwargs):
        context = {
            'tariff': self.object,
            'services': TariffService.objects.filter(tariff=self.object).
            select_related('service__unit'),
        }
        return context


class TariffCreateVIew(account_views.AdminPermissionMixin, CreateView):
    template_name = 'crm_home/system_settings/tariff/tariff_create.html'
    services_formset = modelformset_factory(TariffService,
                                            forms.TariffServiceForm,
                                            fields=('service', 'price',),
                                            can_delete=True, extra=0)
    check_permission_name = 'tariff'


    def get_context_data(self, **kwargs):
        context = dict()
        data = {'service-TOTAL_FORMS': '0',
                'service-INITIAL_FORMS': '0',
                }
        context['form_tariff'] = forms.TariffForm()
        context['services_formset'] = self.services_formset(prefix='service',
                                                            data=data)
        context['services'] = Service.objects.all().select_related('unit')
        tariff_id = self.request.GET.get('tarif_id')
        if tariff_id:
            tariff = get_object_or_404(Tariff.objects.
                                       prefetch_related('tariffservice_set'),
                                       id=tariff_id)
            x = TariffService.objects.filter(tariff=tariff)
            context['form_tariff'] = forms.TariffForm(initial={
                'name': tariff.name,
                'describe': tariff.describe
            })
            context['services_formset'] = self.services_formset(
                prefix='service',
                queryset=TariffService.objects.filter(tariff=tariff))
        return context

    def post(self, request, *args, **kwargs):
        services_formset = self.services_formset(request.POST, prefix='service')
        form_tariff = forms.TariffForm(request.POST)
        if all([form_tariff.is_valid(), services_formset.is_valid()]):
            form_tariff.save()
            services_formset.save(commit=False)
            for form in services_formset:
                if form.instance.service:
                    form.instance.tariff = form_tariff.instance
                    form.instance.save()
            return HttpResponseRedirect(reverse_lazy('crm_home:tariffs'))
        return render(request, self.template_name, context={'services_formset': services_formset,
                                                            'form_tariff': form_tariff,
                                                            'services': Service.objects.all().select_related('unit')})


class TariffUpdateView(account_views.AdminPermissionMixin, UpdateView):
    template_name = 'crm_home/system_settings/tariff/tariff_update.html'
    services_formset = modelformset_factory(TariffService, forms.TariffServiceForm, fields=('service', 'price',),
                                            can_delete=True, extra=0)
    model = Tariff
    check_permission_name = 'tariff'


    def get_context_data(self, **kwargs):
        context = {'form_tariff': forms.TariffForm(instance=self.object),
                   'services_formset': self.services_formset(queryset=TariffService.objects.filter(tariff=self.object).select_related('service__unit'),
                                                             prefix='service_update'),
                   'services': Service.objects.all().select_related('unit')}
        return context

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        services_formset = self.services_formset(request.POST, queryset=TariffService.objects.filter(tariff=obj),
                                                 prefix='service_update')
        form_tariff = forms.TariffForm(request.POST, instance=obj)
        if all([form_tariff.is_valid(), services_formset.is_valid()]):
            form_tariff.save()
            services_formset.save(commit=False)
            for form in services_formset.deleted_objects:
                form.delete()
            for form in services_formset.changed_objects:
                form[0].save()
            for form in services_formset.new_objects:
                if form.service:
                    form.tariff = form_tariff.instance
                    form.save()
            return HttpResponseRedirect(reverse_lazy('crm_home:tariffs'))
        return render(request, self.template_name, context={'services_formset': services_formset,
                                                            'form_tariff': form_tariff,
                                                            'services': Service.objects.all().select_related('unit')})


def get_unit_for_service(request):
    if request.GET:
        x = request.GET.get('id')
        unit = Service.objects.get(pk=x).unit.title
        return JsonResponse({'unit': unit}, status=200)


def delete_tariff(request):
    if request.GET:
        try:
            pk = request.GET.get('id')
            tariff = Tariff.objects.get(pk=pk)
            tariff_services = TariffService.objects.filter(tariff=tariff)
            for tariff_and_service in tariff_services:
                tariff_and_service.delete()
            tariff.delete()
            return JsonResponse({'success': 'success'}, status=200)
        finally:
            return JsonResponse({'error': 'error'}, status=500)


class RolesUpdateView(account_views.AdminPermissionMixin, FormView):
    queryset = Role.objects.all()
    template_name = 'crm_home/system_settings/roles/roles.html'
    roles_formset = modelformset_factory(Role, RoleForm, extra=0)
    check_permission_name = 'role'


    def get_context_data(self, **kwargs):
        context = {
            'roles_formset': self.roles_formset(queryset=self.queryset)
        }
        return context

    def post(self, request, *args, **kwargs):
        roles_formset = self.roles_formset(request.POST, queryset=self.queryset)
        if roles_formset.is_valid():
            roles_formset.save()
            return HttpResponseRedirect(reverse_lazy('crm_home:roles'))
        return render(request, self.template_name,
                      context={'roles_formset': roles_formset})


class RequisitesUpdateView(account_views.AdminPermissionMixin, UpdateView):
    model = Requisites
    form_class = forms.RequisitesForm
    check_permission_name = 'requisites'


    def get_object(self, queryset=None):
        return Requisites.objects.first()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['label_suffix'] = ''
        return kwargs

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        form_class = self.form_class(request.POST, instance=obj)
        if form_class.is_valid():
            messages.success(request, 'Выполнено успешно.')
            form_class.save()
            return HttpResponseRedirect(reverse_lazy('crm_home:requisites'))


class PaymentStateCreateView(account_views.AdminPermissionMixin, CreateView):
    success_url = reverse_lazy('crm_home:payment_states')
    model = PaymentState
    form_class = forms.PaymentStateForm
    check_permission_name = 'tariff'

    def post(self, request, *args, **kwargs):
        form_class = self.form_class(request.POST)
        response = super().post(self, request, *args, **kwargs)
        messages.success(request, 'Успешно выполнено')
        return response


class PaymentStateListView(account_views.AdminPermissionMixin, ListView):
    queryset = PaymentState.objects.all().order_by('id')
    check_permission_name = 'tariff'


class PaymentStateUpdateView(account_views.AccountCreateView, UpdateView):
    success_url = reverse_lazy('crm_home:payment_states')
    model = PaymentState
    form_class = forms.PaymentStateForm
    check_permission_name = 'tariff'

    def post(self, request, *args, **kwargs):
        response = super().post(self, request, *args, **kwargs)
        messages.success(request, 'Успешно выполнено')
        return response


def delete_payment_state(request):
    if request.GET:
        try:
            pk = request.GET.get('id')
            state = PaymentState.objects.get(pk=pk)
            state.delete()
            return JsonResponse({'success': 'success'}, status=200)
        finally:
            return JsonResponse({'error': 'error'}, status=500)


class CounterDataCreateView(account_views.AdminPermissionMixin, CreateView):
    model = CounterData
    template_name = 'crm_home/counterdata_form.html'
    form_class = forms.CounterDataForm
    success_url = reverse_lazy('crm_home:counter_data_list')
    check_permission_name = 'meter'

    def get_success_url(self, form_class):
        if 'save_and_add' in self.request.POST.keys():
            address = f'{self.success_url}create/?counter_id={form_class.instance.id}'
            return address
        else:
            return self.success_url

    def get(self, request, *args, **kwargs):
        counter_id = request.GET.get('counter_id')
        if counter_id:
            counter_data = CounterData.objects.get(id=counter_id)
            self.initial = {
                'number': get_next_counter_number,
                'house': counter_data.house,
                'section': counter_data.section,
                'flat': counter_data.flat,
                'service': counter_data.service,

            }
        return super().get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form_class = self.form_class(request.POST or None)
        if form_class.is_valid():
            form_class.save()
            return HttpResponseRedirect(self.get_success_url(form_class))
        else:
            return render(request, self.template_name, context={
                'form': form_class
            })


class CounterDataListView(account_views.AdminPermissionMixin, ListView):
    model = CounterData
    check_permission_name = 'meter'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = {
            'houses': House.objects.all(),
            'services': Service.objects.all()
        }
        return context


class CounterDataListViewAjax(BaseDatatableView):
    model = CounterData
    columns = ['house', 'section', 'flat.number', 'service', 'data',
               'service.unit', 'id', 'service.id', 'flat.id']
    order_columns = ['house', 'section', 'flat', 'service']

    def get_initial_queryset(self):
        flat_id = self.request.GET.get('flat_id')
        if flat_id:
            queryset = self.model.objects.filter(flat_id=flat_id)
        else:
            queryset = self.model.objects.all()
        return queryset.select_related('flat', 'service__unit')

    def filter_queryset(self, qs):
        house = self.request.GET.get('house')
        section = self.request.GET.get('section')
        service = self.request.GET.get('service')
        flat = self.request.GET.get('flat')
        if house:
            qs = qs.filter(house=house)
        if section:
            qs = qs.filter(section=section)
        if service:
            qs = qs.filter(service=service)
        if flat:
            qs = qs.filter(flat__number__icontains=flat)
        return qs


class FlatCounterDataListView(account_views.AdminPermissionMixin, TemplateView):
    model = CounterData
    template_name = 'crm_home/counterdata_flat_list.html'
    check_permission_name = 'meter'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = dict()
        context['houses'] = House.objects.all()
        context['services'] = Service.objects.all()
        flat_id = self.request.GET.get('flat_id')
        service_id = self.request.GET.get('service_id')
        context['flat'] = Flat.objects.get(pk=flat_id)
        if service_id:
            context['service'] = Service.objects.get(pk=service_id)
        context['counters'] = CounterData.objects.filter(flat_id=flat_id,
                                                         service_id=service_id)
        return context


class FlatCounterDataGetViewAjax(BaseDatatableView):
    model = CounterData
    columns = ['house', 'section', 'flat.number', 'service', 'data',
               'service.unit', 'id', 'service.id', 'flat.id', 'number',
               'status', 'date']
    order_columns = ['house', 'section', 'flat', 'service']

    def get_initial_queryset(self):
        flat_id = self.request.GET.get('id_flat')
        if flat_id:
            qs = self.model.objects.filter(flat_id=flat_id).select_related(
                'flat', 'service__unit')
        else:
            qs = self.model.objects.all().select_related('flat',
                                                         'service__unit')
        return qs

    def filter_queryset(self, qs):
        number = self.request.GET.get('number')
        house = self.request.GET.get('house')
        status = self.request.GET.get('status')
        date_range = self.request.GET.get('date_range')
        section = self.request.GET.get('section')
        flat_number = self.request.GET.get('flat_number')
        service = self.request.GET.get('service')
        if date_range:
            date_start = datetime.datetime.strptime(date_range.split(' - ')[0],
                                                    '%m/%d/%Y')
            date_end = datetime.datetime.strptime(date_range.split(' - ')[1],
                                                    '%m/%d/%Y')
            qs = qs.filter(Q(date__gt=date_start), Q(date__lt=date_end))
        if house:
            qs = qs.filter(house=house)
        if number:
            qs = qs.filter(number=number)
        if status:
            qs = qs.filter(status=status)
        if section:
            qs = qs.filter(section=section)
        if service:
            qs = qs.filter(service=service)
        if flat_number:
            qs = qs.filter(flat__number__icontains=flat_number)
        return qs


class CounterDeleteAjax(DeleteView):
    model = CounterData

    def post(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_staff:
            counter_id = request.POST.get('id')
            counter = get_object_or_404(CounterData, id=counter_id)
            counter.delete()
            return JsonResponse({'success': 'success'})
        else:
            return JsonResponse(
                {'success': "У Вас недостаточно прав для удаления."}
            )


class CounterDetailView(account_views.AdminPermissionMixin, DetailView):
    model = CounterData
    check_permission_name = 'meter'

    def get_queryset(self):
        return self.model.objects.all().\
            select_related('flat__owner', 'service__unit')


class CounterDataUpdateView(account_views.AdminPermissionMixin, UpdateView):
    model = CounterData
    template_name = 'crm_home/counterdata_update_form.html'
    form_class = forms.CounterDataForm
    success_url = reverse_lazy('crm_home:counter_data_list')
    check_permission_name = 'meter'

    def get_success_url(self, form_class):
        if 'save_and_add' in self.request.POST.keys():
            address = f'{self.success_url}create/?counter_id={form_class.instance.id}'
            return address
        else:
            return self.success_url

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        form_class = self.form_class(request.POST or None, instance=instance)
        if form_class.is_valid():
            form_class.save()
            return HttpResponseRedirect(self.get_success_url(form_class))
        else:
            return render(request, self.template_name, context={
                'form': form_class
            })


