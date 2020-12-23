import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt


from .models import User
from .models import Post


# Padination function to display 10 posts at the page
def paginator(request, all_posts):
    paginator = Paginator(all_posts, 10)
    page = request.GET.get("page")
    paged_posts = paginator.get_page(page)

    return paged_posts


def index(request):
    # Get all the post in reversed chronological order
    all_posts = Post.objects.all().order_by("-created")
    paged_posts = paginator(request, all_posts)

    return render(request, "network/index.html", {
        "posts": paged_posts
    })


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        print(user)
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


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
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


# Create new post
@login_required(login_url='login')
def create_post(request):
    print(request.user)
    if request.method == "POST":
        post = Post()
        post.post = request.POST["post-content"]
        post.creator = request.user
        post.save()
    # return render(request, "network/index.html")
    return HttpResponseRedirect(reverse("index"))


# Edit post
@csrf_exempt
@login_required(login_url='login')
def edit_post(request, post_id):
        # Edit post if request is PUT
    if request.method =="PUT":
        # Find the requested post
        post = Post.objects.get(id=post_id)

        # If post is not found, send back error msg
        if not post:
            return JsonResponse({"error": "Post not found."}, status=404)
        
        # Update post content
        new_data = json.loads(request.body)
        # new assignment to the content field of the post
        post.post = new_data['content']

        # save changes/updates
        post.save()
        
        return HttpResponse(status=204)

    # Request must be via PUT
    else:
        return JsonResponse({"error": "PUT request required."}, status=400)

# Toggle like post
@csrf_exempt
@login_required(login_url='login')
def toggle_like(request, post_id):
    print(post_id)
    # Toggle request must be PUT
    if request.method == "PUT":
        # checking the requested post
        post = Post.objects.filter(id=post_id)
        if not post:
            print("POST NOT FOUND")
            return JsonResponse({"error": "Your post is not found"}, status=404)
        print(post[0])
        # toggle post like
        if request.user in post[0].likes.all():
            print("liked will be unliked")
            post[0].likes.remove(request.user)
        else:
            print("adding like")
            print(request.user)
            print(post[0].likes)
            post[0].likes.add(request.user)

        # save changes
        post[0].save()
        return HttpResponse(status=204)
    else:
        return JsonResponse({"error": "PUT request required."}, status=400)

# Save changes in post
@login_required(login_url='login')
def save_changes(request):
    # new post content
    post_content = request.POST["post-content"]

    # existing post from db
    existing_post = Post.objects.get(id=request.POST["save"])

    # save new post
    existing_post.post = post_content
    existing_post.save()

    return index(request)


# user profile
@login_required(login_url='login')
def profile(request, username):
    
    # Pull out the user and his posts info from db
    profile = User.objects.get(username=username)
    print(profile.following.all())
    print(profile.followers.all())

    # Pull out all of the posts for the user, in reverse chronological order.
    posts = Post.objects.filter(creator=profile).order_by("-created")

    # Call for paginator function
    paged_posts = paginator(request, posts)

    return render(request, "network/profile.html", {
        "username": profile,
        "posts": paged_posts,
    })

# Toggle following
@login_required
def toggle_following(request, profile_username):
    # Pull out the profile user info from db
    profile_user = User.objects.get(username = profile_username)
    print(profile_user)

    # Check if the current user in the list of followers in profile_user
    # Unfollow if current user is following the profile_user
    if request.user in profile_user.followers.all():
        request.user.following.remove(profile_user)
        print("inside remove")
    # Follow if current user is unfollowing the profile_user
    else:
        request.user.following.add(profile_user)
        print("inside add")
    return HttpResponseRedirect(reverse("profile", args=(profile_username,)))

# Page displays all users that signed user follows
@login_required
def following(request):
    # Pull out the list of all posts that crwators are followed by logged in user
    # '__in' syntax - In a given iterable; often a list, tuple, or queryset.
    # equivalent in SQL: SELECT ... WHERE id IN (1, 3, 4);
    all_posts = Post.objects.filter(creator__in=request.user.following.all()).order_by("-created")
    
    # Call for paginator function
    paged_posts = paginator(request, all_posts)

    return render(request, "following.html", {
        "posts": paged_posts
    })