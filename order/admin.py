from django.contrib import admin

from order.models import OrderItem, Order


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'is_paid', 'address', 'created', 'updated']
    list_filter = ['is_paid', 'created', 'updated']
    list_editable = ['is_paid']
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
