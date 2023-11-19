# crypto_highlights/management/commands/add_crypto_data.py

from django.core.management.base import BaseCommand
from mainApp.models import Cryptocurrency

class Command(BaseCommand):
    help = 'Add data to the Crypto model'

    def handle(self, *args, **options):
        # Add data to the Crypto model
        crypto_data = [
        {
            "name": "Bitcoin",
            "price": 34500,
            "one_hour_change": 0.27,
            "one_hour_flag": -1,
            "twenty_four_hour_change": 0.67,
            "twenty_four_hour_flag": -1,
            "market_cap": 673,
            "volume": 1734565467567
        },
        {
            "name": "Ethereum",
            "price": 2600,
            "one_hour_change": 0.42,
            "one_hour_flag": 1,
            "twenty_four_hour_change": 1.25,
            "twenty_four_hour_flag": 1,
            "market_cap": 456577868,
            "volume": 3537758
        },
        {
            "name": "Solana",
            "price": 1.23,
            "one_hour_change": 0.11,
            "one_hour_flag": -1,
            "twenty_four_hour_change": 0.75,
            "twenty_four_hour_flag": -1,
            "market_cap": 436586,
            "volume": 76879780
        },
        {
            "name": "XRP",
            "price": 155,
            "one_hour_change": 0.33,
            "one_hour_flag": 1,
            "twenty_four_hour_change": 0.85,
            "twenty_four_hour_flag": 1,
            "market_cap": 4368790,
            "volume": 3245678
        },
        {
            "name": "BNB",
            "price": 2.45,
            "one_hour_change": 0.28,
            "one_hour_flag": 1,
            "twenty_four_hour_change": 0.92,
            "twenty_four_hour_flag": 1,
            "market_cap": 345678,
            "volume": 2345678
        }
    
        ]

        for data in crypto_data:
            Cryptocurrency.objects.create(**data)

        self.stdout.write(self.style.SUCCESS('Successfully added data to the Crypto model'))
