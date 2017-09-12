$('#form-username').blur(function(){
    $.ajax({
        url: '/validate_username',
        data: $('#form-username').serialize(),
        type: 'POST',
        dataType: 'json'
    }).done(function(data){
        console.log('username ajax success');
        if(data['issue'] == 'username' && data['OK'] == true){
            $('#username-alert-success').css('display', 'block');
            $('#username-alert-danger').css('display', 'none');
        }else if(data['issue'] == 'username' && data['OK'] == false){
            $('#username-alert-danger').css('display', 'block');
            $('#username-alert-success').css('display', 'none');
        }
    });
});

$('#form-repassword').blur(function(){
    var password = $('#form-password').val();
    var repassword = $('#form-repassword').val();
    if(password != repassword){
        $('#repassword-alert-danger').css('display', 'block');
    }else{
        $('#repassword-alert-danger').css('display', 'none');
    }
});

$('#form-sign').blur(function(){
    var l = $('#form-sign').val().length;
    if(l >= 255){
        $('#sign-alert-danger').css('display', 'block');
    }else{
        $('#sign-alert-danger').css('display', 'none');
    }
});
$('#form-submit-tri').click(function(){
    $('#form-submit').click();
});