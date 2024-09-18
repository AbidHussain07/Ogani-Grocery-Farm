from django.shortcuts import render , redirect
from Core.models import *
from django.db.models import Count , Avg
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import JsonResponse
from django.contrib import messages
from django.template.loader import render_to_string
from django.core import serializers
from django.core.mail import send_mail
# Create your views here.

def home(request):
    category = Category.objects.all()
    products = Product.objects.filter(product_status = "published").order_by("category")
    # wishlist = Wishlist.objects.filter(user =request.user)
    
    context = {
        'products' : products,
        'category' : category,
        # 'wishlist' : wishlist,
    }
    return render(request, 'core/home.html' , context)

def category_view(request):
    category = Category.objects.all()
    
    context = {
        'category' : category
    }
    return render(request, 'core/category.html' , context)

def product_view(request , cid):
    category = Category.objects.get(cid = cid)
    products = Product.objects.filter(category = category , product_status = "published")
    context = {
        'products' : products,
        'category' : category
    }

    return render(request, 'core/product.html' , context)

def blog_view(request):
    return render(request, 'core/blog.html')

def contact_view(request):
    if request.method == "POST":
        data = request.POST
        name = data.get('name')
        email = data.get('email')
        message = data.get('review')
        
        Contact.objects.create(
            name = name ,
            email = email ,
            review = message,
        )
        messages.success(request , f"Thanks For Your Message! We will see to it.")  
        return redirect(request.META.get('HTTP_REFERER', '/'))
    return render(request, 'core/contact.html')
       
def product_detail(request , pid):
    product = Product.objects.get(pid = pid)
    products = Product.objects.filter(category = product.category).exclude(pid = pid)
    review = ProductReview.objects.filter(product = product).order_by("date")
    
    # getting average review
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating = Avg('rating'))
    
    # product = get_object_or_404 (Product , pid = pid)  # ====>another method same as above
    p_image = product.p_image.all()
    
    context = {
        'p' : product,
        "p_image":p_image,
        'products' : products,
        'review' : review , 
        'average_rating' : average_rating
    }
    return render(request, 'core/product_details.html' , context)

def search_view(request):
    query = request.GET.get("q")
    
    product = Product.objects.filter(title__icontains=query).order_by("-date")
    
    context = {
        'product' : product,
        'query' : query,
    }
    return render(request, 'core/search.html' , context)

@login_required
def add_to_cart(request):
    cart_product = {}
    
    cart_product[str(request.GET['id'])] = {
        'title' : request.GET['title'],
        'qty' : request.GET['qty'],
        'price' : request.GET['price'],
        'image' : request.GET['image'],
        'pid' : request.GET['pid'],
    }
    
    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product
        
    return JsonResponse({"data":request.session['cart_data_obj'] , "totalcartitems":len(request.session['cart_data_obj'])})

