function redirect_to_main_page() {
    window.location.replace("index");
};

function add_to_cart(id){
    var data = new FormData(); // Init new FormData object.
    data.append("item_id", id); // Add mail address in the FormData object.
    fetch("add_good_to_cart/", {
        method: "POST",
        body: data,
        contentType: 'application/json',
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": $.cookie("csrftoken")
        },
    }).then(function(response){
        response.json().then(
            function(data){
                if (data==true){
                    //redirect_to_main_page(); // Redirect on the main page.
                    var cart_btn = document.getElementsByName(`cart_btn_${id}`)[0];
                    cart_btn.innerHTML = '<i class="bi bi-check-lg"></i>';
                }else{
                    alert("User is not authorized!");
                }
            }
        );
    });
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
            "X-CSRFToken": $.cookie("csrftoken")
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
            "X-CSRFToken": $.cookie("csrftoken")
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
            "X-CSRFToken": $.cookie("csrftoken")
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

function go_to_clearance_form(id){

}

function cart_decrease_value(id){
    var data = new FormData(); // Init new FormData object.
    var cart_item = document.getElementById(`value_${id}`);
    var deinc_item_value = parseInt(cart_item.value) - 1;
    if (deinc_item_value < 1){
        alert("Значение не может быть меньше 1.");
    }
    else{
        var to_pay = document.getElementById("to_pay");
        var item_price = document.getElementById(`item_price_${id}`);
        cart_item.value = deinc_item_value;
        to_pay.innerText = `${parseFloat(to_pay.innerText) - parseFloat(item_price.innerText)}₽`;
    }
}

function cart_increase_value(id){
    var data = new FormData(); // Init new FormData object.
    var cart_item = document.getElementById(`value_${id}`);
    var available_qty = document.getElementById(`available_qty_${id}`);
    var inc_item_value = parseInt(cart_item.value) + 1;
    if (parseInt(available_qty.innerText) < inc_item_value){
        alert("Количество товара превышает доступное количество");
    }else{
        var to_pay = document.getElementById("to_pay");
        var item_price = document.getElementById(`item_price_${id}`);
        cart_item.value = inc_item_value;
        to_pay.innerText = `${parseFloat(to_pay.innerText) + parseFloat(item_price.innerText)}₽`;
    }
}

