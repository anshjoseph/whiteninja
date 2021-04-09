from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout
from accounts.models import profile
from .models import tonament_list,partcepant,blacklist
import time
def ch_black(username):
    for i in blacklist.objects.all():
        if i.user.username == username:
            return True
    return False
def ch_tonament(username,tonament_name):
    if username != None:
        user = partcepant.objects.filter(name_tt=tonament_name,le_name=username)
        if len(user) == 0:
            user = partcepant.objects.filter(name_tt=tonament_name,m1_name=username)
        if len(user) == 0:
            user = partcepant.objects.filter(name_tt=tonament_name,m1_name=username)
        if len(user) == 0:
            user = partcepant.objects.filter(name_tt=tonament_name,m1_name=username)
        if len(user) != 0:
            return False
        else:
            return True
    else:
        return False
@login_required(login_url="login")
def part(request):
    if ch_black(request.user.get_username()):
        logout(request)
        return render(request,"./global/error.html",{"error":{"tittle": "user auth problem","message":"you are blocked"}})
    tt_list = tonament_list.objects.all()
    user = list(profile.objects.filter(user_name=request.user.get_username()).values())[0]
    return render(request,"./management/sel_part.html",{"tt_list":tt_list,"user":user})
@login_required(login_url="login")
def data_part(request):
    if ch_black(request.user.get_username()):
        logout(request)
        return render(request,"./global/error.html",{"error":{"tittle": "user auth problem","message":"you are blocked"}})
    tt_name = request.POST.get("tt_name")
    user_comp = partcepant.objects.filter(name_tt=tt_name,le_name=request.user.get_username())
    if (len(user_comp)==0):
        user_comp = partcepant.objects.filter(name_tt=tt_name,m1_name=request.user.get_username())
    if (len(user_comp)==0):
        user_comp = partcepant.objects.filter(name_tt=tt_name,m2_name=request.user.get_username())
    if (len(user_comp)==0):
        user_comp = partcepant.objects.filter(name_tt=tt_name,m3_name=request.user.get_username())
    #print(user_comp)
    if len(user_comp) != 0:
        #return render(request,"./global/error.html",{"error":{"tittle": "tonament part error","message":"you alredy take part in this tonament"}})
        return render(request,"./global/error.html",{"error":{"tittle": "tonament part error","message":"you alredy take part in this tonament"}})
    if tt_name != None:
        tt_data = list(tonament_list.objects.filter(tonament_name=tt_name).values())[0]
        if tt_data.get("pubg"):
            if len(partcepant.objects.filter(name_tt=tt_name)) == 50:
                # return HttpResponse("tonament is full")
                return render(request,"./global/error.html",{"error":{"tittle": "status full","message":"tonament is full"}})
        if tt_data.get("free_fire"):
            if len(partcepant.objects.filter(name_tt=tt_name)) == 12:
                return render(request,"./global/error.html",{"error":{"tittle": "status full","message":"tonament is full"}})
    else:
        return redirect("particepant")
    return render(request,"./management/ac_part.html",{"tt_data":tt_data,"tt_name":tt_name})
