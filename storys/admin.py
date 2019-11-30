from django.contrib import admin


from .models import Story
from .models import Rubric

class SAdmin(admin.ModelAdmin):
	list_display = ('title', 'content', 'price','published','rubric')
	list_display_links = ('title', 'content')
	search_fields = ('title', 'content',)

admin.site.register(Story, SAdmin)
admin.site.register(Rubric)