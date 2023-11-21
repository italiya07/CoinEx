# crypto_highlights/management/commands/add_news_data.py
from datetime import date

from django.core.management.base import BaseCommand
from mainApp.models import News

class Command(BaseCommand):
    help = 'Add data to the News model'

    def handle(self, *args, **options):
        # Add data to the News model
        news_data = [
            {'title': 'Bitcoin Hits New All-Time High', 'link': 'https://example.com/bitcoin-news1',
             'published_date': date(2022, 1, 10)},
            {'title': 'Ethereum Upgrades to Ethereum 2.0', 'link': 'https://example.com/ethereum-news1',
             'published_date': date(2022, 2, 15)},
            {'title': 'Binance Launches NFT Marketplace', 'link': 'https://example.com/binance-news1',
             'published_date': date(2022, 3, 20)},
            {'title': 'Cardano Announces Smart Contract Integration', 'link': 'https://example.com/cardano-news1',
             'published_date': date(2022, 4, 25)},
            {'title': 'Solana Surpasses All-Time High in Daily Transactions',
             'link': 'https://example.com/solana-news1', 'published_date': date(2022, 5, 30)},
            {'title': 'Polkadot Partners with Major Tech Firm', 'link': 'https://example.com/polkadot-news1',
             'published_date': date(2022, 6, 5)},
            {'title': 'Ripple Faces Legal Challenges', 'link': 'https://example.com/ripple-news1',
             'published_date': date(2022, 7, 10)},
            {'title': 'Dogecoin Community Raises Funds for Charity', 'link': 'https://example.com/dogecoin-news1',
             'published_date': date(2022, 8, 15)},
            {'title': 'Avalanche Launches DeFi Platform', 'link': 'https://example.com/avalanche-news1',
             'published_date': date(2022, 9, 20)},
            {'title': 'Chainlink Partners with Leading Data Provider', 'link': 'https://example.com/chainlink-news1',
             'published_date': date(2022, 10, 25)},
            {'title': 'Bitcoin Reaches $100,000 Milestone', 'link': 'https://example.com/bitcoin-news2',
             'published_date': date(2022, 11, 30)},
            {'title': 'Ethereum Surges Amidst Growing Adoption', 'link': 'https://example.com/ethereum-news2',
             'published_date': date(2022, 12, 5)},
            {'title': 'Cryptocurrency Market Sees Year-End Rally', 'link': 'https://example.com/crypto-news1',
             'published_date': date(2022, 12, 31)},
            {'title': 'Top Altcoins to Watch in 2023', 'link': 'https://example.com/crypto-news2',
             'published_date': date(2023, 1, 10)},
            {'title': 'NFT Craze Continues in the Art World', 'link': 'https://example.com/nft-news1',
             'published_date': date(2023, 2, 15)},
            {'title': 'Decentralized Finance Gains Traction', 'link': 'https://example.com/defi-news1',
             'published_date': date(2023, 3, 20)},
            {'title': 'Cardano Implements Major Protocol Upgrade', 'link': 'https://example.com/cardano-news2',
             'published_date': date(2023, 4, 25)},
            {'title': 'Bitcoin Mining Council Formed for Sustainable Practices',
             'link': 'https://example.com/bitcoin-news3', 'published_date': date(2023, 5, 30)},
            {'title': 'Ethereum 2.0 Phase 2 Development Begins', 'link': 'https://example.com/ethereum-news3',
             'published_date': date(2023, 6, 5)},
            {'title': 'Binance Launches New Fiat-to-Crypto Onramp', 'link': 'https://example.com/binance-news2',
             'published_date': date(2023, 7, 10)},
            {'title': 'Bitcoin Price Surges Ahead of Thanksgiving', 'link': 'https://example.com/bitcoin-news4',
             'published_date': date(2023, 10, 5)},
            {'title': 'Ethereum Developers Introduce EIP-1559 Upgrade', 'link': 'https://example.com/ethereum-news4',
             'published_date': date(2023, 10, 15)},
            {'title': 'Major Exchanges Implement Security Enhancements', 'link': 'https://example.com/exchange-news1',
             'published_date': date(2023, 10, 25)},
            {'title': 'Cardano Launches Developer Grant Program', 'link': 'https://example.com/cardano-news3',
             'published_date': date(2023, 11, 5)},
            {'title': 'New NFT Platforms Showcase Digital Art Collections', 'link': 'https://example.com/nft-news2',
             'published_date': date(2023, 11, 15)},
            {'title': 'DeFi Protocols Continue to Expand Across Chains', 'link': 'https://example.com/defi-news2',
             'published_date': date(2023, 11, 19)},
            {'title': 'Bitcoin Hits New All-Time High in November Rally', 'link': 'https://example.com/bitcoin-news5',
             'published_date': date(2023, 11, 10)},
            {'title': 'Ethereum 2.0 Phase 1 Reaches Completion', 'link': 'https://example.com/ethereum-news5',
             'published_date': date(2023, 11, 21)},
            {'title': 'Top Altcoins to Watch in the Coming Months', 'link': 'https://example.com/crypto-news3',
             'published_date': date(2023, 11, 20)},
            {'title': 'Latest Developments in Decentralized Finance', 'link': 'https://example.com/defi-news3',
             'published_date': date(2023, 10, 10)},
        ]

        for data in news_data:
            News.objects.create(**data)

        self.stdout.write(self.style.SUCCESS('Successfully added data to the News model'))
