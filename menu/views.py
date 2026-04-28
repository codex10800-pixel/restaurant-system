from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from .models import Category, MenuItem, Reservation, Order, OrderItem
from .cart import get_cart, add_to_cart, remove_from_cart, update_quantity, clear_cart, get_cart_total, get_cart_count
import uuid
import hashlib
from datetime import datetime, timedelta

def home(request):
    featured_items = MenuItem.objects.filter(featured=True, available=True)[:6]
    categories = Category.objects.all()
    cart_count = get_cart_count(request)
    return render(request, 'home.html', {
        'featured_items': featured_items,
        'categories': categories,
        'cart_count': cart_count
    })

def menu(request):
    categories = Category.objects.all()
    menu_items = MenuItem.objects.filter(available=True)
    cart_count = get_cart_count(request)
    return render(request, 'menu.html', {
        'categories': categories,
        'menu_items': menu_items,
        'cart_count': cart_count
    })

def about(request):
    cart_count = get_cart_count(request)
    return render(request, 'about.html', {'cart_count': cart_count})

def contact(request):
    cart_count = get_cart_count(request)
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        date = request.POST.get('date')
        time = request.POST.get('time')
        guests = request.POST.get('guests')
        message = request.POST.get('message')
        
        # Save reservation to database
        reservation = Reservation(
            name=name, email=email, phone=phone,
            date=date, time=time, guests=guests, message=message
        )
        reservation.save()
        
        # Build WhatsApp message
        whatsapp_number = '27XXXXXXXXX'  # Replace with actual restaurant number
        message_text = f"Reservation Request:%0A%0AName: {name}%0APhone: {phone}%0AGuests: {guests}%0ADate: {date}%0ATime: {time}%0AMessage: {message or 'None'}"
        whatsapp_url = f"https://wa.me/{whatsapp_number}?text={message_text}"
        
        # Redirect to WhatsApp
        return redirect(whatsapp_url)
    
    return render(request, 'contact.html', {'cart_count': cart_count})


# ==========================================
# CART VIEWS
# ==========================================

def cart_view(request):
    """Display cart page"""
    cart = get_cart(request)
    total = get_cart_total(request)
    cart_count = get_cart_count(request)
    
    # Calculate subtotals for each item
    for item in cart:
        item['subtotal'] = item['price'] * item['quantity']
    
    return render(request, 'cart.html', {
        'cart': cart,
        'total': total,
        'cart_count': cart_count
    })


def add_to_cart_api(request):
    """API endpoint to add item to cart"""
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        try:
            menu_item = MenuItem.objects.get(id=item_id)
            cart = add_to_cart(request, item_id, menu_item.name, float(menu_item.price), menu_item.image)
            cart_count = get_cart_count(request)
            return JsonResponse({
                'success': True,
                'cart_count': cart_count,
                'message': f'{menu_item.name} added to cart!'
            })
        except MenuItem.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Item not found'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})


def remove_from_cart_api(request):
    """API endpoint to remove item from cart"""
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        cart = remove_from_cart(request, item_id)
        total = get_cart_total(request)
        cart_count = get_cart_count(request)
        
        return JsonResponse({
            'success': True,
            'cart': cart,
            'total': total,
            'cart_count': cart_count
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})


def update_cart_api(request):
    """API endpoint to update item quantity"""
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('quantity', 1))
        
        cart = update_quantity(request, item_id, quantity)
        total = get_cart_total(request)
        cart_count = get_cart_count(request)
        
        return JsonResponse({
            'success': True,
            'cart': cart,
            'total': total,
            'cart_count': cart_count
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})


# ==========================================
# CHECKOUT VIEWS
# ==========================================

def checkout(request):
    """Checkout page with user info form"""
    cart = get_cart(request)
    total = get_cart_total(request)
    cart_count = get_cart_count(request)
    
    if not cart:
        return redirect('menu')
    
    # Calculate subtotals for each item
    for item in cart:
        item['subtotal'] = item['price'] * item['quantity']
    
    # Generate default pickup times (next 2 hours)
    pickup_times = []
    now = datetime.now()
    for i in range(2, 6):  # 2 to 5 hours from now
        pickup_time = now + timedelta(hours=i)
        pickup_times.append(pickup_time.strftime('%H:%M'))
    
    return render(request, 'checkout.html', {
        'cart': cart,
        'total': total,
        'cart_count': cart_count,
        'pickup_times': pickup_times
    })


