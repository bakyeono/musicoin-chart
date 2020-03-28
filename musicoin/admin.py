from django.contrib import admin

from musicoin.models import MusicCopyright


@admin.register(MusicCopyright)
class MusicCopyrightAdmin(admin.ModelAdmin):
    fields = ('title', 'artist', 'stock_income_rate', 'last_12_months_income', 'stock_lowest_price', 'stock_sales')
