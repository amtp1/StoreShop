from datetime import datetime as dt
from tabnanny import verbose

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django .urls import reverse
from PIL import Image

User=get_user_model()

choices = [
    ('1', "Отменен"),
    ('2', "В процессе"),
    ('3', "Завершен"),
]


class Staffs(models.Model):
    staff = models.OneToOneField(User, on_delete=models.CASCADE)
    is_manager = models.BooleanField(null=True, verbose_name = "Менеджер по заказам")
    is_booker = models.BooleanField(null=True, verbose_name="Бухгалтер")
    is_merchandiser = models.BooleanField(null=True, verbose_name="Товаровед")

    def __repr__(self):
        return self.staff

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"


class Customers(models.Model):
    user=models.ForeignKey(User, verbose_name='Заказчик', on_delete=models.CASCADE)
    phone=models.CharField(max_length=20, verbose_name='Номер телефона')
    address=models.CharField(max_length=255, verbose_name='Адрес')

    def __str__ (self):
        return "Customer: {} {}".format(self.user.pk, self.user.username)

    class Meta:
        verbose_name = "Заказчик"
        verbose_name_plural = "Заказчики"


class Categories(models.Model):
    name=models.CharField(max_length=255, verbose_name='Имя категории')

    def __str__(self):
        return self.name

    class Meta: 
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Goods(models.Model):
    Min_R = (400,400)
    Max_R = (800,800)

    category = models.ForeignKey(Categories, verbose_name='Категория', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Название')
    image = models.ImageField(upload_to="images/", verbose_name='Картинка')
    description = models.TextField(verbose_name='Описание', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')
    qty = models.IntegerField(default=0, verbose_name="Количество")

    def __str__(self):
        return self.title

    def as_json(self):
        return dict(
            category=self.category.name, title=self.title,
            image=self.image.url, description=self.description,
            price=float(self.price), qty=self.qty
        )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class Orders(models.Model):
    good = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name="Товар")
    last_name = models.CharField(default=None, max_length=255, verbose_name="Фамилия")
    first_name = models.CharField(default=None, max_length=255, verbose_name="Имя")
    phone = models.CharField(default=None, max_length=128, verbose_name="Номер телефона")
    home_address = models.CharField(default=None, max_length=255, verbose_name="Домашний адрес")
    email = models.CharField(default=None, max_length=255, verbose_name="Электронная почта")
    is_cash = models.BooleanField(default=False, verbose_name="Наличные")
    deli_method = models.IntegerField(default=0, verbose_name="Метод доставки")
    place_datetime = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    complete_datetime = models.DateTimeField(auto_now_add=True, verbose_name="Дата завершения")
    qty = models.IntegerField(default=1, verbose_name="Количество")
    customer = models.ForeignKey(Customers, null=True, on_delete=models.CASCADE, verbose_name="Заказчик")
    status = models.CharField(max_length=128, choices=choices, default='2', verbose_name="Статус")

    def status_value(self):
        return eval(self.status)[0]

    def as_json(self, good: bool = False):
        good_data = None
        if good:
            good_data = self.good.as_json()

        return dict(good_data=good_data, last_name=self.last_name,
            first_name=self.first_name, phone=self.phone,
            home_address=self.home_address, email=self.email,
            is_cash=self.is_cash, deli_method=self.deli_method,
            qty=self.qty, status=self.status, place_datetime=self.place_datetime.strftime("%Y/%m/%d %H:%M:%S")
        )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


"""
class Supplies(models.Model):
    supplier = models.ForeignKey('Suppliers', on_delete=models.CASCADE, verbose_name="Supplier")
    datetime = models.DateTimeField(auto_now_add=True, verbose_name="Datetime")


class Suppliers(models.Model):
    name_supplier = models.CharField(max_length=255, verbose_name="Name supplier")
    person = models.CharField(max_length=128, verbose_name="Person")
    phone = models.IntegerField(verbose_name="Phone")
    address = models.CharField(max_length=255, verbose_name="Address")


class CartProduct(models.Model):
    user = models.ForeignKey(Customers, verbose_name='Customer', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Cart', on_delete=models.CASCADE, related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')

    def __str__(self):
        return "Product: {}".format(self.product.title)


class Cart(models.Model):
    owner = models.ForeignKey(Customers, verbose_name='Customer', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Sum price')

    def __str__(self):
        return str(self.id)
"""