/**
 * @brief Class used to represent the specification box ui
 *        element.
 *
 * @param $specificationsContainer A jQuery object representing
 *        the div where the specifications are store.
 * @param specifications A dictionary of the form
 *        <spec_name>:<value>.
 */
function SpecificationsBox($specificationsContainer,
                           specifications) {
    this.$specificationsContainer = $specificationsContainer;

    this.specsCounter = this.$specificationsContainer.
        children("div.row").length -1;
    this.specifications = specifications;

    this.specNamePlaceholder = "specification name";
    this.specValuePlaceholder = "specification value";
}
/**
 * @brief Use this method to add a specification to the specifications
 *        container. This method is intended to be used only by the
 *        object's methods. When no arguments are passed to this function
 *        it sets placeholder attribute with the default value for the
 *        form input.
 *
 * @param name The name of the specification.
 * @param value The value of the specification.
 *
 * @return void It doesn't return something.
 */
SpecificationsBox.prototype.appendSpecToContainer = function(name, value) {
    var nameAttribute;
    var valueAttribute;

    if(arguments.length !== 0) {
        // The user wants to add the div with placeholders
        // instead of values.
        nameAttribute = 'value="' + name + '"';
        valueAttribute = 'value="' + value + '"';
    } else {
        nameAttribute = 'placeholder="' + this.specNamePlaceholder + '"';
        valueAttribute = 'placeholder="' + this.specValuePlaceholder + '"';
    }

    this.$specificationsContainer.append('<div class="row">' +
            '<div class="col-xs-4">' +
                '<div class="form-group">' +
                    '<input type="text" class="form-control specification-name"' +
                           nameAttribute + '"/>' +
                '</div>' +
            '</div>' +
            '<div class="col-xs-7">' +
                '<div class="form-group">' +
                    '<input class="form-control specification-value" type="text"' +
                           valueAttribute + '"/>' +
                '</div>' +
            '</div>' +
            '<div class="col-xs-1">' +
                '<button type="button" class="close">' +
                    '<span class="close"> &times; </span>' +
                '</button>' +
            '</div>' +
        '</div>');
}

/**
 * @brief Use this method to generate the initial representation of the
 *        of the specifications box.
 *
 * @return void It doesn't return anything.
 */
SpecificationsBox.prototype.generateHTML = function() {
    for(var key in this.specifications) {
        if(this.specifications.hasOwnProperty(key)) {
            this.appendSpecToContainer(key, this.specifications[key]);
        }
    }
};

/**
 * @brief Use this method to add new blank specification.
 *
 * @return Integer The index of the newly added specification.
 */
SpecificationsBox.prototype.addNewBlankSpecification = function() {
    this.appendSpecToContainer();
    this.specificationsContainer++;

    return this.specificationsContainer;
};

/**
 * @brief Use this method to update the specification property
 *        of the current object with the new specifications that
 *        the user has added.
 *
 * @return void It doesn't return anything.
 */
SpecificationsBox.prototype.collectData = function() {
   var collectedSpecs = {};
   this.$specificationsContainer.children().each(function(index) {
        var specName = $(this).find(".specification-name").val();
        var specVal = $(this).find(".specification-value").val();

        collectedSpecs[specName] = specVal;
   });

   this.specifications = collectedSpecs;
};

/**
 * @brief Use this method to check if the specifications entered
 *        by the user are valid. Empty specifications name, or
 *        empty specifications values are considered invalid.
 *
 * @return Boolean It returns true if the specifications are
 *         valid or false otherwise.
 */
SpecificationsBox.prototype.validate = function() {
    this.collectData();
    for(var name in this.specifications) {
        if(this.specifications.hasOwnProperty(name)) {
            if(name === "" || this.specifications === "") {
                return false;
            }
        }
    }

    return true;
};

/**
 * @brief Use this method to return the JSON string representation of
 *        the specifications dictionary.
 *
 * @return String A JSON string.
 */
SpecificationsBox.prototype.getJSONString = function() {
    this.collectData();
    return JSON.stringify(this.specifications);
};