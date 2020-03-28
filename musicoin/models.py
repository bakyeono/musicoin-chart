from django.db import models
from django.contrib.postgres.fields import JSONField


class MusicCopyright(models.Model):
    created = models.DateTimeField(verbose_name='생성일시', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='수정일시', auto_now=True, db_index=True)
    number = models.IntegerField(verbose_name='번호', db_index=True)
    title = models.CharField(verbose_name='제목', max_length=200, db_index=True)
    artist = models.CharField(verbose_name='음악가', max_length=200, db_index=True)
    stock_income_rate = models.FloatField(verbose_name='주당 수익률', db_index=True)
    last_12_months_income = models.IntegerField(verbose_name='지난 12개월 수익', default=0)
    stock_lowest_price = models.IntegerField(verbose_name='주식 최저가', default=0)
    stock_sales = JSONField(verbose_name='판매중 주식', default=dict)

    class Meta:
        verbose_name = '음악 저작권'
        verbose_name_plural = '음악 저작권'

    def __str__(self):
        return f'음악 저작권({self.number}: {self.title})'
