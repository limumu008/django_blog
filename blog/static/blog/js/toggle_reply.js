$(document).ready(function () {
    $('.toggle_reply_btn').click(function () {
        let current_comment_id = $(this).val();
        let name = $(this).attr('name');
        if (name === 'close') {
            $(this).text('展开回复').attr('name', 'open');
        }
        else if (name === 'open') {
            $(this).text('收起回复').attr('name', 'close');
        }
        $('#replies-' + current_comment_id).slideToggle('fast');
    });
});