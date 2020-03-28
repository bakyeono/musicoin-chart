from sys import stderr

from . import crawler


def find_and_update_music_copyrights():
    crawler.find_song_documents(crawler.update_song_info, lambda e: print(e, file=stderr))

