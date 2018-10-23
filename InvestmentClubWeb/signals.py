from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from InvestmentClubWeb.models import Profile, JournalEntry, Stock, StockAsset, Ledger


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    When a user is created, this functions detects the django signal and creates a corresponding Profile for the user.

    :param sender: Model triggering the signal
    :param instance: ??
    :param created: ??
    :param kwargs: other keyword arguments that are sent.
    :return: N/A
    """
    if created:
        Profile.objects.create(user=instance, units=0)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    When a user account is modified, this function detects the django signal and ensures the Profile and user are in
    sync.

    :param sender: Model triggering the signal
    :param instance: ??
    :param kwargs: other keyword arguments that are sent.
    :return:
    """
    instance.profile.save()


@receiver(post_save, sender=JournalEntry)
def create_journal_entry(sender, instance, created, **kwargs):
    """
    do any required calculations here
    :param sender: sender is the Model being created
    :param instance:  ???
    :param created: ??
    :param kwargs: other keyword arguments that are sent.
    :return:
    """
    if created:
        pass


@receiver(post_save, sender=Stock)
def create_stock_entry(sender, instance, created, **kwargs):
    if created:
        Ledger.objects.create(name=instance)


def buy_shares(asset):
    """
    this function provides the JournalEntry for buying shares

    :param asset: StockAsset object
    :return: N/A
    """
    # actual stock transaction
    JournalEntry.objects.create(notes='Stock purchase: {} shares of {}'.format(asset.shares, asset.stock),
                                debit_ledger=Ledger.objects.get(name=asset.stock),
                                debit_amount=asset.shares*asset.cost_per_share,
                                credit_ledger=Ledger.objects.get(name='cash'),
                                credit_amount=asset.shares*asset.cost_per_share)
    # broker trade expense
    JournalEntry.objects.create(notes='Stock purchase {} shares of {}'.format(asset.shares, asset.stock),
                                debit_ledger=Ledger.objects.get(name='cash'),
                                debit_amount=6.95,
                                credit_ledger=Ledger.objects.get(name="trade expense"),
                                credit_amount=6.95)


def sell_shares(asset):
    """
    this function provides the JournalEntry for buying shares

    :param asset: StockAsset object
    :return: N/A
    """
    JournalEntry.objects.create(notes='Stock sell: {} shares of {}'.format(asset.shares, asset.stock),
                                debit_ledger=Ledger.objects.get(name='cash'),
                                debit_amount=asset.shares * asset.cost_per_share,
                                credit_ledger=Ledger.objects.get(name=asset.stock),
                                credit_amount=asset.shares * asset.cost_per_share)
    # broker trade expense
    JournalEntry.objects.create(notes='Stock purchase {} shares of {}'.format(asset.shares, asset.stock),
                                debit_ledger=Ledger.objects.get(name='cash'),
                                debit_amount=6.95,
                                credit_ledger=Ledger.objects.get(name="trade expense"),
                                credit_amount=6.95)


@receiver(post_save, sender=StockAsset)
def create_stock_asset(sender, instance, created, **kwargs):
    if created:
        if instance.shares > 0:
            buy_shares(instance)
        elif instance.shares < 0:
            sell_shares(instance)
        else:
            raise(ValueError('Number of shares cannot be 0'))
