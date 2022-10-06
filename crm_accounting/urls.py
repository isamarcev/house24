from django.urls import path, include
from . import views

app_name = 'crm_accounting'

urlpatterns = [

    # accounts
    # path('account/detail/<int:pk>/', views.main_page, name='account_detail'),


    # counter
    path('account/counter/detail/<int:pk>/', views.main_page, name='counter_data'),

    # transaction приходная ведомость
    path('account/', views.AccountListView.as_view(), name='account_list'),
    path('account/get-ajax-list/', views.AccountListViewAjax.as_view(), name='get_account_ajax_list'),
    path('account/create/', views.AccountCreateView.as_view(), name='account_create'),
    path('account/detail/<int:pk>/', views.PersonalAccountDetailView.as_view(), name='detail_account'),
    path('account/update/<int:pk>/', views.PersonalAccountUpdateView.as_view(), name='account_update'),
    path('account/delete/', views.DeletePersonalAccount.as_view(), name='delete_account'),
    path('get-flats/', views.get_flats, name='get_flats'),
    path('get-users/', views.get_users, name='get_users'),
    path('account/transaction/', views.main_page, name='transaction_account_detail'),
    path('account/transaction/create/', views.main_page, name='transaction_account_create'),


    # invoice для
    path('account/invoice/detail/<int:pk>/', views.main_page, name='invoices_for_flat'),
    path('account/invoice/create/', views.main_page, name="create_invoice_for_flat"),

]