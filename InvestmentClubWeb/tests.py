from django.test import TestCase
import random
import string
from InvestmentClubWeb import models
from django.contrib.auth.models import User
import datetime


def rand_string(rrange=25):
    """
    creates a random string of rrange characters

    :param rrange: number of random characters in the desired string
    :return: a random length string of random characters
    """
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(rrange))


def rand_int(rmin=30000, rmax=70000):
    """
    creates a random integer between rmin and rmax

    :param rmin: lowest integer possible
    :param rmax: highest integer possible
    :return: a random integer
    """
    return random.randint(rmin, rmax)


def rand_float(rmin=0.000001, rmax=20000.9999999):
    """
    creates a random float between rmin and rmax

    :param rmin: lowest float possible
    :param rmax: highest float possible
    :return: a random float
    """
    return random.uniform(rmin, rmax)


def rand_datetime():
    """
    creates a random datetime that is +-1000 days from today.

    :return: returns a random datetime
    """
    c = datetime.datetime.utcnow()
    return str(c + datetime.timedelta(minutes=random.randrange(60),
                                      hours=random.randrange(24),
                                      days=random.randrange(1000)))


def create_stock():
    """
    creates a random stock object

    :return: a random stock with a random symbol and random market exchange
    """
    return models.Stock.objects.create(symbol=rand_string(4), market_exchange=rand_string(5))


def create_user():
    """
    creates a random user object

    :return: a random user
    """
    return User.objects.create(first_name=rand_string(10),
                               last_name=rand_string(10),
                               username=rand_string(10),
                               email='{}@{}.com'.format(rand_string(10),rand_string(7)))


class StockTestCase(TestCase):
    fixtures = ['ledgers.json', 'users.json']

    def setUp(self):
        self.market = rand_string(4)
        self.symbol = rand_string(4)
        models.Stock.objects.create(symbol=self.symbol, market_exchange=self.market)

    def test_create_stock(self):
        stock1 = models.Stock.objects.get(symbol=self.symbol)
        self.assertEqual(stock1.symbol, self.symbol)
        self.assertEqual(stock1.market_exchange, self.market)

    def test_created_ledger(self):
        """this tests that a corresponding ledger was created when the stock was created"""
        stock = create_stock()
        stock_ledger = models.Ledger.objects.get(name=stock.symbol)
        self.assertEqual(stock_ledger.name, stock.symbol)

    def test_created_ledgers_fixture(self):
        cash_ledger = models.Ledger.objects.get(name='cash')
        self.assertEqual(cash_ledger.name, 'cash')


class StockAssetTestCase(TestCase):
    fixtures = ['ledgers.json', 'users.json']

    def setUp(self):
        pass

    def test_create_stockasset(self):
        rand_stock = create_stock()
        rand_shares = rand_int(3, 1000)
        rand_price = rand_float()
        rand_asset = models.StockAsset.objects.create(stock=rand_stock, shares=rand_shares, cost_per_share=rand_price)
        self.assertEqual(rand_asset.stock, rand_stock)
        self.assertEqual(rand_asset.shares, rand_shares)
        self.assertEqual(rand_asset.cost_per_share, rand_price)
        self.assertEqual(rand_asset.date_transaction, datetime.date.today())


class ProfileTestCase(TestCase):
    fixtures = ['ledgers.json', 'users.json']

    def setUp(self):
        pass

    def test_create_user(self):
        first_name = rand_string(10)
        last_name = rand_string(10)
        username = rand_string(10)
        email = '{}@{}.com'.format(rand_string(10), rand_string(7))
        user = User.objects.create(first_name=first_name,
                                   last_name=last_name,
                                   username=username,
                                   email=email)
        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)
        self.assertEqual(user.username, username)
        self.assertEqual(user.email, email)
        profile = models.Profile.objects.get(user=user)
        self.assertEqual(profile.user.first_name, first_name)
        self.assertEqual(profile.user.last_name, last_name)
        self.assertEqual(profile.user.username, username)
        self.assertEqual(profile.user.email, email)
        self.assertEqual(profile.units, 0)


# class DuesTestCase(TestCase):
#     fixtures = ['ledgers.json', 'users.json']
#
#     def setUp(self):
#         self.members = []
#         for x in range(rand_int(10)):
#             self.members.append(create_user())
#
#     def test_journal_entry(self):
#         for x in self.members:
#


class JournalTestCase(TestCase):
    fixtures = ['ledgers.json', 'users.json']

    def setUp(self):
        pass

    def test_ref_journal_buy_stocks(self):
        rand_stock = create_stock()
        rand_shares = rand_int(3, 1000)
        rand_price = rand_float()
        rand_asset = models.StockAsset.objects.create(stock=rand_stock, shares=rand_shares, cost_per_share=rand_price)
        self.assertEqual(rand_asset.stock, rand_stock)
        self.assertEqual(rand_asset.shares, rand_shares)
        self.assertEqual(rand_asset.cost_per_share, rand_price)
        self.assertEqual(rand_asset.date_transaction, datetime.date.today())
        journal = models.JournalEntry.objects.get(date=datetime.date.today())
        self.assertEqual(rand_asset.stock.symbol, journal.debit_ledger.name)
        self.assertEqual(rand_asset.shares * rand_asset.cost_per_share, journal.debit_amount)

    def test_ref_journal_buy_stocks(self):
        rand_stock = create_stock()
        rand_shares = rand_int(-1000, -3)
        rand_price = rand_float()
        rand_asset = models.StockAsset.objects.create(stock=rand_stock, shares=rand_shares, cost_per_share=rand_price)
        self.assertEqual(rand_asset.stock, rand_stock)
        self.assertEqual(rand_asset.shares, rand_shares)
        self.assertEqual(rand_asset.cost_per_share, rand_price)
        self.assertEqual(rand_asset.date_transaction, datetime.date.today())
        journal = models.JournalEntry.objects.get(date=datetime.date.today())
        self.assertEqual(rand_asset.stock.symbol, journal.credit_ledger.name)
        self.assertEqual(rand_asset.shares * rand_asset.cost_per_share, journal.credit_amount)





