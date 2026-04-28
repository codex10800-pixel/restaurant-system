"""
Session-based Cart Utility
No login required - uses Django sessions
"""

def get_cart(request):
    """Get cart from session or create empty cart"""
    return request.session.get('cart', [])


def save_cart(request, cart):
    """Save cart to session"""
    request.session['cart'] = cart


def add_to_cart(request, item_id, name, price, image=''):
    """Add item to cart or increment quantity"""
    cart = get_cart(request)
    
    # Check if item already in cart
    for item in cart:
        if str(item['id']) == str(item_id):
            item['quantity'] += 1
            save_cart(request, cart)
            return cart
    
    # Add new item
    cart.append({
        'id': str(item_id),
        'name': name,
        'price': float(price),
        'image': image,
        'quantity': 1
    })
    save_cart(request, cart)
    return cart


def remove_from_cart(request, item_id):
    """Remove item from cart"""
    cart = get_cart(request)
    cart = [item for item in cart if str(item['id']) != str(item_id)]
    save_cart(request, cart)
    return cart


def update_quantity(request, item_id, quantity):
    """Update item quantity in cart"""
    cart = get_cart(request)
    
    for item in cart:
        if str(item['id']) == str(item_id):
            if quantity <= 0:
                cart.remove(item)
            else:
                item['quantity'] = quantity
            break
    
    save_cart(request, cart)
    return cart


def clear_cart(request):
    """Clear all items from cart"""
    save_cart(request, [])


def get_cart_total(request):
    """Calculate cart total"""
    cart = get_cart(request)
    total = sum(item['price'] * item['quantity'] for item in cart)
    return total


def get_cart_count(request):
    """Get total item count in cart"""
    cart = get_cart(request)
    return sum(item['quantity'] for item in cart)