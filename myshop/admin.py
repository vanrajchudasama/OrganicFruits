from django.contrib import admin
from .models import Product,Product_meta,Product_review,Category,Product_category,Tag,Product_tag, Cart, Cart_item
from django.utils.translation import gettext_lazy as _
from myshop.forms import CreateProductForm, UpdateProductForm,ProductDetailsForm
from django.utils.html import format_html,mark_safe
import datetime
from django.utils import timezone
# Register your models here.

"""
 product_id
category_id
"""
# admin.site.register(ProductDetailsForm)

@admin.display(description='Name')
def upper_case_title(obj):
    return ("%s" % (obj.title[0:15])).upper()

@admin.display(description='Stock keeping unit')
def sky_disp(obj):
    return obj.sku


# AdminSite.index_template='templates\\index.html'

class ProductCategoryInline(admin.TabularInline):
    model=Product_category
    extra=1
class ProductMetaInline(admin.TabularInline):
    model=Product_meta
    extra=1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    save_on_top = True

    autocomplete_fields = ['user_id']
    list_display_links=['user_id',upper_case_title,'image']
    list_per_page = 5
    add_form = CreateProductForm
    form = UpdateProductForm
    inlines=[ProductCategoryInline,ProductMetaInline]
    prepopulated_fields={'slug':('meta_title',)}
    search_fields = ['title','meta_title','summary','created_at','updated_at','published_at','starts_at','ends_at']
    raw_id_fields = ("user_id",)
    list_display=['user_id',upper_case_title,'image','view_on_site','meta_title','slug','_summary','_type',
    sky_disp,'price','discount','quantity','is_sale','created_at','updated_at','published_at','starts_at','ends_at','content']
    # fieldsets = (
    #     (None, {
    #         # 'classes': ('wide'),
    #         'fields': ('user_id','title','img','meta_title','slug','summary','_type',
    # 'sku',('price','discount','quantity'),('published_at','starts_at','ends_at'),'content')}
    #     ),
    #     (_('Permission'),{'classes': ('collapse',),'fields':('is_sale',)})
        
    # )
    readonly_fields = ('thumbnail_preview',)
    
    def _summary(self,obj):
        return obj.summary[0:20]+'...'
    def view_on_site(self,obj):
        if obj.is_sale==True:
            start_date = datetime.date.today()

            if obj.published_at<=timezone.now():
                if obj.starts_at<=timezone.now():
                    # if obj.ends_at>=timezone.now():
                    return mark_safe('<img src="/static/admin/img/icon-yes.svg" alt="True">')
        return mark_safe('<img src="/static/admin/img/icon-no.svg" alt="False">')
    
    def thumbnail_preview(self, obj):
        if obj.img:
            return mark_safe('<img src="{}" width="300" height="300" />'.format(obj.img.url))
        return ""
    # thumbnail_preview.allow_tags = True
    def image(self,obj):
        if obj.img:
            return mark_safe('<img src="{}"  width="200" height="200" style="width:100px;height:100px;max-width:100px;" />'.format(obj.img.url))
        return "No image"
    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide'),
    #         'fields': ('user_id','title','meta_title','slug','summary','_type',
    # 'sku',('price','discount','quantity'),'published_at','starts_at','ends_at','content')}
    #     ),
        
    # )
    # class Media:
    #     css = {
    #         "all": ("new/css/bootstrap.css",)
    #     }
    #     js = ("new/js/jquery.js",)
@admin.register(Product_meta)
class ProductMetaAdmin(admin.ModelAdmin):
    autocomplete_fields = ['product_id']
    raw_id_fields = ("product_id",)
    list_display=['product_id','key','content']


@admin.register(Product_review)
class ProductReiewAdmin(admin.ModelAdmin):
    list_display=['product_id','parent_id','title','rating','is_publish','created_at','published_at','content']
    search_fields = ['title','rating']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('meta_title',)}
    list_display=['title','parent_id','meta_title','slug','content']
@admin.register(Product_category)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display=['product_id','category_id']



class EmailSendAdmin(admin.ModelAdmin):
    list_display=['Email_send',]
    def Email_send(self):
        pass

# -------------------------------Start Tag Table-----------------------------------------
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('meta_title',)}
    list_display=['title','meta_title','slug','content']
@admin.register(Product_tag)
class ProductTagAdmin(admin.ModelAdmin):
    list_display=['product_id','tag_id']
# -------------------------------End Tag Table-------------------------------------------

# ---------------------------------start cart table-----------------------------------------

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display=['user_id','session_id','token','status','first_name','last_name','mobile','email','line1','line2','city','province','country','created_at','updatedAt','content']
    autocomplete_fields = ['user_id']
# ---------------------------------end cart table-------------------------------------------


# ---------------------------------start cart-items table-----------------------------------------

@admin.register(Cart_item)
class CartAdmin(admin.ModelAdmin):
    list_display=['product_id','cart_id','sku','price','discount','quantity','active','created_at','updated_at','content']
    autocomplete_fields = ['product_id']
# ---------------------------------end cart-items table-------------------------------------------
