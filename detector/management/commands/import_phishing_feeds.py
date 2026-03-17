import requests
from urllib.parse import urlparse
from django.core.management.base import BaseCommand
from detector.models import PhishingURL


class Command(BaseCommand):

    help = "Download phishing feeds and store domains or IPs in database"

    feeds = {
        "openphish": "https://openphish.com/feed.txt",
        "urlhaus": "https://urlhaus.abuse.ch/downloads/text_recent/"
    }

    def extract_domain(self, url):

        # Skip empty lines or comments
        if not url or url.startswith("#"):
            return None

        try:
            parsed = urlparse(url if "://" in url else f"http://{url}")
            domain = parsed.netloc or parsed.path.split("/")[0]
            domain = domain.split(":")[0]
            return domain.lower()

        except:
            return None

    def handle(self, *args, **kwargs):

        headers = {
            "User-Agent": "Django-Phishing-Detector/1.0"
        }

        for source, feed_url in self.feeds.items():
            self.stdout.write(f"Processing {source} feed...")
            try:
                response = requests.get(
                    feed_url,
                    headers=headers,
                    timeout=30,
                    stream=True
                )

                response.raise_for_status()

                unique_domains = set()

                for line in response.iter_lines(decode_unicode=True):

                    url = line.strip()

                    domain = self.extract_domain(url)

                    if domain:
                        unique_domains.add(domain)

                # Check existing domains
                existing = set(
                    PhishingURL.objects.filter(
                        domain__in=unique_domains
                    ).values_list("domain", flat=True)
                )

                # Prepare new objects
                new_domains = [
                    PhishingURL(domain=d, source=source)
                    for d in unique_domains if d not in existing
                ]

                # Bulk insert
                PhishingURL.objects.bulk_create(
                    new_domains,
                    batch_size=1000,
                    ignore_conflicts=True
                )

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Added {len(new_domains)} entries from {source}"
                    )
                )

            except Exception as e:

                self.stdout.write(
                    self.style.ERROR(
                        f"Error fetching {source}: {e}"
                    )
                )

        self.stdout.write(self.style.SUCCESS("Import finished."))