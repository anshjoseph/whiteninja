from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete,post_save
from django.conf import settings
from django.contrib.auth.models import User
user = settings.AUTH_USER_MODEL
# Create your models here.
class partcepant(models.Model):
    slot = models.IntegerField(auto_created=True,blank=True)
    name_tt = models.CharField(max_length=20)
    team_name = models.CharField(max_length=20,default="none")
    leader_dicord_id = models.CharField(max_length=30,default="none")
    le_name = models.CharField(max_length=20)
    leader = models.CharField(max_length=20)
    m1_name = models.CharField(max_length=20,blank=True)
    mem1 = models.CharField(max_length=20,blank=True)
    m2_name = models.CharField(max_length=20,blank=True)
    mem2 = models.CharField(max_length=20,blank=True)
    m3_name = models.CharField(max_length=20,blank=True)
    mem3 = models.CharField(max_length=20,blank=True)
    def __str__(self):
        return self.name_tt
    
class tonament_list(models.Model):
    tonament_name = models.CharField(max_length=20)
    data = models.CharField(max_length=70)
    solo = models.BooleanField(default=False)
    team = models.BooleanField(default=False)
    pubg = models.BooleanField(default=False)
    free_fire =models.BooleanField(default=False)
    #call_of_duty = models.BooleanField(default=False)
    date = models.DateTimeField()
    def __str__(self):
        return self.tonament_name
    
class news_win_list(models.Model):
    data = models.CharField(max_length=70)
    def __str__(self):
        return self.data
class blacklist(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.user)
class room_pass_id(models.Model):
    competation = models.OneToOneField(tonament_list,on_delete=models.CASCADE)
    room_id = models.CharField(max_length=20)
    room_pass = models.CharField(max_length=20)
    def __str__(self):
        return str(self.competation)
    
@receiver(post_delete,sender=tonament_list)
def del_tonament(**kargs):
    #print(kargs.get('instance'))
    data = partcepant.objects.filter(name_tt=kargs.get('instance'))
    for d in data:
        if str(kargs.get('instance')) == str(d.name_tt):
            d.delete()
        