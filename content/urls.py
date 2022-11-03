from django.urls import path, include
from . import views

app_name = 'content'
urlpatterns = [
    path('', views.main_page, name='main'),
    path('about-us/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contacts/', views.contacts, name='contacts'),

    # page_changes
    path('main/change/', views.MainUpdateView.as_view(), name='main-change'),
    path('about/change/', views.AboutUpdateView.as_view(), name='about-change'),
    path('services/change/', views.ServicesUpdateView.as_view(), name='services-change'),
    path('delete-service/<int:pk>/', views.delete_service, name='delete-service'),
    path('contacts/change/', views.ContactsUpdateView.as_view(), name='contacts-change'),

    # delete_gallery
    path('delete-gallery/<int:pk>/', views.delete_gallery, name='delete-gallery'),
    path('delete-additional-gallery/<int:pk>/', views.delete_additional_gallery, name='delete-add-gallery'),

]