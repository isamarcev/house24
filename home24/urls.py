from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('samartsev/', admin.site.urls),
    path('', include('content.urls')),
    path('admin/', include('houses.urls')),
    path('users/', include('users.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    # path('users/', include('users.urls')),
    # path('cabinet/', include('users.urls')),
    # path('cabinet/', include('users.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
