from django.shortcuts import redirect
from .models import Story
from .models import Rubric
from .forms import Storyform, SearchForm
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.core.paginator import Paginator, Page
from django.views.generic.dates import ArchiveIndexView, MonthArchiveView, YearArchiveView
from django.views.generic.dates import DateDetailView
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.forms import modelformset_factory, BaseModelFormSet, inlineformset_factory
from django.forms.formsets import ORDERING_FIELD_NAME
from django.core import validators
from django.core.exceptions import ValidationError
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count,Q
from .models import Img
from .forms import ImgForm
from myfirst.settings import BASE_DIR
import os
from django.http import FileResponse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.signals import post_save
from django.core.mail import send_mail
from .serializers import RubricSerializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

MESSAGE_LEVEL = messages.DEBUG

class APIRubricViewSet(ModelViewSet):
	queryset = Rubric.objects.all()
	serializer_class = RubricSerializers
	permission_classes = (IsAuthenticated,)

class APIRubrics(generics.ListCreateAPIView):
	queryset = Rubric.objects.all()
	serializer_class = RubricSerializers
	permission_classes = (IsAuthenticated,)

class APIRubricDetail(generics.RetrieveUpdateAPIView):
	queryset = Rubric.objects.all()
	serializer_class = RubricSerializers
	permission_classes = (IsAuthenticated,)

# class APIRubricDetail(APIView):
# 	def get(self, request, pk):
# 		rubric = Rubric.objects.get(pk=pk)
# 		serializer = RubricSerializers(rubric)
# 		return Response(serializer.data)
# 	def putch(self, request, pk):
# 		rubric = Rubric.objects.get(pk=pk)
# 		serializer = RubricSerializers(rubric, data=request.data)
# 		if serializer.is_valid():
# 			serializer.save()
# 			return Response(serializer.data)
# 		return Response(serializer.errors,
# 						status=status.HTTP_400_BAD_REQUEST)
# 	def put(self, request, pk):
# 		rubric = Rubric.objects.get(pk=pk)
# 		serializer = RubricSerializers(rubric, data=request.data)
# 		if serializer.is_valid():
# 			serializer.save()
# 			return Response(serializer.data)
# 		return Response(serializer.errors,
# 						status=status.HTTP_400_BAD_REQUEST)
# 	def delete(self, request, pk):
# 			rubric = Rubric.objects.get(pk=pk)
# 			rubric.delete()
# 			return Response(status=status.HTTP_204_NO_CONTENT)


# class APIRubrics(APIView):
# 	def get(self, request):
# 		rubric = Rubric.objects.all()
# 		serializer = RubricSerializers(rubric, many = True)
# 		return Response(serializer.data)
# 	def post(self, request):
# 		serializer = RubricSerializers(data = request.data)
# 		if serializer.is_valid():
# 			serializer.save()
# 			return Response(serializer.data, 
# 							status = status.HTTP_201_CREATED)
# 		return Response(serializer.data,
# 							status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE', 'PUTCH'])
def api_rubrics_detail(request, pk):
	rubric = Rubric.objects.get(pk=pk)
	if request.method == 'GET':
		serializer = RubricSerializers(rubric)
		return Response(serializer.data)
	elif request.method == 'PUT' or request.method == 'PUTCH':
		serializer = RubricSerializers(rubric, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors,
						status=status.HTTP_400_BAD_REQUEST)
	elif request.method == 'DELETE':
		rubric.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def api_rubrics(request):
	if request.method == 'GET':
		rubrics = Rubric.objects.all()
		serializer = RubricSerializers(rubrics, many = True)
		return Response(serializer.data)
	elif request.method == 'POST':
		serializer = RubricSerializers(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.errors,
							status = status.HTTP_400_BAD_REQUEST)

# send_mail('Subject here', 'Here is the message.', 'from@example.com',
#     ['Stuart688@yandex.ru'], fail_silently=False)

def post_save_dispatcher(sender, **kwargs):
	if kwargs['created']:
		print('Объявление в рубрике "%s" создано' % \
			kwargs['instance'].rubric.name)

post_save.connect(post_save_dispatcher, sender= Story)

def delet(request, filename):
	img = Img.objects.get(img=filename)
	img.img.delete()
	img.delete()
	return redirect('index')

FILES_ROOT = os.path.join(BASE_DIR, 'media')

def get(request, filename):
	fn = os.path.join(FILES_ROOT, filename)
	return FileResponse(open(fn,'rb'), content_type = 'application/octet-stream')	

