let table = new Vue(
    {
        delimiters: ['[[', ']]'],
        el: 'table',
        data: {
            total_price: total_price,
            discount: discount,
            total_price_after_discount: total_price_after_discount,
        },
        methods: {
            rm_product: function (e) {
                let product_id = e.target.value;
                $.post(change_cart_url, {
                    action: 'remove_product',
                    product_id: product_id
                }, function (data) {
                    if (data['status'] === 'rm_success') {
                        $('#tr-' + product_id).hide();
                        table.total_price -= data['this_price'];
                        table.discount = table.total_price * data['discount'] / 100;
                        table.total_price_after_discount = table.total_price - table.discount;
                    }
                });
            }
        }
    }
);