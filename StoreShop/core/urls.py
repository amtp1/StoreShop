from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import *

urlpatterns = [
    path("", Web.index, name="index"),
    path("cart", Web.cart, name="cart"),
    path("auth", Web.auth, name="auth"),
    path("profile", Web.profile, name="profile"),
    path("logout", Web._logout, name="logout"),
    path("my_orders", Web.my_orders, name="my_orders"),
    path("<str:good_type>", Web.goods, name="goods"),
    path("add_good_to_cart/", Web.add_good_to_cart, name="add_good_to_cart"),
    path("clearance_of_good/<int:order_id>", Web.clearance_of_good, name="clearance_of_good"),

    path("remove_order_from_cart/", Web.remove_order_from_cart, name="remove_order_from_cart"),
    path("remove_all_orders_from_cart/", Web.remove_all_orders_from_cart, name="remove_all_orders_from_cart")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#handler500 = "core.views.handler500"