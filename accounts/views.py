from django.shortcuts import render,Http404,HttpResponse,redirect,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import profile
from django.contrib.auth.decorators import login_required
from management.models import news_win_list,blacklist,tonament_list,partcepant,room_pass_id
import datetime
# Create your views here.
class List(list):
    def __init__(self,ls):
        for i in ls:
            self.append(i)
def ch_black(username):
    for i in blacklist.objects.all():
        if i.user.username == username:
            return True
    return False
@login_required(login_url="login")
def user_logout(request):
    logout(request)
    return redirect("login")
    
    #return HttpResponseRedirect("login")
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()        
    return render(request,"./accounts/register.html",{"form":form})
def login_pg(request):
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request,username=username,password=password)
        if user != None:
            login(request,user)
            if ch_black(request.user.get_username()):
                logout(request)
                return render(request,"./global/error.html",{"error":{"tittle": "user auth problem","message":"you are blocked"}})
            return redirect("profile")
        else:
            return redirect("register")
    return render(request,"./accounts/login.html")
@login_required(login_url="login")
def profile_page(request):
    #date_time = datetime.datetime.now()
    if ch_black(request.user.get_username()):
        logout(request)
        return render(request,"./global/error.html",{"error":{"tittle": "user auth problem","message":"you are blocked"}})
    user_data = list(profile.objects.filter(user_name=request.user.get_username()).values())[0]
    news_data = news_win_list.objects.all()
    if user_data.get("free_fire_ch_box") == False and user_data.get("pubg_ch_box") == False:
        return redirect("change_profile")
    if len(user_data) !=0:
        #print(dict(user_data.values()))
        ls_try = list()
        user_comp = partcepant.objects.filter(le_name=request.user.get_username())
        if len(user_comp) != 0:
            ls_try.extend(user_comp)
        user_comp = partcepant.objects.filter(m1_name=request.user.get_username())
        if len(user_comp) != 0:
            ls_try.extend(user_comp)
        user_comp = partcepant.objects.filter(m2_name=request.user.get_username())
        if len(user_comp) != 0:
            ls_try.extend(user_comp)
        user_comp = partcepant.objects.filter(m3_name=request.user.get_username())
        if len(user_comp) != 0:
            ls_try.extend(user_comp)
        #print(len(ls_try))
        comp_detail = list()
        if len(ls_try) != 0:
            for j in ls_try:
                #print(j.slot)
                data = j
                tt_name = data.name_tt
                time = tonament_list.objects.filter(tonament_name=tt_name)[0].date
                try:
                    room_id = list(room_pass_id.objects.filter(competation=tonament_list.objects.filter(tonament_name=tt_name)[0]).values())[0]
                except:
                    room_id = None
                comp_detail.append({"data":data,"room_id":room_id,"time":time})
        
        
        #print(ls_try)
        #print(comp_detail)
        return render(request,"./accounts/profile.html",{"user":user_data,"news":news_data,"comps":comp_detail})
    else:
        #return HttpResponse("talk to admin")
        return render(request,"./global/error.html",{"error":{"tittle": "problem in data creation","message":"talk to admin"}})
@login_required(login_url="login")
def change_profile(request):
    if ch_black(request.user.get_username()):
        logout(request)
        #return render(request,"./global/error.html",{"error":{"tittle": "user auth problem","message":"you are blocked"}})
        return render(request,"./global/error.html",{"error":{"tittle": "user auth problem","message":"you are blocked"}})
    user = profile.objects.filter(user_name=request.user.get_username())
    data = list(user.values())[0]
    if data.get("free_fire_ch_box") and data.get("pubg_ch_box"):
        return redirect("profile")
    if request.method == "POST":
        #cod_ch = request.POST.get('cod_ch')
        ff_ch = request.POST.get('ff_ch')
        pg_ch = request.POST.get('pg_ch')
        if ff_ch != None:
            us_ff = request.POST.get('ff_us')
            id_ff = request.POST.get('ff_id')
            user.update(free_fire_ch_box=True,free_fire_us_id=id_ff,free_fire_us_na=us_ff)
        if pg_ch != None:
            us_pg = request.POST.get('pg_us')
            id_pg =request.POST.get('pg_us')
            user.update(pubg_ch_box=True,pubg_us_id=id_pg,pubg_us_na=us_pg)
        return redirect("profile")
    return render(request,"./accounts/ch_profile.html",{"data":list(user.values())[0]})
@login_required(login_url="login")
def ch_pg(request):
    if ch_black(request.user.get_username()):
        logout(request)
        return render(request,"./global/error.html",{"error":{"tittle": "user auth problem","message":"you are blocked"}})
    user2 = profile.objects.filter(user_name=request.user.get_username())
    if list(user2.values())[0].get('pubg_ch_box') == False:
        return redirect("profile")
    if request.method == "POST":
        
        us_pg = request.POST.get('pg_us')
        id_pg = request.POST.get('pg_id')
        delete = request.POST.get('del')
        if delete == None:
            if len(us_pg) != 0:
                user2.update(pubg_us_na=us_pg)
            if len(id_pg) != 0:
                user2.update(pubg_us_id=id_pg)
        else:
            user2.update(pubg_ch_box=False,pubg_us_na="",pubg_us_id="")
        return redirect("profile")
    return render(request,"./accounts/pg_ch.html",{"data":list(user2.values())[0]})
@login_required(login_url="login")
def ch_ff(request):
    if ch_black(request.user.get_username()):
        logout(request)
        return render(request,"./global/error.html",{"error":{"tittle": "user auth problem","message":"you are blocked"}})
    user3 = profile.objects.filter(user_name=request.user.get_username())
    if list(user3.values())[0].get('free_fire_ch_box') == False:
        return redirect("profile")
    if request.method == "POST":
        
        us_ff = request.POST.get('ff_us')
        id_ff = request.POST.get('ff_id')
        delete = request.POST.get('del')
        if delete == None:
            if len(us_ff) != 0:
                user3.update(free_fire_us_na=us_ff)
            if len(id_ff) != 0:
                user3.update(free_fire_us_id=id_ff)
        else:
            user3.update(free_fire_ch_box=False,free_fire_us_id="",free_fire_us_na="")
        return redirect("profile")
    return render(request,"./accounts/ff_ch.html",{"data":list(user3.values())[0]})
@login_required(login_url="login")
def leave_team(request):
    if request.method == "POST":
        tt_name = request.POST.get("tt_name")
        slot = request.POST.get("slot")
        comp = partcepant.objects.filter(slot=slot,name_tt=tt_name)
        comp.delete()
        return redirect("profile")
    else:
        return redirect("profile")

