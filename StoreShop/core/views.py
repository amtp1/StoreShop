import hashlib
from datetime import datetime as dt
from json import dumps, loads
from time import sleep

from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth import login, logout

from core.models import *

class Web:
    def index(request):
        if "search_good" in request.POST:
            good_title = request.POST["search_good"]
        return render(request, "index.html")

    def signin(request):
        message: str = "" # Notify message
        
        if request.POST:
            # Received user data
            email = request.POST["email"]
            password = request.POST["password"]

            hash_password: str = hashlib.md5(password.encode("utf-8")).hexdigest() # Convert password to md5 hash.
            user = User.objects.filter(email=email, password=hash_password) # Create user object from db.
            if user.exists():
                user = user.get() # Get user object from db.
                user.last_login = dt.now() # Update datetime in last_login.
                user.save() # Save changes.
                login(request, user) # Auth user in the system.
                return redirect("profile") # Redirect to 'profile' page.
            else:
                message = "Пользователь не существует" # Set message.
        return render(request, "auth/signin.html", dict(message=message))

    def signup(request):
        message: str = "" # Notify message

        if request.POST:
            # Received user data
            email = request.POST["email"]
            username = request.POST["username"]
            password = request.POST["password"]

            if not email or not username or not password:
                message = "Нужно заполнить все данные"
            elif len(password) < 6:
                message = "Короткий пароль"
            else:
                user = User.objects.filter(email=request.POST["email"])
                if not user.exists():
                    hash_password: str = hashlib.md5(password.encode("utf-8")).hexdigest() # Convert password to md5 hash
                    user = User.objects.create(
                        email=email, username=username, password=hash_password,
                    )
                    login(request, user) # Auth user in the system.
                    return redirect("profile") # Redirect to 'profile' page.
        return render(request, "auth/signup.html", dict(message=message))

    def profile(request):
        if not request.user.is_authenticated:
            return redirect("signin")
        else:
            user_id = request.session["_auth_user_id"] # Get user id.
            user = User.objects.get(pk=user_id)
            customer = Customers.objects.filter(user=user_id)
            if not customer.exists():
                Customers.objects.create(user=User.objects.get(pk=user_id), phone="", address="")
            else:
                customer = customer.get()
            orders = Orders.objects.filter(customer=customer).all()
            data: dict = dict(user=user, orders=orders)
            return render(request, "profile.html", data)

    def my_orders(request):
        user_id = request.session["_auth_user_id"] # Get user id.
        customer = Customers.objects.filter(user=user_id).get()
        """if not customer.exists():
            Customer.objects.create(user=User.objects.get(pk=user_id), phone="", address="")
        else:
            customer = customer.get()"""
        orders = Orders.objects.filter(customer=customer).all()
        return render(request, "my_orders.html", dict(orders=orders))

    def cart(request):
        if not request.user.is_authenticated:
            return redirect("auth")

        end_price = 0
        items = request.session.get("items")
        if items:
            items = [Goods.objects.filter(id=k).get() for k in items]
            end_price = sum([p.price for p in items])
        return render(request, "cart.html", dict(items=items, end_price=int(end_price)))

    def add_good_to_cart(request):
        if request.user.is_authenticated:
            item_id = request.POST["item_id"]
            items = request.session.get("items")
            if not items:
                itemsArr = []
                itemsArr.append(item_id)
                request.session["items"] = itemsArr
            else:
                if not item_id in items:
                    items.append(item_id)
                    request.session["items"] = items
            return HttpResponse(dumps(True), content_type="application/json")
        else:
            return HttpResponse(dumps(False), content_type="application/json")

    def goods(request, good_type):
        if good_type == "mans":
            goods = Goods.objects.filter(category_id=1).all()
        elif good_type == "womans":
            goods = Goods.objects.filter(category_id=2).all()
        elif good_type == "kids":
            goods = Goods.objects.filter(category_id=3).all()
        else:
            goods = None
        return render(request, "goods.html", dict(goods=goods))

    def remove_order_from_cart(request):
        if request.user.is_authenticated:
            request.session["items"].remove(str(request.POST["item_id"]))
            request.session["items"] = request.session["items"]
            return HttpResponse(dumps(True), content_type="application/json")

    def clearance_of_good(request, order_id):
        good = Goods.objects.filter(id=order_id).get()
        response = render(request, "clearance_of_good.html", dict(good=good))
        response.set_cookie("order_id", good.pk)
        return response

    def clearance_from_cart(request):
        return render(request, "clearance_from_cart.html")

    def remove_all_orders_from_cart(request):
        if request.user.is_authenticated:
            request.session["items"] = None
            return HttpResponse(dumps(True), content_type="application/json")

    def cart_decrease_value(request):
        if request.user.is_authenticated:
            return HttpResponse(dumps(True), content_type="application/json")

    def cart_increase_value(request):
        if request.user.is_authenticated:
            return HttpResponse(dumps(True), content_type="application/json")

    def process_payment(request):
        try:
            user_id = request.session["_auth_user_id"]
        except KeyError:
            user_id = None
        if user_id:
            customer = Customers.objects.get(user_id=request.session["_auth_user_id"])
        else:
            customer = None
        payment_response = loads(request.POST["response"])
        good = Goods.objects.get(pk=payment_response.get("order_id"))
        Orders.objects.create(
            good=good, last_name=payment_response.get("floatingLastNameInput"), first_name=payment_response.get("floatingFirstNameInput"),
            phone=payment_response.get("floatingPhoneInput"), home_address=payment_response.get("floatingAddressHomeInput"),
            email=payment_response.get("floatingeEmailInput"), is_cash=payment_response.get("is_cash"),
            deli_method=payment_response.get("Deli"), customer=customer
        )
        sleep(2)
        return HttpResponse(dumps(True), content_type="application/json")

    def order_more_info(request):
        order = Orders.objects.get(id=request.POST["order_id"])
        content: dict = dict(status=True, order_data=order.as_json(good=True))
        return HttpResponse(dumps(content), content_type="application/json")

    def search_good(request):
        good = Goods.objects.filter(title__contains=request.POST["good_title"]).all()[0]
        good_obj = dict(id=good.pk, title=good.title, image_url=good.image.url, price=int(good.price), qty=good.qty)
        return HttpResponse(dumps(good_obj), content_type="application/json")

    def _logout(request):
        logout(request)
        return redirect("index") # Redirect to 'index' page.

def handler505(request):
    pass