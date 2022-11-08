from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('samartsev/', admin.site.urls),
    path('', include('content.urls')),
    path('admin/', include('houses.urls')),
    path('crm-accounting/', include('crm_accounting.urls')),
    path('system-settings/', include('crm_home.urls')),
    path('users/', include('users.urls')),
    path('__debug__/', include('debug_toolbar.urls')),

]

handler404 = 'users.views.handlers404'
handler403 = 'users.views.handler403'

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
