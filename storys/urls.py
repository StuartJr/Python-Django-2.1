from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.views import PasswordChangeDoneView
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetCompleteView
from django.views.decorators.cache import cache_page
from .views import rubrics, bbs, search, media, get, imags, delet
from .views import StorysIndexView, StoryByRubricView
from .views import StoryCreateView, StoryEditView, StoryDeleteView
from .views import StoryAddView, StoryDetailView, StoryRedirectView
from .views import StoryArchiveYear, StoryArchiveMounth, index, editet, delete


urlpatterns = [
	path('media/get/<path:filename>', delet, name = 'delet'),
	path('media/get/', imags, name = 'imags'),
	path('get/<path:filename>', get, name = 'get'),
	path('media/', media , name = 'media'),
	path('search/', cache_page(60*5) (search), name = 'search'),
	path('accounts/reset/done/', PasswordResetCompleteView.as_view(template_name = 'registration/password_confirmed.html'), name = 'password_reset_comlete'),
	path('accounts/reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name = 'registration/confirm_password.html'), name = 'password_reset_confirm'),
	path('accounts/password_reset/done/', PasswordResetDoneView.as_view(template_name = 'registration/email_sent.html'), name = 'password_reset_done'),
	path('accounts/password_reset/', PasswordResetView.as_view(template_name = 'registration/reset_password.html',
		subject_template_name = 'registration/reset_object.txt', email_template_name = 'registration/reset_email.html'),
		name = 'password_reset'),
	path('accounts/password_change/', PasswordChangeView.as_view(template_name = 'registration/change_password.html'), name = 'password_change'),
	path('accounts/password_change/done/', PasswordChangeDoneView.as_view(template_name = 'registration/password_change.html'), name = 'password_change_done'),
	path('accounts/logout/', LogoutView.as_view(next_page=None), name = 'logout'),
	path('accounts/login/', LoginView.as_view(), name = 'login'),
	path('bbs/<int:rubric_id>/', bbs, name = 'bbs'),
	path('rubrics/', rubrics, name='rubrics' ),
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