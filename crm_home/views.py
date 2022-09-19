from django.forms import modelformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from . import forms
from .models import *
from django.views.generic import DetailView, UpdateView, DeleteView, FormView, ListView, CreateView


class ServiceSettings(FormView):
    formset_service = modelformset_factory(Service, forms.ServiceForm,
                                           extra=0, can_delete=True, fields=('name', 'show', 'unit'))
    template_name = 'crm_home/system_settings/services.html'
    queryset = Service.objects.all()
    formset_units = modelformset_factory(Unit, forms.UnitForm, extra=0, can_delete=True, fields=('title',))

    def get_context_data(self, **kwargs):
        context = {'formset_service': self.formset_service(queryset=self.queryset, prefix='service'),
                   'formset_units': self.formset_units(queryset=Unit.objects.all(), prefix='unit')}
        return context

    def post(self, request, *args, **kwargs):
        formset_service = self.formset_service(request.POST, queryset=Service.objects.all(), prefix='service')
        formset_units = self.formset_units(request.POST, queryset=Unit.objects.all(), prefix='unit')
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
            return HttpResponseRedirect(reverse_lazy('crm_home:set_services'))
        return render(request, self.template_name, context={'formset_service': formset_service,
                                                            'formset_units': formset_units})


class TariffListView(ListView):
    queryset = Tariff.objects.all().order_by('-updated_at')
    template_name = 'crm_home/system_settings/tariff/tariff_list.html'


class TariffDetailView(DetailView):
    model = Tariff
    template_name = 'crm_home/system_settings/tariff/tariff_detail_view.html'

    def get_context_data(self, **kwargs):
        context = {
            'tariff': self.object,
            'services': TariffService.objects.filter(tariff=self.object).select_related('service__unit'),
        }
        return context


class TariffCreateVIew(CreateView):
    template_name = 'crm_home/system_settings/tariff/tariff_create.html'
    services_formset = modelformset_factory(TariffService, forms.TariffServiceForm, fields=('service', 'price',),
                                            can_delete=True, extra=0)
    def get_context_data(self, **kwargs):
        context = {'form_tariff': forms.TariffForm(),
                   'services_formset': self.services_formset(prefix='service'),
                   'services': Service.objects.all().select_related('unit')}
        return context

    def post(self, request, *args, **kwargs):
        services_formset = self.services_formset(request.POST, prefix='service')
        form_tariff = forms.TariffForm(request.POST)
        print(form_tariff.is_valid(), form_tariff.errors)
        print(services_formset.is_valid(), services_formset.errors)
        print(request.POST)
        if all([form_tariff.is_valid(), services_formset.is_valid()]):
            form_tariff.save()
            services_formset.save(commit=False)

            for form in services_formset:
                if form.instance.service:
                    form.instance.tariff = form_tariff.instance
                    form.instance.save()
            # services_formset.save()
            return HttpResponseRedirect(reverse_lazy('crm_home:tariffs'))
        return render(request, self.template_name, context={'services_formset': services_formset,
                                                            'form_tariff': form_tariff,
                                                            'services': Service.objects.all().select_related('unit')})


class TariffUpdateView(UpdateView):
    template_name = 'crm_home/system_settings/tariff/tariff_update.html'
    services_formset = modelformset_factory(TariffService, forms.TariffServiceForm, fields=('service', 'price',),
                                            can_delete=True, extra=0)
    model = Tariff

    def get_context_data(self, **kwargs):
        context = {'form_tariff': forms.TariffForm(instance=self.object),
                   'services_formset': self.services_formset(queryset=TariffService.objects.filter(tariff=self.object),
                                                             prefix='service_update'),
                   'services': Service.objects.all().select_related('unit')}
        return context

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        services_formset = self.services_formset(request.POST, queryset=TariffService.objects.filter(tariff=obj),
                                                 prefix='service_update')
        form_tariff = forms.TariffForm(request.POST, instance=obj)
        print(form_tariff.is_valid(), form_tariff.errors)
        print(services_formset.is_valid(), services_formset.errors, services_formset)
        print(request.POST)

        if all([form_tariff.is_valid(), services_formset.is_valid()]):
            form_tariff.save()
            services_formset.save(commit=False)
            for form in services_formset.deleted_objects:
                form.delete()
            for form in services_formset.new_objects:
                if form.service:
                    form.tariff = form_tariff.instance
                    form.save()
            # services_formset.save()
            return HttpResponseRedirect(reverse_lazy('crm_home:tariffs'))
        return render(request, self.template_name, context={'services_formset': services_formset,
                                                            'form_tariff': form_tariff,
                                                            'services': Service.objects.all().select_related('unit')})

