# crypto_highlights/management/commands/add_news_data.py
from django.core.management.base import BaseCommand
from datetime import date, timedelta
from django.utils import timezone
import random
from mainApp.models import News

class Command(BaseCommand):
    help = 'Add data to the News model'

    def handle(self, *args, **options):
        # Add data to the News model
        news_data = [
            {'title': 'Bitcoin Hits New All-Time High', 'link': 'https://example.com/bitcoin-news1'},
            {'title': 'Ethereum Upgrade Announced', 'link': 'https://example.com/ethereum-news2'},
            {'title': 'Cardano Partners with Major Tech Company', 'link': 'https://example.com/cardano-news3'},
            {'title': 'Ripple Faces Regulatory Challenges', 'link': 'https://example.com/ripple-news4'},
            {'title': 'NFT Market Surpasses $1 Billion in Sales', 'link': 'https://example.com/nft-news5'},
            {'title': 'Bitcoin ETF Approved by Regulatory Authority', 'link': 'https://example.com/bitcoin-etf-news6'},
            {'title': 'New DeFi Protocol Launches on Ethereum', 'link': 'https://example.com/defi-news7'},
            {'title': 'Litecoin Halving Event Approaches', 'link': 'https://example.com/litecoin-news8'},
            {'title': 'Binance Launches NFT Marketplace', 'link': 'https://example.com/binance-nft-news9'},
            {'title': 'Ethereum 2.0 Upgrade Progress Update', 'link': 'https://example.com/ethereum-2-news10'},
        ]

        for data in news_data:
            News.objects.create(
                title=data['title'],
                link=data['link'],
                published_date=self.generate_random_date(),
            )

        self.stdout.write(self.style.SUCCESS('Successfully added data to the News model'))

    def generate_random_date(self):
        # Generate a random date between May 2023 and October 2023
        start_date = date(2023, 5, 1)
        end_date = date(2023, 10, 31)
        random_days = random.randint(0, (end_date - start_date).days)
        random_date = start_date + timedelta(days=random_days)
        return timezone.make_aware(timezone.datetime(random_date.year, random_date.month, random_date.day))
