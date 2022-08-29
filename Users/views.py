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

    l=[]
    for slot in slots:
        court = slot.court
        sl = str(slot.slot).strip("Slot object (")
        timing = sl.strip(")")
        if str(slot.available)=="True":
            availability = "Available"
        else:
            availability = "Not available"
        d={
            'court':court,
            'slot':timing,
            'available':availability
        }
        l.append(d)
    
    if request.method=="POST":
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
    return render(request,'authenticate/sport.html',{'name':sportname,'slots':l})


def bookings(request):
    username = request.user.username
    firstname = request.user.first_name
    lastname = request.user.last_name
    userlist = {
        'username': username,
        'firstname': firstname,
        'lastname': lastname
    }

    userid = User.objects.get(username=username)
    memberid = Member.objects.get(username=userid)
    userbookings = Booking.objects.filter(member=memberid)

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

    return render(request,'authenticate/userbookings.html',{'user':userlist,'bookings':l})
