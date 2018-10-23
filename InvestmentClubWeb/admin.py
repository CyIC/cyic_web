from django.contrib import admin
from . import models

admin.site.register(models.Stock)
admin.site.register(models.StockAsset)
admin.site.register(models.Ledger)
admin.site.register(models.JournalEntry)