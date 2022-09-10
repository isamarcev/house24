from django.urls import path, include
from . import views

app_name = 'houses'
urlpatterns = [
    path('', views.main_page, name='main'),


    # path('about-us/', views.about, name='about'),
    # path('services/', views.services, name='services'),
    # path('contacts/', views.contacts, name='contacts'),

]