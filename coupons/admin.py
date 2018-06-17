from django.contrib import admin

from coupons.models import Coupon


class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'valid_from', 'valid_to', 'discount', 'is_actived']
    list_filter = ['is_actived', 'valid_from', 'valid_to']
    search_fields = ['code']


admin.site.register(Coupon, CouponAdmin)
