$(document).ready(function() {
    $("#change_name").click(function() {
        $("#change_name_modal").modal("show");
    });

    $("#done_changing_name").click(function() {
        $.post('/change_user_name', {
            newName: $("#new_name").val()
        }).done(function(data) {
            if(data.status != "ok") {
                alert("Ceva nu a mers bine");
            }
        });

        $("#change_name_modal").modal("hide");
        location.reload();
    });

    $("#change_password").click(function() {

    });

    $("#change_email").click(function() {

    });
});