from django.core.management.base import BaseCommand

from musicoin import crawler


class Command(BaseCommand):
    def handle(self, *args, **options):
        crawler.crawl_and_update_song_infos()
