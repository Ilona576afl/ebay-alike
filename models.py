
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    watchers = models.ManyToManyField(User, blank=True, related_name='watchlist')

    def __str__(self):
        return f"{self.title} (${self.starting_bid})"

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    placed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount} by {self.bidder} on {self.listing}"

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.listing}"
