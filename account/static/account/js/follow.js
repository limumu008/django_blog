$(document).ready(function () {
    $('#follow_button').click(function () {
        ``
        let now_fans = parseInt($('#total_fans').text());
        $.post(follow_url,
            {
                user_id: user_id,
                action: $('#follow_button').val()
            },
            function (data) {
                {
                    if (data['action'] === '取消关注') {
                        $('#follow_button').text(data['action']).val(data['action']);
                        now_fans += 1;
                        $('#total_fans').text(now_fans);
                    }
                    else if (data['action'] === '关注') {
                        $('#follow_button').text(data['action']).val(data['action']);
                        now_fans -= 1;
                        $('#total_fans').text(now_fans);
                    }
                    else if (data['action'] === 'self') {
                        alert('不能关注自己');
                    }
                }
            });
    });
});