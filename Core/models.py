from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from Accounts.models import User
# Create your models here.

STATUS_CHOICES = (
    ("process" , "Processing"),
    ("shipped" , "Shipped"),
    ("out_for_delivery" , "Out for Delivery"),
    ("delivered" , "Delivered"),
)

STATUS = (
    ("draft" , "Draft"),
    ("disabled" , "Disabled"),
    ("rejected" , "Rejected"),
    ("in_review" , "In Review"),
    ("published" , "Published"),
)

RATING = (
    ( 1, "★ ☆ ☆ ☆ ☆"),
    ( 2, "★	★ ☆ ☆ ☆"),
    ( 3, "★	★ ★ ☆ ☆"),
    ( 4, "★	★ ★	★ ☆"),
    ( 5, "★	★ ★	★ ★"),
)


def user_directory_path(instance , filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=15, prefix="cat" , alphabet = "abcdefghilk123456789" )
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to="Category")
    
    class Meta:
        verbose_name_plural = "Categories"
        
    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' %(self.image.url))
    
    def __str__(self) -> str:
        return self.title


class Vendor(models.Model):
    vid = ShortUUIDField(unique=True, length=10, max_length=15, prefix="ven", alphabet = "abcdefghilk123456789")
    
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to= user_directory_path)
    description = models.TextField(max_length=100 , blank=True)
    
    address = models.CharField(max_length=100 , default="Mira road , Mumbai")
    contact = models.CharField(max_length=12 , default="+123 (456) 789")
    
    chat_resp_time = models.CharField(max_length=100 , default="100")
    authenticate_rating = models.CharField(max_length=100 , default="100")
    days_return = models.CharField(max_length=100 , default="100")
    warranty_period = models.CharField(max_length=100 , default="100")
    
    
    user = models.ForeignKey(User , on_delete=models.SET_NULL , null=True )
    
    class Meta:
        verbose_name_plural = "Vendors"
        
    def vendor_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' %(self.image.url))
    
    def __str__(self) -> str:
        return self.title
    
class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=15, alphabet = "abcdefghilk123456789" )
    vendor = models.ForeignKey(Vendor , on_delete=models.SET_NULL , null=True , related_name="vendor")
    category = models.ForeignKey(Category , on_delete=models.SET_NULL , null=True, related_name="category")
    
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to= user_directory_path)
    description = models.TextField(max_length=100 , blank = True , default="This is a Grocery product.")
    
    price = models.DecimalField(max_digits=999999999 ,decimal_places=2 , default="2.99" )
    old_price = models.DecimalField(max_digits=999999999 ,decimal_places=2, default = "1.99")
    
    specification = models.TextField(null=True, blank=True)
    # tags = models.ForeignKey(Tags , on_delete=models.SET_NULL , null=True)
    
    product_status = models.CharField(choices=STATUS , max_length=10 , default="in_review")
    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)
    
    sku = ShortUUIDField(unique=True, length=4, max_length=10, prefix="sku", alphabet = "1234567890")
    
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null = True , blank = True)
    
    class Meta:
        verbose_name_plural = "Products"
        
    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' %(self.image.url))
    
    def __str__(self) -> str:
        return self.title
    
    def get_percentage(self):
        new_price = ((self.old_price - self.price) / self.old_price) * 100
        return new_price
    
    
class ProductImages(models.Model):
    product = models.ForeignKey(Product, related_name="p_image", on_delete=models.SET_NULL , null=True)
    image = models.ImageField(upload_to="Product_images")
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Product Images"

# ==============================================================================================================================

class Cart(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=999999999 ,decimal_places=2 , default="2.99" )
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICES , max_length=20 , default="processing")
    
    class Meta:
        verbose_name_plural = "Cart Order"


class CartOrderItems(models.Model):
    order = models.ForeignKey(Cart, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    qty = models.IntegerField(default=0)
    
    price = models.DecimalField(max_digits=999999999 ,decimal_places=2 , default="2.99" )
    total = models.DecimalField(max_digits=999999999 ,decimal_places=2, default = "1.99")
    
    class Meta:
        verbose_name_plural = "Cart Order Items"

    def order_img(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' %(self.image))
    
# =====================================================================================================================================
# Product review , Wishlist , Address 

class ProductReview(models.Model):
    user = models.ForeignKey(User , on_delete=models.SET_NULL , null=True )
    product = models.ForeignKey(Product , related_name="reviews" ,on_delete=models.SET_NULL , null=True )
    review = models.TextField()
    rating = models.IntegerField(choices=RATING , default=None)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Product Reviews"
    
    def __str__(self) -> str:
        return self.product.title
    
    def get_rating(self):
        return self.rating
    
class Wishlist(models.Model):
    user = models.ForeignKey(User , on_delete=models.SET_NULL , null=True )
    product = models.ForeignKey(Product , on_delete=models.SET_NULL , null=True )
    
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Wishlist"
    
    def __str__(self) -> str:
        return self.product.title
    

class Address(models.Model):
    user = models.ForeignKey(User , on_delete=models.SET_NULL , null=True )
    address1 = models.CharField(max_length=100 , null=True)
    address2 = models.CharField(max_length=100 , null=True)
    city = models.CharField(max_length=100 , null=True)
    state = models.CharField(max_length=100 , null=True)  # You might want to use choices for states or regions
    zip_code = models.IntegerField(null=True)
    phone_no = models.IntegerField( null=True)
    status = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Address"
 
class Contact(models.Model):
    name = models.CharField(max_length=50 , null=True , blank=True)
    email = models.EmailField(null=True , blank=True)
    review = models.TextField(null=True , blank=True)
    
    def __str__(self) -> str:
        return self.name
    
    