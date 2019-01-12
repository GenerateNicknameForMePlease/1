from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse

TITLE_CHOICES = (('red', 'не готово'),
                 ('yellow', 'необходима проверка'),
                 ('green', 'готово')
                 )


class Work_category(models.Model):
    category = models.CharField(max_length=100)
    slug = models.SlugField()

    def get_absolute_url(self):
        return reverse('index1', kwargs={'work_category_slug': self.slug})

    def __str__(self):
        return self.category


class Task(models.Model):
    slug1 = models.SlugField(default='')
    intro_text = models.CharField(max_length=200, verbose_name='Заголовок')
    task_text = models.TextField(max_length=2000, verbose_name='Текст задания')
    authors_class = models.ForeignKey(Work_category, on_delete=models.CASCADE, null=True, blank=True,
                                      verbose_name='Категория задания')

    authors_name = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
                                     verbose_name='Имя исполнителя')
    status = models.CharField(max_length=256, choices=TITLE_CHOICES, default=TITLE_CHOICES[0],
                              verbose_name='Статус выполнения')
    pub_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    end_date = models.DateTimeField('Дата окончания')

    def get_absolute_url(self):
        return reverse('task_view', kwargs={'task_slug': self.slug1})

    def get_absolute_url1(self):
        return reverse('order_create_view', kwargs={'task_slug': self.slug1})

    def get_absolute_url_cat(self):
        return reverse('task_cat', kwargs={'task_slug': self.slug1})

    def to_dist(self):
        return {
            "intro_text": self.intro_text,
            "task_text": self.task_text,
            "pub_date": self.pub_date,
            "end_date": self.end_date
        }

    def __str__(self):
        return self.intro_text


class ResponseOnTask(models.Model):
    responce_task = models.ForeignKey(Task, on_delete=models.CASCADE, default=None, verbose_name='Задание для ответа')
    user_responce = models.CharField(max_length=200, verbose_name='Пользователь')
        #models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    intro_text_responce = models.CharField(max_length=200, verbose_name='Введение')
    responce_text = models.TextField(max_length=2000, verbose_name='Текст ответа')
    time_responce = models.DateTimeField(auto_now_add=True, auto_now=False)
    status_task = models.CharField(max_length=30, choices=TITLE_CHOICES, default=TITLE_CHOICES[1])

    def __str__(self):
        return self.intro_text_responce