from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Dailyfeed
from .models import Book
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime, date
from .forms import dailyfeedForm
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.views.generic import DetailView,DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from .serializer import BookSerializers,FeedSerializers
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth.models import User, auth

class feed_view(APIView):
    def get(self,request):
        data = Dailyfeed.objects.all()
        serializer = FeedSerializers(data, many=True)
        return Response(serializer.data)

    def post(self,request,format=None):
        try:
            serializer = FeedSerializers(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data , status =status.HTTP_200_OK)
            else:
                return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
           return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = FeedSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class book_view(APIView):
    def get(self,request):
        data = Book.objects.all()
        serializer = BookSerializers(data, many=True)
        return Response(serializer.data)

    def post(self,request,format=None):
        try:
            serializer = BookSerializers(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data , status =status.HTTP_200_OK)
            else:
                return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
           return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = BookSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    

@login_required
def mainhome(request):
    return render(request, 'diary/index.html')

def UpdatePostView(request, slug_text):
    if request.user.is_authenticated:
        post = get_object_or_404(Dailyfeed, slug=slug_text)
        print(post)

        if post.blog_creator != request.user:
            return HttpResponse('<h1>Permission Denied</h1>')
        form = dailyfeedForm(instance=post)

        if request.method == 'POST':
            post = get_object_or_404(Dailyfeed, slug=slug_text)
            form = dailyfeedForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data.get('title')
                blog= form.cleaned_data.get('blog')
                

                post.title = title
                post.blog = blog
                
                post.save()
                return redirect('mainhome')

        return render(request, 'diary/update.html', {'form': form})
    else:
        return redirect('contact')



class DeletePostView(DeleteView): 
    model=Dailyfeed
    
    success_url= reverse_lazy("blog")

    
  
    
 

def Postdetail(request, slug_text):

    q = Dailyfeed.objects.filter(slug=slug_text)
    if q.exists():
        q = q.first()
    else:
        return HttpResponse('<h1>Post Not Found</h1>')
    context = {

        'post': q
    }
    return render(request, 'diary/post_detail.html', context)
    
    

def blog(request):
    logged_user=request.user
    Dailyfeeds = Dailyfeed.objects.filter(blog_creator=logged_user).order_by('-created_at')
    context = {'Dailyfeeds' : Dailyfeeds}
    return render(request, 'diary/blog.html', context)

def about(request):
    Books= Book.objects.all()
    context = {'Books' : Books}
    return render(request, 'diary/about.html', context)

#def creatediary(request):
        #if request.method == 'POST':
            #if request.POST.get('mood') and request.POST.get('content'):
                #post=Dailyfeed()
                #blog_creator=User.objects.get(username=request.user.username)
                #blog_creator.save()
                #post.blog_creator = blog_creator
                #post.title= request.POST.get('mood')
                #post.blog= request.POST.get('content')
                #post.save()
                
                #return render(request, 'diary/index.html')  

        #else:
                #return render(request,'diary/contact.html')
	
"""def creatediary(request):
    if request.method  == 'POST':
        form = dailyfeedForm(request.POST)
        if form.is_valid():
            model_instance = form.save()
            model_instance.blog_creator=request.user
            model_instance.title = form.cleaned_data.get('title')
            model_instance.blog = form.cleaned_data.get('blog')
            
            model_instance.save()
            return redirect('mainhome')
    else:
         form = dailyfeedForm()
    return render(request, 'diary/contact.html', {'form': form})"""

def creatediary(request):
    if request.user.is_authenticated:
        blog_creator = request.user

        if request.method == 'GET':
            form = dailyfeedForm()
            context = {
                'form': form
            }
            return render(request, 'diary/contact.html', context)

        else:
            form = dailyfeedForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data.get('title')
                blog= form.cleaned_data.get('blog')
                

                Dailyfeed.objects.create(
                    blog_creator=blog_creator,  # user who is active will be the owner of post created
                    title=title,
                    blog=blog
                    
                )
                return redirect('mainhome')
            else:
                return render(request, 'posts/contact.html', context)
    else:
        return redirect('contact.html')

def profile(request):
    return render(request, 'diary/profile.html')

