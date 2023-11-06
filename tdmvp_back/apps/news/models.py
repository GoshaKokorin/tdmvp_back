from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django_extensions.db.fields import AutoSlugField

from tdmvp_back.utils import image_upload_to, generate_slug


class NewsTag(models.Model):
    name = models.CharField('Название', max_length=64)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['-id']

    def __str__(self):
        return self.name


# TODO: Сделать добавление видео и прочее
class News(models.Model):
    title = models.CharField('Название', max_length=255)
    slug = AutoSlugField('Slug', populate_from='title', slugify_function=generate_slug)
    image = models.ImageField('Изображение', upload_to=image_upload_to)
    short_description = models.CharField('Короткое описание', max_length=255)
    description = RichTextUploadingField(verbose_name='Описание')
    date = models.DateField('Дата публикации')
    is_active = models.BooleanField('Активность', default=False)

    tags = models.ManyToManyField(NewsTag, verbose_name='Теги')

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-id']

    def __str__(self):
        return self.title
