from django.db import models
from django.contrib.auth.models import User

class Story(models.Model):
	title = models.CharField(max_length=50, verbose_name='Товар')
	content = models.TextField(null = True, blank=True, verbose_name='Описание')
	price = models.FloatField(null = True, blank=True, verbose_name='Цена')
	published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')
	rubric = models.ForeignKey('Rubric', null=True, on_delete = models.PROTECT,verbose_name = 'Рубрика',
		related_name='entries', related_query_name='entry')

	class Meta():
		verbose_name_plural = 'Объявления'
		verbose_name = 'Объявление'
		ordering = ['-published']

class Rubric(models.Model):
	name = models.CharField(max_length=20, db_index=True, verbose_name = 'Название')
	order = models.SmallIntegerField(default = 0, db_index=True)
	def __str__(self):
		return self.name

	class Meta():
		verbose_name_plural = 'Рубрики'
		verbose_name = 'Рубрика'
		ordering = ['order','name']

class AdvUser (models.Model):
	is_activated = models.BooleanField(default = True)
	user = models.OneToOneField(User, on_delete=models.CASCADE)