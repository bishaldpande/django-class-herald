from django.urls import path
from blog import views

from rest_framework import routers
from django.urls import include


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'blogs', views.BlogViewSet)

urlpatterns = [
	#  Rest API
	path('rest_api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

	path('home/', views.home, name="home"),
	path('add/blog/', views.add_blog, name='add_blog'),
	path('blog/detail/<id>/', views.blog_details, name='blog_details'),
	path('blog/edit/<id>/', views.edit_blog, name='edit_blog'),
	path('blog/delete/<id>/', views.delete_blog, name='delete_blog'),
		
	path('accounts/signup/', views.user_registration, name='signup'),

	path('search/', views.search, name='search'),
	# Class Based Views.

	path('class/home/', views.HomeView.as_view(), name='class_home'),
	path('class/add/blog/', views.AddBlog.as_view(), name='class_add_blog'),

	# Generic views
	path('generic/blog/list/', views.BlogListView.as_view(), name='generic_blog_list'),
	path('generic/blog/detail/<int:pk>/', views.BlogDetailView.as_view(), name='generic_blog_detail'),
]
