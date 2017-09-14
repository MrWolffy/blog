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
/** change avatar */
$('#change-avatar-button').click(function(){
    $('#change-avatar-submit').click();
});
$('#avatar-tri').click(function(){
    $('#change-avatar-input').click();
    $('#change-avatar-button').css('display', 'block')
});
/** start tooltip */
$("[data-toggle='tooltip']").tooltip(
    {html: true}
);
console.log('tooltip started');