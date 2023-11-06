import datetime
import logging
import random

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from faker import Faker

from tdmvp_back.apps.news.models import News, NewsTag
from tdmvp_back.utils import generate_slug
from tdmvp_back.seed_utils import get_file_logo

logger = logging.getLogger('seed_news')


class Command(BaseCommand):
    help = 'Заполнение новостей тестовыми данными.'

    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise CommandError('Только для режима DEBUG')

        fake = Faker('ru_Ru')

        logger.info('-------Заполнение тегов-------')
        NewsTag.objects.all().delete()
        if not NewsTag.objects.count():
            for tag_name in ['Обновление', 'Станки', 'Компания', 'Цены', 'Скидки']:
                logger.info(NewsTag.objects.create(**{'name': tag_name}))
        else:
            logger.info('Таблица NewsTag не пустая')

        logger.info('-------Заполнение новостей-------')
        News.objects.all().delete()
        if not News.objects.count():
            tag_max_variants = 3 if NewsTag.objects.count() > 3 else NewsTag.objects.count()
            for _ in range(15):
                title = fake.catch_phrase()
                slug = generate_slug(title)
                new_news = {
                    'title': title,
                    'slug': slug,
                    'short_description': fake.text(max_nb_chars=100),
                    'description': f'<p>{fake.text(max_nb_chars=300)}</p>',
                    'image': get_file_logo(),
                    'date': fake.date_of_birth(),
                    'is_active': random.choice([True, False]),
                }
                try:
                    obj = News.objects.create(**new_news)
                    # add tags
                    obj.tags.set(NewsTag.objects.order_by('?')[0: random.randint(1, tag_max_variants)])

                    logger.info(obj)
                except Exception as exc:
                    logger.error('News create: {}'.format(exc))
        else:
            logger.info('Таблица News не пустая')
