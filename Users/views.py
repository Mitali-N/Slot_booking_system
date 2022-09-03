from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm
from .models import Staff, Member
from django.contrib.auth.models import User

import sys
sys.path.append('../')

from Sports.models import Sport, SportSpecificSlot, Booking, Slot


def usertype(request, id):
    for obj in Staff.objects.all():
        if obj.username == id:
            request.session['usertype'] = 'staff'
    for obj in Member.objects.all():
        if obj.username == id:
            request.session['usertype'] = 'member'


def limit(request, id):
    query = Booking.objects.filter(member=Member.objects.get(username=User.objects.get(username=id)))
    n=0
    for result in query:
        n+=1
    if n<3:
        return False
    else:
        return True


def login_user(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            if request.user.username=="admin":
                return redirect('/admin/')
            else:
                userid = User.objects.get(username=request.user.username)
                usertype(request, userid)
                return redirect('home')
        else:
            messages.success(request,("Incorrect username or password. Please try again"))
            return redirect('login')
    else:
        return render(request,'authenticate/login.html',{})

def logout_user(request):
    logout(request)
    messages.success(request,("Logged out successfully."))
    return redirect('landing')

def register_user(request):
    if request.method=="POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #user = authenticate(username=username, password=password)
            #login(request, user)
            messages.success(request, ("Registration Successful!"))
            return redirect('landing')
    else:
        form = RegisterUserForm()
    return render(request, 'authenticate/register_user.html',{
        'form':form,
    })


def home(request):
    username = request.user.username
    firstname = request.user.first_name
    lastname = request.user.last_name
    userlist = {
        'username': username,
        'firstname': firstname,
        'lastname': lastname
    }

    sportlist = Sport.objects.all()

    if request.method=="POST":
        request.session['sport'] = request.POST['sport']
        return redirect('sport')


    return render(request, 'authenticate/home.html',{'info':userlist, 'sports':sportlist})


def sportpage(request):
    sportname = request.session['sport']
    slots = SportSpecificSlot.objects.filter(name=sportname)
    

    if request.session['usertype']=="member":
        lmt = limit(request, request.user.username)
    else:
        lmt=None

    l=[]
    for slot in slots:
        court = slot.court
        sl = str(slot.slot).strip("Slot object (")
        timing = sl.strip(")")
        if str(slot.available)=="True":
            availability = "Available"
            person = ""
        else:
            availability = "Not available"
            findBooking = Booking.objects.get(sport= Sport.objects.get(name=sportname), court= court, slot= Slot.objects.get(slot= timing))
            person = findBooking.member.username
        
        d={
            'court':court,
            'slot':timing,
            'available':availability,
            'bookedby':person
        }
        l.append(d)
    
    if request.method=="POST":
        if request.session['usertype'] == 'member':
            c = request.POST['court']
            s = request.POST['slot']
            
            update_availablity = SportSpecificSlot.objects.get(name=sportname, slot=s, court=c)
            update_availablity.available = False
            update_availablity.save()

            
            userid = User.objects.get(username=request.user.username)
            memberid = Member.objects.get(username=userid)
            sportid = Sport.objects.get(name=sportname)
            slotid = Slot.objects.get(slot=s)
            
            table = Booking()
            table.member = memberid
            table.sport = sportid
            table.court = c
            table.slot = slotid
            table.save()
            
            
            messages.success(request, ("Slot Booked"))
            return redirect('sport')
        
        if request.session['usertype'] == 'staff':
            try:
                if request.POST['book']:
                    request.session['court'] = request.POST['court']
                    request.session['slot'] = request.POST['slot']
                    return redirect('bookslot')
            except:
                pass
            try:
                if request.POST['edit']:
                    request.session['membername'] = request.POST['bookedby']
                    request.session['oldcourt'] = request.POST['court']
                    request.session['oldslot'] = request.POST['slot']
                    return redirect('edit')
            except:
                pass
            try:
                if request.POST['cancel']:
                    request.session['court'] = request.POST['court']
                    request.session['slot'] = request.POST['slot']
                    request.session['membername'] = request.POST['bookedby']
                    return redirect('cancel')
            except:
                pass
   
    return render(request,'authenticate/sport.html',{'name':sportname,'slots':l,'limit':lmt,'username':request.user.username})


def bookings(request):
    if request.session['usertype']=='member':
        username = request.user.username
        firstname = request.user.first_name
        lastname = request.user.last_name
    if request.session['usertype']=='staff':
        pass 

    userlist = {
        'username': username,
        'firstname': firstname,
        'lastname': lastname
    }
    lmt = limit(request, username)
    userid = User.objects.get(username=username)
    userbookings = []
    
    try:
        memberid = Member.objects.get(username=userid)
        userbookings = Booking.objects.filter(member=memberid)
    except:
        pass

    l=[]
    for booked in userbookings:
        b1 = str(booked.sport).strip("Sport object ")
        b2 = b1.strip("(")
        sp = b2.strip(")")

        s1 = str(booked.slot).strip("Slot object ")
        s2 = s1.strip("(")
        sl = s2.strip(")")

        d={
            'sport': sp,
            'court': booked.court,
            'slot': sl
        }
        l.append(d)

    return render(request,'authenticate/userbookings.html',{'user':userlist,'bookings':l, 'limit':lmt})


def addsport(request):
    if request.method=="POST":
        table = Sport()
        table.name = request.POST['sportname']
        table.save()
        messages.success(request, ('Sport added!'))
        return redirect('home')
    return render(request, 'authenticate/addsport.html')


def addslot(request):
    slottings = Slot.objects.all()

    l1 = []
    for slotting in slottings:
        a = str(slotting).strip("Slot object ")
        b = a.strip("(")
        c = b.strip(")")
        l1.append(c)
    
    if request.method == "POST":
        table = SportSpecificSlot()
        table.name = Sport.objects.get(name=request.session['sport'])
        table.court = request.POST['court']
        table.slot = Slot.objects.get(slot=request.POST['slot'])
        table.available = True
        table.save()
        messages.success(request, ('Slot added!'))

        return redirect('sport')
    
    return render(request, 'authenticate/addslot.html',{'slots': l1})


def bookslot(request):

    membrs = Member.objects.all()
    l1 = []
    for memr in membrs:
        l1.append(memr.username)

    sp = Sport.objects.all()
    l2 = []
    for spt in sp:
        a2 = str(spt).strip("Sport object ")
        b2 = a2.strip("(")
        c2 = b2.strip(")")
        l2.append(c2)

    slottings = Slot.objects.all()
    l3 = []
    for slotting in slottings:
        a3 = str(slotting).strip("Slot object ")
        b3 = a3.strip("(")
        c3 = b3.strip(")")
        l3.append(c3)

    if request.method=="POST":
        table = Booking()
        userid = User.objects.get(username=request.POST['member'])
        table.member = Member.objects.get(username=userid)
        table.sport = Sport.objects.get(name=request.session['sport'])
        table.court = request.session['court']
        table.slot = Slot.objects.get(slot=request.session['slot'])
        table.save()

        update = SportSpecificSlot.objects.get(name=(Sport.objects.get(name=request.session['sport'])),court=request.session['court'],slot=(Slot.objects.get(slot=request.session['slot'])))
        update.available = False
        update.save()

        messages.success(request, ('Slot booked!'))
        return redirect('sport')

    return render(request, 'authenticate/bookslot.html', {'members':l1,'sportss':l2,'slots':l3})


def edit(request):
    membrs = Member.objects.all()
    l1 = []
    for memr in membrs:
        l1.append(memr.username)

    sp = Sport.objects.all()
    l2 = []
    for spt in sp:
        a2 = str(spt).strip("Sport object ")
        b2 = a2.strip("(")
        c2 = b2.strip(")")
        l2.append(c2)

    slottings = Slot.objects.all()
    l3 = []
    for slotting in slottings:
        a3 = str(slotting).strip("Slot object ")
        b3 = a3.strip("(")
        c3 = b3.strip(")")
        l3.append(c3)

    if request.method=="POST":
        userid = User.objects.get(username=request.session['membername'])
        memberid = Member.objects.get(username=userid)
        sportid = Sport.objects.get(name=request.session['sport'])
        slotid = Slot.objects.get(slot=request.session['oldslot'])
        table = Booking.objects.get(member=memberid,sport=sportid,court=request.session['oldcourt'],slot=slotid)
        table.court = request.POST['court']
        table.slot = Slot.objects.get(slot=request.POST['slot'])
        table.save()

        update = SportSpecificSlot.objects.get(name=(Sport.objects.get(name=request.session['sport'])),court=request.POST['court'],slot=(Slot.objects.get(slot=request.POST['slot'])))
        update.available = False
        update.save()
                
        freeslot = SportSpecificSlot.objects.get(name=(Sport.objects.get(name=request.session['sport'])),court=request.session['oldcourt'],slot=(Slot.objects.get(slot=request.session['oldslot'])))
        freeslot.available = True
        freeslot.save()

        messages.success(request, ('Slot updated!'))
        return redirect('sport')

    return render(request, 'authenticate/edit.html',{'members':l1,'sportss':l2,'slots':l3})

def cancel(request):
    if request.method=="POST":
        userid = User.objects.get(username=request.session['membername'])
        memberid = Member.objects.get(username=userid)
        sportid = Sport.objects.get(name=request.session['sport'])
        court = request.session['court']
        slotid = Slot.objects.get(slot=request.session['slot'])
        delbooking = Booking.objects.get(member=memberid,sport=sportid,court=court,slot=slotid)
        delbooking.delete()

        update = SportSpecificSlot.objects.get(name=(Sport.objects.get(name=request.session['sport'])),court=request.session['court'],slot=(Slot.objects.get(slot=request.session['slot'])))
        update.available = True
        update.save()

        messages.success(request, ('Booking cancelled!'))
        return redirect('sport')

    return render(request, 'authenticate/cancel.html')


def refresh(request):
    sport_refresh = SportSpecificSlot.objects.all()
    for refreshing in sport_refresh:
        refreshing.available = True
        refreshing.save()

    user_refresh = Booking.objects.all()
    for refrsh in user_refresh:
        refrsh.delete()
    
    messages.success(request, ('Refresh successful!'))
    return redirect('home')