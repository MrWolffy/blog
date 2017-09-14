/**
 * Created by jian on 2017/8/21.
 */

$(function (){
/** comment-switch   */
$('#comment-switch').click(function(){
    $('.comment-content-wrap').toggle(800);
});

/** submit edit form by another button */
$('#comment-submit-button').click(function(){
    $('#comment-submit').click();
});

/** flash message */
$('.flash-message').delay(2000).fadeOut(1500);
});




