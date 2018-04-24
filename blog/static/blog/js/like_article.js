$(document).ready(function () {
    let articles_likes = parseInt($('.liked_count').text());
    $('#like_article_btn').click(function () {
        // {# 用户未登录 #}
        if (login_status === 'no') {
            window.location.href = login_url;
        }
        else {
            $.post(like_url,
                {
                    article_id: article_id
                },
                function (data) {
                    // {# 用户点赞成功 #}
                    if (data['status']) {
                        $('#like_article_btn').text('取消赞');
                        articles_likes += 1;
                        $('.liked_count').text(articles_likes);
                    }
                    else {
                        $('#like_article_btn').text('赞');
                        articles_likes -= 1;
                        $('.liked_count').text(articles_likes);
                    }
                });
        }
    });
});