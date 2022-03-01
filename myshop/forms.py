from django.forms import ModelForm,Form,CharField,ImageField
from django import forms
from myshop.models import Product

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
