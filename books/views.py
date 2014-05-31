# Create your views here.
import json

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext, Context, loader
from django.contrib.auth import authenticate, login

from django import forms
from django.forms import ModelForm
from django.forms import widgets
from django.forms.models import inlineformset_factory

from django.core.mail import send_mail

from books.models import Book, Collaboration
from people.models import FernandUser

class CheckUserExistenceForm(forms.Form):
    email = forms.EmailField()

class BookForm(ModelForm):
    class Meta:
        model = Book
        exclude = ['slug', 'people', 'is_submitted', 'submitted_by', 'submitted_on']

class FernandUserForm(ModelForm):
    class Meta:
        exclude = ['title', 'password', 'last_login', 'is_superuser', 'groups', 'user_permissions', 'email_invalid', 'alternate_email', 'phone_alternate', 'fax', 'gender', 'national_number', 'id_card_number', 'sis_number', 'vat', 'rc', 'bank_iban', 'is_active', 'date_joined', 'is_staff', 'subscribed_to_mailing']
        model = FernandUser

class CollaborationForm(forms.ModelForm):
    class Meta:
        model = Collaboration
        widgets = {
            'person': widgets.HiddenInput() 
           }

class CollaborationRoleForm(forms.ModelForm):
    class Meta:
        model = Collaboration
        exclude = ['person', 'book']

def edit(request, slug):
    book = get_object_or_404(Book, slug=slug)
    if request.method == 'POST': # If the form has been submitted...
        form = BookForm(request.POST, instance=book) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            form.save()
            return HttpResponseRedirect(reverse('books-edit-collaborators', kwargs={ 'slug' : book.slug }))
    else:
        form = BookForm(instance=book) # A form to edit an existing book
    tpl_params = { 'form' : form, 'book': book }
    return render_to_response("register.html", tpl_params, context_instance = RequestContext(request))

def register(request):
    if request.method == 'POST': # If the form has been submitted...
        print "got request"
        form = BookForm(request.POST) # A form bound to the POST data
        print "found a form"
        if form.is_valid(): # All validation rules pass
            print "form is valid"
            new_book = form.save()
            print "form saved"
            return HttpResponseRedirect(reverse('books-edit-collaborators', kwargs={ 'slug' : new_book.slug }))
    else:
        form = BookForm(initial = { 'publication_year' : 2013, 'isbn' : '-' }) # An unbound form for a new book
    tpl_params = { 'form' : form }
    return render_to_response("register.html", tpl_params, context_instance = RequestContext(request))


def users_for_lookahead():
    for u in FernandUser.objects.all():
        full_name = u.get_full_name()
        yield {
               'value': u.id,
               'tokens': full_name.split(' '),
               'name': full_name
               }

def edit_book_collaborators(request, slug):
    book = get_object_or_404(Book, slug=slug)
    users_hash = json.dumps(list(users_for_lookahead()), ensure_ascii=False)
    # How much required roles are we still missing?
    required = set([2,1,3,4])
    present = set(c.role.id for c in Collaboration.objects.filter(book=book))
    missing = required - present
    
    # We want a (pre-filled) form for all of them, and one extra empty
    # to suggest that additional roles are welcome
    extra = len(missing) + 1
    
    BookCollaboratorFormSet = inlineformset_factory(Book, Book.people.through, form=CollaborationForm, extra=extra)
    
    if request.method == 'POST': # If the form has been submitted...
        formset = BookCollaboratorFormSet(request.POST, instance=book)
        if formset.is_valid():
            #import pdb; pdb.set_trace()
            f = formset.save()
            return HttpResponseRedirect(reverse('books-submit', kwargs={ 'slug' : book.slug }))
    else:
        formset = BookCollaboratorFormSet(instance=book)
    tpl_params = { 'formset': formset, 'book' : book, 'users_hash': users_hash }
    return render_to_response("register_book_collaborators.html", tpl_params, context_instance = RequestContext(request))

