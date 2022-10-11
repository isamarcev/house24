from django.urls import path, include
from . import views

app_name = 'crm_home'
urlpatterns = [
    path('set-services/', views.ServiceSettings.as_view(),
         name='set_services'),

    # tariff
    path('tariff/', views.TariffListView.as_view(), name='tariffs'),
    path('tariff/create/', views.TariffCreateVIew.as_view(),
         name='tariff_create'),
    path('tariff/update/<int:pk>/', views.TariffUpdateView.as_view(),
         name='tariff_update'),
    path('tariff/delete/', views.delete_tariff,
         name='delete_tariff'),
    path('tariff/<int:pk>/', views.TariffDetailView.as_view(),
         name='tariff_detail'),
    path('get-unit-for-service/', views.get_unit_for_service,
         name='unit_for_service'),

    # roles
    path('roles/update/', views.RolesUpdateView.as_view(),
         name='roles'),

    # requisites
    path('requisites/', views.RequisitesUpdateView.as_view(),
         name='requisites'),

    #payment state
    path('payment-states/', views.PaymentStateListView.as_view(),
         name='payment_states'),
    path('payment-states/create/', views.PaymentStateCreateView.as_view(),
         name='payment_state_create'),
    path('payment-states/update/<int:pk>/',
         views.PaymentStateUpdateView.as_view(), name='payment_state_update'),
    path('payment-states/delete/', views.delete_payment_state,
         name='payment_state_delete'),


    #counter
    path('counter-data/', views.CounterDataListView.as_view(),
         name='counter_data_list'),
    path('counter-data/flat-counter-list/',
         views.FlatCounterDataListView.as_view(),
         name='flat_counter_list'),



    path('counter-data-ajax-list/', views.CounterDataListViewAjax.as_view(),
         name='counter_data_list_ajax'),
    path('counters-flat-ajax/', views.FlatCounterDataGetViewAjax.as_view(),
         name='counter_data-flat_get_ajax'),
    path('counter-data/delete', views.CounterDeleteAjax.as_view(),
         name='counter_delete_ajax'),
    path('counter-data/create/', views.CounterDataCreateView.as_view(),
         name='counter_data_create'),
    path('counter-data/detail/<int:pk>/',
         views.CounterDetailView.as_view(),
         name='counter_data_detail'),
    path('counter-data/update/<int:pk>/',
         views.CounterDataUpdateView.as_view(),
         name='counter_data_update'),

]