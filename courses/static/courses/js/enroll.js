let enroll = new Vue({
    delimiters: ['[[', ']]'],
    el: '#enroll_button',
    data: {
        is_enrolled: is_enrolled,
        is_logined: is_logined,
        course_id: course_id,
    },
    computed: {
        text: function () {
            if (this.is_enrolled) {
                return '已报名'
            }
            else if (!this.is_enrolled) {
                return '报名'
            }
        }
    },
    methods: {
        enroll: function () {
            if (!this.is_logined) {
                location.href = login_url;
            }
            else {
                $.post(enroll_url,
                    {
                        is_enrolled: this.is_enrolled,
                        course_id: this.course_id
                    },
                    function (data) {
                        if (data['is_enrolled']) {
                            enroll.is_enrolled = true;
                        }
                        else if (!data['is_enrolled']) {
                            enroll.is_enrolled = false;
                        }
                    }
                );
            }
        },
    }
});