function payment_process(){
    const under_data = new Object();
    const owner_data = new FormData();
    let floatingLastNameInput = document.getElementById("floatingLastNameInput")
    let floatingFirstNameInput = document.getElementById("floatingFirstNameInput");
    let floatingPhoneInput = document.getElementById("floatingPhoneInput");
    let floatingAddressHomeInput = document.getElementById("floatingAddressHomeInput");
    let floatingeEmailInput = document.getElementById("floatingeEmailInput");
    let flexRadioDeli1 = document.getElementById("flexRadioDeli1");
    let flexRadioDeli2 = document.getElementById("flexRadioDeli2");
    let floatingPaymentMethodSelect = document.getElementById("floatingPaymentMethodSelect");

    if (!floatingLastNameInput.value){
        floatingLastNameInput.className = "form-control is-invalid";
    }else if(floatingLastNameInput.value){
        floatingLastNameInput.className = "form-control is-valid";
        under_data["floatingLastNameInput"] = floatingLastNameInput.value;
    }

    if(!floatingFirstNameInput.value){
        floatingFirstNameInput.className = "form-control is-invalid";
    }else if(floatingFirstNameInput.value){
        floatingFirstNameInput.className = "form-control is-valid";
        under_data["floatingFirstNameInput"] = floatingFirstNameInput.value;
    }

    if(!floatingPhoneInput.value){
        floatingPhoneInput.className = "form-control is-invalid";
    }else if(floatingPhoneInput.value){
        floatingPhoneInput.className = "form-control is-valid";
        under_data["floatingPhoneInput"] = floatingPhoneInput.value;
    }

    if(!floatingAddressHomeInput.value){
        floatingAddressHomeInput.className = "form-control is-invalid";
    }else if(floatingAddressHomeInput.value){
        floatingAddressHomeInput.className = "form-control is-valid";
        under_data["floatingAddressHomeInput"] = floatingAddressHomeInput.value;
    }

    if(!floatingeEmailInput.value){
        floatingeEmailInput.className = "form-control is-invalid";
    }else if(floatingeEmailInput.value){
        floatingeEmailInput.className = "form-control is-valid";
        under_data["floatingeEmailInput"] = floatingeEmailInput.value;
    }

    if (!flexRadioDeli1.checked && !flexRadioDeli2.checked){
        flexRadioDeli1.className = "form-check-input is-invalid";
        flexRadioDeli2.className = "form-check-input is-invalid";
    }else{
        flexRadioDeli1.className = "form-check-input is-valid";
        flexRadioDeli2.className = "form-check-input is-valid";
        if(flexRadioDeli1.checked){
            under_data["Deli"] = flexRadioDeli1.value;
        }else{
            under_data["Deli"] = flexRadioDeli2.value;
        }
    };

    under_data["is_cash"] = floatingPaymentMethodSelect.value;
    under_data["order_id"] = $.cookie("order_id");
    owner_data.append("response", JSON.stringify(under_data));

    if (Object.keys(under_data).length > 7){
        var payment_spinner_div = document.createElement("div");
        payment_spinner_div.className = "spinner-border text-dark";
        var payment_btn = document.getElementById("payment_btn");
        payment_btn.disabled = true;
        payment_btn.innerHTML = payment_spinner_div.outerHTML;

        fetch("process_payment/", {
            method: "POST",
            body: owner_data,
            contentType: 'application/json',
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": $.cookie("csrftoken")
                },
            }).then(function(response){
            response.json().then(
                function(data){
                    if (data==true){
                        window.location.replace("/"); // Redirect on the main page.
                    }
                }
            );
        });
    };
}

function more_order_info(order_id){
    var data = new FormData();
    data.append("order_id", order_id);
    fetch("order_more_info/", {
        method: "POST",
        body: data,
        contentType: 'application/json',
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": $.cookie("csrftoken")
            },
        }).then(function(response){
        response.json().then(
            function(data){
                if (data["status"]==true){
                    let payment_method = null;
                    if (data["order_data"]["is_cash"]){
                        payment_method = "Наличными";
                    }else{
                        payment_method = "Банковской картой";
                    }
                    var modal = document.createElement("div");
                    modal.id = `OrderModal_${order_id}`;
                    modal.className = "modal";
                    modal.tabIndex = "-1";
                    modal.innerHTML = `
                        ${'<div class="modal-dialog">'}
                          ${'<div class="modal-content">'}
                            ${'<div class="modal-header">'}
                              ${`<h3 class="modal-title">Order #${order_id}</h3>`}
                              ${'<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>'}
                            ${'</div>'}
                            ${'<div class="modal-body">'}
                              ${'<p><h4 class="text-center">О товаре</h4></p>'}
                              ${'<div class="row">'}
                                ${'<div class="col">'}
                                  ${`<img src="${data["order_data"]["good_data"]["image"]}" class="img-thumbnail w-100 h-100" alt="...">`}
                                ${'</div>'}
                                ${'<div class="col">'}
                                  ${`<h6>${data["order_data"]["good_data"]["title"]}</h6>`}
                                  ${`<h6><small class="text-muted">Цена:</small> ${data["order_data"]["good_data"]["price"]}₽</h6>`}
                                ${'</div>'}
                                ${'<p><h4 class="text-center">О заказе</h4></p>'}
                                  ${'<table class="table pre-scrollable">'}
                                    ${'<table class="table">'}
                                     ${'<thead class="table-dark">'}
                                       ${'<tr>'}
                                         ${'<th scope="col">Пункты</th>'}
                                         ${'<th scope="col">Данные</th>'}
                                       ${'</tr>'}
                                     ${'</thead>'}
                                     ${'<tbody>'}
                                       ${'<tr>'}
                                         ${`<td><b>ID</b></td>`}
                                         ${`<td>${order_id}</td>`}
                                       ${'</tr>'}
                                       ${'<tr>'}
                                         ${`<td><b>Фамилия</b></td>`}
                                         ${`<td>${data["order_data"]["last_name"]}</td>`}
                                       ${'</tr>'}
                                       ${'<tr>'}
                                         ${`<td><b>Имя</b></td>`}
                                         ${`<td>${data["order_data"]["first_name"]}</td>`}
                                       ${'</tr>'}
                                       ${'<tr>'}
                                         ${`<td><b>Метод оплаты</b></td>`}
                                         ${`<td>${payment_method}</td>`}
                                       ${'</tr>'}
                                       ${'<tr>'}
                                         ${`<td><b>Адрес доставки</b></td>`}
                                         ${`<td>${data["order_data"]["home_address"]}</td>`}
                                       ${'</tr>'}
                                       ${'<tr>'}
                                         ${`<td><b>Количество</b></td>`}
                                         ${`<td>${data["order_data"]["qty"]}</td>`}
                                       ${'</tr>'}
                                       ${'<tr>'}
                                         ${`<td><b>Дата и время заказа</b></td>`}
                                         ${`<td>${data["order_data"]["place_datetime"]} UTC</td>`}
                                       ${'</tr>'}
                                     ${'</tbody>'}
                                    ${'</table>'}
                                ${'</div>'}
                              ${'</div>'}
                            ${'</div>'}
                          ${'</div>'}
                        ${'</div>'}`;
                    var body = document.body;
                    body.append(modal);
                    $(`#OrderModal_${order_id}`).modal('show');
                }
            }
        );
    });
}

