from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name = "create"),
    path("auction/<int:auction_id>", views.auction, name="auction"),
    path("auction/<int:auction_id>/close", views.close, name="close"),
    path("auction/watchlist", views.watchlist, name="watchlist"),
    path("auction/add_watchlist/<int:auction_id>", views.add_watchlist, name = "add_watchlist"),
    path("auction/comment/<int:auction_id>", views.comment, name="comment"),
    path("categories", views.category_list, name="category_list"),
    path("auction_by_category/<str:category_name>", views.auction_by_category, name="auction_by_category")
]
