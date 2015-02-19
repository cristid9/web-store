"use strict";
$(document).ready(function() {

    $("#publish_comment").click(function() {
        var poster = userData.name;
        var content = $("#comment_content").val();
        var comment = new Comment(poster, content, $("#comments_container"));
        alert(comment.isValid());
    });

});