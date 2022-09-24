from django.urls import path, include
from . import views

app_name = 'users'
urlpatterns = [
    path('accounts/login/', views.LoginUser.as_view(), name='login'),
    path('accounts/admin-login/', views.LoginUser.as_view(), name='admin-login'),

    path('', views.UsersListView.as_view(), name='users'),
    path('create/', views.UserCreateView.as_view(), name='user_create'),
    path('update/<int:pk>/', views.UserUpdateView.as_view(), name='user_update'),
    path('detail/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    path('delete/<int:pk>/', views.delete_user, name='user_delete'),

    path('ajax-user-list/', views.AjaxUsersListView.as_view(), name='ajax-users'),

    # path('accounts/login/', views.LoginUser.as_view(), name='login'),

    # path('admin/login/', views.LoginUser.as_view(), name='login'),

    # path('accounts/logout/', views.LoginUser.as_view, name='logout'),

    # path('about-us/', views.about, name='about'),
    # path('services/', views.services, name='services'),
    # path('contacts/', views.contacts, name='contacts'),

]