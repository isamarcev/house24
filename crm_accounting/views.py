from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DetailView

from houses.models import Section, Flat
from .models import *
from .forms import *

# Create your views here.


def main_page(request, pk):
    pass


class AccountCreateView(CreateView):
    model = PersonalAccount
    form_class = PersonalAccountForm

    # def post(self, request, *args, **kwargs):


def get_flats(request):
    if request.GET:
        flat_list = list()
        if request.GET.get('section'):
            section = request.GET.get('section')
            flats = Flat.objects.filter(section=section).select_related('owner')
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
                owner_info['name'] = f'{owner.first_name} {owner.last_name} {owner.father_name}'
                owner_info['phone'] = owner.phone
                owner_info['id'] = owner.id
            except:
                pass
        return JsonResponse({'owner': owner_info}, status=200)