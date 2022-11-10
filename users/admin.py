from django.contrib import admin
from .models import CustomUser, Role, Request, Message, MessageUsers

admin.site.register(CustomUser)
admin.site.register(Role)
admin.site.register(Request)
admin.site.register(Message)
admin.site.register(MessageUsers)