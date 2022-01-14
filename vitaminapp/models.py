from django.db import models
from datetime import datetime
from django.conf import settings
import re, bcrypt

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['last_name'] = "Name must be at least 2 characters long."
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Name must be at least 2 characters long."
        if len(postData['password']) < 8:
            errors['password'] = "Password cannot be less than 8 characters."
        if postData['password'] != postData['confirm_password']:
            errors['match'] = "Passwords do not match."
        if len(postData['email']) < 6:
            errors['email'] = "email is too short"
        EMAIL_REGEX = re.compile('^[_a-z0-9-]+(.[_a-z0-9-]+)@[a-z0-9-]+(.[a-z0-9-]+)(.[a-z]{2,4})$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['reg_email'] = "Email in wrong format"
        users_with_email = User.objects.filter(email=postData['email'])
        if len(users_with_email) >= 1:
            errors['dup'] = "Email taken, use another"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    register_date = models.DateTimeField(auto_now_add=True, verbose_name="modification_date ")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to='images')

    objects = UserManager()

    def __str__(self):    
        return self.first_name

    class Meta:
        db_table = 'vitamin_user'
        verbose_name = 'user'
        verbose_name_plural = 'user'

class ProductManager(models.Manager):
    def product_validator(self, postData):
        errors = {}
        if len(postData['product_name']) < 1:
            errors['product_name'] = "Name must at least 5 characters long."
        if datetime.strptime(postData['date'], '%YYYY-%MM-%DD') < datetime.now():
            errors['date'] = 'Date should be future'

        return errors

class Product(models.Model):
    product_name = models.CharField(max_length=45,blank=True)
    price= models.IntegerField(verbose_name='product_price' )
    description = models.TextField(verbose_name='product_info')
    stock = models.IntegerField(verbose_name='product_stock')
    date = models.DateTimeField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    product_pic = models.ImageField(null=True, blank=True, upload_to='product_images')


    objects = ProductManager()

    def __unicode_(self):    
        return self.product_name


    class Meta:
        db_table = 'vitamin_product'
        verbose_name = 'product'
        verbose_name_plural = 'product'

class OrderProduct(models.Model):
    products = models.ForeignKey(Product, on_delete=models.CASCADE, default="")
    cart_id = models.CharField(max_length=250, blank=True, default="")
    class Meta:
        db_table = 'OrderProduct'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user')

    products = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='product')
    items = models.ManyToManyField(OrderProduct, default="")
    quantity = models.IntegerField(verbose_name='quantity')
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    register_date = models.DateTimeField(auto_now_add=True, verbose_name='Order_time')
    order_pic = models.ImageField(null=True, blank=True, upload_to='order_images')
    
  
    class Meta:
        db_table = 'vitamin_order'
        verbose_name = 'order'
        verbose_name_plural = 'order'


