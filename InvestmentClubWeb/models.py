from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime

MARKET_CHOICES = (
    ('nasdaq', 'NASDAQ'),
    ('nyse', 'NYSE')
)


class Stock(models.Model):
    symbol = models.CharField(max_length=6)
    market_exchange = models.CharField(max_length=10, choices=MARKET_CHOICES, default='nasdaq')

    def __str__(self):
        return '{}'.format(self.symbol)


class StockAsset(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date_purchased = models.DateField('Date Purchased', default=datetime.date.today)
    shares = models.IntegerField('Number of Shares owned', default=0)
    cost_per_share = models.FloatField('Cost per Share', default=0.0)

    def __str__(self):
        return '{}.{}'.format(self.stock.symbol, self.date_purchased)


class Ledger(models.Model):
    name = models.CharField(max_length=160, default='cash')

    def __str__(self):
        return self.name


class JournalEntry(models.Model):
    date = models.DateTimeField('Date of Activity', default=datetime.date.today)
    notes = models.CharField(max_length=500, default='')
    debit_ledger = models.ForeignKey(Ledger, related_name="debit_ledger", on_delete=models.CASCADE)
    credit_ledger = models.ForeignKey(Ledger, related_name="credit_ledger", on_delete=models.CASCADE)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    join_date = models.DateField('Date Joined', default=datetime.date.today)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
