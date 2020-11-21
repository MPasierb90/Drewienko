from django.db import models
from django.urls import reverse
from django.utils import timezone


class Category(models.Model):
    objects = models.Manager()
    name = models.CharField(verbose_name='Kategoria', max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Announcement(models.Model):
    objects = models.Manager()
    title = models.CharField(verbose_name="Tytuł", max_length=100)
    picture = models.ImageField(verbose_name="Zdjęcie", upload_to='annouc_photos')
    content = models.TextField(verbose_name="Opis", )
    city = models.CharField(verbose_name="Miasto", max_length=100)
    date_posted = models.DateTimeField(verbose_name="Data opublikowania", default=timezone.now)
    author = models.ForeignKey('auth.User', verbose_name="Autor", on_delete=models.CASCADE)
    price = models.DecimalField(verbose_name="Cena", max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
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
