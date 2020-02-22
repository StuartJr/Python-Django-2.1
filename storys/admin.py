from django.contrib import admin
from django.db import models
from django import forms
from django.urls import reverse
from .models import Story
from .models import Rubric
from django.db.models import F

def discount(modeladmin, request, queryset):
	f = F('price')
	for rec in queryset:
		rec.price = f/2
		rec.save()
	modeladmin.message_user(request, 'Действие выполнено')
discount.short_description = 'Уменьшить цену вдвое'

class SAdmin(admin.ModelAdmin):

	def view_on_site(self, rec):
		return reverse('detail', kwargs = {'pk':rec.pk})

	formfield_overrides = {
		models.ForeignKey: {'widget': forms.widgets.Select(
													attrs = {'size': 8})},
	}

	def get_fields(self, request, obj=None): #У исправляемого объявления нельзя указать рубрику
		f = ['title', 'content', 'price']
		if not obj:
			f.append('rubric')
		return f

	def get_list_display(self, request):
		ld = ['title', 'content', 'price']
		if request.user.is_superuser:
			ld+= ['published', 'rubric']
		return ld
	list_display = ('title', 'content', 'price','published','rubric')
	list_display_links = ('title', 'content')
	search_fields = ('title', '^content',)
	actions = (discount,)
	list_filter = ('title', 'rubric__name',)

admin.site.register(Story, SAdmin)
admin.site.register(Rubric)