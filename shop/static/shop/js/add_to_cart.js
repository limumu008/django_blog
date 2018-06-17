$(document).ready(function () {
    $('#to-cart').click(function () {
        if (!is_logined) {
            location.href = login_url;
        }
        else {
            let product_id = $(this).val();
            $.post(change_cart_url, {
                    action: 'add_product',
                    product_id: product_id
                }, function (data) {
                    if (data['status'] === 'add_success') {
                        $.growl({title: '提示', message: '已加入购物车', duration: 1000});
                        let cart_products = parseInt($('#cart-product-count').text());
                        $('#cart-product-count').text(cart_products + 1);
                    }
                }
            );
        }
    });
});