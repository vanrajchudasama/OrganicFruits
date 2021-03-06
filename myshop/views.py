from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from .models import Product, Product_review,Cart,Cart_item,Category,Product_category,Product_Viewed
from accounts.models import CustomUser
from threading import Thread
import time
import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models.query_utils import Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Avg, Count, Min, Sum

# Create your views here.
from itertools import chain 
from django.views.decorators.cache import never_cache
from django.utils import timezone
from myshop.forms import ProductReviewForm
from django.contrib import messages
import secrets
import uuid

def my_fun(desc):
    for t in desc:
        p=Product.objects.filter(summary__icontains=t)
        print(p)
        return p
    return False
def get_total(request):

    user_obj=CustomUser.objects.get(id=request.user.id)
    cart_obj=Cart.objects.filter(user_id=user_obj).first()
    total_price=0
    tot_product=0
    items=Cart_item.objects.filter(cart_id=cart_obj)#.aggregate(Sum('price'))
    for item in items:
        total_price=(total_price+(item.price*item.quantity))
        tot_product=(tot_product+(item.product_id.price*item.quantity))
    return total_price,tot_product #int(total_price['price__sum'])*int(total_quantity['quantity__sum'])

def home(request):
    list_product={}
    start_date = datetime.date.today()
    # start_time=datetime.datetime.now()
    page = request.GET.get('page', 1)
    if request.user.is_authenticated:
        # user_purchage_product=
        cart=Cart.objects.get(user_id=request.user)
        cart_item=Cart_item.objects.filter(cart_id=cart)[:5]
        title_list=[]
        desc_list=[]
        meta_title=[]
        for p in cart_item:
            title_list.append(p.product_id.title)
            meta_title.append(p.product_id.meta_title)
            desc_list.append(p.product_id.summary)
        # f=filter(my_fun, desc_list)
        # print(list(f))
        most_viewed_product=Product_Viewed.objects.filter(user_id=request.user).order_by('-tot_views')[0:6]
        # category_items=Product_category.objects.filter(category_id=cart)
        # print(category_items)
        list_product['Recomandations']=cart_item
        list_product['MostViewed']=most_viewed_product
        # for p in cart_item:
        #     product_obj=Product.objects.get(id=p.product_id.id)
            # recomandations_dict.update({'r'+str(p.id):product_obj})
        # list_product['Products']=Product.objects.filter(is_sale=True,starts_at__date__lte=datetime.date(start_date.year,start_date.month,start_date.day)
        # ,published_at__date__lte=datetime.date(start_date.year,start_date.month,start_date.day)
        # )
    category=Category.objects.all()
    products_obj=Product.objects.filter(is_sale=True,starts_at__date__lte=datetime.date(start_date.year,start_date.month,start_date.day)
        # ,ends_at__date__gte=datetime.date(start_date.year,start_date.month,start_date.day)
        ,published_at__date__lte=datetime.date(start_date.year,start_date.month,start_date.day)
        ).order_by('-discount')
    list_product['Categories']=category
    # All_p=chain(products_obj,category)

    # list_product['Produts'] = products_obj
    
    paginator = Paginator(products_obj, 18)
    try:
        list_product['Produts'] = paginator.page(page)
    except PageNotAnInteger:
        list_product['Produts'] = paginator.page(1)
    except EmptyPage:
        list_product['Produts'] = paginator.page(paginator.num_pages)
    # list_product['Recomandations']=recomandations_dict
    # print(datetime.datetime.today)
    # list_product['Reviews'] = Product_review.objects.all()
    
    return render(request, template_name='myshop/index.html',context=list_product)    

def product_recomanded(product_obj):
    product_title=product_obj.title
    product_desc=product_obj.summary
    c_p=Product_category.objects.filter(product_id=product_obj)
    c_p=Product_category.objects.filter(Q(category_id__title__icontains=c_p.category_id.title) | Q(category_id__content__icontains=c_p.category_id.content))
    list_product=Product.objects.filter(title__icontains=product_title,summary__icontains=product_desc)
    return 0
def product_list(request,title):
    most_viewed_product=Product_Viewed.objects.filter(user_id=request.user).order_by('-tot_views')[0:6]

    list_product['Produts'] = most_viewed_product
    return render(request, template_name='myshop/product_list.html',context=list_product)

