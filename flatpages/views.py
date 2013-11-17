# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext 

from flatpages.models import FlatPage

def flatpage(request, slug='about'):
    obj = get_object_or_404(FlatPage, slug=slug)
    tpl_params = { 'flatpage' : obj }
    return render_to_response("flatpage_detail.html", tpl_params, context_instance = RequestContext(request))
