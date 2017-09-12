/**
 * Created by jian on 2017/8/21.
 */

$('#comment-switch').click(function(){
    $('.comment-content-wrap').toggle(800);
});

$('#comment-submit-button').click(function(){
    $('#comment-submit').click();
});
$(function(){
    $('.flash-message').delay(2000).fadeOut(1500);
});
