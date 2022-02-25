from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.http import JsonResponse
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
import json

from .models import User, Contacts

def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return render(request, "chat/login.html", {
                "message": "Invalid username and/or password."
            })

    else:
        logout(request)
        return render(request, "chat/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login')


def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST["email"]
        gender = request.POST["gender"]
        dob = request.POST["dob"]
        age = request.POST["age"]
        status = request.POST["status"]
        if status == "":
            status = "Hey there, I am using Chaticon"
        avatar = request.POST["avatar-link"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        # Ensure password matches confirmation
        if password != confirmation:
            return render(request, "chat/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(
                username = username,
                email = email,
                gender = gender,
                dob = dob,
                age = age,
                status = status,
                avatar = avatar,
                password=password
            )
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "chat/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect('/')

    else:
        return render(request, "chat/register.html")


@login_required(login_url='login/')
def index(request):
    contacts = Contacts.objects.filter(user1=request.user)

    contact_list = list()
    for contact in contacts:
        contact_list.append(contact.user2)

    return render(request, 'chat/room.html', {
        'username': mark_safe(json.dumps(request.user.username)),
        'user': request.user,
        'contacts': contacts
    })


@csrf_exempt
@login_required(login_url='login/')
def addcontact(request):

    #  If POST request
    if request.method == "POST":
        logged_user = request.user

        data = json.loads(request.body)
        addContacts = data.get("newcontacts")

        if not addContacts:
            return JsonResponse({"message": "No Contacts Added."}, status=201)
        else:
            n = 0
            for contact_name in addContacts:
                contact = User()
                contact = User.objects.get(username=contact_name)
                c1 = Contacts(user1=logged_user, user2=contact)
                c1.save()
                c2 = Contacts(user1=contact, user2=logged_user)
                c2.save()
                n = n + 1
            return JsonResponse({"message": f"{n} Contacts Added Successfully."}, status=201)

    # If GET request
    else:
        contacts = Contacts.objects.filter(user1=request.user)
        contacts_list = list()
        for contact in contacts:
            contacts_list.append(contact.user2)

        all_contacts = User.objects.exclude(username=request.user)

        new_contacts = list()
        for contact in all_contacts:
            if contact not in contacts_list:
                new_contacts.append(contact)

        # If no new users are there to be added
        if not new_contacts:
                return render(request, 'chat/addcontact.html', {
                'username': mark_safe(json.dumps(request.user.username)),
                'allcontacts': "No Users Available"
            })
        # If new users can be added
        else:
            return render(request, 'chat/addcontact.html', {
                'username': mark_safe(json.dumps(request.user.username)),
                'allcontacts': new_contacts
            })


@login_required(login_url='login/')
def profile(request, username):
    logged_user = request.user
    user = User.objects.get(username=username)
    return render(request, 'chat/profile.html', {
        'logged_user': logged_user,
        'user': user
    })


@login_required(login_url='login/')
def edit(request):
    #  If POST request
    if request.method == "POST":
        email = request.POST["email"]
        gender = request.POST["gender"]
        age = request.POST["age"]
        status = request.POST["status"]
        if status == "":
            status = "Hey there, I am using Chaticon"
        avatar = request.POST["avatar-link"]

        # Attempt to edit user
        try:
            user = User.objects.get(username=request.user)
            user.email = email
            user.gender = gender
            user.age = age
            user.status = status
            user.avatar = avatar
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "chat/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect('/')

    #  If GET request
    else:
        logged_user = request.user
        return render(request, 'chat/edit.html', {
            'user': logged_user
        })
