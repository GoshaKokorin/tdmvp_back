from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class FeedbackCall(models.Model):
    name = models.CharField('Имя', max_length=255)
    number = PhoneNumberField(verbose_name='Телефон', region='RU')
    is_processed = models.BooleanField('Обработано', default=False)
    is_spam = models.BooleanField('Спам', default=False)
    created_at = models.DateTimeField('Дата заявки', auto_now_add=True)

    class Meta:
        verbose_name = 'Заявка на звонок'
        verbose_name_plural = 'Заявки на звонки'

    def __str__(self):
        return f'{self.name}: {self.number}'


class FeedbackQuestion(FeedbackCall):
    text = models.TextField('Вопрос')

    class Meta:
        verbose_name = 'Заявка c вопросом'
        verbose_name_plural = 'Заявки с вопросами'
