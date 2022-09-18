from django.forms import modelformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from . import forms
from .models import *
from django.views.generic import DetailView, UpdateView, DeleteView, FormView


class ServiceSettings(FormView):
    formset_service = modelformset_factory(Service, forms.ServiceForm,
                                      extra=0, can_delete=True, fields=('name', 'show', 'unit'))
    template_name = 'crm_home/system_settings/services.html'
    queryset = Service.objects.all().select_related('unit')
    formset_units = modelformset_factory(Unit, forms.UnitForm, extra=0, can_delete=True, fields=('title',))

    # def get_object(self, queryset=None):
    #     return Service.objects.all()

    # def get_queryset(self):
    #     return Service.objects.all()

    def get_context_data(self, **kwargs):
        # context = super().get_context_data()
        context = {'formset_service': self.formset_service(queryset=self.queryset, prefix='service'),
                   'formset_units': self.formset_units(queryset=Unit.objects.all(), prefix='unit')}
        print(context)
        for i in context['formset_service']:
            print(i.instance.unit.id, i.instance.unit.title)
        return context
