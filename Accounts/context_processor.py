from ast import Add
from Core.models import *
from django.contrib import messages

def default(request):
    try:
        wishlist = Wishlist.objects.filter(user=request.user)
    except:
        messages.warning(request , "You need to login before Accesing Wishlist")
        wishlist = 0
        
    try:
        address = Address.objects.get(user=request.user)
    except:
        address = None
        
    return{
        'wishlist' : wishlist,
        'address' : address
    }