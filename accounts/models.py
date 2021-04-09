from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.
user = settings.AUTH_USER_MODEL
#---------------------------------
class profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    user_name = models.CharField(max_length=50,default="not defined")
    #-------------------------
    #call_of_duty
    #call_of_duty_ch_box= models.BooleanField(default=False)
    #call_of_duty_us_na = models.CharField(max_length=40,blank=True)
    #call_of_duty_us_id = models.CharField(max_length=40,blank=True)
    #---------
    #free_fire
    free_fire_ch_box= models.BooleanField(default=False)
    free_fire_us_na = models.CharField(max_length=40,blank=True)
    free_fire_us_id = models.CharField(max_length=40,blank=True)
    #---------
    #pubg
    pubg_ch_box= models.BooleanField(default=False)
    pubg_us_na = models.CharField(max_length=40,blank=True)
    pubg_us_id = models.CharField(max_length=40,blank=True)
    #---------------user_id----------
    def __str__(self):
        name = str(self.user)
        return name
#-----------------------signals--------------------------
@receiver(post_save,sender=user)
def make_profile(**kargs):
    username = kargs.get('instance')
    if len(profile.objects.filter(user_name=username)) == 0:
        profile(user=username,user_name=str(username)).save()