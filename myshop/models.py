from django.db import models
from accounts.models import CustomUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError
# Create your models here.

class Product(models.Model):
    user_id = models.ForeignKey(to=CustomUser,db_index=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=75)
    meta_title = models.CharField(max_length=100)
    slug = models.SlugField(null=False,unique=True)
    summary = models.TextField()
    _type = models.IntegerField()
    sku = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ])
    quantity = models.PositiveIntegerField()
    is_sale = models.BooleanField()
    created_at=models.DateTimeField(editable=False,verbose_name=_("Creat date"), auto_now_add=True, null=True)
    updated_at = models.DateTimeField(editable=False,verbose_name=_("Update date"), auto_now_add=True, null=True)
    published_at = models.DateTimeField(verbose_name=_('Publish date'),auto_now_add=False,null=True)
    starts_at = models.DateTimeField(verbose_name=_('start sale date'),auto_now_add=False,null=True)
    ends_at = models.DateTimeField(verbose_name=_('end sale date'),auto_now_add=False,null=True)
    content = models.TextField(null=True,blank=True)
    img = models.ImageField(verbose_name=_('Image'),upload_to='product/')
    specification_json=models.JSONField(blank=True,null=True)

    # def specification_json_formatted(self):

    #     # dump the json with indentation set

    #     # example for detail_text TextField
    #     # json_obj = json.loads(self.detail_text)
    #     # data = json.dumps(json_obj, indent=2)

    #     # with JSON field, no need to do .loads
    #     data = json.dumps(self.specification_json, indent=2)

    #     # format it with pygments and highlight it
    #     formatter = HtmlFormatter(style='colorful')
    #     response = highlight(data, JsonLexer(), formatter)

    #      # include the style sheet
    #     style = "<style>" + formatter.get_style_defs() + "</style><br/>"

    #     return mark_safe(style + response)
    # specification_json_formatted='Specification Details'

    @property
    def get_discount(self):
        percenttag=100-self.discount
        price = int((percenttag*self.price)/100)

        return price
    @property
    def tot_r(self):
        tot = Product_review.objects.filter(product_id=self.id,is_publish=True).count()
        return tot
    @property
    def tot_rating(self):
        tot = Product_review.objects.filter(product_id=self.id,is_publish=True,rating__isnull=False).count()
        return tot
    @property
    def tot_review(self):
        '''(5 * 252 + 4 * 124 + 3 * 40 + 2 * 29 + 1 * 33) / 478 = 4.11'''
        tot = Product_review.objects.filter(product_id=self.id,is_publish=True,rating__gt=0,rating__lte=5)
        if tot.exists():
            l=[]
            for i in tot:
                l.append(i.rating)

            five_star=l.count(5)
            four_star=l.count(4)
            three_star=l.count(3)
            two_star=l.count(2)
            one_star=l.count(1)
            r=0
            try:
                r = (5*five_star+4*four_star+3*three_star+2*two_star+1*one_star)/(len(l))
            except:
                pass
            return ("%.1f" % r)
        return 0
    def get_absolute_url(self):
        return reverse('product_detail',kwargs={'slug':self.slug})
    def get_full_name(self):
        return self.user_id.first_name+' '+self.user_id.last_name
    def __str__(self):
        return str(self.title)


class Product_meta(models.Model):
    product_id = models.OneToOneField(to=Product,db_index=True, on_delete=models.CASCADE)
    key = models.CharField(max_length=100,unique=True)
    content = models.TextField(null=True,blank=True)
def validate_rating_number(value):
    if value>5 or value<1:  # Your conditions here
        raise ValidationError(' Rating value is between (1-5) but you given %s' % value)
class Product_review(models.Model):
    user_id = models.ForeignKey(to=CustomUser,db_index=True,null=True, on_delete=models.CASCADE)
    product_id = models.ForeignKey(to=Product,db_index=True,null=True, on_delete=models.CASCADE)
    parent_id = models.ForeignKey(to="self",db_index=True, on_delete=models.CASCADE,null=True,blank=True)
    title = models.CharField(max_length=100,blank=True,null=True)
    rating = models.PositiveIntegerField(blank=True,null=True,validators=[validate_rating_number])
    is_publish = models.BooleanField()
    created_at = models.DateTimeField(editable=False,verbose_name=_("Creat date"), auto_now_add=True, null=True)
    published_at = models.DateTimeField(verbose_name=_('publish date'),auto_now_add=False,null=True)
    content = models.TextField()

    def sub_review(self):
        sub_html=''
        if self.parent_id is not None:
            list_sub_review = Product_review.objects.filter(parent_id=self.parent_id)
            for i in list_sub_review:
                
                sub_html=sub_html+f'''
                <div class="card p-1">
                <div class="card-body p-1">
                    {i.title}
                </div>
                </div>
                '''
            return '''<h6>Replays</h6>'''+sub_html
        else:
            return ''
    
    def __str__(self):
        return str(self.title)
    class Meta:
        unique_together = ('user_id', 'product_id')

class Category(models.Model):
    parent_id = models.ForeignKey(to="self",db_index=True, on_delete=models.CASCADE,null=True,blank=True)
    title = models.CharField(max_length=100)
    meta_title = models.CharField(max_length=100)
    slug = models.SlugField(null=False,unique=True)
    content = models.TextField(null=True,blank=True)
    # def get_absolute_url(self):
    #     return reverse('category_detail',kwargs={'slug':self.slug})
    def __str__(self):
        return str(self.title)
        
class Product_category(models.Model):
    product_id = models.ForeignKey(to=Product,db_index=True, on_delete=models.CASCADE)
    category_id = models.ForeignKey(to=Category,db_index=True, on_delete=models.CASCADE)
    # class Meta:
    #     unique_together=(('product_id','category_id'))
