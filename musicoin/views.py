from django.views.generic import TemplateView

from musicoin.models import MusicCopyright


class MusicCopyrightListView(TemplateView):
    template_name = 'musicoin/music_copyright_list.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        musics = MusicCopyright.objects.exclude(title='').order_by('-stock_income_rate', '-number')
        context_data.update({'musics': musics})
        return context_data

