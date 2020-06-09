// $(document).ready(function () {
//     // Station dropdown
//      $("#id_hub").change(function () {
//       var url = $("#admin_submission_form").attr("data-stations-url");
//       var hubId = $(this).val();

//       $.ajax({
//         url: url,
//         data: {'hub': hubId },
//         success: function (data) {
//           $("#id_station").html(data);
//         }
//       });
//     });

//     //Submitting Data
//     $('#admin_submission_form').on('submit', function (e) {
//         e.preventDefault();
//         const $form = $(this);
//         var form_data = new FormData($form[0]);
//         var save_btn = $form.find('.save_btn');

//         save_btn.attr('disabled', 'disabled');
//         save_btn.empty().append('<i class="fa fa-spinner fa-spin"></i> Processing');
//         console.log($form[0]);

//         setTimeout(function () {
//             $.ajax({
//                 url: $form.attr('action'),
//                 type: 'POST',
//                 data: form_data,
//                 processData: false,
//                 contentType: false,

//                 success: function (data) {
//                     save_btn.remove('btn-primary').addClass('btn-success');
//                     save_btn.empty().append('<i class="fa fa-check"></i> Submission Created');
//                     setTimeout(function () {
//                         window.location = data.url;
//                     }, 500);
//                 },

//                 error: function (data) {
//                     $('#admin_submission_errors').empty().append(data.responseJSON.html);
//                     save_btn.removeAttr('disabled').empty().append('Create Submission');
//                 }
//             });

//         }, 500);
//     });
// });