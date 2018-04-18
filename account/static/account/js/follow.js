$(document).ready(function () {
    $('#follow-button').click(function () {
        var now_fans = parseInt($('#total-fans').text());
        $.post(follow_url,
            {
                user_id: user_id,
                action: $('#follow-button').attr('value')
            },
            function (data) {
                {
                    if (data['action'] === '取消关注') {
                        $('#follow-button').text(data['action']).val(data['action']);
                        now_fans += 1;
                        $('#total-fans').text(now_fans);
                    }
                    else if (data['action'] === '关注') {
                        $('#follow-button').text(data['action']).val(data['action']);
                        now_fans -= 1;
                        $('#total-fans').text(now_fans);
                    }
                    else if (data['action'] === 'self') {
                        alert('不能关注自己');
                    }
                    else {
                        window.location.href = data['url']
                    }
                }
            });
    });
});