import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse

from .models import User, Post, Like, Relation


def index_view(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def latest_post_id_view(request):
    if request.method == "GET":
        # Get all Post objects
        posts = Post.objects.all()
        # Get id
        latest_post_id = posts[len(posts)-1].id
        # Return id as JSON
        return JsonResponse({"id": int(latest_post_id)})


def all_posts_view(request):
    if request.method == "GET":
        # Get all Post objects
        posts = Post.objects.all()
        # Return posts as JSON
        return JsonResponse([post.serialize() for post in posts], safe=False)


def single_post_view(request, post_id):
    if request.method == "GET":
        # Get Post object with matching id
        try:
            post = Post.objects.get(id=post_id)
        # If does not exist, return error message as JSON
        except Post.DoesNotExist:
            return JsonResponse({
                # TODO create custom page for that exception/message it on main page
                "error": "Post with that id does not exist."
            }, safe=False, status=404)
        # If does exist, return as JSON
        return JsonResponse(post.serialize())


@login_required
def compose_new_post_view(request):
    pass
