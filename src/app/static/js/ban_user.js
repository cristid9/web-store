$(document).ready(function() {

    $("#ban_user").click(function() {
        if(confirm("Sunteti sigur ca doriti sa stergi acest utilizator?")) {
            $("#check_password_modal").modal("show");
        }
    });

    $("#done_checking_password").click(function() {
        if($("#check_current_password").val() !== "") {
            var password = $("#check_current_password").val();
            var isCorrectPassword = null;

            $.post('/check_password', {
                currentPassword: password
            }).done(function(data) {
                if(data.status === "correct") {
                    isCorrectPassword = true;
                } else if(data.status === "wrong") {
                    alert("Parola nu este corecta");
                }

                if(isCorrectPassword) {
                    $.post('/ban_user', {
                        user: username,
                        admin: admin
                    }).done(function(data) {
                        console.log(data);
                        if(data.status === "ok") {
                            alert("Userul " + username + " a fost sters cu sucess");
                            location.replace(data.redirectPage);
                        } else {
                            alert("A aparut o problema");
                        }
                    });
                } else {
                    alert("Parola este incorecta");
                }
            });

            $("#check_password_modal").modal("hide");

        } else {
            alert("Parola nu poate fi nula!");
            alert($("#check_current_password").val());
        }
    });

});




