from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Product, Variation
from apps.category.models import Category

from apps.carts.views import _cart_id
from apps.carts.models import CartItem

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from django.db.models import Q

def store(request, category_slug=None):
    # Initialize product queryset
    products = None

    if category_slug:
        # Retrieve the single Category instance matching the slug
        categories = get_object_or_404(Category, slug=category_slug)
        # Filter products belonging to this category and that are available
        products = Product.objects.filter(category=categories, is_available=True) 

        paginator = Paginator(products, 10)
        page = request.GET.get("page")
        paged_products = paginator.get_page(page)

    else:
        # No category filter, fetch all available products
        products = Product.objects.filter(is_available=True).order_by("id")
        
        # pagination
        paginator = Paginator(products, 10)
        page = request.GET.get("page")
        paged_products = paginator.get_page(page)
        print("paged_products: ", paged_products)

    context = {
        "products": paged_products
    }

    return render(request, "store/store.html", context)


def product_detail(request, category_slug, product_slug):
    single_product = get_object_or_404(
        Product,
        category__slug=category_slug,
        slug=product_slug,
    )

    in_cart = CartItem.objects.filter(
        cart__cart_id=_cart_id(request),
        product=single_product
    ).exists()

    colors = Variation.objects.filter(
        product=single_product,
        variation_category="color",
        is_active=True
    )

    sizes = Variation.objects.filter(
        product=single_product,
        variation_category="size",
        is_active=True
    )

    context = {
        "single_product": single_product,
        "in_cart": in_cart,
        "colors": colors,
        "sizes": sizes,
    }

    return render(request, "store/product_detail.html", context)
    
def search(request):
    if "keyword" in request.GET:
        keyword = request.GET["keyword"]
        print("keyword: ", keyword)
        if keyword:
            products = Product.objects.order_by("-created_date").filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
        else:
            products = Product.objects.filter(is_available=True).order_by("id")
    
    paginator = Paginator(products, 10)
    page = request.GET.get("page")
    paged_products = paginator.get_page(page)
    
    context = {
        "products": paged_products
    }
    return render(request, "store/store.html", context)