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
    '''
    Returns JSON response with value of id of latest post.
    _____________________________________________
    If post not found, returns JSON response with error: Post not found.
    '''
    if request.method == "GET":
        try:
            post = Post.objects.latest('id')
        except Post.DoesNotExist:
            return JsonResponse({
                "error": "Post not found."
            }, safe=False, status=404)
        latest_post_id = int(post.id)
        return JsonResponse({
            "id": latest_post_id
            }, safe=False, status=200)


def all_posts_view(request):
    if request.method == "GET":
        try:
            posts = Post.objects.all()
        except Post.DoesNotExist:
            return JsonResponse({
                "error": "Post not found."
            }, safe=False, status=404)
        return JsonResponse([post.serialize() for post in posts], safe=False)


def single_post_view(request, post_id):
    #TODO: Refactor this function - REST
    '''
    Returns JSON response, depending on what HTTP method was passed in request:
    - for method GET:
        JSON with post data with 'id' matching 'post_id' passed in request,
    - for method PUT:
        JSON with confirmaton message that post was succesfully updated,
    - for method DELETE:
        JSON with confirmation message that post was succesfully deleted.
    _____________________________________________
    If post with matching id not found,
    returns JSON response with error: Post not found.
    Additionally for PUT and DELETE methods, if user was not authenticated
    or user does not have permissions required,
    returns JSON response with error: Permission denied.
    '''
    try:
        post = Post.objects.get(id=post_id)
    except ValueError:
        return JsonResponse({
            "error": "Bad request. 'id' expected to be a number."
        }, safe=False, status=400)
    except Post.DoesNotExist:
        return JsonResponse({
            "error": "Post not found."
        }, safe=False, status=404)

    if request.method == "GET":
        return JsonResponse(post.serialize())

    post_owner = User.objects.get(id=post.user_id)

    if request.method == "PUT":
        if request.user.is_authenticated == True:
            if request.user == post_owner:
                return
            else:
                return JsonResponse({
                    "error": "Permission denied."
                }, safe=False, status=403)
        else:
            return JsonResponse({
                "error": "Permission denied."
            }, safe=False, status=403)

    if request.method == "DELETE":
        if request.user.is_authenticated == True:
            if request.user == post_owner:
                post.delete()
                return JsonResponse({
                    "message": "Post deleted successfully."
                }, safe=False, status=200)
            else:
                return JsonResponse({
                    "error": "Permission denied."
                }, safe=False, status=403)
        else:
            return JsonResponse({
                "error": "Permission denied."
            }, safe=False, status=403)


@login_required
def compose_new_post_view(request):
    pass
