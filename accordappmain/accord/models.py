from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=20, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)

    avatar = models.ImageField(null=True, default='avatar.svg')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Lobby(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lobby = models.ForeignKey(Lobby, on_delete=models.CASCADE)
    post = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.post[0:10]


class Pages(models.Model):
    page_name = models.CharField(max_length=100, null=True, blank=True)


class Product(models.Model):
    product_name = models.CharField(max_length=200, null=True, blank=True)
    product_details = models.TextField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    preorder = models.IntegerField(null=True, blank=True)
    product_id = models.CharField(max_length=200, null=True, blank=True)
    product_type = models.CharField(max_length=200, null=True, blank=True)
    available = models.CharField(max_length=200, null=True, blank=True)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='product')
    created_date = models.DateTimeField(null=True, blank=True)


class Order(models.Model):
    order_id = models.CharField(max_length=200, null=True, blank=True)
    # product_name = models.CharField(max_length=200, null=True, blank=True)
    # product_details = models.TextField(null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    customer_name = models.CharField(max_length=200, null=True, blank=True)
    customer_contactnumber = models.CharField(max_length=200, null=True, blank=True)
    customer_address = models.TextField(null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    total_price = models.IntegerField(null=True, blank=True)
    status = models.IntegerField(null=True, blank=True)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='order')
    created_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.product


class Tasks(models.Model):
    task_id = models.CharField(max_length=200, null=True, blank=True)
    task_details = models.TextField(null=True)
    assign_date = models.DateField(auto_now_add=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned')
    deadline_date = models.DateField()
    completed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='complete')
    remarks = models.TextField(null=True, blank=True)
    status = models.IntegerField(null=True, blank=True)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='task')
    created_date = models.DateTimeField(null=True, blank=True)
