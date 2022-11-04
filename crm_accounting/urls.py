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
         views.TransactionDetailView.as_view(),
         name='transaction_detail'),
    path('transactions/delete/', views.DeleteTransaction.as_view(),
         name='delete_transaction'),
    path('transactions/export/', views.download_file,
         name='export_transaction'),
    path('transactions/get-personal-accounts-ajax/',
         views.get_personal_accounts_ajax,
         name='get_personal_accounts_ajax'),
    path('transactions/get-ajax-transaction-list/',
         views.TransactionListViewAjax.as_view(),
         name='get_transaction_ajax_list'),

    # invoices
    path('account/invoice/detail/<int:pk>/', views.main_page,
         name='invoices_for_flat'),
    path('account/invoice/create/', views.main_page,
         name="create_invoice_for_flat"),
    path('invoices/', views.InvoiceListView.as_view(), name='invoice_list'),
    path('invoices/get-ajax-list/', views.InvoiceListViewAjax.as_view(),
         name='get_invoices_ajax_list'),
    path('invoices/create/', views.InvoiceCreateView.as_view(),
         name='invoice_create'),
    path('invoices/detail/<int:pk>/', views.InvoiceDetailView.as_view(),
         name='invoice_detail'),
    path('invoices/update/<int:pk>/', views.InvoiceUpdateView.as_view(),
         name='invoice_update'),
    path('invoices/delete/', views.InvoiceDeleteView.as_view(),
         name='delete_invoice'),
    path('invoices/get-section-flat-ajax/', views.SectionAjaxView.as_view(),
         name='get_section_and_flat'),
    path('invoices/get-flats-ajax/', views.FlatAjaxList.as_view(),
         name='invoice_get_flats'),
    path('invoices/get-info-by-flat/', views.FlatAjaxInfo.as_view(),
         name='get_info_by_flat'),
    path('invoices/get-tariff-info/', views.tariff_ajax_info,
         name="get_tariff_info"),
    path('invoices/print/<int:pk>/', views.TemplatePrintView.as_view(),
         name='print_invoice'),
    path('invoices/template/', views.TemplatesUpdateView.as_view(),
         name='update_templates'),

    #
    path('transactionыаыфав/create/', views.TransactionCreateView.as_view(),
         name='transaction_account_create'),

]