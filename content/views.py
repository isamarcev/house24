from django.forms import modelformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy

from crm_home.models import Tariff
from . import forms
from .models import *
from django.views.generic import DetailView, UpdateView, DeleteView


def main_page(request):
    return render(request, 'content/layout/base.html')


class MainUpdateView(UpdateView):
    form_class = forms.MainForm
    template_name = 'content/admin_main_page/admin_main_page.html'
    blocks = Block.objects.prefetch_related('main')
    seo = Seo.objects.prefetch_related('main')
    formset = modelformset_factory(Block, forms.BlockForm, max_num=6, fields=('header', 'description', 'image',))
    success_url = reverse_lazy('content:main-change')

    def get_object(self, queryset=None):
        return Main.objects.first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['formset'] = self.formset(queryset=self.blocks)
        context['form3'] = forms.SeoForm(instance=self.object.seo)
        return context

    def post(self, request, *args, **kwargs):
        print(request.FILES)
        object = self.get_object()
        form = forms.MainForm(request.POST, request.FILES, instance=object)
        form_class3 = forms.SeoForm(request.POST, instance=object.seo)
        formset = self.formset(request.POST, request.FILES, queryset=self.blocks)
        print(formset.is_valid(), formset.errors)
        if form.is_valid():
            form.save()
            if formset.is_valid():
                print(formset.cleaned_data)
                # print(formset)
                formset.save()
            # else:
            #     return super().form_invalid(formset)
            if form_class3.is_valid():
                form_class3.save()
            # else:
            #     return super().form_invalid((form_class3))
            return super().post(request, *args, **kwargs)
        else:
            return super().form_invalid(form)
#         redirect + messeges framework прокидывать


class AboutUpdateView(UpdateView):
    form_class = forms.AboutForm
    success_url = reverse_lazy('content:about-change')
    template_name = 'content/edit_pages/about_us.html'
    formset = modelformset_factory(Document, forms.DocumentForm, extra=0, can_delete=True, fields=('document','title',))

    def get_object(self, queryset=None):
        return About.objects.first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form_gallery'] = forms.GalleryForm(prefix='gallery_form')
        context['add_form_gallery'] = forms.GalleryForm(prefix='add_gallery_form')
        context['gallery'] = Gallery.objects.filter(page_id=self.object.id)
        context['add_gallery'] = AdditionalGallery.objects.filter(page_id=self.object.id)
        context['form3'] = forms.SeoForm(instance=self.object.seo)
        context['formset'] = self.formset(queryset=Document.objects.filter(page_id=self.object.id))
        return context

    def post(self, request, *args, **kwargs):
        object = self.get_object()
        form_class = self.form_class(request.POST, request.FILES, instance=object)
        form3 = forms.SeoForm(request.POST, instance=object.seo)
        formset = self.formset(request.POST, request.FILES, queryset=Document.objects.filter(page_id=object.id))
        form_gallery = forms.GalleryForm(request.POST, request.FILES, prefix='gallery_form')
        add_gallery = forms.AdditionalGalleryForm(request.POST, request.FILES, prefix='add_gallery_form')
        if form_class.is_valid():
            form_class.save()
        if form3.is_valid():
            form3.save()
        if formset.is_valid():
            formset.save(commit=False)
            for foo in formset.new_objects:
                if foo.document:
                    foo.page = object
                    foo.save()
            for foo in formset.deleted_objects:
                foo.delete()
            formset.save()
        if form_gallery.is_valid():
            form_gallery.save()
        if add_gallery.is_valid():
            add_gallery.save()
        return super().post(request, *args, **kwargs)


class ServicesUpdateView(UpdateView):
    success_url = reverse_lazy('content:services-change')
    template_name = 'content/edit_pages/services.html'
    formset_service = modelformset_factory(AboutService, forms.ServiceForm,
                                      extra=0, can_delete=True, fields=('title', 'text', 'image'))
    form_class = forms.ServicePageForm

    def get_object(self, queryset=None):
        return ServicePage.objects.first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form_seo'] = forms.SeoForm(instance=self.object.seo)
        context['formset_service'] = self.formset_service(
            queryset=AboutService.objects.filter(service_page=self.object.id))
        return context

    def post(self, request, *args, **kwargs):
        object = self.get_object()
        print(request.POST, request.FILES)
        formset_service = self.formset_service(request.POST, request.FILES,
                                               queryset=AboutService.objects.filter(service_page=object.id))
        form_seo = forms.SeoForm(request.POST, request.FILES, instance=object.seo)
        print(formset_service.is_valid(), formset_service.errors)
        # form_class = self.form_class(request.POST, request.FILES, instance=object)
        if form_seo.is_valid():
            form_seo.save()
        if formset_service.is_valid():
            formset_service.save(commit=False)
            for foo in formset_service.new_objects:
                if foo.image:
                    foo.service_page = object
                    foo.save()
            for foo in formset_service.deleted_objects:
                foo.delete()
            formset_service.save()
        object.seo = form_seo.instance
        object.save()
        return HttpResponseRedirect(self.success_url)



class TariffUpdateView(UpdateView):
    # queryset = Tariff.objects.all()
    pass


class ContactsUpdateView(UpdateView):
    template_name = 'content/edit_pages/contacts.html'
    form_class = forms.ContactsForm
    success_url = reverse_lazy('content:contacts-change')
    queryset = Contacts.objects.first()

    def get_object(self, queryset=None):
        obj = Contacts.objects.first()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form_seo'] = forms.SeoForm(instance=self.object.seo, prefix='seo_form')
        return context

    def post(self, request, *args, **kwargs):
        object = self.get_object()
        print(request.POST, request.FILES)
        form_seo = forms.SeoForm(request.POST, request.FILES, instance=object.seo, prefix='seo_form')
        form_class = forms.ContactsForm(request.POST, request.FILES, instance=object)
        print(form_class.is_valid(), form_class.errors)
        print(form_seo.is_valid(), form_seo.errors)
        if all([form_seo.is_valid(), form_class.is_valid()]):
            form_seo.save()
            form_class.save(commit=False)
            print(form_class.instance.text)
            form_class.instance.seo = form_seo.instance
            form_class.save()
            return HttpResponseRedirect(self.success_url)
        else:
            return HttpResponse(form_class.errors, form_seo.errors)


def delete_gallery(request, pk):
    object = Gallery.objects.get(pk=pk)
    object.delete()
    return HttpResponseRedirect(reverse_lazy('content:about-change'))


def delete_additional_gallery(request, pk):
    object = AdditionalGallery.objects.get(pk=pk)
    object.delete()
    return HttpResponseRedirect(reverse_lazy('content:about-change'))


def delete_service(request, pk):
    pass
    # service = AboutService.objects.get(pk=pk)
    # service.delete()
    # return HttpResponseRedirect(reverse_lazy('content:services-change'))


def about(request):
    return HttpResponse('about')


def contacts(request):
    return HttpResponse('contacts')


def services(request):
    return HttpResponse('services')