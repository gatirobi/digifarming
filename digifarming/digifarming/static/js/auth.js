// $(document).ready(function () {
//     //Admin registration
//     $('#admin_register_form').on('submit', function (e) {
//         e.preventDefault();
//         const $form = $(this);
//         var form_data = new FormData($form[0]);
//         var save_btn = $form.find('.save_btn');

//         save_btn.attr('disabled', 'disabled');
//         save_btn.empty().append('<i class="fa fa-spinner fa-spin"></i> Processing');
//         // console.log($form[0]);
//         console.log('inside auth function');


//         setTimeout(function () {
//             $.ajax({
//                 url: $form.attr('action'),
//                 type: 'POST',
//                 data: new FormData(this),
//                 dataType: 'json',
//                 processData: false,
//                 contentType: false,

//                 success: function (data) {
//                     console.log('inside js function');
//                     console.log(data);
//                     save_btn.remove('btn-primary').addClass('btn-success');
//                     save_btn.empty().append('<i class="fa fa-check"></i> Account Created Successfully');
//                     setTimeout(function () {
//                         window.location = data.url;
//                     }, 500);
//                 },

//                 error: function (data) {
//                     console.log('inside error function');
//                     console.log(data);
//                     $('#admin_auth_errors').empty().append(data.responseJSON.html);
//                     save_btn.removeAttr('disabled').empty().append('Create User Account');
//                 }
//             });

//         }, 500);
//     });
// });