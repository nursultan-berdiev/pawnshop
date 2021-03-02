$(document).ready(function(){
    var loadForm = function() {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function(){
                $("#modal-loan .modal-content").html("");
                $("#modal-loan").modal("show");
            },
            success: function(data) {
                $("#modal-loan .modal-content").html(data.html_form);
            }
        });
    };

    $(".js-create-product").click(loadForm);
});

//$(document).ready(function(){
//    $('.show-form').click(function(){
//        $.ajax({
//            url: '/client/new'
//            type: 'get'
//            dataType: 'json'
//            beforeSend: function(){
//                $('#modal-loan').modal('show')
//            },
//            success: function(data) {
//                $('#modal-loan .modal-content').html(data.html_form)
//            }
//        })
//    })
//})