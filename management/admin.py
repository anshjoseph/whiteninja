from django.contrib import admin
from .models import partcepant,tonament_list,news_win_list,blacklist,room_pass_id
# Register your models here.
admin.site.register(partcepant)
admin.site.register(tonament_list)
admin.site.register(news_win_list)
admin.site.register(blacklist)
admin.site.register(room_pass_id)