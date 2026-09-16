from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect

from .models import Cart, CartItem
from apps.store.models import Product, Variation

from apps.store.models import variation_category_choice

from django.contrib.auth.decorators import login_required

# Create your views here.


def _cart_id(request):
    """
    This function generates a unique cart ID for each session.
    If the cart ID is not found, it creates a new cart ID.
    """
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    # Fetch product first so it is available for variation lookup
    product = get_object_or_404(Product, id=product_id)

    # Collect selected variations (color, size) from POST data
    product_variation = []
    if request.method == "POST":
        for key, value in request.POST.items():
            print("key: ",key)
            print('value: ', value)
            try:
                variation = Variation.objects.get(
                    product=product,
                    variation_category__iexact=key,
                    variation_value__iexact=value
                )
                product_variation.append(variation)
            except Variation.DoesNotExist:
                pass

    # Get or create the cart
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))

    # Check if an identical cart item (same product + same variations) already exists
    cart_items = CartItem.objects.filter(product=product, cart=cart)
    # if len(product_variation) > 0:    
    existing_item = None
    for item in cart_items:
        if list(item.variations.all()) == product_variation:
            existing_item = item
            break

    if existing_item:
        existing_item.quantity += 1
        existing_item.save()
    else:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart
        )
        if product_variation:
            cart_item.variations.set(product_variation)
        cart_item.save()

    return redirect("cart")


def cart(request):
    total = 0
    quantity = 0
    cart_items = []
    tax = 0
    grand_total = 0

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total) / 100
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass

    context = {
        "total": total,
        "quantity": quantity,
        "cart_items": cart_items,
        "tax": tax,
        "grand_total": grand_total,
    }
    return render(request, "store/cart.html", context)


def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect("cart")


def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect("cart")


def update_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.quantity += 1
    cart_item.save()
    return redirect("cart")

@login_required(login_url="login")
def checkout(request):
    total = 0
    quantity = 0
    cart_items = []
    tax = 0
    grand_total = 0

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total) / 100
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass

    context = {
        "total": total,
        "quantity": quantity,
        "cart_items": cart_items,
        "tax": tax,
        "grand_total": grand_total,
    }

    return render(request, "store/checkout.html", context)