from django.db import models
from django_extensions.db.fields import AutoSlugField

from tdmvp_back.utils import image_upload_to, generate_slug


class ProductTag(models.Model):
    name = models.CharField('Название', max_length=64)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['-id']

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField('Название', max_length=255)
    slug = AutoSlugField('Slug', populate_from='name', slugify_function=generate_slug)
    image = models.ImageField('Изображение', upload_to=image_upload_to)

    tags = models.ManyToManyField(ProductTag, verbose_name='Теги')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, verbose_name='Категории', on_delete=models.PROTECT)
    tags = models.ManyToManyField(ProductTag, verbose_name='Теги')

    name = models.CharField('Название', max_length=255)
    slug = AutoSlugField('Slug', populate_from='name', slugify_function=generate_slug)
    short_description = models.CharField('Короткое описание', max_length=255)
    description = models.TextField('Описание')
    price = models.CharField('Цена', max_length=255)

    additional_title = models.CharField('Дополнительный заголовок', max_length=255, blank=True, null=True)
    additional_description = models.TextField('Дополнительное описание', blank=True, null=True)

    advantages = models.TextField('Преимущества', blank=True, null=True)
    accessories = models.TextField('Комплектующие', blank=True, null=True)
    guarantees = models.TextField('Гарантии', blank=True, null=True)

    is_active = models.BooleanField('Активность', default=False, db_index=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-id']

    def __str__(self):
        return self.name


class ProductCharacteristic(models.Model):
    product = models.ForeignKey(
        Product, verbose_name='Характеристики', related_name='product_characteristics',
        related_query_name='product_characteristic', on_delete=models.CASCADE,
    )
    name = models.CharField('Название', max_length=64)
    value = models.CharField('Значение', max_length=64)
    position = models.PositiveSmallIntegerField('Позиция', default=0, blank=False, null=False)

    class Meta:
        verbose_name = 'Характеристика товара'
        verbose_name_plural = 'Характеристики товаров'
        ordering = ['position']

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, verbose_name='Изображения', related_name='product_images',
        related_query_name='product_image', on_delete=models.CASCADE,
    )
    image = models.ImageField('Изображение', upload_to=image_upload_to)
    position = models.PositiveSmallIntegerField('Позиция', default=0, blank=False, null=False)

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображение товаров'
        ordering = ['position']

# gzip nginx
