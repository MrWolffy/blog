/**
 * Created by jian on 2017/9/3.
 */
$('#interested-tab').click(function(){
    $(this).addClass('active');
    $('#wrote-tab').removeClass('active');
    $('#interested-article').fadeIn();
    $('#wrote-article').fadeOut();
});
$('#wrote-tab').click(function(){
    $(this).addClass('active');
    $('#interested-tab').removeClass('active');
    $('#interested-article').fadeOut();
    $('#wrote-article').fadeIn();
});