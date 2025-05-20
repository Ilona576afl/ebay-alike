
from django.urls import path
from . import views

urlpatterns = [
    path("listing/<int:listing_id>/", views.listing, name="listing"),
    path("listing/<int:listing_id>/bid/", views.bid, name="bid"),
    path("listing/<int:listing_id>/comment/", views.comment, name="comment"),
    path("listing/<int:listing_id>/watchlist/", views.toggle_watchlist, name="toggle_watchlist"),
    path("listing/<int:listing_id>/close/", views.close, name="close"),

    path("create/", views.create, name="create"),
    path("", views.index, name="index"),
]
