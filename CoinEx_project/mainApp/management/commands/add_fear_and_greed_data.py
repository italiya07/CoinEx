# myapp/management/commands/populate_data.py

import os
from django.core.management.base import BaseCommand
from django.utils import timezone
from random import randint
from datetime import timedelta
from mainApp.models import FearAndGreedIndex


class Command(BaseCommand):
    help = 'Populate FearAndGreedIndex model with synthetic data'

    def handle(self, *args, **options):
        # Set the start and end dates for data generation
        start_date = timezone.datetime(2023, 9, 1).date()
        end_date = timezone.datetime(2023, 11, 29).date()

        # Clear existing data
        self.stdout.write(self.style.SUCCESS('Deleting existing data...'))
        FearAndGreedIndex.objects.all().delete()

        # Generate and insert new data with varying trends
        self.stdout.write(self.style.SUCCESS('Populating data...'))
        current_date = start_date
        trend_direction = 1  # 1 for upward trend, -1 for downward trend
        base_value = randint(30, 70)  # Base value for the index

        while current_date <= end_date:
            index_value = base_value + trend_direction * randint(0, 10)
            FearAndGreedIndex.objects.create(date=current_date, value=index_value)

            # Toggle the trend direction after every 10 days
            if (current_date - start_date).days % 10 == 0:
                trend_direction *= -1

            current_date += timedelta(days=1)

        self.stdout.write(self.style.SUCCESS('Data population complete.'))
