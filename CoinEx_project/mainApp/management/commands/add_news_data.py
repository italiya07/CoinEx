# crypto_highlights/management/commands/add_news_data.py

from django.core.management.base import BaseCommand
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
            News.objects.create(**data)

        self.stdout.write(self.style.SUCCESS('Successfully added data to the News model'))
