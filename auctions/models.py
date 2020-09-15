from django.contrib.auth.models import AbstractUser
from django.db import models




class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"


class Auction(models.Model):
    

    name = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    photo = models.CharField(max_length=200, default='SOME STRING')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctions")
    isClosed = models.CharField(max_length=10, default='FALSE')
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="won_auction", null=True)
    watchlisted = models.ManyToManyField(User, blank=True, related_name="watchlisted")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="auctions", null = True)
    
    
    def __str__(self):
        return f"{self.name} {self.description}"




class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids", null=True)
    price = models.FloatField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid", null=True)
    


    def __str__(self):
        return f"{self.price}"

class Comment(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comments", null=True)
    content = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment", null=True)

    def __str__(self):
        return f"{self.content} by {self.owner.username}"






