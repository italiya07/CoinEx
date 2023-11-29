import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from mainApp.models import News

class Command(BaseCommand):
    help = 'Populate News model with dummy data'

    def handle(self, *args, **options):
        # Delete existing data
        News.objects.all().delete()

        titles = [
            "Breaking News: Bitcoin Surges to a New All-Time High, Breaking Previous Records",
            "Ethereum Successfully Implements ETH 2.0 Upgrade, Bringing Scalability and Sustainability",
            "Crypto Market Experiences Remarkable Surge Following Positive Regulatory Developments",
            "New DeFi Project Gains Unprecedented Traction, Redefining Decentralized Finance",
            "NFT Craze Continues with Record-Breaking Sales and High-Profile Artist Collaborations",
            "Major Exchange Lists Exciting New Altcoin, Generating Buzz Amongst Crypto Enthusiasts",
            "Government Explores Comprehensive Cryptocurrency Legislation to Ensure Market Stability",
            "Blockchain Technology Revolutionizes Supply Chain Management, Ensuring Transparency",
            "Crypto Influencer Makes Bold Predictions for the Next Bull Run, Backed by Analytical Insights",
            "Security Experts Identify Critical Vulnerability in Popular Wallet, Urging Immediate Updates",
            "Central Bank Takes Steps Toward Centralized Digital Currency, Potentially Reshaping Finance",
            "Celebrity Endorses Cryptocurrency on Social Media, Sparking Increased Mainstream Interest",
            "Smart Contracts Transform Legal Industry, Providing Efficient and Transparent Solutions",
            "Investors Flock to Stablecoins Amid Market Volatility, Seeking Safe-Haven Assets",
            "Decentralized Finance Platforms Achieve Billion-Dollar Total Value Locked (TVL), Reshaping Finance",
            "Top Analyst Sets Ambitious Price Target for Leading Cryptocurrency, Citing Positive Indicators",
            "Crypto Exchange Faces Regulatory Investigation Over Recent Security Breach, Users Concerned",
            "New Partnership Aims to Bring Cryptocurrency to Mainstream Audiences, Promoting Adoption",
            "Top 10 Altcoins to Watch in the Year 2023: Promising Projects Making Waves",
            "Cryptocurrency Adoption Reaches New Heights as Traditional Institutions Embrace Digital Assets"
        ]

        date_range = [timezone.now().date() - timezone.timedelta(days=i) for i in range(10)]

        for _ in range(20):
            title = random.choice(titles)
            link = f"https://example.com/news/{title.lower().replace(' ', '-')}"
            published_date = random.choice(date_range)
            News.objects.create(title=title, link=link, published_date=published_date)

        self.stdout.write(self.style.SUCCESS('Successfully populated News model with dummy data'))
