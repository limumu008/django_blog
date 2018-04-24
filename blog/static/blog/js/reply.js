$(document).ready(function () {
    $('.reply').click(function () {
            // 回复评论：点击回复按钮，展开回复表单，隐藏自己，如未登录则重定向
            if (login_status === 'no') {
                window.location.href = login_url;
            }
            let reply_commend_id = $(this).val();
            $(this).before(`<form action="${reply_url}" method="post" class="reply_comment">` +
                `<textarea name="content" rows="2" class="input_reply" placeholder="输入回复内容"></textarea>`
                + `<input type="number" hidden="hidden" name="comment" value="${reply_commend_id}">`
                + `<input type="hidden" name="csrfmiddlewaretoken" value="${csrftoken}">`
                + `<input type="submit" class="btn btn-default btn-xs"  value="回复">`
                + `</form>`
            );
            $(this).hide();
        }
    );
    $('.re-reply').click(function () {
        // 回复回复：点击回复按钮，展开回复表单，隐藏自己，如未登录则重定向
        if (login_status === 'no') {
            window.location.href = login_url;
        }
        let reply_id = $(this).val();
        $('#reply-' + reply_id).after(`<form action="${reply_url}" method="post" class="reply_reply">` +
            `<textarea name="content" rows="2" class="input_reply" placeholder="输入回复内容"></textarea>`
            + `<input type="number" hidden="hidden" name="reply" value="${reply_id}">`
            + `<input type="hidden" name="csrfmiddlewaretoken" value="${csrftoken}">`
            + `<input type="submit" class="btn btn-default btn-xs" value="回复">`
            + `</form>`
        );
        $(this).hide();
    });
    $(document).on('submit', '.reply_comment', function (e) {
        // 针对回复评论的成功回调
        if ($(this).attr('id') !== 'new_comment') {
            let content = $(this).find('textarea').val();
            let comment = $(this).find('input').first().val();
            let action = 'reply_comment';
            $(this).hide();
            $('.reply').show();
            e.preventDefault();
            // 登录则重定向
            if (login_status === 'no') {
                window.location.href = login_url;
            }
            $.post(reply_url, {
                action: action,
                comment: comment,
                content: content
            }, function (data) {
                if (data['status'] === 'reply_ok') {
                    $('#replies-' + comment).append(data['reply_text']);
                }
            });
        }
    });
    $(document).on('submit', '.reply_reply', function (e) {
        // 针对回复回复的成功回调
        if ($(this).attr('id') !== 'new_comment') {
            let content = $(this).find('textarea').val();
            let reply = $(this).find('input').first().val();
            let action = 'reply_reply';
            $(this).hide();
            $('.re_reply').show();
            e.preventDefault();
            // 登录则重定向
            if (login_status === 'no') {
                window.location.href = login_url;
            }
            $.post(reply_url, {
                action: action,
                selected_reply: reply,
                content: content
            }, function (data) {
                if (data['status'] === 'reply_ok') {
                    $('#replies-' + data['comment_id']).append(data['reply_text']);
                }
            });
        }
    });
});