@login_required(login_url="login")
def ac_part(request):
    if ch_black(request.user.get_username()):
        logout(request)
        return render(request,"./global/error.html",{"error":{"tittle": "user auth problem","message":"you are blocked"}})
    tt_name = request.POST.get("to_na")
    tm_name = request.POST.get("tt_name")
    t1 = request.POST.get("mem1",None)
    t2 = request.POST.get("mem2",None)
    t3 = request.POST.get("mem3",None)
    t4 = request.POST.get("mem4",None)
    dis_id = request.POST.get("dis_id",None)
    print(tt_name,tm_name,t1,t2,t3,t4)
    user_comp = partcepant.objects.filter(name_tt=tt_name,le_name=request.user.get_username())
    if (len(user_comp)==0):
        user_comp = partcepant.objects.filter(name_tt=tt_name,m1_name=request.user.get_username())
    if (len(user_comp)==0):
        user_comp = partcepant.objects.filter(name_tt=tt_name,m2_name=request.user.get_username())
    if (len(user_comp)==0):
        user_comp = partcepant.objects.filter(name_tt=tt_name,m3_name=request.user.get_username())
    #print(user_comp)
    if len(user_comp) != 0:
        return render(request,"./global/error.html",{"error":{"tittle": "tonament part error","message":"you alredy take part in this tonament"}})
    tt_data = list(tonament_list.objects.filter(tonament_name=tt_name).values())[0]
    if tt_data.get("pubg"):
        if len(partcepant.objects.filter(name_tt=tt_name)) == 50:
            return HttpResponse("tonament is full")
    if tt_data.get("free_fire"):
        if len(partcepant.objects.filter(name_tt=tt_name)) == 12:
            return HttpResponse("tonament is full")
    #-------------------------------------------------------



    if tt_data.get("solo"):
        user = list(profile.objects.filter(user_name=t1).values())
        if len(user) != 0:
            user = user[0]
            tn1 = ""
            if len(t1) != 0:
                if ch_black(t1):
                    return render(request,"./global/error.html",{"error":{"tittle": "team menber is blocked","message":f"{t1} is blocked by admin or by managemnt"}})
            if user.get("free_fire_ch_box") == True and tt_data.get("free_fire") == True:
                tn1 = user.get("free_fire_us_id")
            if user.get("pubg_ch_box") == True and tt_data.get("pubg") == True:
                tn1 = user.get("pubg_us_id")
            # print(tt_name,tm_name,dis_id,t1,tn1)
            count = len(partcepant.objects.filter(name_tt=tt_name))
            form = partcepant(slot=count+1,name_tt=tt_name,team_name=tm_name,leader_dicord_id=dis_id,le_name=t1,leader=tn1)
            form.save()
        else:
            return HttpResponse("user name is not found!(hint: try username register in website)")
    else:
        tn1 = ""
        tn2 = ""
        tn3 = ""
        tn4 = ""
        user = list(profile.objects.filter(user_name=t1).values())
        flag = [0,0,0,0]
        
        
        if len(user) != 0:
            user = user[0]
            #print(blacklist(t1))

            if len(t1) != 0:
                if ch_black(t1):
                    return render(request,"./global/error.html",{"error":{"tittle": "team menber is blocked","message":f"{t1} is blocked by admin or by managemnt"}})
                if ch_tonament(t1,tt_name) != True:
                    return render(request,"./global/error.html",{"error":{"tittle": "user already registed","message":f"{t1} is already register"}})
            if user.get("free_fire_ch_box") == True and tt_data.get("free_fire") == True:
                tn1 = user.get("free_fire_ud_id")
            if user.get("pubg_ch_box") == True and tt_data.get("pubg") == True:
                tn1 = user.get("pubg_us_id")
            flag[0] = 1
        else:
             return render(request,"./global/error.html",{"error":{"tittle": "not found leader","message":"for register leader name is nessary"}})
        if len(t1) != 0 and flag[0] == 0:
            return render(request,"./global/error.html",{"error":{"tittle": "finding data error","message":"user website username you team menbers to register in competation"}})
        user = list(profile.objects.filter(user_name=t2).values())
        if len(user) != 0:
            user = user[0]
            if len(t2) != 0:
                if ch_black(t2):
                    #logout(request)
                    return render(request,"./global/error.html",{"error":{"tittle": "team menber is blocked","message":f"{t2} is blocked by admin or by managemnt"}})
                if ch_tonament(t2,tt_name) != True:
                    return render(request,"./global/error.html",{"error":{"tittle": "user already registed","message":f"{t2} is already register"}})
            # tn2 = ""
            if user.get("free_fire_ch_box") == True and tt_data.get("free_fire") == True:
                tn2 = user.get("free_fire_ud_id")
            if user.get("pubg_ch_box") == True and tt_data.get("pubg") == True:
                tn2 = user.get("pubg_us_id")
            flag[1] = 1
        # else:
        #     return render(request,"./global/error.html",{"error":{"tittle": "not found 2","message":"for register leader name is nessary"}})
        if len(t2) != 0 and flag[1] == 0:
            return render(request,"./global/error.html",{"error":{"tittle": "finding data error","message":"user website username you team menbers to register in competation"}})
        user = list(profile.objects.filter(user_name=t3).values())
        if len(user) != 0:
            user = user[0]
            # tn3 = ""
            if len(t3) != 0:
                if ch_black(t3):
                    return render(request,"./global/error.html",{"error":{"tittle": "team menber is blocked","message":f"{t3} is blocked by admin or by managemnt"}})
                if ch_tonament(t3,tt_name) != True:
                    return render(request,"./global/error.html",{"error":{"tittle": "user already registed","message":f"{t3} is already register"}})
            if user.get("free_fire_ch_box") == True and tt_data.get("free_fire") == True:
                tn3 = user.get("free_fire_ud_id")
            if user.get("pubg_ch_box") == True and tt_data.get("pubg") == True:
                tn3 = user.get("pubg_us_id")
            flag[2] = 1
        # else:
        #     return HttpResponse("user name is not found!(hint: try username register in website)")
        if len(t3) != 0 and flag[2] == 0:
            return render(request,"./global/error.html",{"error":{"tittle": "finding data error","message":"user website username you team menbers to register in competation"}})
        user = list(profile.objects.filter(user_name=t4).values())
        if len(user) != 0:
            user = user[0]
            if len(t4) != 0:
                if ch_black(t4):
                    return render(request,"./global/error.html",{"error":{"tittle": "team menber is blocked","message":f"{t4} is blocked by admin or by managemnt"}})
                if ch_tonament(t4,tt_name) != True:
                    return render(request,"./global/error.html",{"error":{"tittle": "user already registed","message":f"{t4} is already register"}})
            # tn4 = ""
            if user.get("free_fire_ch_box") == True and tt_data.get("free_fire") == True:
                tn4 = user.get("free_fire_ud_id")
            if user.get("pubg_ch_box") == True and tt_data.get("pubg") == True:
                tn4 = user.get("pubg_us_id")
            flag[3] = 1
        # else:
        #     return HttpResponse("user name is not found!(hint: try username register in website)")
        #------------------------------flag-----------------------------------
        if len(t4) != 0 and flag[3] == 0:
            return render(request,"./global/error.html",{"error":{"tittle": "finding data error","message":"user website username you team menbers to register in competation"}})
        if sum(flag) == 4:
            count = len(partcepant.objects.filter(name_tt=tt_name))
            form = partcepant(slot=count+1,name_tt=tt_name,team_name=request.POST.get("tt_name",None),leader=tn1,mem1=tn2,mem2=tn3,mem3=tn4,le_name=t1,m1_name=t2,m2_name=t3,m3_name=t4,leader_dicord_id=dis_id)
            #request.POST.get("tt_name",None)
            form.save()
        elif sum(flag) >= 2 and sum(flag) <= 4:
            ls = [len(tn2),len(tn3),len(tn4)]
            found = []
            for i in ls:
                if i != 0:
                    if ls.index(i) == 0:
                        found.append(tn2)
                    elif ls.index(i) == 1:
                        found.append(tn3)
                    elif ls.index(i) == 2:
                        found.append(tn4)
                else:
                    found.append("")
            #print(found)
            count = len(partcepant.objects.filter(name_tt=tt_name))
            print(ch_tonament(t1,tt_name),ch_tonament(t2,tt_name),ch_tonament(t3,tt_name),ch_tonament(t4,tt_name))
            form = partcepant(slot=count+1,name_tt=tt_name,team_name=request.POST.get("tt_name",None),leader=tn1,mem1=found[0],mem2=found[1],mem3=found[2],le_name=t1,m1_name=t2,m2_name=t3,m3_name=t4,leader_dicord_id=dis_id)
            # #request.POST.get("tt_name",None)
            form.save()
        else:
            return render(request,"./global/error.html",{"error":{"tittle": "not enought member","message":"for register in tonament 2 menber is necarry"}})
    #return HttpResponse(f"cogralations your team is registered{tt_name}")
    return render(request,"./global/error.html",{"error":{"tittle": f"{tm_name}","message":"you team is registered"}})
@staff_member_required(login_url="login")
def get_data(request):
    data = ""
    tt_name=""
    if request.method == "POST":
        tt_name = request.POST.get("tt_name",None)
        if tt_name != None:
            data = partcepant.objects.filter(name_tt=tt_name)
    #print(data)
    return render(request,"./management/get_data.html",{"data":data,"to_name":tt_name})
@staff_member_required(login_url="login")
def get_doc(request):
    if request.method == "POST":
        to_name = request.POST.get("to_name",None)
        if to_name != None:
            data = partcepant.objects.filter(name_tt=to_name)
            return render(request,"./man_doc/doc.txt",{"data":data,"to_name":to_name})
        else:
            return render(request,"./global/error.html",{"error":{"tittle": "Error","message":"Data not fonud"}})
    else:
        return render(request,"./global/error.html",{"error":{"tittle": "Error","message":"this page is not ment to use in this way"}})



