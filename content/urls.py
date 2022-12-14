from django.urls import path, include
from . import views

app_name = 'content'
urlpatterns = [
    path('', views.MainPage.as_view(), name='main'),
    path('about/', views.AboutPage.as_view(), name='about'),
    path('services/', views.ServicesPage.as_view(), name='services'),
    path('contacts/', views.ContactsPage.as_view(), name='contacts'),

    # page_changes
    path('main/change/', views.MainUpdateView.as_view(), name='main-change'),
    path('about/change/', views.AboutUpdateView.as_view(), name='about-change'),
    path('services/change/', views.ServicesUpdateView.as_view(), name='services-change'),
    path('delete-service/<int:pk>/', views.delete_service, name='delete-service'),
    path('contacts/change/', views.ContactsUpdateView.as_view(), name='contacts-change'),

# <<<<<<< HEAD

# =======
# >>>>>>> c3cfeb46f5660de3a34d81e93cda02d9477346ae
    # delete_gallery
    path('delete-gallery/<int:pk>/', views.delete_gallery, name='delete-gallery'),
    path('delete-additional-gallery/<int:pk>/', views.delete_additional_gallery, name='delete-add-gallery'),

]