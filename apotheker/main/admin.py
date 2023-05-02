from django.contrib import admin
from .models import Receipt, ReceiptSchedule, Drug

admin.site.register(Receipt)
admin.site.register(ReceiptSchedule)
admin.site.register(Drug)
