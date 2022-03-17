import os
import urllib

from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.files import File
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import ValidationError
from django .urls import reverse
from PIL import Image

User=get_user_model()

"""
def get_product_url(obj, viewname):
    ct_model=obj.__class__.__name__
    return reverse(viewname, kwargs={'ct_model': ct_model, 'slug':obj.
    slug})


class LatestProductManager:
    @staticmethod
    def get_products_for_main_page( *args, **kwargs):
        products=[]
        ct_models=ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products=ct_model.model_class().objects.all().order_by('-id')[:5]
            products.extend(model_products)
        return products


class LatesProducts:

    objects=LatestProductManager()
"""

class Staffs(models.Model):
    last_name = models.CharField(max_length=128, verbose_name="Last name")
    first_name = models.CharField(max_length=128, verbose_name="First name")
    position = models.CharField(max_length=128, verbose_name="Position")
    birthday = models.DateField(verbose_name="Birthday")
    address = models.CharField(max_length=255, verbose_name="Address")
    phone = models.IntegerField(verbose_name="Phone")
    note = models.TextField(verbose_name="Note")

    class Meta:
        verbose_name = "Staff"
        verbose_name_plural = "Staffs"


class Categories(models.Model):
    name=models.CharField(max_length=255, verbose_name='Имя категории')
    slug=models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Goods(models.Model):
    Min_R=(400,400)
    Max_R=(800,800)

    category=models.ForeignKey(Categories, verbose_name='Gategory', on_delete=models.CASCADE)
    title=models.CharField(max_length=255, verbose_name='Title')
    slug=models.SlugField(unique=True)
    image=models.ImageField(upload_to="images/", verbose_name='Image')
    description=models.TextField(verbose_name='Description', null=True)
    price=models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Price')

    def __str__(self):
        return self.title

    """
    def save(self, *args, **kwargs):
        img=Image.open(Image)
        print(img)
        img=self.image
        min_height, min_width=self.Min_R
        max_height, max_width=self.Max_R
        if img.height < min_height or img.width < min_width:
            raise ValidationError('Разрешение изоброжение меньше минимального ')
        if img.height > max_height or img.width > max_width:
            raise ValidationError('Разрешение изоброжение больше максимального ')
        super().save(*args,**kwargs)
    """

    """
    def save(self, *args, **kwargs):
        if self.image:
            #result = urllib.urlretrieve(self.image)
            self.image.save(File(open(self.image, 'r')))
            self.save()
            super(Goods, self).save()
    """

    class Meta:
        verbose_name = "Good"
        verbose_name_plural = "Goods"


class Orders(models.Model):
    good = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name="Good")
    staff = models.ForeignKey(Staffs, on_delete=models.CASCADE, verbose_name="Staff")
    place_datetime = models.DateTimeField(auto_now_add=True, verbose_name="Place datetime")
    complete_datetime = models.DateTimeField(auto_now_add=True, verbose_name="Complete datetime")
    customer = models.ForeignKey('Customers', on_delete=models.CASCADE, verbose_name="Customer")


class Supplies(models.Model):
    supplier = models.ForeignKey('Suppliers', on_delete=models.CASCADE, verbose_name="Supplier")
    datetime = models.DateTimeField(auto_now_add=True, verbose_name="Datetime")


class Suppliers(models.Model):
    name_supplier = models.CharField(max_length=255, verbose_name="Name supplier")
    person = models.CharField(max_length=128, verbose_name="Person")
    phone = models.IntegerField(verbose_name="Phone")
    address = models.CharField(max_length=255, verbose_name="Address")


class Customers(models.Model):
    user=models.ForeignKey(User, verbose_name='Customer', on_delete=models.CASCADE)
    phone=models.CharField(max_length=20, verbose_name='Phone')
    address=models.CharField(max_length=255, verbose_name='Address')

    def __str__ (self):
        return "Customer: {} {}".format(self.user.pk, self.user.username)


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