def add_book_collaborator(request, slug):
    book = get_object_or_404(Book, slug=slug)
    
    if request.method == 'POST': # If the form has been submitted...
        user_form = FernandUserForm(request.POST) # A form bound to the POST data
        role_form = CollaborationRoleForm(request.POST)
        if user_form.is_valid() and role_form.is_valid(): # All validation rules pass
            
            # The new person!
            person = user_form.save()
            
            # The role_form only specified the role of the collaboration,
            # we associate the other properties by hand.
            collaboration = role_form.save(commit=False)
            collaboration.book = book
            collaboration.person = person
            
            # The new collaboration!
            collaboration.save()
            
            return HttpResponseRedirect(reverse('books-edit-collaborators', kwargs={ 'slug': book.slug }))
    else:
        user_form = FernandUserForm()
        role_form = CollaborationRoleForm()

    tpl_params = { 'user_form' : user_form, 'role_form': role_form, 'book': book }
    return render_to_response("register_book_collaborator_add.html", tpl_params, context_instance = RequestContext(request))

def submit(request, slug):
    book = get_object_or_404(Book, slug=slug)
    if request.method == 'POST':
        book.is_submitted = True
        book.save()
        mail_template = loader.get_template('confirmation_mail.txt')
        subject = book.title
        c = Context({"submission_uri": 'http://' + request.get_host() + request.path, 'book' : book })
        mail_text = mail_template.render(c)
        send_mail(subject, mail_text, 'info@prixfernandbaudinprijs.be', [request.user.email, 'info@prixfernandbaudinprijs.be'])
    tpl_params = { 'book' : book }
    return render_to_response("register_submit.html", tpl_params, context_instance = RequestContext(request))


def all_books(request):
    books = Book.objects.all()
    """
    book = {
        "designer": "person, person"
    }
    """
    
    filtered_books = []
    
    def get_collaborators(role_id):
        if isinstance(role_id, list):
            # if the argument to the function is a list, get_collaborators([1, 8, 7])
            # look for all the books collaborators that have one of these roles 
            query = book.collaboration_set.filter(role_id__in=role_id)
        else:
            # if the argument to the function is a number, get_collaborators(5)
            # look for all the books collaborators that have this role
            query = book.collaboration_set.filter(role_id=role_id)
        
        # in the model of each found collaboration, find the person, ask for their name
        names = [c.person.get_full_name() for c in query]
        
        # turn it from a list into a set of unique values (no doubles)
        unique_names = set(names)
        
        # turn the list into a text by joining each item with a comma and a space, return it
        return ", ".join(unique_names)
    
    for book in books:
        filtered_book = {}
        filtered_book['authors']     = get_collaborators(5)
        filtered_book['publishers']  = get_collaborators(2)
        filtered_book['designers']   = get_collaborators([1, 8, 7])
        filtered_book['printers']    = get_collaborators(3)
        filtered_book['bookbinders'] = get_collaborators(4)
        
        filtered_book['id']       = book.id
        filtered_book['title']    = book.title
        filtered_book['subtitle'] = book.subtitle
        filtered_book['category'] = book.category
        
        filtered_books.append(filtered_book)
        
    tpl_params = { 'books' : filtered_books }
    return render_to_response("all_books.html", tpl_params, context_instance = RequestContext(request))


def register_login(request):
    if request.method == 'POST': # If the form has been submitted...
        form = CheckUserExistenceForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            email = form.cleaned_data['email']
            try:
                user = FernandUser.objects.get(email=email)
                authenticated_user = authenticate(user=user)
                login(request, authenticated_user)
                return HttpResponseRedirect(reverse('register'))
            except FernandUser.DoesNotExist:
                return HttpResponseRedirect(reverse('signup') + '?email=' + email) # Redirect after POST
    else:
        form = CheckUserExistenceForm() # An unbound form
    
    tpl_params = { 'form' : form }
    return render_to_response("register_login.html", tpl_params, context_instance = RequestContext(request))

def register_signup(request):
    if request.method == 'POST': # If the form has been submitted...
        form = FernandUserForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            user = form.save()
            authenticated_user = authenticate(user=user)
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('register'))
    else:
        email = request.GET.get('email')
        form = FernandUserForm(initial={'email': email })
    
    tpl_params = { 'form' : form }
    return render_to_response("register_signup.html", tpl_params, context_instance = RequestContext(request))
