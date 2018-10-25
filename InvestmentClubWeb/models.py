from django.db import models
from django.contrib.auth.models import User
import datetime

MARKET_CHOICES = (
    ('nasdaq', 'NASDAQ'),
    ('nyse', 'NYSE')
)


class Stock(models.Model):
    """
    Stock class that carries the type of stock researched / purchased, and the exchange it is traded on
    """
    symbol = models.CharField(max_length=6)
    market_exchange = models.CharField(max_length=10, choices=MARKET_CHOICES, default='nasdaq')

    def __str__(self):
        return '{}'.format(self.symbol)


class StockAsset(models.Model):
    """
    This is a single stock asset transaction. (e.g., buying 5 shares of MSFT at $81.00 per share)
    This is a
    """
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date_transaction = models.DateField('Date of Transaction', default=datetime.date.today)
    shares = models.IntegerField('Number of Shares owned', default=0)
    cost_per_share = models.FloatField('Cost per Share', default=0.0)

    def __str__(self):
        return '{}.{}'.format(self.stock.symbol, self.date_transaction)

    def get_stock(self):
        return self.stock.symbol

    def get_shares(self):
        return self.shares


class Ledger(models.Model):
    name = models.CharField(max_length=160, default='cash')

    def __str__(self):
        return self.name


class JournalEntry(models.Model):
    date = models.DateField('Date of Activity', default=datetime.date.today)
    notes = models.CharField(max_length=500, default='')
    debit_ledger = models.ForeignKey(Ledger, related_name="debit_ledger", on_delete=models.CASCADE)
    debit_amount = models.FloatField(default=0.0)
    credit_ledger = models.ForeignKey(Ledger, related_name="credit_ledger", on_delete=models.CASCADE)
    credit_amount = models.FloatField(default=0.0)
    # TODO build logic into model to check where debit_amount === credit_amount
    # TODO build logic to allow multiple credit, or debit line items in a single transaction Issue #1


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    join_date = models.DateField('Date Joined', default=datetime.date.today)
    units = models.FloatField('Number of Units Owned', default=0)

    def get_ytd_paid_in(self):
        return 4

    def get_total_paid_in(self):
        """
        a function which will grab all transactions from the general ledger, and add all the debits together, and
        subtract all the credits

        :return: total sum of all transactions within general ledger
        """
        debit_results = JournalEntry.objects.filter(debit_ledger=self.user.username)
        credit_results = JournalEntry.objects.filter(credit_ledger=self.user.username)
        sum = 0
        for x in debit_results:
            sum += x.debit_amount
        for x in credit_results:
            sum -= x.credit_amount
        return sum

    def get_paid_in_plus_earnings(self):
        return 12

    def get_ytd_units(self):
        return 10

    def get_total_units(self):
        return 5

    def get_market_value(self):
        return 6

    def __str__(self):
        return '{}'.format(self.user.username)
