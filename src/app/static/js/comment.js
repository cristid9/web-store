"use strict";
function Comment(poster,
                 content,
                 $container,
                 productId) {

    this.poster = poster;
    this.content = content;
    this.$container = $container;
    this.minLength = 10;
    // Ajax route to post the message to the server.
    this.route = '/publish_comment';
    // Id of the commented product.
    this.productId = productId;
}

Comment.prototype.isValid = function() {
    if(this.content.length < this.minLength) {
        // I will throw some exception on the future.
        return false;
    }
    return true;
};

Comment.prototype.__sendToServer = function() {
    $.post(this.route, {
        poster: this.poster,
        content: this.content,
        productId: this.productId
    });
};

Comment.prototype.__addToPage = function() {
    this.$container.prepend('<div class="row">' +
            '<strong> ' + this.content + '</strong>' +
        '</div>');
};

Comment.prototype.publish = function() {
    this.__sendToServer();
    this.__addToPage();
};