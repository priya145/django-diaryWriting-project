from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from diary import views as user_views
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [

path('index.html', user_views.mainhome, name="mainhome"),
path('blog_view', user_views.blog, name="blog"),
path('diary_view', user_views.creatediary, name="diary"),
path('books_view', user_views.about, name="books"),
path('profile_view', user_views.profile, name="profile"),
path('<slug:slug_text>', user_views.Postdetail, name="post_detail"),
path('<slug:slug_text>/update', user_views.UpdatePostView, name="post_update"),
path('<slug>/delete', user_views.DeletePostView.as_view(), name="post_delete"),

]

