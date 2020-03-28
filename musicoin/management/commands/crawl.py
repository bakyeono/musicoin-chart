from django.core.management.base import BaseCommand
from django.utils import timezone

from musicoin import crawler


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(f'{timezone.localtime()} crawler start'))
        try:
            crawler.crawl_and_update_song_infos()
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'{timezone.localtime()} crawler error: f{e}'))
        self.stdout.write(self.style.SUCCESS(f'{timezone.localtime()} crawler end'))