@login_required
def cart_items(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id , item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
        return render(request, 'core/shopping-cart.html' , {"cart_data":request.session['cart_data_obj'] , "totalcartitems":len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
    else:
        messages.warning(request , "Your Cart is Empty Please Add Something ...")
        return redirect('/')
        # return render(request, 'core/shopping-cart.html' )

@login_required     
def delete_item_from_cart(request):
    product_id = str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data
    
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id , item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
            
    context = render_to_string("core/async/cart-list.html" , {"cart_data":request.session['cart_data_obj'] , "totalcartitems":len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
    return JsonResponse({"data":context, "totalcartitems":len(request.session['cart_data_obj'])})

@login_required
def update_cart(request):
    product_id = str(request.GET['id'])
    product_qty = request.GET['qty']
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = product_qty
            request.session['cart_data_obj'] = cart_data
    
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id , item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
            
    context = render_to_string("core/async/cart-list.html" , {"cart_data":request.session['cart_data_obj'] , "totalcartitems":len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
    return JsonResponse({"data":context, "totalcartitems":len(request.session['cart_data_obj'])})

@login_required
def checkout_view(request):
    # Initialize context dictionary
    context = {
        'cart_data': None,
        'totalcartitems': 0,
        'cart_total_amount': 0.0,
        'active_address': Address.objects.filter(user=request.user)
    }
    
    # Check if 'cart_data_obj' exists in session
    if 'cart_data_obj' in request.session:
        # Calculate cart total amount
        cart_total_amount = 0
        cart_data = request.session['cart_data_obj']
        for p_id, item in cart_data.items():
            cart_total_amount += int(item['qty']) * float(item['price'])
        
        context.update({
            'cart_data': cart_data,
            'totalcartitems': len(cart_data),
            'cart_total_amount': cart_total_amount
        })
    
    return render(request, 'core/checkout.html', context)


# def after_order_placed(request):
    
#     total_amount = 0
#     if 'cart_data_obj' in request.session:
#         for p_id , item in request.session['cart_data_obj'].items():
#             total_amount += int(item['qty']) * float(item['price'])
#         # create Order Object   
#         order = Cart.objects.create(
#             user=request.user,
#             price = total_amount
#         )
#         # getting total_amount for cart
#         for p_id , item in request.session['cart_data_obj'].items():
#             total_amount += int(item['qty']) * float(item['price'])
            
#             cart_item = CartOrderItems.objects.create(
#                 order=order,
#                 invoice_no = "INVOICE_NO-" + str(order.id),
#                 item = item['title'],
#                 image = item['image'],
#                 qty = item['qty'],
#                 price = item['price'],
#                 total = int(item['qty']) * float(item['price'])
#             )
    
#     cart_total_amount = 0
#     if 'cart_data_obj' in request.session:
#         for p_id , item in request.session['cart_data_obj'].items():
#             cart_total_amount += int(item['qty']) * float(item['price'])
#     return render(request, 'core/invoice.html' , {"cart_data":request.session['cart_data_obj'] , "totalcartitems":len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})

@login_required
def after_order_placed(request):
    cart_data = request.session.get('cart_data_obj', {})

    # if not cart_data:
    #     # If no cart data, redirect to checkout or home page
    #     return redirect('checkout')  # or any other suitable redirection

    total_amount = sum(int(item['qty']) * float(item['price']) for item in cart_data.values())

    # Create Order Object
    order = Cart.objects.create(
        user=request.user,
        price=total_amount
    )

    # Create Cart Order Items
    for p_id, item in cart_data.items():
        CartOrderItems.objects.create(
            order=order,
            invoice_no="INVOICE_NO-" + str(order.id),
            item=item['title'],
            image=item['image'],
            qty=item['qty'],
            price=item['price'],
            total=int(item['qty']) * float(item['price'])
        )

    # Email Details
    subject = 'Order Confirmation'
    message = render_to_string('core/order_confirmation_email.txt', {
        'user': request.user,
        'order': order,
        'cart_data': cart_data,
        'total_amount': total_amount,
    })
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [request.user.email]

    # Send Email
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

    # Clear cart data
    request.session.pop('cart_data_obj', None)
    messages.success(request , f"Your Order has been Placed Successfully.")
    
    # Return the invoice view
    return render(request, 'core/invoice.html', {
        "cart_data": cart_data,
        "totalcartitems": len(cart_data),
        'cart_total_amount': total_amount
    })
    
@login_required   
def customer_dashboard(request):
    orders = Cart.objects.filter(user = request.user).order_by("-id")
    address = Address.objects.filter(user = request.user)
    context = {
        "orders" : orders,
        "address" : address,
    }
    if request.method == "POST":
        data = request.POST
        address1 = data.get('address1')
        address2 = data.get('address2')
        city = data.get('city')
        state = data.get('state')
        zipcode = data.get('zip')
        phone = data.get('phone')
        
        Address.objects.create(
            user = request.user ,
            address1 = address1 ,
            address2 = address2 ,
            city = city,
            state = state,
            zip_code = zipcode,
            phone_no = phone,
        )
        return redirect(request.META.get('HTTP_REFERER', '/'))
    return render(request, 'core/dashboard.html',context)

@login_required   
def order_view(request , id):
    order = Cart.objects.get(user = request.user , id=id)
    items = CartOrderItems.objects.filter(order = order)
    context = {
        "items" : items
    }
    return render(request, 'core/order-view.html',context)

@login_required
def update_address(request):
    queryset = Address.objects.get(user = request.user)
    
    if request.method == "POST":
        data = request.POST
        
        address1 = data.get('address1')
        address2 = data.get('address2')
        city = data.get('city')
        state = data.get('state')
        zipcode = data.get('zip')
        phone = data.get('phone')
        
        queryset.address1 = address1
        queryset.address2 = address2
        queryset.city = city
        queryset.state = state
        queryset.zip_code = zipcode
        queryset.phone_no = phone
            
        queryset.save()
        return redirect('/dashboard/')
    context = {'address' : queryset}
    return render (request ,'core/update-address.html' , context)

@login_required
def wishlist_view(request):
    wishlist = Wishlist.objects.filter(user =request.user)

        
    context = {
        'wishlist' : wishlist,
    }
    return render (request ,'core/wishlist.html' , context)

@login_required
def add_to_wishlist(request):
    product_id = request.GET['id']
    product = Product.objects.get(id=product_id)
    
    context = {}
    
    wishlist_count = Wishlist.objects.filter(product=product , user=request.user).count()
    if  wishlist_count > 0:
        context ={
            "bool":True
        }
    else:
        new_wishlist = Wishlist.objects.create(
            product=product ,
            user=request.user
        )
        context = {
            "bool":True
        }
    return JsonResponse(context)
 
@login_required   
def remove_wishlist(request):
    pid = request.GET['id']
    wishlist = Wishlist.objects.filter(user = request.user)
    
    product = Wishlist.objects.get(id=pid)
    product.delete()
    
    context ={
        "bool":True,
        "wishlist" : wishlist
    }
    wishlist_json = serializers.serialize('json',wishlist)
    data = render_to_string("core/async/wishlist-list.html" ,context)
    return JsonResponse({'data' : data , 'wishlist':wishlist_json})
    