from django.forms import ModelForm,Form,CharField,ImageField
from django import forms
from myshop.models import Product,Product_review

class CreateProductForm(ModelForm):
    def __init__(self,*args,**kwargs):
        super(CreateProductForm,self).__init__(*args,**kwargs)
        self.fields['title'].help_text='product title'
    class Meta:
        model = Product
        exclude  = ['id']
class UpdateProductForm(ModelForm):
    def __init__(self,*args,**kwargs):
        super(UpdateProductForm,self).__init__(*args,**kwargs)
        # self.fields['sku'].help_text='product title'
    class Meta:
        model = Product
        exclude  = ['id']

class ProductDetailsForm(Form):
    name = CharField(max_length=50,widget=forms.TextInput(attrs={'class':'form-control'}))
    desc = CharField(max_length=50)

class ProductReviewForm(ModelForm):
    rating=forms.CharField(widget=forms.HiddenInput(attrs={'name':'rating','id':'rating'}))
    title=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','name':'title','id':'title'}))
    content=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','rows':'8','name':'desc','id':'desc'}))
    class Meta:
        model=Product_review
        exclude  = ['id','user_id','product_id','parent_id','is_publish','published_at']