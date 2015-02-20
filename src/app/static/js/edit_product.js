$(document).ready(function() {

    var imageCollection = new ImageCollection(collectionItems, $("#imageCollection"));
    var mainImage = new MainImage(placeholder, $("#mainImage"));
    var specificationsBox = new SpecificationsBox($("#specifications_container"),
        specifications);
    imageCollection.generateHTML();
    specificationsBox.generateHTML();

    // If there are no images available we will use the
    // default one.
    if(collectionItems.length === 0) {
        mainImage.setDefaultMainItem();
        // Hide controls for the default image.
        $("#removeImage").hide();
        $("#editImage").hide();
    } else {
        // Otherwise we will set the first element from the
        // list as the active element.
        (function() {
            // We use a function just to reduce the scope of the
            // variables created here
            var $item = imageCollection.setCurrentItem(0);
            mainImage.setCurrentMainItem($item);
        })();
    }

    $("#edit_images_button").click(function() {
        $("#edit_images_dialog").modal("show");
    });

    $("#imageCollection").click(function(event) {
        // We care only about the elements that have the
        // collection-item class.
        if($(event.target).hasClass("collection-item")) {
            // Enable controls.
            $("#removeImage").show();
            $("#editImage").show();
            // Get the index of the clicked item.
            // Since in the container of the div.row are, also, br elements
            // we only care about the id of the div among the other div.
            (function() { // Just to minimize the scope of the variables.
                var index = $(event.target).closest("div.row").index();
                // Save the item thus we can use it to set the main item.
                var $item = imageCollection.setCurrentItem(index);
                mainImage.setCurrentMainItem($item);
            })();
        }
    });

    $("#removeImage").click(function(event) {
        (function () {
            var answer = confirm("Esti sigur ca vrei stergi imaginea?");
            if(answer) {
                var index = imageCollection.getCurrentSelectedItemIndex();
                var $item = imageCollection.removeItem(index);
                if($item !== null) {
                    // There is an element after deleting the current
                    // one.
                    mainImage.setCurrentMainItem($item);
                } else {
                    mainImage.setDefaultMainItem();
                    // Disable controls.
                    $("#editImage").hide();
                    $("#removeImage").hide();
                }
            }
        })();
    });

    $("#editImage").click(function(event) {
        var newUrl = prompt("Enter the new url");
        // Check to see if the user has clicked the cancel button.
        if(newUrl !== null) {
            var $changedItem = imageCollection.changeCurrentItem(newUrl);
            mainImage.setCurrentMainItem($changedItem);
        }
    });

    $("#addImage").click(function(event) {
        var imageUrl = prompt("Enter image url here");
        if(imageUrl !== null) {
            // This is just to reduce scope of the variables created
            // here.
            (function() {
                var $item = imageCollection.addItem(imageUrl);
                if(mainImage.isDefaultItem()) {
                    mainImage.setCurrentMainItem($item);
                }
            })();
        }

    });

    $("#finish_editing_images").click(function() {
        $("#edit_images_dialog").modal("hide");
    });

    $("#edit_specifications").click(function() {
        $("#edit_specifications_modal").modal("show");
    });

    $("#add_new_specification").click(function() {
        specificationsBox.addNewBlankSpecification();
    });

    $("#finish_editing_specifications").click(function() {
        if(specificationsBox.validate()) {
            $("#edit_specifications_modal").modal("hide");
        } else {
            alert("Nu ati completat corect. Verificati campurile goale.");
        }
    });

    $("#add_the_edits").click(function() {
        $("#specifications").val(specificationsBox.getJSONString());
        $("#pictures").val(imageCollection.getJSONString());
        $("#edit_product_form").submit();
    });
});