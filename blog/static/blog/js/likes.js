$(document).ready(function () {
    let articles_likes = parseInt($('#article_like_count').text());
    $('#like_article_btn').click(function () {
        let target = 'article';
        // {# 用户未登录 #}
        if (login_status === 'no') {
            window.location.href = login_url;
        }
        else {
            $.post(like_url,
                {
                    article_id: article_id,
                    target: target
                },
                function (data) {
                    // {# 用户点赞成功 #}
                    $('#like_article_btn').toggleClass('already_like');
                    if (data['status']) {
                        articles_likes += 1;
                        $('#article_like_count').text(articles_likes);
                    }
                    else {
                        articles_likes -= 1;
                        $('#article_like_count').text(articles_likes);
                    }
                });
        }
    });
    $('.like_comment_btn').click(function () {
        let target = 'comment';
        let comment_id = $(this).val();
        let count_likes = parseInt($('#like_comment_count_' + comment_id).text());
        // {# 用户未登录 #}
        if (login_status === 'no') {
            window.location.href = login_url;
        }
        else {
            $.post(like_url,
                {
                    comment_id: comment_id,
                    target: target
                },
                function (data) {
                    // {# 用户点赞成功 #}
                    $('#like_c_btn_' + comment_id).toggleClass('already_like');
                    if (data['status']) {
                        count_likes += 1;
                        $('#like_comment_count_' + comment_id).text(count_likes);
                    }
                    else {
                        count_likes -= 1;
                        $('#like_comment_count_' + comment_id).text(count_likes);
                    }
                });
        }
    });
    $('.like_reply_btn').click(function () {
        let target = 'reply';
        let reply_id = $(this).val();
        let count_likes = parseInt($('#like_reply_count_' + reply_id).text());
        // {# 用户未登录 #}
        if (login_status === 'no') {
            window.location.href = login_url;
        }
        else {
            $.post(like_url,
                {
                    reply_id: reply_id,
                    target: target
                },
                function (data) {
                    // {# 用户点赞成功 #}
                    $('#like_r_btn_' + reply_id).toggleClass('already_like');
                    if (data['status']) {
                        count_likes += 1;
                        $('#like_reply_count_' + reply_id).text(count_likes);
                    }
                    else {
                        count_likes -= 1;
                        $('#like_reply_count_' + reply_id).text(count_likes);
                    }
                });
        }
    });
});