$(document).ready(function () {
    $('button').click(function () {
        let product_id = $(this).val();
        $.post(change_cart_url, {
            action: 'remove_product',
            product_id: product_id
        }, function (data) {
            if (data['status'] === 'rm_success') {
                $('#tr-' + product_id).hide();
                let total_price = parseFloat($('#total-price').text());
                total_price -= data['this_price'];
                $('#total-price').text(total_price);
            }
        });
    });
});