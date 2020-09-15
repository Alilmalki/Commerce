from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.db.models import Max

from .models import *

class NewBidForm(forms.Form):
    price = forms.FloatField(label = "price")

def index(request):
    #pass list of auctions if user.authenticated
    
    return render(request, "auctions/index.html", {
        "auctions": Auction.objects.all()
    })


def auction(request, auction_id):

    auction = Auction.objects.get(pk=auction_id)
    last_bid = auction.bids.latest('id')
    watchlisted = request.user.watchlisted.all()
    isWatchlist = False

    for watchlist in watchlisted:
        if watchlist == auction:#the auction is in the watchlist of the user
            isWatchlist = True
            break


    
    if request.method == "POST":#placing a bid
                

        form = NewBidForm(request.POST)

        if form.is_valid():
            price = form.cleaned_data["price"]
            

        if price > last_bid.price:
            bid = Bid(auction = auction, price = price, bidder = request.user)
            bid.save()
            return HttpResponseRedirect(reverse("auction", args=(auction_id,)))#go to this functio again but skipping the first if statement
        else:
            return render(request, "auctions/error.html", {
                "auction_id": auction_id
            })

    else:
        return render(request, "auctions/auction.html", {
            "auction": auction,
            "last_bid_owner":last_bid.bidder,
            "comments":auction.comments.all(),
            "isWatchlist":isWatchlist,
            "category": auction.category
        })

def create(request):
    if request.method == "POST":

        name = request.POST["name"]
        description = request.POST["description"]
        owner = request.user
        photo = request.POST["photo"]

        auction = Auction(name = name, description = description, photo = photo, owner = owner)
        auction.save()

        form = NewBidForm(request.POST)

        if form.is_valid():
            price = form.cleaned_data["price"]
            


        b = Bid(price=price, auction=auction, bidder = owner)
        b.save()
        

        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "auctions/create.html")



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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def category_list(request):
    categories = Category.objects.all()

    return render(request, "auctions/category_list.html", {
        "categories":categories
    })


def auction_by_category(request, category_name):
    category = Category.objects.get(name=category_name)
    
    auctions = category.auctions.all()
    return render(request, "auctions/index.html", {
        "auctions":auctions
    })


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def close(request, auction_id):

    if request.method == "POST":

        auction = Auction.objects.get(pk=auction_id)

        last_bid = auction.bids.latest('id')

        Auction.objects.filter(pk=auction_id).update(isClosed="TRUE")
        Auction.objects.filter(pk=auction_id).update(winner=last_bid.bidder)

        return HttpResponseRedirect(reverse("index"))


def watchlist(request):
    auctions = request.user.watchlisted.all()

    return render(request, "auctions/watchlist.html", {#better render auctions/index.html
        "auctions":auctions
    })

def add_watchlist(request, auction_id):

    if request.method == "POST":
        auction = Auction.objects.get(pk=auction_id)
        request.user.watchlisted.add(auction)
        return HttpResponseRedirect(reverse("watchlist"))
    else:
        return HttpResponseRedirect(reverse("auction", args=(auction_id,)))

def comment(request, auction_id):
    if request.method == "POST":
        auction = Auction.objects.get(pk=auction_id)
        content = request.POST["content"]
        owner = request.user
        comment = Comment(auction = auction, content = content, owner = owner)
        comment.save()
        return HttpResponseRedirect(reverse("auction", args=(auction_id,)))
    else:
        pass


