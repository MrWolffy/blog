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

    /** toastr设置 */
    toastr.options = {
        "closeButton": true,
        "debug": false,
        "newestOnTop": false,
        "progressBar": false,
        "positionClass": "toast-bottom-center",
        "preventDuplicates": false,
        "showDuration": "300",
        "hideDuration": "1000",
        "timeOut": "5000",
        "extendedTimeOut": "1000",
        "showEasing": "swing",
        "hideEasing": "linear",
        "showMethod": "fadeIn",
        "hideMethod": "fadeOut"
    };

    /** 评论框的逻辑 */
    var width = $('div.comment-detail').width();
    $('.reply-btn').click(function(){
        $(this).fadeOut(600);
        $(this).parent().parent().next().prepend(
            $('.reply-form-hide').fadeIn(600)
        );
    });
    $('.btn-sub_com-cancel').click(function(){
        $(this).parent().parent().parent().fadeOut(600);
        $('.reply-btn').fadeIn(600);
    });
    window.um = UM.getEditor('container-for-sub-comment', {
        autoHeightEnabled: true,

        autoFloatEnabled: true,

        initialFrameWidth: width,

        initialFrameHeight: 170,

        toolbar:['source | undo redo | bold italic underline strikethrough | superscript subscript | forecolor backcolor | removeformat |',
            'insertorderedlist insertunorderedlist | selectall cleardoc paragraph | fontfamily fontsize' ,
            '| justifyleft justifycenter justifyright justifyjustify |',
            'link unlink | emotion | horizontal print preview fullscreen', 'drafts']
    });

    /** 提交子评论 */
    $('.btn-sub_com-submit').click(function(){
        var main_comment_id = $(this).closest('li').attr('id');
        var content = $('#container-for-sub-comment').html();
        $.ajax({
            url: '/sub_comment_get',
            data: JSON.stringify({
                main_comment_id: main_comment_id,
                content: content
            }),
            type: 'POST',
            dataType: 'json'
        }).done(function(data){  /** 成功后弹出提示，再刷新页面 */
            toastr.success(data['info'], '提示信息');
            setTimeout("window.location.reload()", 5000);
        })
    });

    /** 小屏的侧边栏 */
    $('#side-nav-trigger').click(function(){
        $('#tiny-side-nav').animate({
                left: "0"
            }, 300
        );
    });
    $('#fold-side-nav').click(function(){
        $('#tiny-side-nav').animate({
                left: "-60%"
            }, 300
        );
    })
});




