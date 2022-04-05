from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import *

urlpatterns = [
    path("", Web.index, name="index"),
    path("cart", Web.cart, name="cart"),
    path("signin", Web.signin, name="signin"),
    path("signup", Web.signup, name="signup"),
    path("profile", Web.profile, name="profile"),
    path("logout", Web._logout, name="logout"),
    path("my_orders", Web.my_orders, name="my_orders"),
    path("<str:good_type>", Web.goods, name="goods"),
    path("add_good_to_cart/", Web.add_good_to_cart, name="add_good_to_cart"),
    path("clearance_of_good/<int:order_id>", Web.clearance_of_good, name="clearance_of_good"),
    path("clearance_of_good/process_payment/", Web.process_payment, name="process_payment"),
    path("clearance_from_cart", Web.clearance_from_cart, name="clearance_from_cart"),
    path("search_good/", Web.search_good, name="search_good"),

    path("remove_order_from_cart/", Web.remove_order_from_cart, name="remove_order_from_cart"),
    path("remove_all_orders_from_cart/", Web.remove_all_orders_from_cart, name="remove_all_orders_from_cart"),
    path("cart_decrease_value/", Web.cart_decrease_value, name="cart_decrease_value"),
    path("cart_increase_value/", Web.cart_increase_value, name="cart_increase_value"),
    path("order_more_info/", Web.order_more_info, name="order_more_info")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#handler500 = "core.views.handler500"