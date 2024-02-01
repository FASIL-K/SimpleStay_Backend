from django.contrib import admin

from .models import Post,PropertyImage,Amenity

# Register your models here.
admin.site.register(Post)
admin.site.register(PropertyImage)
admin.site.register(Amenity)