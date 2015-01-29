$(document).ready(function() {
    var fieldCounter = 1; // because id 0 is assigned to the first text field.
    var imageLinks = [];

    $("#add_images_button").on('click', function() {
        $("#add_images_dialog").modal("show");
    });

    $("#add_another_image").on('click', function() {
        $("#links_container").append('\
            <div class="row">\
                <br>\
                <div class="col-xs-7">\
                    <input type="text" placeholder="link here" class="form-control" />\
                </div>\
                <div class="col-xs-1">\
                    <button type="button" class="close">\
                        <span class="close"> &times; </span>\
                    </button>\
                </div>\
            </div>');
        fieldCounter++;
    });

    $("#finish_adding_images").on('click', function() {

        // Verify if there are two identical values
        var identicalElements = 0;
        $("#links_container").find("input").each(function(index, element) {
            $("#links_container").find("input").each(function(index2, element2) {
                if(index === index2) {
                    return false;
                }
                if($(element).val() === $(element2).val()) {
                    identicalElements++;
                        return true;
                }
                return true;
            });

        });

        if(identicalElements > 0) {
            alert("Ai introdus doua linkuri cu aceeasi valoare");
            return;
        }

        $("#links_container").find("input").each(function(index) {
            imageLinks.push(this.value + "|"); // It is easier to split links by the | character
        });

        // Before hiding the dialog we must also check if all the boxes are not empty.
        var allFieldsAreCompleted = false;
        $("#links_container").find("input[type=text]").each(function(index, element) {
            console.log($(element));
            allFieldsAreCompleted = $(element).val() !== "";
        });

        if(allFieldsAreCompleted) {
            $("#add_images_dialog").modal("hide");
        }
        else {
            alert("You haven't completed all the fields");
        }

    });

    $('#links_container').on('click', function(event) {
        if($(event.target).hasClass("close")) {
            for(var i = 0; i < imageLinks.length; i++) {
                // The last charachter is a "|" and we need to get rid of it.
                if(imageLinks[i].slice(0, -1) === $(event.target).closest("div.row").find("input[type=text]").
                    val()) {
                    imageLinks.splice(i, 1);
                }
            }
            console.log(imageLinks);
            $(event.target).closest("div.row").remove();
            $(event.target).remove();
            fieldCounter--;
            if(fieldCounter === 0) {
                $("#add_images_dialog").modal("hide");
            }
        }
    });

    $("#add_the_product").on('click', function() {
        if(imageLinks.length === 0) {
            // 1 hidden input is added by wtforms.
            alert("You haven't added any image. Please add at least one image and submit the form after");
        }
        else {
            $("#pictures").val(imageLinks);
            $("#image_uploading_form").submit();
        }

    });
});