// add to cart functionality 


$(document).ready(function (){
    $(".add-to-cart-btn").on("click",function(){

        let this_val = $(this)
        let index = this_val.attr("data-index")

        let quantity = $(".product-quantity-" + index).val()
        let product_title = $(".product-title-" + index).val()
        let product_id = $(".product-id-" + index).val()
        let product_price = $(".current-product-price-" + index).text()
        let product_pid = $(".product-pid-" + index).val()
        let product_image = $(".product-image-" + index).val()

        console.log("Quantity :", quantity);
        console.log("Title :", product_title);
        console.log("Id :", product_id);
        console.log("Price :", product_price);
        console.log("P-ID :", product_pid);
        console.log("Image :", product_image);
        console.log("Current Element :", this_val);

        $.ajax({
            url: '/add-to-cart',
            data:{
                'id' : product_id,
                'pid' : product_pid,
                'image': product_image,
                'qty' : quantity,
                'title':product_title,
                "price":product_price,
            },
            dataType: 'json',
            beforeSend: function(){
                console.log("Adding Product to Cart...");
            },
            success: function(response){
                this_val.html("👍")
                console.log("Product Added to Cart");
                $(".cart-items-count").text(response.totalcartitems)
            }
        })
    })


    $(document).on("click",'.delete-product',function(){

        let product_id = $(this).attr("data-product")
        let this_val = $(this)
        console.log("Id :", product_id);

        $.ajax({
            url: "/delete-from-cart",
            data:{
                "id" : product_id,
            },
            dataType: "json",
            beforeSend: function(){
                this_val.hide()
            },
            success: function(response){
                this_val.show()
                $(".cart-items-count").text(response.totalcartitems)
                $("#cart-list").html(response.data)
            }
        })

    })

    $(document).on("click",'.update-product',function(){

        let product_id = $(this).attr("data-product")
        let this_val = $(this)
        let product_quantity = $(".product-quantity-" +product_id).val()

        console.log("Id :", product_id);
        console.log("Quantity :", product_quantity);

        $.ajax({
            url: "/update-cart",
            data:{
                "id" : product_id,
                "qty" : product_quantity,
            },
            dataType: "json",
            beforeSend: function(){
                this_val.hide()
            },
            success: function(response){
                this_val.show()
                $(".cart-items-count").text(response.totalcartitems)
                $("#cart-list").html(response.data)
            }
        })

    })

    $(document).on("click", ".add-to-wishlist", function(){
        let product_id = $(this).attr("data-product-item")
        let this_val = $(this)

        console.log("Product Id :", product_id);

        $.ajax({
            url: "/add-to-wishlist",
            data:{
                "id" : product_id
            },
            dataType: "json",
            beforeSend: function(){
                console.log("Adding Product to Wishlist...");
            },
            success: function(response){
                this_val.html("❤️")
                if (response.bool === true){
                console.log("Added To Wishlist...")
                }
            }

        })
    })

    $(document).on("click",'.delete-wishlist-product',function(){

        let wishlist_id = $(this).attr("data-wishlist-product")
        let this_val = $(this)

        console.log("Wishlist Id :", wishlist_id);

        $.ajax({
            url: "/remove-from-wishlist",
            data:{
                "id" : wishlist_id,
            },
            dataType: "json",
            beforeSend: function(){
                console.log("Removing Product to Wishlist...");
            },
            success: function(response){
                $("#wishlist-list").html(response.data)
            }
        })

    })

})


