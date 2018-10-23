from django.apps import AppConfig


class InvestmentclubwebConfig(AppConfig):
    name = 'InvestmentClubWeb'

    def ready(self):
        import InvestmentClubWeb.signals
