$(document).ready(function() {

    // Handle events for images adding modal.
    var fieldCounter = 1; // because id 0 is assigned to the first text field.
    var imageLinks = [];

    // This object will contain all the specifications that the user will add.
    var specificationsObject = {};

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
            imageLinks.push(this.value); // It is easier to split links by the | character
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
                if(imageLinks[i] === $(event.target).closest("div.row")
                                        .find("input[type=text]")
                                        .val()) {
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
            $("#pictures").val(JSON.stringify(imageLinks));
            $("#specifications").val(JSON.stringify(specificationsObject));
            $("#image_uploading_form").submit();
        }

    });

    //Handle events for specifications modal.
    $("#add_specifications").click(function() {
        $("#add_specifications_modal").modal("show");
    });

    $("#add_new_specification").click(function() {
        $("#specifications_container").append('\
            <div class="row">\
                <br>\
                <div class="col-xs-4">\
                    <div class="form-group">\
                        <input type="text" class="form-control specification-name" \
                                placeholder="nume specificatie"/>\
                    </div>\
                </div>\
                <div class="col-xs-7">\
                    <div class="form-group">\
                        <input class="form-control specification-value" type="text" placeholder="specificatia"/>\
                    </div>\
                </div>\
                <div class="col-xs-1">\
                    <button type="button" class="close">\
                        <span class="close"> &times; </span>\
                    </button>\
                </div>\
            </div>');
    });

    $("#specifications_container").click(function(event) {
        if($(event.target).hasClass("close")) {
            // Before remove the row that contains the specifications,
            // we have to remove the respective property from the
            // specifications object.
            var specificationName = $(event.target).closest("div.row").
                find(".specification-value").val();

            delete specificationsObject[specificationName];

            $(event.target).closest("div.row").remove();
        }

    });

    $("#finish_adding_specifications").click(function() {
        var displayAlert = false;

        // First lets check if there are empty input fields.
        $("#specifications_container").find(".specification-name").
                each(function(index, element) {

            var $specName = $(element);
            var $specValue = $(element).closest("div.row").find(".specification-value");

            // If the input is empty we will add the has-error class, thus adding
            // a red border to the input field.
            if($specName.val() === "") {
                $specName.closest("div.form-group").addClass("has-error");
            }

            if($specValue.val() === "") {
                $specValue.closest("div.form-group").addClass("has-error");
            }

            // If both the name and the value of the specification are ok
            // we can add that entry to the specification object.
            if($specName.val() !== "" && $specValue.val() !== "") {
                if(!_.has(specificationsObject, $specName.val())) {
                    specificationsObject[$specName.val()] = $specValue.val();
                }
            }
        });

        if(displayAlert) {
            alert("Nu ai completat bine formularul");
        }

        $("#add_specifications_modal").modal("hide");
    });

    // Monitor user while is typing.
    var timer;
    var interval = 500; // 500 milliseconds will be more than enough.

    $("#specifications_container").keyup(function(event) {
        timer = setTimeout(function() {
            // At this moment the validation only checks to see if the input fields
            // are not empty. The validation part will be extended in the future.
            if($(event.target).val() !== "") {
                // Remove the error decoration.
                var $parent = $(event.target).closest("div.form-group");
                $parent.removeClass("has-error");
                $parent.addClass("has-success");
            }
        }, interval);
    });

    $("#specifications_container").keydown(function() {
        clearTimeout(timer);
    });

});