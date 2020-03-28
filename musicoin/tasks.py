from datetime import timedelta
from sys import stderr

from django.utils import timezone

from . import crawler
from .models import MusicCopyright


def find_and_update_music_copyrights():
    crawler.find_song_documents(crawler.update_song_info, lambda e: print(e, file=stderr))


def delete_old_music_copyrights():
    before_24hours = timezone.localtime() - timedelta(hours=24)
    MusicCopyright.objects.filter(updated__lt=before_24hours).delete()