def process_checkout(request):
    """Process checkout and create order"""
    if request.method == 'POST':
        cart = get_cart(request)
        
        if not cart:
            return redirect('menu')
        
        # Get form data
        customer_name = request.POST.get('customer_name')
        phone = request.POST.get('phone')
        pickup_time = request.POST.get('pickup_time')
        
        if not all([customer_name, phone, pickup_time]):
            return render(request, 'checkout.html', {
                'cart': cart,
                'total': get_cart_total(request),
                'cart_count': get_cart_count(request),
                'error': 'Please fill in all required fields'
            })
        
        # Calculate total
        total = get_cart_total(request)
        
        # Generate unique order number
        order_number = f"ORD-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        
        # Create order
        from django.utils.dateparse import parse_time
        order = Order(
            order_number=order_number,
            customer_name=customer_name,
            phone=phone,
            pickup_time=parse_time(pickup_time),
            total=total,
            status='pending'
        )
        order.save()
        
        # Create order items
        for item in cart:
            menu_item = MenuItem.objects.get(id=item['id'])
            OrderItem.objects.create(
                order=order,
                menu_item=menu_item,
                quantity=item['quantity'],
                unit_price=menu_item.price,
                subtotal=item['price'] * item['quantity']
            )
        
        # Clear cart
        clear_cart(request)
        
        # Redirect to payment
        return redirect('payment', order_id=order.id)
    
    return redirect('checkout')


# ==========================================
# PAYFAST PAYMENT
# ==========================================

def payment(request, order_id):
    """Display payment page with PayFast form"""
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return redirect('menu')
    
    cart_count = get_cart_count(request)
    
    # PayFast sandbox credentials - replace with real ones in production
    PAYFAST_MERCHANT_ID = '10024000'  # Sandbox merchant ID
    PAYFAST_MERCHANT_KEY = '46f0cd694581a'  # Sandbox merchant key
    PAYFAST_URL = 'https://sandbox.payfast.co.za/eng/process'
    
    # Build PayFast payment data
    pf_data = {
        'merchant_id': PAYFAST_MERCHANT_ID,
        'merchant_key': PAYFAST_MERCHANT_KEY,
        'return_url': request.build_absolute_uri(reverse('payment_success', args=[order.id])),
        'cancel_url': request.build_absolute_uri(reverse('payment_cancel', args=[order.id])),
        'notify_url': request.build_absolute_uri(reverse('payment_notify')),
        'm_payment_id': order.order_number,
        'amount': str(order.total),
        'item_name': f'Molteno Grill Order {order.order_number}',
        'item_description': f'Order for {order.customer_name} - Pickup at {order.pickup_time}',
        'name_first': order.customer_name.split()[0] if order.customer_name else '',
        'name_last': ' '.join(order.customer_name.split()[1:]) if len(order.customer_name.split()) > 1 else '',
        'cell_number': order.phone,
        'email_address': f'{order.order_number.lower()}@moltenogrill.co.za',
    }
    
    # Generate passphrase and signature
    passphrase = 'MoltenoGrill2024'
    pf_data['passphrase'] = passphrase
    
    # Create signature
    signature = '&'.join([f"{k}={v}" for k, v in sorted(pf_data.items()) if v])
    pf_data['signature'] = hashlib.md5(signature.encode()).hexdigest()
    
    return render(request, 'payment.html', {
        'order': order,
        'pf_data': pf_data,
        'payfast_url': PAYFAST_URL,
        'cart_count': cart_count
    })


@csrf_exempt
def payment_notify(request):
    """PayFast ITN callback"""
    if request.method == 'POST':
        # Verify payment with PayFast
        # In production, you would verify with PayFast server
        payment_status = request.POST.get('payment_status')
        m_payment_id = request.POST.get('m_payment_id')
        
        if payment_status == 'COMPLETE':
            try:
                order = Order.objects.get(order_number=m_payment_id)
                order.status = 'paid'
                order.payment_id = request.POST.get('pf_payment_id', '')
                order.save()
            except Order.DoesNotExist:
                pass
    
    return HttpResponse('OK')


def payment_success(request, order_id):
    """Payment success page"""
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return redirect('menu')
    
    # Update order status
    order.status = 'paid'
    order.save()
    
    # Build WhatsApp message
    whatsapp_number = '27XXXXXXXXX'  # Replace with actual restaurant number
    whatsapp_message = f"Order Confirmed - Order ID {order.order_number}"
    whatsapp_url = f"https://wa.me/{whatsapp_number}?text={whatsapp_message.replace(' ', '%20')}"
    
    return render(request, 'payment_success.html', {
        'order': order,
        'whatsapp_url': whatsapp_url
    })


def payment_cancel(request, order_id):
    """Payment cancelled page"""
    try:
        order = Order.objects.get(id=order_id)
        order.status = 'cancelled'
        order.save()
    except Order.DoesNotExist:
        pass
    
    return render(request, 'payment_cancel.html', {
        'order_id': order_id
    })
