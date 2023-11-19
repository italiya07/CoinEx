# crypto_highlights/management/commands/add_fear_and_greed_data.py
from django.core.management.base import BaseCommand
from mainApp.models import FearAndGreedIndex
from datetime import date, timedelta
import random

class Command(BaseCommand):
    help = 'Add data to the FearAndGreedIndex model'

    def handle(self, *args, **options):
        # Add data to the FearAndGreedIndex model
        fear_and_greed_data = self.generate_data_points()

        for data in fear_and_greed_data:
            FearAndGreedIndex.objects.create(**data)

        self.stdout.write(self.style.SUCCESS('Successfully added data to the FearAndGreedIndex model'))

    def generate_data_points(self):
        # Generate 60 data points for the last 2 months (September 2023 to October 2023)
        start_date = date(2023, 9, 1)
        end_date = date(2023, 10, 31)
        delta = timedelta(days=1)

        data_points = []

        current_value = random.randint(60, 80)

        while start_date <= end_date:
            # Simulate a dip in the middle of the period
            if start_date == date(2023, 9, 15):
                current_value -= 10

            # Simulate an increase after the dip
            if start_date == date(2023, 9, 30):
                current_value += 15

            data_points.append({
                'date': start_date,
                'value': current_value,
            })

            start_date += delta

        return data_points