def imags(request):
	imgs = []
	for entry in os.scandir(FILES_ROOT):
		imgs.append(os.path.basename(entry))
	context = {'imgs':imgs}
	return render(request, 'storys/imags.html', context)

def media(request):
	if request.method == 'POST':
		form = ImgForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			messages.success(request, 'Изображение добавлено')
			return redirect('index')
	else:
		form = ImgForm()
	context = {'form':form}
	return render(request, 'storys/add.html', context)

def search(request):
	if request.method == 'POST':
		sf = SearchForm(request.POST)
		if sf.is_valid():
			keyword = sf.cleaned_data['keyword']
			rubric_id = sf.cleaned_data['rubric'].pk
			rubric = Rubric.objects.get(pk=rubric_id)
			bbs = Story.objects.filter(rubric = rubric_id, title__icontains = keyword)
			context = {'current_rubric':rubric, 'bbs':bbs, 'keyword':keyword, 'rubric_id':rubric_id}
			return (render(request, 'storys/search_result.html', context))
	else:
		sf=SearchForm()
	context = {'form':sf}
	return render(request, 'storys/search.html', context)

def bbs(request, rubric_id):
	StorysFormSet = inlineformset_factory(Rubric, Story, form = Storyform, extra = 1)
	rubric = Rubric.objects.get(pk=rubric_id)
	if request.method == 'POST':
		formset = StorysFormSet(request.POST, instance = rubric)
		if formset.is_valid():
			formset.save()	
			return redirect('index')
	else:
		formset = StorysFormSet(instance = rubric)
	context = {'formset':formset, 'current_rubric':rubric}
	return render(request, 'storys/bbs.html', context)
	print(context)

class RubricBaseFormSet(BaseModelFormSet):
	def clean(self):
		super().clean()
		names = [form.cleaned_data['name'] for form in self.forms \
		if 'name' in form.cleaned_data]
		if('Недвижимост'not in names) or ('Транспорт'not in names) or ('Мебель'not in names):
			raise ValidationError('Добавте рубрики недвижимости,' +\
									'транспорта и мебели')
@login_required
def rubrics(request):
	RubricFormSet = modelformset_factory(Rubric, fields=('name',),
										can_delete = True, can_order = True,
										formset = RubricBaseFormSet)
	# if request.user.is_authenticated:
	if request.method == 'POST':
		formset = RubricFormSet(request.POST)
		if formset.is_valid():
			for form in formset:
				if form.cleaned_data:
					rubric = form.save(commit = False)
					rubric.order = form.cleaned_data[ORDERING_FIELD_NAME]
					rubric.save()
			formset.save()			
			return redirect('index')
	else:
		formset = RubricFormSet()
	context = {'formset':formset}
	return render(request, 'storys/rubrics.html', context)
	# else:
	# 	return redirect_to_login(reverse('rubrics'))

@login_required
def delete(request, pk):
	bb=Story.objects.get(pk=pk)
	if request.method == 'POST':
		bb.delete()
		messages.success(request, 'Объявлене успешно удалено')
		return HttpResponseRedirect(reverse('by_rubric',
				kwargs = {'rubric_id':bb.rubric.pk}))
	else:
		context = {'bb':bb}
		return render(request, 'storys/story_confirm_delete.html', context)

@login_required
def editet(request, pk):
	bb=Story.objects.get(pk=pk)
	if request.method == 'POST':
		bbf=Storyform(request.POST, instance = bb)
		if bbf.is_valid():
			bbf.save()
			messages.success(request, 'Объявлене успешно изменено')
			return HttpResponseRedirect(reverse('by_rubric',
				kwargs = {'rubric_id':bbf.cleaned_data['rubric'].pk}))

		else:
			context = {'form':bbf}
			return render (request, 'storys/story_form.html', context)
	else:
		bbf = Storyform(instance = bb)
		context = {'form':bbf}
		return render (request, 'storys/story_form.html', context)


def index(request):
		rubrics = Rubric.objects.all()
		bbs = Story.objects.all()
		paginator = Paginator(bbs, 2)
		if 'page' in request.GET:
			page_num = request.GET['page']
		else:
			page_num = 1
		page = paginator.get_page(page_num)
		
		context = {'rubrics': rubrics, 'page':page, 'bbs':page}
		return render(request, 'storys/index.html', context)

# class StoryByRubricView(SingleObjectMixin, ListView):
# 	template_name = 'storys/by_rubric.html'
# 	pk_url_kwarg = 'rubric_id'
	

# 	def get(self, request, *args, **kwargs):
# 		self.object = self.get_object(queryset = Rubric.objects.all())
# 		return super().get(request, *args, **kwargs)

