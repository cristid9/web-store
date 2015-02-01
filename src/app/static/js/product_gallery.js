function MainImage(placeholder,
                   $mainImageObject) {

    this.$currentMainItem = null;
    this.placeholder = placeholder;
    this.$mainImageObject = $mainImageObject;
}

MainImage.prototype.setCurrentMainItem = function($item) {
    this.$currentMainItem = $item;
    this.$mainImageObject.html('<img src="' + $item.attr('src') +
        '" width="100%" height="100%" />');
};

MainImage.prototype.setDefaultMainItem = function() {
    this.$mainImageObject.html('<img src="' + this.placeholder +
        '" width="100%" height="100%" />');
};

function ImageCollection(collectionItems,
                         imageCollectionObject) {

    this.$imageCollectionObject = imageCollectionObject;
    this.$currentItem = null;
    this.collectionItems = collectionItems;
    this.bgColorSelect = "blue";
    this.bgColorNormal = "white";
}

ImageCollection.prototype.changeCurrentItem = function(link) {
    var $changedItem = $('<div class="row">' +
            '<div class="col-xs-2">' +
            '</div>' +
            '<div class="col-xs-8">' +
                '<img src="' + link + '" width="100%" height="100%"' +
                    'class="collection-item" />' +
            '</div>' +
            '<div class="col-xs-2">' +
            '</div>' +
        '</div>' +
        '<br>');

    // Add the new item after the old one.
    this.$currentItem.closest("div.row").after($changedItem);
    // Now remove the old one.
    this.$currentItem.remove();

    // Now update the image gallery.
    this.$currentItem = $changedItem;
    this.setCurrentItem($changedItem);

    return this.$currentItem;
};

ImageCollection.prototype.addItem = function(imageLink) {
    this.collectionItems.push(imageLink);
    this.$imageCollectionObject.append('<div class="row">' +
            '<div class="col-xs-2">' +
            '</div>' +
            '<div class="col-xs-8">' +
                '<img src="' + imageLink + '" width="100%" height="100%"' +
                    'class="collection-item" />' +
            '</div>' +
            '<div class="col-xs-2">' +
            '</div>' +
        '</div>' +
        '<br>');
};

ImageCollection.prototype.setCurrentItem = function($item) {
     // If it is null, then the user clicks an element for the first time.
     if(this.$currentItem !== null) {
        // First, deselect the current selected item.
        this.$currentItem.closest("div.col-xs-8").css("background-color",
            this.bgColorNormal);
     }
    // Then mark the new one as selected.
    this.$currentItem = $item;
    this.$currentItem.closest("div.col-xs-8").css("background-color",
        this.bgColorSelect);

};

ImageCollection.prototype.removeItem = function($item) {
    // First remove that value from the internal list.
    _.without(this.collectionItems, $item.attr('src'));
    // Now remove it from the page.
    $item.closest("div.row").remove();
};

ImageCollection.prototype.generateHTML = function() {
    for(var i = 0; i < this.collectionItems.length; i++) {
        this.$imageCollectionObject.append('<div class="row">' +
                '<div class="col-xs-2">' +
                '</div>' +
                '<div class="col-xs-8">' +
                    '<img src="' + this.collectionItems[i] +
                        '" width="100% " height="100%"' +
                     ' class="collection-item" />' +
                '</div>' +
                '<div class="col-xs-2">' +
                '</div>' +
            '</div>' +
            '<br>');
    }
};
