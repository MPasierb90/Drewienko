from django.db import models
from django.urls import reverse
from django.utils import timezone


# class Category(models.Model):
#     # name = models.CharField(choices=((1, 'szafy'), (2, 'komody'), (3, 'sofy'),
#     (4, 'zestawy wypoczynkowe'), (5, 'meblościanki'), (6, 'ławy i stoliki'), (7, 'krzesła')), max_length=100)
#
#     def __str__(self):
#         return self.name


class Announcement(models.Model):
    objects = models.Manager()
    title = models.CharField(verbose_name="Tytuł", max_length=100)
    picture = models.ImageField(verbose_name="Zdjęcie", upload_to='annouc_photos')
    content = models.TextField(verbose_name="Opis", )
    city = models.CharField(verbose_name="Miasto", max_length=100)
    date_posted = models.DateTimeField(verbose_name="Data opublikowania", default=timezone.now)
    author = models.ForeignKey('auth.User', verbose_name="Autor", on_delete=models.CASCADE)
    price = models.DecimalField(verbose_name="Cena", max_digits=10, decimal_places=2)
    category = models.CharField(verbose_name="Kategoria", choices=(
        ('szafy', 'szafy'), ('komody', 'komody'), ('sofy', 'sofy'), ('zestawy wypoczynkowe', 'zestawy wypoczynkowe'),
        ('meblościanki', 'meblościanki'), ('ławy i stoliki', 'ławy i stoliki'), ('krzesła', 'krzesła')), max_length=100)
    shipping = models.CharField(verbose_name="Wysyłka", choices=(('tak', 'tak'), ('nie', 'nie')), default='nie',
                                max_length=100)
    sell_or_exchange = models.CharField(verbose_name="Wymiana/Sprzedaż",
                                        choices=(('na sprzedaż', 'na sprzedaż'), ('na wymianę', 'na wymianę'),
                                                 ('na sprzedaż lub wymianę', 'na sprzedaż lub wymianę')),
                                        max_length=100)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('announcement-detail', kwargs={'pk': self.pk})
