from django.urls import path, include
from . import views

app_name = 'houses'
urlpatterns = [
    path('main/', views.main_page, name='main'),


    path('houses/', views.HousesListView.as_view(), name='house_list'),

    path('houses/create/', views.HouseCreateView.as_view(), name='house_create'),
    path('houses/detail/<int:pk>/', views.HousesDetail.as_view(), name='house_detail'),
    path('houses/update/<int:pk>/', views.HouseUpdateView.as_view(), name='house_update'),
    path('houses/delete/', views.delete_house, name='delete_house'),
    path('houses/create/get-role/', views.get_role, name='get_role'),

    # path('create/', views.HousesListView.as_view(), name='house_create'),

    # path('about-us/', views.about, name='about'),
    # path('services/', views.services, name='services'),
    # path('contacts/', views.contacts, name='contacts'),

]