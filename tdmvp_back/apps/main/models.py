from django.db import models

from tdmvp_back.utils import image_upload_to


# TODO: add sortable admin
class Main(models.Model):
    title = models.CharField('Название', max_length=255)
    image = models.ImageField('Изображение', upload_to=image_upload_to)
    description = models.TextField('Описание')
    link = models.CharField('Ссылка на страницу', max_length=255)
    position = models.PositiveSmallIntegerField('Позиция', default=0, blank=False, null=False)
    is_active = models.BooleanField('Активность', default=False)

    class Meta:
        verbose_name = 'Слайдер'
        verbose_name_plural = 'Слайдеры'
        ordering = ['position']

    def __str__(self):
        return self.title
