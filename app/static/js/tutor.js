/**
 * Created by jian on 2017/8/21.
 */

$(function (){
/** comment-switch   */
$('#comment-switch').click(function(){
    $('.comment-content-wrap').toggle(500);
});

/** submit edit form by another button */
$('#comment-submit-button').click(function(){
    $('#comment-submit').click();
});

/** 切换comment 编辑窗口 */
$('#comment-button').click(function(){
    $('#comment-edit-window').toggle(500)
});

/** flash message */
$('.flash-message').delay(2000).fadeOut(1500);
});




