from django.core.validators import FileExtensionValidator
from django.db import models
from user.models import CustomUser

class OwnerInfo(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    phone = models.PositiveBigIntegerField(null=True, blank=True)
    profile_photo = models.FileField(
        upload_to='Ownerprofiles/', blank=True, null=True)
    
    def __str__(self):
        return self.owner.email
    
class Post(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    looking_to = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    property_type = models.CharField(max_length=50)
    furnished_type = models.CharField(max_length=50)
    bhk_type = models.CharField(max_length=50)
    house_name = models.CharField(max_length=50)
    locality = models.CharField(max_length=50)
    build_up_area = models.PositiveIntegerField(null=True, blank=True)
    monthly_rent = models.PositiveBigIntegerField(null=True, blank=True)
    available_from = models.DateField(null=True, blank=True)
    security_deposit = models.CharField(max_length=50)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Add this line
    is_verify = models.BooleanField(default=False)
    is_blocked_by_admin = models.BooleanField(default=False)


class PropertyImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property_images/', validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])])

    def __str__(self):
        return self.image.name

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'
