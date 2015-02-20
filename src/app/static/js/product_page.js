"use strict";
$(document).ready(function() {

    $("#publish_comment").click(function() {
        var poster = userData.name;
        var content = $("#comment_content").val();
        var comment = new Comment(poster,
                                  content,
                                  $("#comments_container"),
                                  userData.productId);

        if(!comment.isValid()) {
            alert("Comentariul nu este valid, ai grija ca nu poti folosi mai" +
                  "putin de 10 caractere");
        } else {
            comment.publish();
        }
    });

});