# 	def get_context_data(self, *args, **kwargs):
# 		context = super().get_context_data(*args, **kwargs)
# 		context['current_rubric'] = self.object
# 		context['bbs'] = context['object_list']
# 		context['rubrics'] = Rubric.objects.all()
# 		return context

# 	def get_queryset(self):
# 		return self.object.rubrics_set.all()

class StoryRedirectView(RedirectView):
	url = '/storys/detail/%(pk)d/'

class StoryDetailView(DateDetailView):
	
	model = Story
	date_field = 'published'
	month_format = '%m'
	template_name ='storys/index.html'

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['rubrics'] = Rubric.objects.all()
		return context


class StoryArchiveMounth(MonthArchiveView):
	model = Story
	date_field ='published'
	template_name ='storys/index.html'
	context_object_name = 'bbs'
	allow_empty = True
	month_format = '%m'

class StoryArchiveYear(YearArchiveView):
	model = Story
	date_field ='published'
	template_name ='storys/index.html'
	context_object_name = 'bbs'
	allow_empty = True
	year_format = '%Y'

class StorysIndexView(ArchiveIndexView):
	model = Story
	date_field = 'published'
	template_name ='storys/index.html'
	context_object_name = 'bbs'
	allow_empty = True

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['rubrics'] = Rubric.objects.all()
		return context


class StoryDeleteView(DeleteView):
	model = Story
	success_url = '/'

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['rubrics'] = Rubric.objects.all()
		return context

class StoryEditView(UpdateView):
	model = Story
	form_class = Storyform
	success_url = '/'

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['rubrics'] = Rubric.objects.all()
		return context

class StoryAddView(FormView, SuccessMessageMixin):
	initial = {'price': 0.0}
	template_name='storys/create.html'
	from_class=Storyform
	success_url = '/{rubric_id}'
	success_message = 'Объявлене "%(title)s" успешно создано'


	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args,**kwargs)
		context['rubrics']=Rubric.objects.all()
		return context

	def form_valid(self, form):
		form.save()
		return super().form_valid(form)

	def get_form(self, form_class=None):
		self.object = super().get_form(form_class)
		return self.object

	def get_success_url(self):
		return reverse('storys:by_rubric', 
			kwargs={'rubric_id':self.object.cleaned_data['rubric'].pk})


class StoryIndexView(TemplateView):
	template_name='storys/index.html'

	def get_context_data(self, *args, **kwargs):
		context=super().get_context_data(*args,**kwargs)
		context['bbs']=Story.objects.all()
		context['rubrics']=Rubric.objects.all()
		return context
		
class StoryByRubricView(ListView):
	template_name='storys/by_rubric.html'
	context_object_name='bbs'

	def get_queryset(self):
		return Story.objects.filter(rubric=self.kwargs['rubric_id'])

	def get_context_data(self, *args, **kwargs):
		context=super().get_context_data(*args,**kwargs)
		context['rubrics']=Rubric.objects.all()
		context['current_rubric'] = Rubric.objects.get(pk=self.kwargs['rubric_id'])
		return context

		

class StoryDetailView(DetailView):
	model = Story
	

	def get_context_data(self, *args,**kwargs):
		context=super().get_context_data(*args,**kwargs)
		context['rubrics']=Rubric.objects.all()
		return context

class StoryCreateView(LoginRequiredMixin, CreateView):
	template_name='storys/create.html'
	form_class=Storyform
	success_url=reverse_lazy('index')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['rubrics']=Rubric.objects.all()
		return context

def by_rubric(request, rubric_id):
	bbs = Story.objects.filter(rubric = rubric_id)
	rubrics = Rubric.objects.all()
	current_rubric = Rubric.objects.get(pk=rubric_id)
	context = {'bbs':bbs, 'rubrics':rubrics, 
	'current_rubric':current_rubric}
	return render(request, "storys/by_rubric.html", context)



# def index(request):
# 	bbs = Story.objects.all()
# 	rubrics = Rubric.objects.all()
# 	context = {'bbs':bbs, 'rubrics':rubrics}
# 	return render(request,'storys/index.html', {'bbs':bbs})
	
def add_and_save(request):
	if request.method == 'POST':
		bbf=Storyform(request.POST)
		if bbf.is_valid():
			bbf.save()
			return HttpResponseRedirect(reverse('by_rubric', kwargs={'rubric_id':bbf.cleaned_data['rubric'].pk}))
		else:
			context={'form':bbf}
			return render(request,'storys/create.html', context)
	else:
		bbf=Storyform()
		context={'form':bbf}
		return render(request, 'storys/create.html', context)