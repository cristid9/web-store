/**
 * @brief Class used to represent the main image(the selected one)
 *        in the image gallery.
 *
 * @param placeholder A link to a placeholder image, it will be
 *        used if there is not any image available.
 * @param $mainImageObject A jQuery object representing the div
 *        where the main image is located.
 */
function MainImage(placeholder,
                   $mainImageObject) {

    this.$currentMainItem = null;
    this.placeholder = placeholder;
    // true when the default image is set.
    this.isDefault = false;
    this.$mainImageObject = $mainImageObject;
}

/**
 * @brief Use this method to set the current image in image
 *        gallery.
 *
 * @param $item A jQuery object representing the new main
 *        object.
 *
 * @return void It doesn't return anything.
 */
MainImage.prototype.setCurrentMainItem = function($item) {
    this.$currentMainItem = $item;
    this.$mainImageObject.html('<img src="' + $item.attr('src') +
        '" width="100%" height="100%" />');
    this.isDefault = false;
};

/**
 * @brief Use this method to set the main item to the
 *        default one.
 *
 * @return void It doesn't return anything.
 */
MainImage.prototype.setDefaultMainItem = function() {
    this.$mainImageObject.html('<img src="' + this.placeholder +
        '" width="100%" height="100%" />');
    this.isDefault = true;
};

/**
 * @brief Use this method to see if the default image is used.
 *
 * @return Boolean true if the default image is used or false
 *         if not.
 */
MainImage.prototype.isDefaultItem = function() {
    if(this.isDefault) {
        return true;
    }
    return false;
};

function ImageCollection(collectionItems,
                         imageCollectionObject) {

    this.$imageCollectionObject = imageCollectionObject;
    this.$currentItem = null;
    this.collectionItems = collectionItems;
    this.bgColorSelect = "blue";
    this.bgColorNormal = "white";
}

/**
 * @brief Use this method to change the image of the current selected
 *        item.
 *
 * @param link The link to the new image.
 *
 * @return jQuery the new current element.
 */
ImageCollection.prototype.changeCurrentItem = function(link) {
    var $changedItemDiv = $('<div class="row">').html( '<div class="col-xs-2">' +
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
    this.$currentItem.closest("div.row").after($changedItemDiv);
    // Now remove the old one.
    // In order to remove the element we have to remove all
    // the divs in which it resides.
    this.$currentItem.closest("div.row").remove();

    // Now update the image gallery.
    // In order to remain consistent with the API created so far,
    // the returned element should also be the image.
    this.$currentItem = $changedItemDiv.find('.collection-item');
    // We need its index in order to set the current item.
    var currentItemIndex = $changedItemDiv.index();
    this.setCurrentItem(currentItemIndex);

    return this.$currentItem;
};

/**
 * @brief Use this method to add a new element to the image
 *        collection.
 *
 * @param imageLink A String containing the de url of the new
 *        image.
 *
 * @return jQuery The newly added item.
 */
ImageCollection.prototype.addItem = function(imageLink) {
    this.collectionItems.push(imageLink);
    var $newItem = $('<div class="row">' +
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

    this.$imageCollectionObject.append($newItem);
    return $newItem.find(".collection-item");
};

/**
 * @brief Use this method to set the current highlighted element
 *        in the `imageCollection` div.
 *
 * @param index The index of the element that will be added.
 *
 * @return jQuery The newly added element.
 */
ImageCollection.prototype.setCurrentItem = function(index) {
    // First select the element based on its index.
    var $newSelectedElement = this.$imageCollectionObject
        .children()
        .eq(index)
        .find('.collection-item');

     // If it is null, then the user clicks an element for the first time.
    if(this.$currentItem !== null) {
        // First, deselect the current selected item.
        this.$currentItem.closest("div.col-xs-8").css("background-color",
            this.bgColorNormal);
    }
    // Then mark the new one as selected.
    this.$currentItem = $newSelectedElement;
    this.$currentItem.closest("div.col-xs-8").css("background-color",
        this.bgColorSelect);

    return this.$currentItem;
};

/**
 * @brief Use this method to remove an element by its index.
 *
 * @param index The index of the element that will be removed.
 *
 * @return jQuery The next current element or null if there is no
 *         next element.
 */
ImageCollection.prototype.removeItem = function(index) {
    // It would be better to pass the the element directly
    // but we keep the interface that uses indexes just to
    // keep uniform interface.
    $itemDiv = this.$imageCollectionObject
        .children()
        .eq(index);

    // We, also, need to delete the <br> after the div.
    $itemBr = this.$imageCollectionObject
        .children()
        .eq(index + 1);
    $item = $itemDiv.find(".collection-item");

    // Decide which will be the next element after deleting the
    // current one.
    if($itemBr.next().length) {
        console.log("br");
        this.$currentItem = $itemBr
            .next()
            .find(".collection-item");
    } else if($itemDiv.prev().prev().length) {
        console.log("div");
        this.$currentItem = $itemDiv
            .prev()
            .prev()
            .find(".collection-item");
    } else {
        this.$currentItem = null;
    }

    // First remove that value from the internal list.
    _.without(this.collectionItems, $item.attr('src'));
    // Now remove it from the page.
    $itemDiv.remove();
    $itemBr.remove();

    return this.$currentItem;
};

/**
 * @brief Use this method to get the index of the current
 *        selected item of the image collection.
 *
 * @return Integer The current selected item.
 */
ImageCollection.prototype.getCurrentSelectedItemIndex = function() {
    var index = this.$currentItem
        .closest("div.row")
        .index();

    return index;
};

/**
 * @brief Use this method to generate the html code of the
 *        image collection.
 *
 * @return It doesn't return anything.
 */
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

/**
 * @brief This method will generate the json representation of
 *        the collection items list, which holds all the links
 *        of the images added here.
 *
 * @return String A json containing all the image links.
 */
ImageCollection.prototype.getJSONString = function() {
    return JSON.stringify(this.collectionItems);
}
