
from django.shortcuts import render
from .models import Listing

def index(request):
    listings = Listing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "listings": listings
    })


from django.shortcuts import render, redirect
from .models import Listing, Category
from django.contrib.auth.decorators import login_required

@login_required
def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        image_url = request.POST["image_url"]
        category_id = request.POST["category"]

        category = Category.objects.get(pk=category_id) if category_id else None

        listing = Listing.objects.create(
            title=title,
            description=description,
            starting_bid=starting_bid,
            image_url=image_url,
            category=category,
            creator=request.user
        )
        return redirect("index")
    return render(request, "auctions/create.html", {
        "categories": Category.objects.all()
    })


from django.shortcuts import get_object_or_404
from .models import Listing, Bid, Comment

def listing(request, listing_id):
    listing_obj = get_object_or_404(Listing, pk=listing_id)
    comments = Comment.objects.filter(listing=listing_obj).order_by("-posted_at")
    on_watchlist = request.user in listing_obj.watchers.all() if request.user.is_authenticated else False

    return render(request, "auctions/listing.html", {
        "listing": listing_obj,
        "comments": comments,
        "on_watchlist": on_watchlist
    })

@login_required
def bid(request, listing_id):
    listing_obj = get_object_or_404(Listing, pk=listing_id)
    try:
        bid_amount = float(request.POST["bid"])
    except:
        return redirect("listing", listing_id=listing_id)

    current_max = listing_obj.bids.order_by("-amount").first()
    min_bid = current_max.amount if current_max else listing_obj.starting_bid

    if bid_amount > min_bid:
        Bid.objects.create(bidder=request.user, listing=listing_obj, amount=bid_amount)
        listing_obj.starting_bid = bid_amount
        listing_obj.save()
    return redirect("listing", listing_id=listing_id)

@login_required
def toggle_watchlist(request, listing_id):
    listing_obj = get_object_or_404(Listing, pk=listing_id)
    if request.user in listing_obj.watchers.all():
        listing_obj.watchers.remove(request.user)
    else:
        listing_obj.watchers.add(request.user)
    return redirect("listing", listing_id=listing_id)

@login_required
def comment(request, listing_id):
    listing_obj = get_object_or_404(Listing, pk=listing_id)
    text = request.POST["comment"]
    Comment.objects.create(listing=listing_obj, author=request.user, content=text)
    return redirect("listing", listing_id=listing_id)

@login_required
def close(request, listing_id):
    listing_obj = get_object_or_404(Listing, pk=listing_id)
    if request.user == listing_obj.creator:
        listing_obj.is_active = False
        listing_obj.save()
    return redirect("listing", listing_id=listing_id)

@login_required
def watchlist(request):
    listings = request.user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "watchlist": listings
    })

def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })

def category_listings(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    listings = Listing.objects.filter(category=category, is_active=True)
    return render(request, "auctions/category_listings.html", {
        "category": category,
        "listings": listings
    })
