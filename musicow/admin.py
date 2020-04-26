from django.contrib import admin

from musicow.models import MusicCopyright


@admin.register(MusicCopyright)
class MusicCopyrightAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'stock_income_rate', 'last_12_months_income', 'stock_lowest_price')
    fields = ('title', 'artist', 'stock_income_rate', 'last_12_months_income', 'stock_lowest_price', 'stock_sales')
    sortable_by = ('title', 'artist', 'stock_income_rate', 'last_12_months_income', 'stock_lowest_price')
