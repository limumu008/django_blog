// 监听事件
let bus1 = new Vue();

Vue.component('like-btn', {
    props: ['is_liked'],
    template: `<button class="btn btn-default" v-on:click="like" >\
                    <span class="glyphicon glyphicon-thumbs-up" aria-hidden="true"></span>\
                </button>`,
    methods: {
        like: function () {
            this.$emit('like');
        }
    }
});

let like_article = new Vue({
    delimiters: ['[[', ']]'],
    data: {
        is_liked: is_liked,
        article_likes: article_likes,
    },
    el: '#like-article',
    methods: {
        like: function () {
            if (!login_status) {
                location.href = login_url;
            }
            let target = 'article';
            $.post(like_url, {
                article_id: article_id,
                target: target
            }, function (data) {
                like_article.is_liked = !like_article.is_liked;
                if (like_article.is_liked) {
                    // 赞了
                    like_article.article_likes += 1;
                }
                else {
                    // 取消赞
                    like_article.article_likes -= 1;
                }
            });
        }
    }
});

$(document).ready(function () {
    $('.like_comment_btn').click(function () {
        let target = 'comment';
        let comment_id = $(this).val();
        let count_likes = parseInt($('#like_comment_count_' + comment_id).text());
        // {# 用户未登录 #}
        if (!login_status) {
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
                    if (data['is_liked']) {
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
        if (!login_status) {
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
                    if (data['is_liked']) {
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