class Tag(models.Model):
    title = models.CharField(max_length=100)
    meta_title = models.CharField(max_length=100)
    slug = models.SlugField(null=False,unique=True)
    content = models.TextField(null=True,blank=True)
    def __str__(self):
        return str(self.title)
        
class Product_tag(models.Model):
    product_id = models.ForeignKey(to=Product,db_index=True, on_delete=models.CASCADE)
    tag_id = models.ForeignKey(to=Tag,db_index=True, on_delete=models.CASCADE)
    # class Meta:
    #     unique_together=(('product_id','tag_id'))


CART_STATUS = (
    ('new','New'),
    ('cart','Cart'),
    ('checkout','Checkout'),
    ('paid','Paid'),
    ('complete','Complete'),
    ('abandoned','Abandoned'),
)

class Cart(models.Model):
    user_id = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=100)
    token = models.CharField(max_length=100)
    status = models.CharField(choices=CART_STATUS,max_length=15)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    email = models.CharField(max_length=100)
    line1 = models.CharField(max_length=50)
    line2 = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    province = models.CharField(max_length=50)
    country  = models.CharField(max_length=50)
    created_at = models.DateTimeField(editable=False,verbose_name=_("Create date"), auto_now_add=True, null=True)
    updatedAt  = models.DateTimeField(editable=False,verbose_name=_("Update date"), auto_now_add=True, null=True)
    content = models.TextField()
    def __str__(self):
        return str(self.user_id)

class Cart_item(models.Model):
    product_id = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    cart_id = models.ForeignKey(to=Cart, on_delete=models.CASCADE)
    sku = models.CharField(max_length=100)
    price = models.FloatField()
    discount = models.FloatField(default=0)
    quantity = models.IntegerField()
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(editable=False,verbose_name=_("Create date"), auto_now_add=True, null=True)
    updated_at  = models.DateTimeField(editable=False,verbose_name=_("Update date"), auto_now_add=True, null=True)
    content = models.TextField()
    def __str__(self):
        return str(self.product_id)

class Product_Viewed(models.Model):
    user_id=models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    product_id=models.ForeignKey(to=Product, on_delete=models.CASCADE)
    tot_views=models.IntegerField()
# ORDER_STATUS = (
#     ('new','New'),
#     ('checkout','Checkout'),
#     ('failed','Failed'),
#     ('shipped','Shipped'),
#     ('delivered','Delivered'),
#     ('returned','Returned'),
#     ('complete','Complete')
# )
# class Order(models.Model):
#     user_id = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
#     session_id = models.CharField(max_length=100)
#     token = models.CharField(max_length=100)
#     status = models.CharField(choices=ORDER_STATUS,max_length=15)
#     sub_total = models.FloatField()
#     item_discount = models.FloatField()
#     tax = models.FloatField()
#     shipping = models.FloatField()
#     total = models.FloatField()
#     promo = models.CharField(max_length=50)
#     discount = models.FloatField()
#     grand_total = models.FloatField()

#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     mobile = models.CharField(max_length=15)
#     email = models.CharField(max_length=100)
#     line1 = models.CharField(max_length=50)
#     line2 = models.CharField(max_length=50)
#     city = models.CharField(max_length=50)
#     province = models.CharField(max_length=50)
#     country  = models.CharField(max_length=50)
#     created_at = models.DateTimeField(editable=False,verbose_name=_("Creat date"), auto_now_add=True, null=True)
#     updatedAt  = models.DateTimeField(editable=False,verbose_name=_("Update date"), auto_now_add=True, null=True)
#     content = models.TextField()

# class Order_item(models.Model):
#     product_id = models.ForeignKey(to=Product, on_delete=models.CASCADE)
#     order_id = models.ForeignKey(to=Order, on_delete=models.CASCADE)

#     sku = models.CharField(max_length=100)
#     price = models.FloatField()
#     discount = models.FloatField()
#     quantity = models.IntegerField()
#     active = models.BooleanField()
#     created_at = models.DateTimeField(editable=False,verbose_name=_("Creat date"), auto_now_add=True, null=True)
#     updatedAt  = models.DateTimeField(editable=False,verbose_name=_("Update date"), auto_now_add=True, null=True)
#     content = models.TextField()

# transaction_type = (
#     ('credit','Credit'),
#     ('debit','Debit')
# )
# transaction_mode = (
#     ('offline','Offline'),
#     ('cash_on_delivery','Cash On Delivery'),
#     ('cheque','Cheque'),
#     ('draft','Draft'),
#     ('wired','Wired'),
#     ('online','Online'),
# )
# transaction_status = (
#     ('new','New'),
#     ('cancelled','Cancelled'),
#     ('failed','Failed'),
#     ('pending','Pending'),
#     ('declined','Declined'),
#     ('rejected','Rejected'),
#     ('success','Success')
# )
# class Transaction(models.Model):
#     user_id = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
#     order_id = models.ForeignKey(to=Order, on_delete=models.CASCADE)

#     code = models.CharField(max_length=100)
#     _type = models.CharField(choices=transaction_type,max_length=15)
#     mode = models.CharField(choices=transaction_mode,max_length=20)
#     status = models.CharField(choices=transaction_status,max_length=20)
#     created_at = models.DateTimeField(editable=False,verbose_name=_("Creat date"), auto_now_add=True, null=True)
#     updatedAt  = models.DateTimeField(editable=False,verbose_name=_("Update date"), auto_now_add=True, null=True)
#     content = models.TextField()



    



