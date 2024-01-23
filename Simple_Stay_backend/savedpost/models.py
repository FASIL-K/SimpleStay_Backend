from django.db import models
from user.models import CustomUser
from owner.models import Post
# Create your models here.

class SavedPost(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

    
    

