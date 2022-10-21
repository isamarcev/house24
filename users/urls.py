from django.urls import path, include
from . import views

app_name = 'users'
urlpatterns = [
    path('accounts/login/', views.LoginUser.as_view(), name='login'),
    path('accounts/admin-login/', views.LoginUser.as_view(),
         name='admin-login'),

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

    # MESSAGE

    path('messages/', views.MessageListView.as_view(),
         name='message_list'),
    path('messages/get-ajax-list/', views.MessageAjaxList.as_view(),
         name='message_get_ajax_list'),

    path('messages/get-ajax-house/', views.MessageAjaxHouseInfo.as_view(),
         name='message_ajax_info_for_house'),

    path('messages/get-ajax-section/', views.MessageAjaxSectionInfo.as_view(),
         name='message_ajax_info_for_section'),



    path('messages/create/', views.MessageCreateView.as_view(),
         name='message_create'),
    path('messages/detail/<int:pk>/', views.MessageDetailView.as_view(),
             name='message_detail'),
    path('messages/delete/', views.MessageDeleteView.as_view(),
             name='message_delete'),


    # path('accounts/login/', views.LoginUser.as_view(), name='login'),

    # path('admin/login/', views.LoginUser.as_view(), name='login'),

    # path('accounts/logout/', views.LoginUser.as_view, name='logout'),

    # path('about-us/', views.about, name='about'),
    # path('services/', views.services, name='services'),
    # path('contacts/', views.contacts, name='contacts'),

]