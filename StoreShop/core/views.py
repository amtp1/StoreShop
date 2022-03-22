import hashlib
from datetime import datetime as dt
from json import dumps

from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth import login, logout

from .models import *

class Web:
    def index(request):
        return render(request, "index.html")

    def auth(request):
        if not request.user.is_authenticated:
            message: str = ""
            if request.POST:
                post = request.POST
                username = post.get("username")
                password = post.get("password")

                hash_password: str = hashlib.md5(password.encode("utf-8")).hexdigest() # Convert password to md5 hash.

                if not username or not password:
                    message = "Поля не должны оставаться пустыми"
                else:
                    if "register-button" in request.POST:
                        user = User.objects.filter(username=username).exists() # Check user.
                        if not user:
                            user = User.objects.create(username=username, password=hash_password, is_staff=True) # Create new user.
                            login(request, user) # Auth user in the system.
                            return redirect("profile") # Redirect to 'profile' page.
                        else:
                            message: str = "Пользователь с таким юзернейм существует!" # Set message.
                            #return render(request, "login.html", dict(message=message)) # Render login page with data.
                    elif "login-button" in request.POST:
                        user = User.objects.filter(username=username, password=hash_password) # Create user object from db.
                        if user.exists():
                            user = user.get() # Get user object from db.
                            user.last_login = dt.now() # Update datetime in last_login.
                            user.save() # Save changes.
                            login(request, user) # Auth user in the system.
                            return redirect("profile") # Redirect to 'profile' page.
                        else:
                            message: str = "Пользователь не существует!" # Set message.
                            #return render(request, "login.html", dict(message=message)) # Render login page with data.

            return render(request, "auth.html", dict(message=message))

    def profile(request):
        if not request.user.is_authenticated:
            return redirect("auth")
        else:
            request.session["add_new_account"] = {"status": False}
            user_id = request.session["_auth_user_id"] # Get user id.
            username: str = User.objects.get(pk=user_id).username # Get username from db by user id.
            date_joined = User.objects.get(pk=user_id).date_joined
            customer = Customers.objects.filter(user=user_id)
            if not customer.exists():
                Customers.objects.create(user=User.objects.get(pk=user_id), phone="", address="")
            else:
                customer = customer.get()
            orders = Orders.objects.filter(customer=customer).all()
            data: dict = dict(username=username, date_joined=date_joined, count_orders=orders)
            return render(request, "profile.html", data)

    def my_orders(request):
        request.session["add_new_account"] = {"status": False}
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
        return render(request, "clearance_of_good.html", dict(good=good))

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
        return redirect("index")

    def _logout(request):
        logout(request)
        return redirect("my_orders") # Redirect to 'index' page.

def handler505(request):
    pass