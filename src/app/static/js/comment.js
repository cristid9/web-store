"use strict";
/**
 * @brief This class is used to represent and comment.
 *
 * @param poster The username of the user who posts the comment.
 * @param content The content of the message that the user has
 *        poster.
 * @param $container A jQuery object representing the container
 *        div for comments.
 * @param productId The id of the product whose page these
 *        comments belong to.
 *
 */
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

/**
 * @brief Use this method to check if an comment object is
 *        valid. At this moment, there is only one criterion
 *        for validity, it shouldn't be empty.
 *
 * @return bool It returns `true` if the comment is valid or
 *         `false` otherwise.
 */
Comment.prototype.isValid = function() {
    if(this.content.length < this.minLength) {
        // I will throw some exception on the future.
        return false;
    }
    return true;
};

/**
 * @brief Helper method used to make the logic simpler.
 *        This method is used to send AJAX request to the
 *        server with the comment details.
 *
 * @return void It doesn't return anything.
 */
Comment.prototype.__sendToServer = function() {
    $.post(this.route, {
        poster: this.poster,
        content: this.content,
        productId: this.productId
    });
};

/**
 * @brief Use this method to publish a comment. It will
 *        call `__sendToServer` and will reload the page.
 *
 * @return void It doesn't return anything.
 */
Comment.prototype.publish = function() {
    this.__sendToServer();
    location.reload();
};