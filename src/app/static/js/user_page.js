$(document).ready(function() {
    $("#change_name").click(function() {
        $("#change_name_modal").modal("show");
    });

    $("#done_changing_name").click(function() {
        $.post('/change_user_name', {
            newName: $("#new_name").val()
        }).done(function(data) {
            if(data.status !== "ok") {
                alert("Ceva nu a mers bine");
            }
        });

        $("#new_name").val("");
        $("#change_name_modal").modal("hide");
        location.reload();
    });

    $("#change_password").click(function() {
        $("#change_password_modal").modal("show");
    });

    // Check password correction.
    var passwordTimer;
    var typingInterval = 1000;

    $("#current_password").keyup(function() {
        passwordTimer = setTimeout(function() {
            $.post("/check_password", {
                currentPassword: $("#current_password").val()
            }).done(function(data) {
                console.log(data);
                if(data.status === "wrong") {
                    // If the user didn't know the password it shouldn't be
                    // allowed to type the new one.
                    $("#new_password").prop("disabled", true);
                    $("#repeat_new_password").prop("disabled", true);
                }
                else if(data.status === "correct") {
                    // The password introduced by the user was right, we should
                    // let him add the new one.
                    $("#new_password").prop("disabled", false);
                    $("#repeat_new_password").prop("disabled", false);
                }
                else {
                    alert("Ceva nu a mers bine");
                }
            });
        }, typingInterval);
    });

    $("#current_password").keydown(function() {
        clearTimeout(passwordTimer);
    });

    $("#done_changing_password").click(function() {
        var password1 = $("#new_password").val();
        var password2 = $("#repeat_new_password").val();

        if(password1 !== password2) {
            alert("Parolele nu se potrivesc");
        }
        else {
            $.post("/change_password", {
                newPassword: password1
            }).done(function(data) {
                if(data.status !== "ok") {
                    alert("Ceva nu a mers bine");
                }
                else if(data.status === "ok") {
                    alert("Parola a fost schimbata cu succes");
                }
            });
        }

        // We should, also, clear the value of the text fields.
        $("#current_password").val("");
        $("#new_password").val("");
        $("#repeat_new_password").val("");

        // And we should, also, block the fields again.
        $("#new_password").prop("disabled", true);
        $("#repeat_new_password").prop("disabled", true);

        $("#change_password_modal").modal("hide");
    });

    $("#change_email").click(function() {
        $("#change_email_modal").modal('show');
    });

    $("#done_changing_email").click(function() {
        $.post('/change_user_email', {
            newEmail: $("#new_email").val()
        }).done(function(data) {
            if(data.status !== "ok") {
                alert("Ceva nu a mers bine");
            }
        });

        $("#new_email").val("");
        $("#change_name_modal").modal("hide");
        location.reload();
    });

});