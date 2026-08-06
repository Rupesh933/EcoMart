
from .models import Category

def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)

# This function is create for category name should display in navbar