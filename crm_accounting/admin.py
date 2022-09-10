from django.contrib import admin
from .models import *


admin.site.register(PersonalAccount)
admin.site.register(Transaction)
admin.site.register(Invoice)
admin.site.register(InvoiceService)
