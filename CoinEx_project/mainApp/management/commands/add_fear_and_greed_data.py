# crypto_highlights/management/commands/add_fear_and_greed_data.py

from django.core.management.base import BaseCommand
from mainApp.models import FearAndGreedIndex

class Command(BaseCommand):
    help = 'Add data to the FearAndGreedIndex model'

    def handle(self, *args, **options):
        # Add data to the FearAndGreedIndex model
        fear_and_greed_data = [
            {'date': '2023-11-01', 'value': 70},
            {'date': '2023-11-02', 'value': 65},
            {'date': '2023-11-03', 'value': 68},
            {'date': '2023-11-04', 'value': 75},
            {'date': '2023-11-05', 'value': 72},
            {'date': '2023-11-06', 'value': 67},
            {'date': '2023-11-07', 'value': 73},
            {'date': '2023-11-08', 'value': 69},
            {'date': '2023-11-09', 'value': 71},
            {'date': '2023-11-10', 'value': 66},
        ]

        for data in fear_and_greed_data:
            FearAndGreedIndex.objects.create(**data)

        self.stdout.write(self.style.SUCCESS('Successfully added data to the FearAndGreedIndex model'))
