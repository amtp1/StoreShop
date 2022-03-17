function redirect_to_main_page() {
    window.location.replace("index");
};

function add_to_cart(id){
    //var csrf = document.cookie.match(/csrftoken=([\w-]+)/).toString().split("=")[1];
    var data = new FormData(); // Init new FormData object.
    data.append("item_id", id); // Add mail address in the FormData object.
    fetch("add_good_to_cart/", {
        method: "POST",
        body: data,
        contentType: 'application/json',
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken")
        },
    }).then(function(response){
        response.json().then(
            function(data){
                if (data==true){
                    //redirect_to_main_page(); // Redirect on the main page.
                }else{
                    alert("User is not authorized!");
                }
            }
        );
    });

    /*var cart_btn = document.querySelector("#cart-button");

    var notify_element_1 = document.createElement("span");
    notify_element_1.className = "position-absolute top-0 start-100 translate-middle p-2 bg-danger border border-light rounded-circle";
    var notify_element_2 = document.createElement("span");
    notify_element_2.className = "visually-hidden";
    notify_element_2.innerHTML = "New alerts";
    notify_element_1.append(notify_element_2);
    cart_btn.append(notify_element_1);*/
}

function remove_order_from_cart(id){
    var data = new FormData(); // Init new FormData object.
    data.append("item_id", id); // Add mail address in the FormData object.
    fetch("remove_order_from_cart/", {
        method: "POST",
        body: data,
        contentType: 'application/json',
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken")
        },
    }).then(function(response){
        console.log(response);
        response.json().then(
            function(data){
                if (data==true){
                    window.location.replace("cart"); // Redirect on the main page.
                }
            }
        );
    });
}

function remove_all_orders_from_cart(){
    fetch("remove_all_orders_from_cart/", {
        method: "POST",
        contentType: 'application/json',
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken")
        },
    }).then(function(response){
        console.log(response);
        response.json().then(
            function(data){
                if (data==true){
                    window.location.replace("cart"); // Redirect on the main page.
                }
            }
        );
    });
}

function clearance_of_good(id){
    var data = new FormData(); // Init new FormData object.
    data.append("order_id", id); // Add mail address in the FormData object.
    fetch("clearance_of_good/", {
        method: "POST",
        body: data,
        contentType: 'application/json',
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken")
        },
    }).then(function(response){
        response.json().then(
            function(data){
                if (data==true){
                    window.location.replace("clearance_of_good"); // Redirect on the main page.
                }
            }
        );
    });
}

$(document).ready(function () {
    $('#dtHorizontalExample').DataTable({
      "scrollX": true
    });
    $('.dataTables_length').addClass('bs-select');
  });

/**
 * This is function take cookie from browser.
 * @param {*} name 
 * @returns cookieValue
 */
 function getCookie(name) {
    var cookieValue = null;
    var i = 0;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (i; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}