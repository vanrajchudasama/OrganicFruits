from .models import Product, Product_review,Cart,Cart_item,Category,Product_category,Product_Viewed,CustomUser


def get_cart_items(request):
    user_obj=CustomUser.objects.get(id=request.user.id)
    cart_obj=Cart.objects.get(user_id=user_obj)
    cart_items_obj=Cart_item.objects.filter(cart_id=cart_obj)
    total_cart_items=cart_items_obj.count()
    if total_cart_items<100:
        is_large=True
        return {'total_cart_item':total_cart_items,'is_large':is_large}
    else:
        is_large=False
        return {'total_cart_item':99,'is_large':is_large}