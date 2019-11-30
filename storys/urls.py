from django.urls import path
from .views import StorysIndexView, StoryByRubricView
from .views import StoryCreateView, StoryEditView, StoryDeleteView
from .views import StoryAddView, StoryDetailView, StoryRedirectView
from .views import StoryArchiveYear, StoryArchiveMounth, index, editet, delete


urlpatterns = [
	path('detail/<int:pk>/', StoryDetailView.as_view(), name = 'detail'),
	path('detail/<int:year>/<int:month>/<int:day>/<int:pk>/', StoryRedirectView.as_view(), name ='old_detail' ),
	path('delete/<int:pk>/', delete, name='delete'),
	path('edit/<int:pk>/', editet, name='edit'),
	path('add/<int:pk>/', StoryAddView.as_view(), name='add'),
	path('add/', StoryCreateView.as_view(),name='add'),
	path('<int:rubric_id>/', StoryByRubricView.as_view(), name = 'by_rubric'),
	# path('', StorysIndexView.as_view(), name = 'index'),
	path('', index , name = 'index'),
]