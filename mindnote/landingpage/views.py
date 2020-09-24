from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .tokens import account_activation_token
from django.views.generic import TemplateView
from .serializer import ProfileSerializers
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from .models import Profile



class profile_view(APIView):
    def get(self,request):
        data = Profile.objects.all()
        serializer = ProfileSerializers(data, many=True)
        return Response(serializer.data)

    def post(self,request,format=None):
        try:
            serializer = ProfileSerializers(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data , status =status.HTTP_200_OK)
            else:
                return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
           return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = ProfileSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
 


def home(request):
    return render(request, 'landingpage/index.html')


def signup_view(request):
    if request.method  == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            # user can't login until link confirmed
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Please Activate Your Account'
            # load a template like get_template() 
            # and calls its render() method immediately.
            message = render_to_string('landingpage/activation_request.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                # method will generate a hash value with user related data
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        subject, message, to=[to_email]
            )
            email.send()
            return redirect('landingpage/activation_sent.html')
    else:
         form = SignUpForm()
    return render(request, 'landingpage/signup.html', {'form': form})


def activation_sent_view(request):
    return render(request, 'landingpage/activation_sent.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # checking if the user exists, if the token is valid.
    if user is not None and account_activation_token.check_token(user, token):
        # if valid set active true 
        user.is_active = True
        # set signup_confirmation true
        user.profile.signup_confirmation = True
        user.save()
        login(request, user)
        messages.success(request, f'Thank you for your email confirmation.Now you can login your account.')
        return redirect('home')
    else:
    	messages.success(request, f'Activation link is inivalid')
    	return redirect('home')



def base_layout(request):
    template='landingpage/index.html'
    return render(request,template)







    