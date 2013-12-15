# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext 

from flatpages.models import FlatPage
from django.forms import ModelForm
from books.models import Book

class BookForm(ModelForm):
    class Meta:
        model = Book

def register(request):
    """
    if request.method == 'POST': # If the form has been submitted...
        form = BookForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
    """
    form = BookForm()
    tpl_params = { 'form' : form }
    return render_to_response("register.html", tpl_params, context_instance = RequestContext(request))
