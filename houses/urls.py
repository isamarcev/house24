from django.urls import path, include
from django.views.defaults import permission_denied, page_not_found

from . import views




app_name = 'houses'


urlpatterns = [
    path('main/', views.main_page, name='main'),

    #statistics
    path('', views.StatisticView.as_view(), name='statistics'),

    # houses
    path('houses/', views.HousesListView.as_view(), name='house_list'),
    path('houses/create/', views.HouseCreateView.as_view(), name='house_create'),
    path('houses/detail/<int:pk>/', views.HousesDetail.as_view(), name='house_detail'),
    path('houses/update/<int:pk>/', views.HouseUpdateView.as_view(), name='house_update'),
    path('houses/delete/', views.delete_house, name='delete_house'),
    path('houses/create/get-role/', views.get_role, name='get_role'),


    # flats
    path('flats/', views.FlatsListView.as_view(), name='flat_list'),
    path('flats/create/', views.FlatCreate.as_view(), name='flat_create'),
    path('flats/detail/<int:pk>/', views.FlatDetailView.as_view(), name='flat_detail'),
    path('flats/update/<int:pk>/', views.FlatUpdateView.as_view(), name='flat_update'),
    path('get-account-list/', views.get_account_list, name='get_account_list'),
    path('get-sections-and-floors/', views.get_sections_and_floors, name='get_section_and_floor'),
    path('flats/detail/<int:pk>/', views.HousesDetail.as_view(), name='flat_detail'),
    path('flats/delete/', views.delete_flat, name="delete_flat"),
    path('ajax-data-table/', views.FlatsListViewAjax.as_view(), name='get_ajax'),


    # path('create/', views.HousesListView.as_view(), name='house_create'),

    # path('about-us/', views.about, name='about'),
    # path('services/', views.services, name='services'),
    # path('contacts/', views.contacts, name='contacts'),

]