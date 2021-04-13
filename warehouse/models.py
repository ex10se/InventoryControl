from django.db import models


class Item(models.Model):
    """
    Модель складского ресурса
    """
    title = models.CharField(max_length=250, verbose_name='Наименование')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=1, verbose_name='Количество')
    unit = models.CharField(max_length=20, verbose_name='Единица измерения')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за у.е.')
    date = models.DateField(verbose_name='Дата последнего поступления')

    @property
    def cost(self):
        return self.amount * self.price

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'item'
        verbose_name_plural = 'items'
