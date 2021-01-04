from django.db import models
from django.contrib.auth.models import  User
from django.utils.crypto import get_random_string
# Create your models here.
class Customer(models.Model):
    
    user = models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    name=models.CharField(max_length=30,null=True)
    sn=models.CharField(max_length=20,null=True)
    profile_pic=models.ImageField(default="download.jpg",null=True,blank=True)
    contract=models.CharField(max_length=11,null=True)
    address=models.CharField(max_length=200,null=True)
    email=models.CharField(max_length=100,null=True,blank=True)
    date_created=models.DateTimeField(auto_now_add=True,null=True)



    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=200,null=True)
    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORY=(
        ('Pending','Pending'),
        ('Complited','Complited'),  
    )
    name=models.CharField(max_length=200,null=True)
    catagory=models.CharField(max_length=200,null=True,choices=CATEGORY)
    price=models.FloatField(null=True) 
    weight=models.FloatField(null=True)
    sn=models.CharField(max_length=20,null=True)
    pakagingtype=models.CharField(max_length=150,null=True)
    contract=models.CharField(max_length=200,null=True)
    receiver=models.CharField(max_length=200,null=True)
    date_created=models.DateTimeField(auto_now_add=True,null=True)
    description=models.CharField(max_length=200,null=True,blank=True)
    tags=models.ManyToManyField(Tag)

    def __str__(self):
        return self.name



class Order(models.Model):
    STATUS=(
        ('Pending','Pending'),
        ('Complited','Complited'),
        ('Delivered','Delivered'),
    )

    customer=models.ForeignKey(Customer,null=True,on_delete=models.SET_NULL)

    product=models.ForeignKey(Product,null=True,on_delete=models.SET_NULL)

    date_created=models.DateTimeField(auto_now_add=True,null=True)

    status=models.CharField(max_length=200,null=True,choices=STATUS)
    destination=models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.customer.name

#class GeneratePdf(View):

class GeneralOrder(models.Model):
    serial_no = get_random_string(length=32)
    customer_name=models.CharField(max_length=200,null=True)
    contract=models.CharField(max_length=11,null=True)
    address=models.CharField(max_length=200,null=True)
    email=models.CharField(max_length=100,null=True,blank=True)
    date_created=models.DateTimeField(auto_now_add=True,null=True)
    #pakagingtype=models.CharField(max_length=150,null=True)
    description=models.CharField(max_length=200,null=True,blank=True)
    payment=models.FloatField(null=True) 
    STATUS=(
        ('Pending','Pending'),
        ('Complited','Complited'),
        ('Delivered','Delivered'),
    )
    status=models.CharField(max_length=200,null=True,choices=STATUS)
    receiver=models.CharField(max_length=200,null=True)
    phn=models.CharField(max_length=11,null=True)
    DESTINATION=(
        ('Dhaka','Dhaka'),
        ('Rajshahi','Rajshahi'),
        ('Bogura','Bogura'),
        ('Chittagong','Chittagong'),
        ('Syllet','Syllet'),

    )
    destination=models.CharField(max_length=200,null=True,choices=DESTINATION)
    PACKING=(
        ('Envelope','Envelop'),
        ('Cardboard','Cardboard'),
        ('Paperboard','Paperboard'),
        ('PlasticBox','PlasticBox'),
        ('RigidBoxes','RigidBoxes'),
    )

    packing=models.CharField(max_length=200,null=True,choices=PACKING)

    def __str__(self):
        return self.customer_name
    def pub_date_pretty(self):
        return self.date_created.strftime('%b %e %Y ')