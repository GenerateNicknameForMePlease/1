from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from . import views
from rest_framework .urlpatterns import format_suffix_patterns


urlpatterns = [
    path('', views.index, name='index'),
    url(r'^category/(?P<work_category_slug>[-\w]+)/$', views.index1, name='index1'),
    url(r'^task/(?P<task_slug>[-\w]+)/$', views.task_view, name='task_view'),
    url(r'^responce/(?P<task_slug>[-\w]+)/$', views.order_create_view, name='order_create_view'),
    url(r'^check/$', views.task_check_view, name='task_check_view'),
    url(r'^login/$', views.login_view, name='login_view'),
    url(r'^logout/$', LogoutView.as_view(next_page=reverse_lazy('login_view')), name='logout'),
    path('api/', views.api_login, name='api_login'),
    #path('api/<int:pk>/', views.SnippetDetail.as_view()),
   # path('users/', views.UserList.as_view()),
   # path('users/<int:pk>/', views.UserDetail.as_view()),
   # url(r'^api/$', views.snippet_list),
    #url(r'^api/(?P<pk>[0-9]+)$', views.snippet_detail),

]

urlpatterns = format_suffix_patterns(urlpatterns)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
