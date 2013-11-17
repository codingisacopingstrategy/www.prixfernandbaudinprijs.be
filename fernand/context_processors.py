from flatpages.models import FlatPage

def nav_items(context):
    return {'nav_items': FlatPage.objects.all() }