$(document).ready(function() {

    var imageCollection = new ImageCollection(collectionItems, $("#imageCollection"));
    var mainImage = new MainImage(placeholder, $("#mainImage"));

    imageCollection.generateHTML();
    mainImage.setDefaultMainItem();

    $("#edit_images_button").click(function() {
        $("#edit_images_dialog").modal("show");
    });

    $("#imageCollection").click(function(event) {
        // We care only about the elements that have the
        // collection-item class.
        if($(event.target).hasClass("collection-item")) {
            imageCollection.setCurrentItem($(event.target));
            mainImage.setCurrentMainItem($(event.target));
        }
    });

    $("#removeImage").click(function(event) {

    });

    $("#editImage").click(function(event) {
        var newUrl = prompt("Enter the new url");
        var changedItem = imageCollection.changeCurrentItem(newUrl);
        mainImage.setCurrentMainItem(changedItem);
    });

    $("#addImage").click(function(event) {
        var imageUrl = prompt("Enter image url here");
        if(imageUrl !== null) {
            imageCollection.addItem(imageUrl);
        }

    });

});