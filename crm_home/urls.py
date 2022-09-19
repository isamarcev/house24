from django.urls import path, include
from . import views

app_name = 'crm_home'
urlpatterns = [
    path('set-services/', views.ServiceSettings.as_view(), name='set_services'),
    path('tariff/', views.TariffListView.as_view(), name='tariffs'),
    path('tariff/create/', views.TariffCreateVIew.as_view(), name='tariff_create'),
    path('tariff/update/<int:pk>/', views.TariffUpdateView.as_view(), name='tariff_update'),

    path('tariff/<int:pk>/', views.TariffDetailView.as_view(), name='tariff_detail'),

]