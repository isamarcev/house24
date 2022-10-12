from django.contrib import admin
from .models import CustomUser, Role, Request


admin.site.register(CustomUser)
admin.site.register(Role)
admin.site.register(Request)
