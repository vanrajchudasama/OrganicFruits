from django.shortcuts import render, redirect, HttpResponseRedirect
from .forms import CustomUserCreationForm, UserLoginForm, CustomUserEditForm, ImageFileUploadForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import uuid
from .models import CustomUser
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from threading import Thread
# Create your views here.
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.forms import PasswordResetForm
from django.views.decorators.csrf import csrf_exempt

from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes,force_str

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def home(request):
    if request.user.is_authenticated:
        return render(request, "accounts\index.html")
    else:
        return HttpResponseRedirect('/login')


def user_login(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.POST:
        username = request.POST['email']
        password = request.POST['password']
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():

            # cust_obj = CustomUser.objects.filter(email=username).first()
            # cust_obj = cust_obj.filter(password=password)

            # hashed_pwd = make_password(password)
            user=CustomUser.objects.get(email=username)
            if user is not None:
                if user.is_active == False:
                    messages.warning(request, message='This account is inactive.')
                    return render(request, "accounts\login.html", {'form': login_form})
                    # return HttpResponseRedirect('/accounts/login')

            user = authenticate(request, email=username, password=password)

            if user is not None:
                if user.is_varified == False:

                    messages.warning(
                        request, 'check your mail and varify your account')
                    return render(request, "accounts\login.html", {'form': login_form})
                # if user.is_active == False:
                #     messages.error(request, message='This account is inactive.')
                #     return HttpResponseRedirect('/login')
                login(request, user)
                # messages.success(request, 'Login Success')
                return redirect('/')
            else:
                cust_login = UserLoginForm(request.POST)
                messages.warning(request, 'Invalid login credentials...!')
                return render(request, "accounts\login.html", {'form': cust_login})
        else:
            # cust_login = UserLoginForm(request.POST)
            # messages.warning(request, 'Login Fail')
            return render(request, "accounts\login.html", {'form': login_form})
    else:
        cust_login = UserLoginForm()
        # login_form = UserLoginForm()

        return render(request, "accounts\login.html", {'form': cust_login})

@login_required(login_url='/accounts/login/')
def user_logout(request):
    logout(request)
    messages.success(request, 'Logout Success')
    return HttpResponseRedirect('/accounts/login')


def user_register(request):
    cust_form = CustomUserCreationForm()
    if request.POST:
        cust_form = CustomUserCreationForm(request.POST)
        if cust_form.is_valid():

            first_name = cust_form.cleaned_data.get('first_name')
            last_name = cust_form.cleaned_data.get('last_name')

            email = cust_form.cleaned_data.get('email')
            mobile = cust_form.cleaned_data.get('mobile')
            password = cust_form.cleaned_data.get('password2')
            auth_token = str(uuid.uuid4())

            # cust_form.auth_token=auth_token
            current_site = get_current_site(request)
            hashed_pwd = make_password(password)
            cust_obj = CustomUser(first_name=first_name, last_name=last_name,
                                  email=email, mobile=mobile, password=hashed_pwd)
            cust_obj.auth_token = auth_token
            t1 = Thread(target=varify_send_mail, args=(
                email, auth_token, current_site))
            t1.start()
            # varify_send_mail(email,auth_token,current_site)
            cust_obj.save()
            # cust_form.save()
            # username = request.POST['email']
            # password = request.POST['password']
            # user = authenticate(request, email=username, password=password)
            # login(request, user)
            messages.success(request, 'Register Success')
            cust_form = CustomUserCreationForm()
            return redirect('/login')
    return render(request, "accounts\\register.html", {'form': cust_form})


def varify_send_mail(mail, token, domain):
    subjetc = 'Activate Account'
    # link=my_domain.objects.get_current().domain
    msg_body = 'You have Activate your account click this link http://' + \
        str(domain)+'/varify/'+token

    email = EmailMessage(subjetc, msg_body, to=[mail])

    email.send()
    from time import sleep
    sleep(10)


def varify_token(request, token):

    print(token)
    user_obj = CustomUser.objects.filter(auth_token=token).first()
    if user_obj is not None:
        if user_obj.is_varified == False:

            user_obj.is_varified = True
            user_obj.save()
            messages.success(request, 'Your account varified')
            return redirect('/accounts/login')
        elif user_obj.is_varified == True:
            messages.success(request, 'varify your account')
            return redirect('/accounts/login')
        else:
            messages.warning(
                request, 'check your mail and varify your account')
            return redirect('/accounts/login')
    messages.warning(request, 'Something want to wrong...!')
    return redirect('/accounts/login')


def password_reset_request(request):
    if request.method == 'POST':
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = CustomUser.objects.filter(Q(email=data))

            if associated_users.exists():

                for user in associated_users:
                    current_site=get_current_site(request)
                    subject = "Password Reset Requested"
                    email_template_name = "accounts\password_reset_email.txt"
                    uid=urlsafe_base64_encode(force_bytes(user.pk))
                    c = {
					"email":user.email,
					'domain':str(current_site),
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
                    email = render_to_string(email_template_name, c)
                    try:
                        t1 = Thread(target=send_mail, args=(
                        subject, email, 'admin@example.com', [user.email], False))
                        t1.start()
                        # send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid Header found.')
                    return redirect('/accounts/password_reset/done/')
        else:
            return render(request=request, template_name="accounts/password_reset.html", context={"password_reset_form":password_reset_form})

    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="accounts/password_reset.html", context={"password_reset_form":password_reset_form})

@login_required(login_url='/accounts/login/')
def user_profile(request):
    
    cust_edit_form = CustomUserEditForm()
    if request.POST:
        cust_edit_form = CustomUserEditForm(request.POST)
        if cust_edit_form.is_valid():
            first_name=cust_edit_form.cleaned_data['first_name']
            last_name=cust_edit_form.cleaned_data['last_name']
            email=cust_edit_form.cleaned_data['email']
            gender=cust_edit_form.cleaned_data['gender']
            mobile=cust_edit_form.cleaned_data['mobile']
            dob=cust_edit_form.cleaned_data['dob']
            cform=CustomUser.objects.get(id=request.user.id)
            cform.first_name=first_name
            cform.last_name=last_name
            cform.email=email
            cform.gender=gender
            cform.mobile=mobile
            cform.dob=dob
            cform.save()
        
    
    profile_obj = CustomUser.objects.get(pk=request.user.id)
    img_form=ImageFileUploadForm()
    return render(request, template_name='accounts/profile.html',context={'eform':cust_edit_form,'Profile':profile_obj,'img_form':img_form})


    
# @csrf_exempt
def profile_image_update(request):
    if request.method == 'POST':
            image = request.FILES.get('profile')
            new_profile_pic=CustomUser.objects.get(id=request.user.id)
            new_profile_pic.profile=image
            # new_profile_pic.image= request.POST.get('img_url')
            new_profile_pic.save()
        
    return redirect("/accounts/profile/")
