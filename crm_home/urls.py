from django.urls import path, include
from . import views

app_name = 'crm_home'
urlpatterns = [
    path('set-services/', views.ServiceSettings.as_view(), name='set_services'),

    # tariff
    path('tariff/', views.TariffListView.as_view(), name='tariffs'),
    path('tariff/create/', views.TariffCreateVIew.as_view(), name='tariff_create'),
    path('tariff/update/<int:pk>/', views.TariffUpdateView.as_view(), name='tariff_update'),
    path('tariff/delete/', views.delete_tariff, name='delete_tariff'),
    path('tariff/<int:pk>/', views.TariffDetailView.as_view(), name='tariff_detail'),
    path('get-unit-for-service/', views.get_unit_for_service, name='unit_for_service'),

    # roles
    path('roles/update/', views.RolesUpdateView.as_view(), name='roles'),

    # requisites
    path('requisites/', views.RequisitesUpdateView.as_view(), name='requisites'),

    #payment state
    path('payment-states/', views.PaymentStateListView.as_view(), name='payment_states'),
    path('payment-states/create/', views.PaymentStateCreateView.as_view(), name='payment_state_create'),
    path('payment-states/update/<int:pk>/', views.PaymentStateUpdateView.as_view(), name='payment_state_update'),
    path('payment-states/delete/', views.delete_payment_state, name='payment_state_delete'),

]