# Create your views here.
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login


from flatpages.models import FlatPage
from django import forms
from django.forms import ModelForm
from books.models import Book
from people.models import FernandUser

class CheckUserExistenceForm(forms.Form):
    email = forms.EmailField()

class BookForm(ModelForm):
    class Meta:
        model = Book
        exclude = ['slug', 'people']

class FernandUserForm(ModelForm):
    class Meta:
        exclude = ['title', 'password', 'last_login', 'is_superuser', 'groups', 'user_permissions', 'email_invalid', 'alternate_email', 'phone_alternate', 'fax', 'gender', 'national_number', 'id_card_number', 'sis_number', 'vat', 'rc', 'bank_iban', 'is_active', 'date_joined', 'is_staff']
        model = FernandUser


def register(request):
    if request.method == 'POST': # If the form has been submitted...
        form = BookForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            new_book = form.save()
            tpl_params = { 'book' : new_book, 'submitted': True }
            return render_to_response("register.html", tpl_params, context_instance = RequestContext(request))
    else:
        form = BookForm() # An unbound form
    tpl_params = { 'form' : form }
    return render_to_response("register.html", tpl_params, context_instance = RequestContext(request))

def register_login(request):
    if request.method == 'POST': # If the form has been submitted...
        form = CheckUserExistenceForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            try:
                user = FernandUser.objects.get(email=form.cleaned_data['email'])
                authenticated_user = authenticate(user=user)
                login(request, authenticated_user)
                return HttpResponseRedirect(reverse('register'))
            except FernandUser.DoesNotExist:
                return HttpResponseRedirect(reverse('signup')) # Redirect after POST
    else:
        form = CheckUserExistenceForm() # An unbound form
    
    tpl_params = { 'form' : form }
    return render_to_response("register_login.html", tpl_params, context_instance = RequestContext(request))

def register_signup(request):
    form = FernandUserForm()
    tpl_params = { 'form' : form }
    return render_to_response("register_signup.html", tpl_params, context_instance = RequestContext(request))
