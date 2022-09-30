from django.forms import modelformset_factory, inlineformset_factory, formset_factory
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView, DetailView
from django.contrib import messages
from psycopg2 import IntegrityError

from crm_accounting.models import get_next_account

from users.models import Role
from .forms import SectionForm, FloorForm, HouseForm, UserForm, FlatForm, PersonalAccountForm
from .models import *


# Create your views here.

def main_page(request):
    return render(request, 'houses/layout/base_houses.html')


class HousesListView(ListView):
    model = House


class HouseCreateView(CreateView):
    section_formset = modelformset_factory(Section, SectionForm, fields=('title', ), can_delete=True, extra=0)
    floor_formset = modelformset_factory(Floor, FloorForm, fields=('title', ), can_delete=True, extra=0)
    user_formset = modelformset_factory(CustomUser, UserForm, fields=('name', ), extra=0, can_delete=True)
    model = House
    form_class = HouseForm
    template_name = 'houses/house_form.html'

    def get_context_data(self, **kwargs):
        data_section = {'section-TOTAL_FORMS': '0',
                        'section-INITIAL_FORMS': '0',
                        }
        data_floor = {'floor-TOTAL_FORMS': '0',
                        'floor-INITIAL_FORMS': '0',
                        }
        data_users = {'users-TOTAL_FORMS': '0',
                      'users-INITIAL_FORMS': '0',
                      }

        section_formset = self.section_formset(data_section, prefix='section')
        floor_formset = self.floor_formset(data_floor, prefix='floor')
        users_formset = self.user_formset(data_users, prefix='users')
        context = super().get_context_data()
        context['section_formset'] = section_formset
        context['floor_formset'] = floor_formset
        context['users_formset'] = users_formset
        context['users'] = CustomUser.objects.filter(role=True).select_related('role')
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.form_class(request.POST, request.FILES)
        section_formset = self.section_formset(request.POST, prefix='section')
        floor_formset = self.floor_formset(request.POST, prefix='floor')
        users_formset = self.user_formset(request.POST, prefix='users')
        if form_class.is_valid():
            form_class.save()
            if users_formset.is_valid():
                users_formset.save(commit=False)
                for user in users_formset:
                    use = user.cleaned_data.get('name')
                    form_class.instance.users.add(use)
            form_class.save()
            if section_formset.is_valid():
                section_formset.save(commit=False)
                for form in section_formset.new_objects:
                    if form.title:
                        form.house = form_class.instance
                        form.save()
            if floor_formset.is_valid():
                floor_formset.save(commit=False)
                for form in section_formset.new_objects:
                    if form.title:
                        form.house = form_class.instance
                        form.save()
            floor_formset.save()
            section_formset.save()
            messages.success(request, "Дом добавлен")
            return HttpResponseRedirect(reverse_lazy('houses:house_list'))
        else:
            return render(request, self.template_name, context={
                'form': form_class,
                'section_formset': section_formset,
                'floor_formset': floor_formset,
                'users_formset': users_formset,
                'users': CustomUser.objects.filter(role=True).select_related('role')
            })


class HousesDetail(DetailView):
    model = House

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context['users'] = CustomUser.objects.filter(house=self.object).select_related('role')
        return self.render_to_response(context)


