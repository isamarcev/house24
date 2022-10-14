from django.urls import path, include
from . import views

app_name = 'crm_accounting'

urlpatterns = [

    # accounts
    # path('account/detail/<int:pk>/', views.main_page, name='account_detail'),


    # counter
    path('account/counter/detail/<int:pk>/', views.main_page,
         name='counter_data'),

    # transaction приходная ведомость
    path('account/', views.AccountListView.as_view(), name='account_list'),
    path('account/get-ajax-list/', views.AccountListViewAjax.as_view(),
         name='get_account_ajax_list'),
    path('account/create/', views.AccountCreateView.as_view(),
         name='account_create'),
    path('account/detail/<int:pk>/', views.PersonalAccountDetailView.as_view(),
         name='detail_account'),
    path('account/update/<int:pk>/', views.PersonalAccountUpdateView.as_view(),
         name='account_update'),
    path('account/delete/', views.DeletePersonalAccount.as_view(),
         name='delete_account'),
    path('get-flats/', views.get_flats, name='get_flats'),
    path('get-users/', views.get_users, name='get_users'),


    path('transactions/', views.TransactionListView.as_view(),
         name='transaction_list'),
    path('account/transaction/', views.main_page,
         name='transaction_account_detail'),
    path('transactions/create/', views.TransactionCreateView.as_view(),
         name='transaction_create'),
    path('transactions/update/<int:pk>/',
         views.TransactionUpdateView.as_view(),
         name='transaction_update'),
    path('transactions/detail/<int:pk>/',
         views.TransactionUpdateView.as_view(),
         name='transaction_detail'),
    path('transactions/delete/', views.DeleteTransaction.as_view(),
         name='delete_transaction'),
    path('transactions/get-personal-accounts-ajax/',
         views.get_personal_accounts_ajax,
         name='get_personal_accounts_ajax'),
    path('transactions/get-ajax-transaction-list/',
         views.TransactionListViewAjax.as_view(),
         name='get_transaction_ajax_list'),

    # invoice для
    path('account/invoice/detail/<int:pk>/', views.main_page,
         name='invoices_for_flat'),
    path('account/invoice/create/', views.main_page,
         name="create_invoice_for_flat"),
    #
    path('transactionыаыфав/create/', views.TransactionCreateView.as_view(),
         name='transaction_account_create'),

]