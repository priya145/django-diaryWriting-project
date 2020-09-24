
from django.db import models
from django.contrib.auth.models import User
from landingpage.models import Profile
from datetime import datetime, date
from ckeditor.fields import RichTextField
from django.utils import timezone
from django.db.models.signals import pre_save, post_save
from mindnote.utils import unique_slug_generator


class Dailyfeed(models.Model):
    blog_creator=models.ForeignKey(User, on_delete=models.CASCADE, blank=True , null=False)
    title=models.CharField(max_length=100,blank=True)
    #blog=models.TextField(max_length=1000,blank=True)
    slug = models.SlugField(max_length=250, null=True, blank=True)
    blog=RichTextField(blank=True, null=False)
    created_at = models.DateField(auto_now_add=True,auto_now=False)
    

    def __str__(self):
        return self.blog_creator.username

    

    



def save_title_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(save_title_slug, sender=Dailyfeed)


class Book(models.Model):
    name=models.CharField(max_length=100)
    author=models.CharField(max_length=100)
    published_date=models.DateField()
    description=RichTextField(blank=True, null=False)
    price=models.IntegerField()
    img=models.ImageField(upload_to='uploads/')

    def __str__(self):
        return self.name


