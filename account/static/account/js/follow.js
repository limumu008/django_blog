// 监听事件
let bus = new Vue();

let follow = new Vue({
    delimiters: ['[[', ']]'],
    el: '#follow_button',
    data: {
        follow_status: is_follow,
        login_status: login_status,
    },
    computed: {
        text: function () {
            if (this.follow_status) {
                return '取消关注'
            }
            else if (!this.follow_status) {
                return '关注'
            }
        }
    },
    methods: {
        follow: function () {
            if (!this.login_status) {
                location.href = login_url;
            }
            $.post(follow_url,
                {
                    user_id: user_id,
                    follow_status: this.follow_status
                },
                function (data) {
                    if (data['action'] === 'self') {
                        alert('不能关注自己');
                    }
                    else if (data['action'] === 'followed') {
                        follow.follow_status = true;
                        bus.$emit('followed');
                    }
                    else if (data['action'] === 'unfollow') {
                        follow.follow_status = false;
                        bus.$emit('unfollow');
                    }
                });
        }
    }
});

let fans_count = new Vue({
    delimiters: ['[[', ']]'],
    el: '#total_fans',
    data: {
        fans_quantity: fans_quantity,
    },
    mounted: function () {
        bus.$on('followed', function () {
            fans_count.fans_quantity += 1;
        });
        bus.$on('unfollow', function () {
            fans_count.fans_quantity -= 1;
        })
    }
});
