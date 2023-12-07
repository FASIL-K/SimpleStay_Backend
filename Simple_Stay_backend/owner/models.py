from django.db import models
from user.models import CustomUser



class OwnerInfo(models.Model):
    userId = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    owner_name = models.CharField(max_length=100)
    phone = models.PositiveBigIntegerField(null=True,blank=True)
    streetaddress = models.TextField(null=True)
    country = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100,null=True)
    city = models.CharField(max_length=100,null=True)
    zipcode = models.BigIntegerField(null=True)
    is_verify = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    FURNISHED_TYPE = [
        ('Fully Furnished', 'Fully Furnished'),
        ('Semi Furnished', 'Semi Furnished'),
        ('Unfurnished', 'Unfurnished'),
    ]
    PROPERTY_TYPE = [
        ('Apartment', 'Apartment'),
        ('Independent Floor', 'Independent Floor'),
    ]
    BHK = [
        ('1BHK', '1BHK'),
        ('2BHK', '2BHK'),
        ('3BHK', '3BHK'),
    ]

    ownerinfo = models.ForeignKey(OwnerInfo, on_delete=models.CASCADE, null=True ,blank=True)
    rentprice = models.PositiveBigIntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    furnished_type = models.CharField(max_length=50, blank=True, null=True, choices=FURNISHED_TYPE)
    city = models.CharField(max_length=50)
    build_up_area = models.PositiveIntegerField(null=True, blank=True)
    calendar_date = models.DateField(null=True, blank=True)
    deposit_amount = models.PositiveBigIntegerField(null=True, blank=True)
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPE)
    bhk = models.CharField(max_length=50, choices=BHK)
    is_available = models.BooleanField(default=True)



class PropertyImage(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField()
