from datetime import timedelta

from django.utils import timezone
from django.views.generic import TemplateView

from musicoin.models import MusicCopyright


class MusicCopyrightListView(TemplateView):
    template_name = 'musicoin/music_copyright_list.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        before_48hours = timezone.localtime() - timedelta(hours=48)
        musics = (
            MusicCopyright
                .objects
                .exclude(title='')
                .exclude(updated__lt=before_48hours)
                .exclude(stock_income_rate__lte=0)
                .order_by('-stock_income_rate', '-updated')
        )
        context_data.update({'musics': musics})
        return context_data

