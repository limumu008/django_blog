$(document).ready(function () {
    $('.reply').click(function () {
        $.post(reply_url, {action: 'test_user'},
            function (data) {
                if (data['status'] === 'redirect') {
                    location.href = data['login_url'];
                }
            });
        $(this).hide();
        var reply_global_id = $(this).val();
        var show_form = "#form-" + reply_global_id;
        $(show_form).removeAttr('hidden');
    });
    $('form').submit(function (e) {
        if ($(this).attr('id') !== 'new-comment') {
            var content = $(this).find('textarea').val();
            var comment = $(this).find('input').first().val();
            $(this).hide();
            $('.reply').show();
            e.preventDefault();
            $.post(reply_url, {
                comment: comment,
                content: content
            }, function (data) {
                if (data['status'] === 'reply_ok') {
                    $('#replies-' + comment).append(data['reply_text']);
                }
            });
        }
    });
});