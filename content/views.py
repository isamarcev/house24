from django.forms import modelformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from . import forms
from .models import Main, Block, Seo, About, Gallery, AdditionalGallery, Document
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
    # first

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



# class GalleryDeleteView(DeleteView):
#     model = Gallery
#     success_url = reverse_lazy

def delete_gallery(request, pk):
    object = Gallery.objects.get(pk=pk)
    object.delete()
    return HttpResponseRedirect(reverse_lazy('content:about-change'))


def delete_additional_gallery(request, pk):
    object = AdditionalGallery.objects.get(pk=pk)
    object.delete()
    return HttpResponseRedirect(reverse_lazy('content:about-change'))





def about(request):
    return HttpResponse('about')


def contacts(request):
    return HttpResponse('contacts')


def services(request):
    return HttpResponse('services')