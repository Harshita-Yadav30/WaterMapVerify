from django.shortcuts import render, redirect
import pandas as pd
import plotly.express as px
import datetime, math, os
from django.shortcuts import render, redirect
# from .forms import UploadImageForm
from .models import Location
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .models import Location
from django.conf import settings
from itertools import zip_longest


@csrf_protect
def homeView(request):
    if request.method == 'POST':
        name = request.POST.get('place')
        desc = request.POST.get('description')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        user = request.user

        if 'image' in request.FILES:
            file = request.FILES['image']
            if file.name.split('.')[-1] in ['png','jpg','jpeg','gif','mp4']:
                Location.objects.create(user=user, place=name, latitude=latitude, longitude=longitude, image=file, description=desc)
            else:
                return render(request, 'home.html', {'showAlert':True, 'user':checkUser(request)})

        return redirect('home')

    return render(request, 'home.html', {'showAlert':False, 'user':checkUser(request)})


def mapView(request):
    locations = Location.objects.all()

    location_names = []
    lons = []
    lats = []

    for location in locations:
        location_names.append(location.place)
        lons.append(location.longitude)
        lats.append(location.latitude)

    data = {
        "location": location_names,
        "lon": lons,
        "lat": lats
    }
    df = pd.DataFrame(data)

    fig = px.scatter_geo(df, lon="lon", lat="lat", text="location", scope="asia")
    fig.update_geos(projection_type="natural earth")
    fig.update_layout(title="Locations in India", height=630)

    plot_html = fig.to_html(full_html=False)

    return render(request, 'map.html', {'plot_html':plot_html, 'user':checkUser(request)})


@csrf_protect
def feedView(request):
    if request.method == 'POST':
        long = request.POST.get('long')
        lat = request.POST.get('lat')

        res = Location.objects.all()

        locations = []
        for item in res:
            if haversine(item.latitude,item.longitude,float(lat),float(long)) <= 1800:
                locations.append(item)

        i = 0
        length = len(locations)
        l1, l2, l3 = [], [], []

        for loc in locations:
            if i < length/3:
                l1.append(loc)
            elif i< (2*length)/3:
                l2.append(loc)
            else:
                l3.append(loc)
            i += 1

        data = zip_longest(l1,l2,l3)
        return render(request, 'feed.html', {'data':data, 'post':True, 'user':checkUser(request)})
    
    else:
        return render(request, 'feed.html', {'post':False, 'user':checkUser(request)})


def contactView(request):
    return render(request, 'contact.html', {'user':checkUser(request)})


def haversine(lat1, lon1, lat2, lon2):
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = 6371 * c
    return distance


def login_page(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not User.objects.filter(username=email).exists():
            print("No such user")
            return redirect("login")
        
        user = authenticate(username=email,password=password)

        if user is None:
            print("No such user wrong")
            return redirect("login")
        else:
            login(request,user)
            return redirect('home')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


def register(request):
    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(username=email)

        if user.exists():
            return redirect("register")

        user = User.objects.create(first_name=fname, last_name=lname, username=email)
        user.set_password(password)
        user.save()

    return render(request, 'register.html')


def checkUser(request):
    try:
        user = request.user.first_name
    except:
        user = ''
    return user