from django.shortcuts import render,HttpResponse
from .models import Product, Product_review,Cart,Cart_item,Category,Product_category,Product_Viewed
from threading import Thread
import time
import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models.query_utils import Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
from itertools import chain 
from django.views.decorators.cache import never_cache

def my_fun(desc):
    for t in desc:
        p=Product.objects.filter(summary__icontains=t)
        print(p)
        return p
    return False
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
    print(category_obj)
    products_obj=Product_category.objects.filter(category_id__title__contains=category_obj)
    # print(products_obj.product_id.title)

    # products_obj=Product.objects.filter(title__icontains=products_obj.product_id.title)

    # print(products_obj)
    is_purchesed=False
    if request.user.is_authenticated:
        pl=Product_Viewed.objects.filter(Q(user_id=request.user) & Q(product_id=product_detail)).first()
        is_purchesed=Product_review.objects.filter(Q(product_id=product_detail) & Q(user_id=request.user))
        if is_purchesed is not None:
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
def product_reviews(request,id,slug):
    
    product_obj=get_object_or_404(Product, slug=slug,id=id)
    if request.POST:
        review_filtesr=''
        get_val=request.POST.get('filter')
        if get_val=='MOST_RECENT':
            review_filtesr='-published_at'
        elif get_val=='POSITIVE_FIRST':
            review_filtesr='-rating'
        elif get_val=='NEGATIVE_FIRST':
            review_filtesr='rating'
        product_reviews_obj=Product_review.objects.filter(product_id=product_obj).order_by(review_filtesr)
        review_filtesr=''
        return render(request, template_name='myshop/filter-table.html',context={'Products':product_obj,'Reviews':product_reviews_obj})
    else:
        product_reviews_obj=Product_review.objects.filter(product_id=product_obj).order_by('-rating')
   
    return render(request, template_name='myshop/review.html',context={'Products':product_obj,'Reviews':product_reviews_obj})
