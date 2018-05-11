from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST

from coupons.forms import CouponForm
from coupons.models import Coupon


@require_POST
def apply_coupon(request):
    now = timezone.now()
    coupon_form = CouponForm(request.POST)
    if coupon_form.is_valid():
        code = coupon_form.cleaned_data['code']
        try:
            coupon = get_object_or_404(Coupon,
                                       code=code,
                                       is_actived=True,
                                       valid_from__lt=now,
                                       valid_to__gt=now,
                                       )
            request.session['coupon_id'] = coupon.id
        except Http404:
            messages.warning(request, f"优惠劵代码错误/已过期/已失效")
            request.session['coupon_id'] = None
        return redirect('cart:cart_detail')
