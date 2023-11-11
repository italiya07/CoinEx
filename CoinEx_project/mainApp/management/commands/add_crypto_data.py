# crypto_highlights/management/commands/add_crypto_data.py

from django.core.management.base import BaseCommand
from mainApp.models import Crypto

class Command(BaseCommand):
    help = 'Add data to the Crypto model'

    def handle(self, *args, **options):
        # Add data to the Crypto model
        crypto_data = [
            {'name': 'Bitcoin', 'symbol': 'BTC', 'today_price': 50000.00},
            {'name': 'Ethereum', 'symbol': 'ETH', 'today_price': 3000.00},
            {'name': 'Binance Coin', 'symbol': 'BNB', 'today_price': 400.00},
            {'name': 'Cardano', 'symbol': 'ADA', 'today_price': 2.50},
            {'name': 'Solana', 'symbol': 'SOL', 'today_price': 150.00},
        ]

        for data in crypto_data:
            Crypto.objects.create(**data)

        self.stdout.write(self.style.SUCCESS('Successfully added data to the Crypto model'))