function search_good(){
    var search_input = document.getElementById("search_good");
    var data = new FormData();
    data.append("good_title", search_input.value);

    fetch("search_good/", {
        method: "POST",
        body: data,
        contentType: 'application/json',
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": $.cookie("csrftoken")
            },
        }).then(function(response){
            response.json().then(
                function(data){
                    var modal = document.createElement("div");
                    modal.id = `OrderModal_${data["id"]}`;
                    modal.className = "modal";
                    modal.tabIndex = "-1";
                    modal.innerHTML = `
                        ${'<div class="modal-dialog">'}
                          ${'<div class="modal-content">'}
                            ${'<div class="modal-header">'}
                              ${`<h3 class="modal-title">Результаты поиска</h3>`}
                              ${'<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>'}
                            ${'</div>'}
                            ${'<div class="modal-body">'}
                              ${'<p><h4 class="text-center">О товаре</h4></p>'}
                              ${'<div class="row">'}
                                ${'<div class="col">'}
                                  ${`<img src="${data["image_url"]}" class="img-thumbnail w-100 h-100" alt="...">`}
                                ${'</div>'}
                                ${'<div class="col">'}
                                  ${`<h6>${data["title"]}</h6>`}
                                  ${`<h6><small class="text-muted">Цена:</small> ${data["price"]}₽</h6>`}
                                ${'</div>'}
                                ${'<p>'}
                                ${'<div class="btn-group">'}
                                  ${`<button id="${data["id"]}"  name="cart_btn_${data["id"]}" type="button" class="btn btn-sm btn-outline-secondary w-50" onclick="add_to_cart(this.id)">В корзину</button>`}
                                ${'</div>'}
                                ${'</p>'}
                              ${'</div>'}
                            ${'</div>'}
                          ${'</div>'}
                        ${'</div>'}`;
                    var body = document.body;
                    body.append(modal);
                    $(`#OrderModal_${data["id"]}`).modal('show');
                }
            )
    });
}

$(document).ready(function () {
    $('#dtHorizontalExample').DataTable({
      "scrollX": true
    });
    $('.dataTables_length').addClass('bs-select');
});