/**
 * Created by jian on 2017/8/22.
 */

$(function(){
   $('#form-username').blur(function(){
       console.log('username starts');
       console.log($('#form-username').serialize());
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
   $('#form-email').blur(function(){
       console.log('email starts');
       var email=$(this).val();
       $.ajax({
           url: '/validate_email',
           data: $('#form-email').serialize(),
           type: 'POST',
           dataType: 'json'
       }).done(function(data){
           console.log('email ajax success');
           if(data['issue'] == 'email' && data['OK'] == true){
               $('#email-alert-success').css('display', 'block');
               $('#email-alert-danger').css('display', 'none');
           }else if(data['issue'] == 'email' && data['OK'] == false){
               $('#email-alert-danger').css('display', 'block');
               $('#email-alert-success').css('display', 'none');
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
});



