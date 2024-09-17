from django.contrib import admin
from Core.models import *
# Register your models here.

class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages
    
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = [ 'category', 'title' , 'price' , 'featured' , 'product_status']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title' ,'image']
    
class VendorAdmin(admin.ModelAdmin):
    list_display = ['title' ,'image']
    
class CartAdmin(admin.ModelAdmin):
    list_editable = ['paid_status' , 'product_status']
    list_display = ['user' ,'price' ,'paid_status' , 'order_date' , 'product_status']
       
class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display = ['order' ,'invoice_no' ,'item' , 'qty' , 'price' , 'total']
    
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user' ,'product' ,'review' , 'rating' , 'date']
    
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user' ,'product']
    
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user' ,'address1' , 'status']
    
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name' , 'email']
    
    
admin.site.register(Product , ProductAdmin)
admin.site.register(Category , CategoryAdmin)
admin.site.register(Vendor , VendorAdmin)
admin.site.register(Cart , CartAdmin)
admin.site.register(CartOrderItems , CartOrderItemsAdmin)
admin.site.register(ProductReview , ProductReviewAdmin)
admin.site.register(Wishlist , WishlistAdmin)
admin.site.register(Address , AddressAdmin)
admin.site.register(Contact , ContactAdmin)