def recomandations(user_obj):
    print('============',user_obj)
    if user_obj is not None:
        cart_item=Cart_item.objects.filter(cart_id=user_obj)

def product_detail(request,slug):
    product_detail=get_object_or_404(Product, slug=slug)
    products_obj=Product_category.objects.filter(product_id=product_detail).first()

    category_obj=Category.objects.get(id=products_obj.category_id.id)
    products_obj=Product_category.objects.filter(category_id__title__contains=category_obj)
    # print(products_obj.product_id.title)

    # products_obj=Product.objects.filter(title__icontains=products_obj.product_id.title)

    # print(products_obj)
    is_purchesed=False
    if request.user.is_authenticated:
        pl=Product_Viewed.objects.filter(Q(user_id=request.user) & Q(product_id=product_detail)).first()
        is_purchesed_obj=Product_review.objects.filter(Q(product_id=product_detail) & Q(user_id=request.user))
        # print(is_purchesed_obj)
        # if is_purchesed_obj.exists():
        is_purchesed=True
        if pl is not None:
            pl.tot_views=pl.tot_views+1
            pl.save()
        else:
            pv=Product_Viewed(user_id=request.user,product_id=product_detail,tot_views=1)
            pv.save()
    # product_detail=Product.objects.filter(slug=slug)
    list_reviews = Product_review.objects.filter(Q(product_id=product_detail) & Q(is_publish=True)).order_by('-rating')[:5]
    average_review = product_detail.tot_review
    return render(request, template_name='myshop/product-details.html',context={'Produts':products_obj,'Product':product_detail,'Reviews':list_reviews,'average_review':average_review,'is_purchase':is_purchesed})

@csrf_exempt
def product_reviews_list(request,id,slug):
    
    product_obj=get_object_or_404(Product, slug=slug,id=id)
    product_reviews_obj=Product_review.objects.filter(product_id=product_obj)
    if product_reviews_obj.exists():
        if request.POST:
            review_filtesr=''
            get_val=request.POST.get('filter')
            if get_val=='MOST_RECENT':
                review_filtesr='-published_at'
            elif get_val=='POSITIVE_FIRST':
                review_filtesr='-rating'
            elif get_val=='NEGATIVE_FIRST':
                review_filtesr='rating'
            product_reviews_obj=product_reviews_obj.order_by(review_filtesr)
            review_filtesr=''
            return render(request, template_name='myshop/filter-table.html',context={'Products':product_obj,'Reviews':product_reviews_obj})
        else:
            product_reviews_obj=product_reviews_obj.order_by('-rating')
    
        return render(request, template_name='myshop/review.html',context={'Products':product_obj,'Reviews':product_reviews_obj})
    else:
        return redirect('product_detail',product_obj.slug)

@login_required(login_url='/accounts/login/')
def product_reviews_form(request,id,slug):
    product_obj=get_object_or_404(Product, slug=slug,id=id)
    product_review_form=ProductReviewForm()
    user_obj=CustomUser.objects.get(id=request.user.id)
    p_r=Product_review.objects.filter(user_id=user_obj,product_id=product_obj)
    is_exists=False
    if p_r.exists():
        p_r=Product_review.objects.get(user_id=user_obj,product_id=product_obj)

        product_review_form=ProductReviewForm(instance=p_r)
        is_exists=True
    if request.method=='POST':
        product_review_form=ProductReviewForm(request.POST)
          
        if product_review_form.is_valid():

            title=product_review_form.cleaned_data['title']
            desc=product_review_form.cleaned_data['content']
            rating=product_review_form.cleaned_data['rating']
            if is_exists:
                p_r.rating=rating
                p_r.content=desc
                p_r.title=title
                p_r.save()
                messages.success(request, 'Your Reviews updated...!')
            else:

                reviews_obj=Product_review.objects.create(user_id=request.user,product_id=product_obj,title=title,content=desc,rating=5,is_publish=True,published_at=timezone.now())
                messages.success(request, 'Your Reviews sumnited...!')
                # reviews_obj.save()
            # product_review_form=ProductReviewForm()

    return render(request, template_name='myshop/rating-review-form.html',context={'Products':product_obj,'form':product_review_form})

