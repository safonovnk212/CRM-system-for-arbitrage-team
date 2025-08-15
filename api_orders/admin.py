from django.contrib import admin
from .models import Order, KeitaroEvent

@admin.register(KeitaroEvent)
class KeitaroEventAdmin(admin.ModelAdmin):
    list_display=('id','subid','status','payout','created_at')
    list_filter=('status',); search_fields=('subid',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=('id','keitaro_subid','status','payout','created_at')
    search_fields=('keitaro_subid','email','phone_number')
