from django.urls import path, include
from . import views

app_name = 'users'
urlpatterns = [
    path('accounts/login/', views.LoginUser.as_view(), name='login'),
    path('accounts/admin-login/', views.LoginAdminUser.as_view(),
         name='admin-login'),
    path('accounts/logout/', views.LogoutUser.as_view(),
         name='logout'),

    path('', views.UsersListView.as_view(), name='users'),
    path('create/', views.UserCreateView.as_view(), name='user_create'),
    path('update/<int:pk>/', views.UserUpdateView.as_view(),
         name='user_update'),
    path('detail/<int:pk>/', views.UserDetailView.as_view(),
         name='user_detail'),
    path('delete/<int:pk>/', views.delete_user, name='user_delete'),

    path('ajax-user-list/', views.AjaxUsersListView.as_view(),
         name='ajax-users'),

    # owners
    path('owner/', views.OwnerListView.as_view(), name='owner_list'),
    path('owner/create/', views.OwnerCreateView.as_view(),
         name='owner_create'),
    path('owner/update/<int:pk>/', views.OwnerUpdateView.as_view(),
         name='owner_update'),
    path('owner/detail/<int:pk>/', views.OwnerDetailView.as_view(),
         name='owner_detail'),
    path('owner/delete/', views.OwnerListView.as_view(), name='owner_delete'),


    #CABINET

    path('cabinet/statistic/', views.CabinetStatisticView.as_view(),
         name='statistic_user_view'),
    path('cabinet/invoices/', views.CabinetInvoicesListView.as_view(),
         name='invoice_for_users'),
    path('cabinet/invoices/<int:pk>/', views.CabinetInvoicesDetail.as_view(),
         name='detail_invoice_for_users'),
    path('cabinet/invoices/ajax-request/',
         views.CabinetInvoicesAjaxList.as_view(),
         name='invoice_for_users_ajax'),

    #TARIFF
    path('cabinet/tariff/', views.CabinetTariffForFlatView.as_view(),
         name='tariff_for_users_flat'),
    #MESSAGES
    path('cabinet/messages/', views.MessageUserList.as_view(),
         name='messages_view'),
    path('cabinet/messages/ajax-list/', views.MessageUserAjaxList.as_view(),
         name='messages_user_ajax'),
    path('cabinet/messages/delete/', views.MessageUserAjaxDelete.as_view(),
         name='messages_user_delete'),
    path('cabinet/messages/<int:pk>/', views.MessageUserDetailView.as_view(),
         name='messages_user_detail'),

    #REQUESTS
    path('cabinet/master-request/',
         views.RequestUserListView.as_view(),
         name='request_user_view'),
    path('cabinet/master-request/get-ajax-list/',
         views.RequestUserAjaxListView.as_view(),
         name='request_user_ajax_list'),
    path('cabinet/master-request/create/',
         views.RequestUserCreateView.as_view(),
         name='request_user_create'),
    path('cabinet/master-request/delete/',
         views.RequestUserAjaxDelete.as_view(),
         name='request_user_delete'),

    #PROFILE
    path('cabinet/profile/',
         views.ProfileUserView.as_view(),
         name='user_profile'),
    path('cabinet/profile/update/',
         views.ProfileUserUpdate.as_view(),
         name='user_profile_update'),



    # request
    path('requests/', views.RequestListView.as_view(), name='requests_list'),
    path('requests-get-ajax/', views.RequestGetViewAjax.as_view(),
         name='requests_get_ajax_list'),
    path('delete-request-ajax/', views.RequestDeleteAjax.as_view(),
         name='requests_delete_ajax'),
    path('requests/create/', views.RequestsCreateView.as_view(),
         name='requests_create'),
    path('ajax-user-flats/', views.AjaxUserFlatsList.as_view(),
         name='ajax_user_flats'),
    path('requests/update/<int:pk>/', views.RequestUpdateView.as_view(),
         name='requests_update'),
    path('requests/detail/<int:pk>/', views.RequestDetailView.as_view(),
         name='requests_detail'),

    # MESSAGES
    path('messages/', views.MessageListView.as_view(),
         name='message_list'),
    path('messages/get-ajax-list/', views.MessageAjaxList.as_view(),
         name='message_get_ajax_list'),

    path('messages/get-ajax-house/', views.MessageAjaxHouseInfo.as_view(),
         name='message_ajax_info_for_house'),
    path('messages/delete/', views.MessageAjaxDelete.as_view(),
         name='messages_delete'),

    path('messages/get-ajax-section/', views.MessageAjaxSectionInfo.as_view(),
         name='message_ajax_info_for_section'),

    path('messages/create/', views.MessageCreateView.as_view(),
         name='message_create'),
    path('messages/detail/<int:pk>/', views.MessageDetailView.as_view(),
         name='message_detail'),




    # path('accounts/login/', views.LoginUser.as_view(), name='login'),

    # path('admin/login/', views.LoginUser.as_view(), name='login'),

    # path('accounts/logout/', views.LoginUser.as_view, name='logout'),

    # path('about-us/', views.about, name='about'),
    # path('services/', views.services, name='services'),
    # path('contacts/', views.contacts, name='contacts'),

]