@login_required(login_url='/accounts/login/')
def add_to_cart(request,slug,id):
    product_obj=get_object_or_404(Product, slug=slug,id=id)
    user_obj=CustomUser.objects.get(id=request.user.id)
    cart_obj=Cart.objects.filter(user_id=user_obj)
    is_user_cart=False
    if cart_obj.exists():
        cart_obj=Cart.objects.get(user_id=user_obj)

        cart_item_obj=Cart_item.objects.filter(product_id=product_obj,cart_id=cart_obj)
        if cart_item_obj.exists():
            cart_item_obj=Cart_item.objects.get(product_id=product_obj,cart_id=cart_obj)
            cart_item_obj.quantity=cart_item_obj.quantity+1
            cart_item_obj.save()
            is_user_cart=True
        else:
            cart_item_obj=Cart_item.objects.create(product_id=product_obj,cart_id=cart_obj
            ,sku='nkew',price=product_obj.get_discount,discount=product_obj.discount
            ,quantity='1',active=True,content='')
    else:

        session_id,token_id=make_token()
        Cart.objects.get_or_create(
            user_id=user_obj,session_id=session_id,token=token_id,status='new'
            ,first_name=user_obj.first_name,last_name=user_obj.last_name,mobile=user_obj.mobile
            ,email=user_obj.email,line1='',line2='',city=''
            ,province='',country='',content=''
            )
        
        cart_obj=Cart.objects.get(user_id=user_obj)
        cart_item_obj=Cart_item.objects.create(product_id=product_obj,cart_id=cart_obj
        ,sku='nkew',price=product_obj.get_discount,discount=product_obj.discount
        ,quantity='1',active=True,content='')
    return redirect('cart')


@login_required(login_url='/accounts/login/')
def go_to_cart(request):
    user_obj=CustomUser.objects.get(id=request.user.id)
    cart_obj=Cart.objects.get(user_id=user_obj)
    cart_items_obj=Cart_item.objects.filter(cart_id=cart_obj)
    total,p_total=get_total(request)
    discount=p_total-total

    totale_cart_items=cart_items_obj.count()
    return render(request, template_name='myshop/my-cart.html',context={'cart_items':cart_items_obj,'total':total
    ,'totale_cart_items':totale_cart_items,'discount':discount,'product_total':p_total})


@login_required(login_url='/accounts/login/')
def delete_cart_item(request,id):
    item=Cart_item.objects.get(pk=id)
    item.delete()
    user_obj=CustomUser.objects.get(id=request.user.id)
    cart_obj=Cart.objects.get(user_id=user_obj)
    cart_items_obj=Cart_item.objects.filter(cart_id=cart_obj)
    total,p_total=get_total(request)
    discount=p_total-total
    totale_cart_items=cart_items_obj.count()
    return render(request, template_name='myshop/cart-table.html',context={'cart_items':cart_items_obj,'total':total
    ,'totale_cart_items':totale_cart_items,'discount':discount,'product_total':p_total})

@login_required(login_url='/accounts/login/')
def change_cart_item(request):
    if request.POST:
        id=request.POST.get('id')
        option=request.POST.get('option')
        if option=='delete':
            cart_item_obj=Cart_item.objects.get(pk=id)
            cart_item_obj.quantity=cart_item_obj.quantity-1
            cart_item_obj.save()
        elif option=='add':
            cart_item_obj=Cart_item.objects.get(pk=id)
            cart_item_obj.quantity=cart_item_obj.quantity+1
            cart_item_obj.save()

    user_obj=CustomUser.objects.get(id=request.user.id)
    cart_obj=Cart.objects.get(user_id=user_obj)
    cart_items_obj=Cart_item.objects.filter(cart_id=cart_obj)
    total,p_total=get_total(request)
    discount=p_total-total
    totale_cart_items=cart_items_obj.count()
    return render(request, template_name='myshop/cart-table.html',context={'cart_items':cart_items_obj,'total':total
    ,'totale_cart_items':totale_cart_items,'discount':discount,'product_total':p_total})

def make_token():
    """
    Creates a cryptographically-secure, URL-safe string
    """
    my_uuid = uuid.uuid4()
    token = uuid.uuid4()
    # return secrets.token_urlsafe(16)
    return str(my_uuid),str(token)