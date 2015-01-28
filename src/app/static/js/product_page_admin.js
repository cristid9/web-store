// This file handles events that only admins can trigger on the page of a product
$(document).ready(function() {
    $("#delete_product").click(function() {
        $("#delete_product_dialog").modal("show");
    });

    $("#yes_delete").click(function() {
        $.post("/delete_product", {
            productId: productData.id
        }).done(function(data) {
            if(data.status !== "ok") {
                alert("Ceva n-a mers bine");
            }
        });

        $("#delete_product").modal("hide");
        // Change this to a more dinamically approach.
        location.replace(productData.redirectPage);
    });

    $("#no_delete").click(function() {
        $("#delete_product_dialog").modal("hide");
    });

});