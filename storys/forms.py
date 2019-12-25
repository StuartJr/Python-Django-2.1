from django import forms
from django.core.exceptions import ValidationError
from django.core import validators
from django.forms import ModelForm
from django.forms import DecimalField
from django.forms.widgets import Select, SelectDateWidget
from .models import Story, Rubric
from captcha.fields import CaptchaField


class SearchForm(forms.Form):
	keyword = forms.CharField(max_length=20, label = 'Искомое слово')
	rubric = forms.ModelChoiceField(queryset = Rubric.objects.all(),
		label = 'Рубрика')

class Storyform(forms.ModelForm):
	def clean(self):
		super().clean()
		errors = {}
		if not self.cleaned_data['content']:
			errors['content'] = ValidationError(
								'Укажите описание продоваемого товара')
		if self.cleaned_data['price']<0:
			errors['price'] = ValidationError(
								'Укажите неотрицательное значение цены')
		if errors:
			raise ValidationError(errors)

	def clean_title(self):
		val = self.cleaned_data['title']
		if val == 'Прошлогодний снег':
			raise ValidationError('Прошлогодний снег продовать' + 'не допускается')
		return val

	captcha = CaptchaField(label = 'Введите текст с картинки', 
			error_messages = {'invalid':'Неправильный текст'})
	title = forms.CharField(label='Название товара',
	 validators = [validators.RegexValidator(regex='^.{4,}$')],
	 error_messages = {'invalid':'Неправильное название товара'})
	content = forms.CharField(label = 'Описание', 
		widget = forms.widgets.Textarea())
	price = forms.DecimalField(label = 'Цена', decimal_places=1)
	published = forms.DateField(widget = SelectDateWidget(empty_label = ('Выберите год',
		'Выберите месяц','Выберите число')))
	rubric =forms.ModelChoiceField(queryset = Rubric.objects.all(),
		label = 'Рубрика', help_text='Не забудьте выбрать рубрику!', widget = forms.widgets.Select(attrs={'size':1}))
	class Meta:
		model = Story
		fields = ('title', 'content', 'price','rubric')


