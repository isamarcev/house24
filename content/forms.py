from django import forms
from . import models


class MainForm(forms.ModelForm):

    class Meta:
        model = models.Main
        fields = ['header', 'text', 'apps_links', 'slide1', 'slide2', 'slide3']
        widgets = {
            'header': forms.TextInput(attrs={'class': 'form-control', 'style': 'border-radius: 0; color:#555;' }),
            'text': forms.Textarea(attrs={'class':'form-control',}),
            'apps_links': forms.CheckboxInput()
        }



class BlockForm(forms.ModelForm):
    class Meta:
        model = models.Block
        fields = ['header', 'description', 'image']
        widgets = {
            'header': forms.TextInput(attrs={'class': 'form-control form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-control',})
        }


class SeoForm(forms.ModelForm):
    class Meta:
        model = models.Seo
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'desctiption': forms.Textarea(attrs={'class': 'form-control', 'rows': '6'}),
            'key_words': forms.Textarea(attrs={'class': 'form-control', 'rows': '6'}),

        }

class AboutForm(forms.ModelForm):
    class Meta:
        model = models.About
        fields = ['header', 'text', 'image', 'additional_text', 'additional_header', ]
        widgets = {
            'header': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class':'form-control','rows': '4'}),
            'additional_header': forms.TextInput(attrs={'class': 'form-control'}),
            'additional_text': forms.Textarea(attrs={'class': 'form-control', 'rows': '4'})
        }


class GalleryForm(forms.ModelForm):
    class Meta:
        model = models.Gallery
        fields = ['image',]
        widgets = {
            'image': forms.FileInput(attrs={'id':'gallery_image',
                                            'name':'gallery_image'})
        }


class AdditionalGalleryForm(forms.ModelForm):
    class Meta:
        model = models.AdditionalGallery
        fields = ['image',]
        widgets = {
            'image': forms.FileInput(attrs={'id':'add_gallery_image',
                                            'name':'add_gallery_image'})
        }


class DocumentForm(forms.ModelForm):
    class Meta:
        model = models.Document
        fields = ['document', 'title']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'})
        }


class ServiceForm(forms.ModelForm):
    class Meta:
        model = models.AboutService
        fields = ['title', 'text', 'image',]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': '4'}),
        }


class ServicePageForm(forms.ModelForm):
    class Meta:
        model = models.ServicePage
        fields = '__all__'


class ContactsForm(forms.ModelForm):
    class Meta:
        model = models.Contacts
        fields = ['title', 'text', 'link_comm_site', 'map', 'FIO', 'location', 'address', 'phone', 'email']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'required': 'required'}),
            'link_comm_site': forms.TextInput(attrs={'class': 'form-control'}),
            'map': forms.Textarea(attrs={'class': 'form-control', 'rows': '4'}),
            'FIO': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': "Заголовок",
            'text': "Краткий текст",
            'link_comm_site': "Ссылка на коммерческий сайт",
            'map': 'Код карты',
            'FIO': "ФИО",
            'location': "Локация",
            'address': "Адрес",
            'phone': "Телефон",
            "email": "E-mail",
        }
