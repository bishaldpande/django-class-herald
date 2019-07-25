from django.shortcuts import render
from .models import Blog, Comment
from .forms import BlogForm, CommentForm, UserSignupForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from django.views import View
# Create your views here.
from .temp import Temp


class HomeView(View):
	template_name = 'index.html'
	
	def get(self, request):
		blogs=Blog.objects.all()
		try:
			latest_blog= Blog.objects.all().order_by('created_date')[0]
		except:
			latest_blog = []

		print(request.session)
		last_viewed = request.session.get('last_viewed', None)
		if last_viewed:
			last_viewed = Blog.objects.get(id=last_viewed)

		context_dict={
			'blogs':blogs,
			'latest_blog': latest_blog,
			'last_viewed': last_viewed,
		}
		return render(request, self.template_name, context_dict)


def user_registration(request):
	if request.method == 'POST':
		form = UserSignupForm(request.POST)
		if form.is_valid():
			form.save()
			send_mail(
				'Welcome',
				'Welcome to my site.',
				settings.EMAIL_HOST_USER,
				[request.POST.get('email')]
				)
			messages.success(request, "Added User Sucessfully")
			return redirect('login')
	else:
		form = UserSignupForm()
	return render(request,'registration/create_user.html',{'form':form})


def home(request):
	blogs=Blog.objects.all()
	try:
		latest_blog= Blog.objects.all().order_by('created_date')[0]
	except:
		latest_blog = []

	print(dir(request.session))
	last_viewed = request.session.get('last_viewed', None)
	if last_viewed:
		last_viewed = Blog.objects.get(id=last_viewed)

	context_dict={
		'blogs':blogs,
		'latest_blog': latest_blog,
		'last_viewed': last_viewed,
	}
	return render(request, 'index.html', context_dict)



# https://docs.djangoproject.com/en/2.1/topics/http/file-uploads/
@login_required
def add_blog(request):
	form = BlogForm()
	if request.method =='POST':
		print(request.POST)
		form = BlogForm(request.POST, request.FILES)
		if form.is_valid():
			blog = form.save(commit=False)
			blog.author = request.user
			blog.save()
			messages.success(request, "Added Blog Sucessfully")
			return redirect('home')

	context_dict = {'form':form}
	return render(request, 'add_blog.html', context_dict)

from django.contrib.auth.mixins import LoginRequiredMixin

class AddBlog(LoginRequiredMixin, View):
	template_name = 'add_blog.html'
	form_class = BlogForm

	def get(self, request):
		context_dict = {'form': self.form_class()}
		return render(request, self.template_name, context_dict)

	def post(self, request):
		form = self.form_class(request.POST, request.FILES)
		if form.is_valid():
			blog = form.save(commit=False)
			blog.author = request.user
			blog.save()
			messages.success(request, "Blog has been added")
			return redirect('class_home')


from django.db.models import Q
def search(request):
	sqs = request.POST.get('q')
	# print(sqs)
	if sqs:
		blogs = Blog.objects.filter(Q(title__icontains=sqs) | Q(description__icontains=sqs))
	else:
		blogs = []
	context_dict = {"blogs": blogs}
	return render(request, 'search_result.html', context_dict)


def blog_details(request, id):
	blog = Blog.objects.get(id=id)

	if request.method == 'POST':
		print(request.POST)

		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.blog = blog
			comment.commented_by = request.user
			comment.save()

	request.session['last_viewed'] = blog.id
	print(request.session)

	comments = Comment.objects.filter(blog=blog)
	context_dict = {'blog':blog, 'comments':comments}
	return render(request, 'blog_detail.html', context_dict)


@login_required
def edit_blog(request, id):
	blog = Blog.objects.get(id=id)

	if request.method =='POST':
		form = BlogForm(request.POST, request.FILES, instance=blog)
		if form.is_valid():
			form.save()
			return redirect('home')

	form = BlogForm(instance=blog)
	context_dict = {'form':form}
	return render(request, 'edit_blog.html', context_dict)


@login_required
def delete_blog(request, id):
	blog = Blog.objects.get(id=id)
	blog.delete()	
	return redirect('home')

from django.views.generic import ListView, DetailView

class BlogListView(ListView):
	template_name = 'index.html'
	queryset = Blog.objects.all()

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['blogs'] = Blog.objects.all()
		context['latest_blog'] = Blog.objects.order_by('created_date').first()
		return context

class BlogDetailView(DetailView):
	model = Blog
	form_class = CommentForm
	template_name = 'blog_detail.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['form'] = self.form_class()
		return context

from rest_framework import viewsets, permissions
from .serializers import UserSerializer, BlogSerializer
from django.contrib.auth.models import User

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, )


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


def from_view(request):
	if request.method == "POST":
		Temp.temp(p=request.POST.get('p'), q = request.POST.get('p'))