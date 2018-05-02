from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views import generic

from shop.models import Category, Product


def product_list(request, category_slug=None):
    """
    show products:if no category_slug,show all products,else show specific category products.
    :param request:
    :param category_slug:a category slug
    """
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(is_sold=True)
    if category_slug:
        # if exist slug
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category__slug=category_slug, is_sold=True).select_related('category')
    context = {
        'categories': categories,
        'products': products,
        'category': category,
    }
    return render(request, 'shop/product/list.html', context)


class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'shop/product/detail.html'
    context_object_name = 'product'

    def get(self, request, *args, **kwargs):
        """相对默认实现添加了对 is_sold 字段的判定"""
        self.object = self.get_object()
        if self.object.is_sold:
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)
        else:
            raise Http404('The product is not sold')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            is_logined = True
        else:
            is_logined = False
        context['is_logined'] = is_logined
        return context
