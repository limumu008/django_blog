$(document).ready(function () {
    var articles_likes = parseInt($('.liked-count').text());
    $('#like_article_btn').click(function () {
        $.post(like_url,
            {
                article_id: article_id
            },
            function (data) {
                // {# 用户未登录 #}
                if (data['status'] === 'redirect') {
                    window.location.href = data['url'];
                }
                // {# 用户点赞成功 #}
                else if (data['status']) {
                    $('#like_article_btn').text('取消赞');
                    articles_likes += 1;
                    $('.liked-count').text(articles_likes);
                }
                else {
                    $('#like_article_btn').text('赞');
                    articles_likes -= 1;
                    $('.liked-count').text(articles_likes);
                }

            });

    });
});