class HouseUpdateView(UpdateView):
    section_formset = modelformset_factory(Section, SectionForm, fields=('title',), can_delete=True, extra=0)
    floor_formset = modelformset_factory(Floor, FloorForm, fields=('title',), can_delete=True, extra=0)
    user_formset = modelformset_factory(CustomUser, UserForm, fields=('name',), extra=0, can_delete=True)
    model = House
    form_class = HouseForm
    template_name = 'houses/house_update_form.html'

    def get_context_data(self, **kwargs):
        section_formset = self.section_formset(prefix='section',
                                               queryset=Section.objects.filter(house=self.object))
        floor_formset = self.floor_formset(prefix='floor', queryset=Floor.objects.filter(house=self.object))
        users_formset = self.user_formset(prefix='users',
                                          queryset=CustomUser.objects.filter(house=self.object).select_related('role'))
        context = super().get_context_data()
        context['section_formset'] = section_formset
        context['floor_formset'] = floor_formset
        context['users_formset'] = users_formset
        context['users'] = CustomUser.objects.filter(role=True).select_related('role')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.form_class(request.POST, request.FILES, instance=self.object)
        section_formset = self.section_formset(request.POST, prefix='section',
                                               queryset=Section.objects.filter(house=self.object))
        floor_formset = self.floor_formset(request.POST, prefix='floor',
                                           queryset=Floor.objects.filter(house=self.object))
        users_formset = self.user_formset(request.POST, prefix='users',
                                          queryset=CustomUser.objects.filter(house=self.object))
        if form_class.is_valid():
            form_class.save(commit=False)
            if users_formset.is_valid():
                users_formset.save(commit=False)
                for obj in users_formset.cleaned_data:
                    if len(obj) == 0:
                        del obj
                    elif obj['DELETE']:
                        form_class.instance.users.remove(obj['id'])
                    elif obj['name'] != obj['id']:
                        form_class.instance.users.remove(obj['id'])
                        form_class.instance.users.add(obj['name'])
            form_class.save()
            if section_formset.is_valid():
                section_formset.save(commit=False)
                for form in section_formset.new_objects:
                    if form.title:
                        form.house = form_class.instance
                        form.save()
                for form in section_formset.changed_objects:
                    if form[0].title:
                        form[0].save()
                    else:
                        form[0].delete()
                for form in section_formset.deleted_objects:
                    form.delete()
            if floor_formset.is_valid():
                floor_formset.save(commit=False)
                for form in floor_formset.new_objects:
                    if form.title:
                        form.house = form_class.instance
                        form.save()
                for form in floor_formset.changed_objects:
                    if form[0].title:
                        form[0].save()
                    else:
                        form[0].delete()
                for form in floor_formset.deleted_objects:
                    form.delete()
            floor_formset.save()
            section_formset.save()
            messages.success(request, "Дом добавлен")
            return HttpResponseRedirect(reverse_lazy('houses:house_list'))
        else:
            return render(request, self.template_name, context={
                'form': form_class,
                'section_formset': section_formset,
                'floor_formset': floor_formset,
                'users_formset': users_formset,
                'users': CustomUser.objects.filter(role=True).select_related('role')
            })


def delete_house(request):
    pk = request.GET.get('id')
    house = House.objects.get(pk=pk)
    house.delete()
    return JsonResponse({'success': 200}, status=200)


def get_role(request):
    pk = request.GET.get('id')
    role = CustomUser.objects.get(pk=pk).role.name
    return JsonResponse({'role': role}, status=200)


class FlatsListView(ListView):
    model = Flat
    template_name = 'houses/flat/flat_list.html'

    def get_queryset(self):
        queryset = self.model.objects.all().select_related('personal_account__section', 'floor', 'owner').order_by('-id')
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['houses'] = House.objects.all()
        return context


class FlatCreate(CreateView):
    model = Flat
    form_class = FlatForm
    template_name = 'houses/flat/flat_form.html'
    success_url = reverse_lazy('houses:flat_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['label_suffix'] = ''
        return kwargs

    def get(self, request, *args, **kwargs):
        print(request, args, kwargs)
        return super().get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['account'] = PersonalAccountForm
        return context

    def post(self, request, *args, **kwargs):
        print(request.POST)
        form_class = self.form_class(request.POST)
        account_form = PersonalAccountForm(request.POST)
        if form_class.is_valid():
            form_class.save(commit=False)
            if account_form.is_valid():
                account = PersonalAccount.objects.filter(account_number__exact=request.POST['account_number'])
                if account.exists():
                    if not account.first().flat:
                        account.first().flat = form_class.instance
                        form_class.instance.personal_account = account.first()
                        messages.success(request, 'Квартира успешно создана')
                    else:
                        form_class.save()
                    return HttpResponseRedirect(reverse_lazy('houses:flat_list'))
                else:
                    account_form.save(commit=False)
                    form_class.save()
                    if account_form.instance.account_number:
                        account_form.instance.flat = form_class.instance
                        account_form.instance.house = form_class.instance.house
                        account_form.instance.section = form_class.instance.section
                        account_form.instance.owner = form_class.instance.owner
                        account_form.save()
                        form_class.instance.personal_account = account_form.instance
            form_class.save()
            messages.success(request, 'Квартира успешно создана')
            return HttpResponseRedirect(reverse_lazy('houses:flat_list'))
        else:
            content = {'form': form_class, 'account': account_form}
            return render(request, self.template_name, content)

def get_account_list(request):
    account_list = get_next_account(3)
    return JsonResponse({'data': account_list})

def get_sections_and_floors(request):
    house = request.GET.get('house')
    sections_list = Section.objects.filter(house_id=house)
    sections = []
    for i in sections_list:
        section = {
            'id': i.id,
            'title': i.title
        }
        sections.append(section)
    floors_list = Floor.objects.filter(house_id=house)
    floors = []
    for i in floors_list:
        floor = {
            'id': i.id,
            'title': i.title
        }
        floors.append(floor)
    return JsonResponse({'sectionist': sections, 'floors': floors})



