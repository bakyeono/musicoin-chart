from django.core.management.base import BaseCommand
from django.utils import timezone

from musicow.tasks import find_and_update_music_copyrights


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(f'{timezone.localtime()} crawler start'))
        try:
            find_and_update_music_copyrights()
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'{timezone.localtime()} crawler error: f{e}'))
        self.stdout.write(self.style.SUCCESS(f'{timezone.localtime()} crawler end'))
