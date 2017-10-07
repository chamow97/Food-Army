from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .forms import UserForm
from .models import user_info
from .models import donate_info
from .models import food_info
from random import randint
from django.core.mail import EmailMessage
from datetime import timedelta
from .models import gallery_info
from .models import new_applicants


def index(request):
    return render(request, 'index.html')

def login_user(request):
    if not request.user.is_authenticated():
        if request.method == 'POST':
            username = request.POST["username"]
            password = request.POST["password"]

            user = authenticate(username=username, password=password)
            if user is not None:

                #checking whether user is verified or not

                if user.is_active:
                    user_instance = user_info.objects.filter(username=username)
                    #if verified, login the user
                    if user_instance[0].is_verified == True:
                        login(request, user)
                        return redirect('/')
                    #else check for expiry date of OTP
                    elif user_instance[0].is_verified == False:
                        login(request, user)
                        date_now = timezone.now()
                        #if it has expired, go to reconfirmation page
                        if user_instance[0].expiry_date < date_now:
                            return redirect('/reconfirm')
                        #if it has not expired, go to confirmation page
                        else:
                            return redirect('/confirm')
                else:
                    return render(request, 'login_user.html',
                                  {'error_message' : 'Your account has been disabled!'})
            else:
                return render(request, 'login_user.html',
                              {'error_message': 'Incorrect Username / Password!'})
    elif request.user.is_authenticated():
        return redirect('/')
    return render(request, 'login_user.html')

def donate(request):
    if not request.user.is_active:
       return render(request, 'login_user.html', {'error_message': 'Login to continue'})
    if request.user.is_active:
        user_instance = user_info.objects.filter(username=request.user.username)
        # if verified, login the user
        if user_instance[0].is_verified == True:
            return render(request, 'donate.html')
        # else check for expiry date of OTP
        elif user_instance[0].is_verified == False:
            login(request, request.user)
            date_now = timezone.now()
            # if it has expired, go to reconfirmation page
            if user_instance[0].expiry_date < date_now:
                return redirect('/reconfirm')
            # if it has not expired, go to confirmation page
            else:
                return redirect('/confirm')

def confirmation(request):
    confirmation_code = request.POST['confirmation_code']
    username = request.POST['username']
    user_instance = user_info.objects.filter(username=username)
    if user_instance[0].token == int(confirmation_code):
        current_user = user_info.objects.get(username=username)
        current_user.is_verified = True
        current_user.save()
        return render(request, 'index.html', {'success_message': 'Account Confirmation Successful!'})
    else:
        return render(request, 'confirm_account.html', {'error_message': 'Incorrect Confirmation Code'})

def confirm_account(request):
    return render(request, 'confirm_account.html')

def gallery(request):
    gallery_instance =gallery_info.objects.all()
    return render(request, 'gallery.html', {'gallery' : gallery_instance})

def reconfirm_account(request):
    return render(request, 'reconfirm_account.html')

def reconfirm_code(request):
    username = request.user.username
    expiry_date = timedelta(days=1)
    token = randint(10000, 99999)
    user_instance = user_info.objects.get(username=username)
    user_instance.expiry_date = timezone.now() + expiry_date
    user_instance.token = token
    try:
        subject = "Food Army Confirmation Code"
        message = "Thank you for registering to Food Army. Your Confirmation code is: " + str(token) + ". Do not " \
                                                                                                "share this with anyone. This code expires in a day."
        e_mail = EmailMessage(subject, message, to=[str(user_instance.email)])
        e_mail.send()
        print(user_instance.expiry_date)
        print(user_instance.token)
        user_instance.save()
        return render(request, 'index.html', {'info_message': 'Confirmation Code has been sent again to your mail. Code expires in a day.'})
    except:
        return render(request, 'index.html', {'error_message': 'Some internal issues. Sorry for inconvenience. Try again later.'})

def join_us_page(request):
    return render(request, 'join_us.html')

def join_us(request):
    try:
        name = request.POST['name']
        street = request.POST['street']
        locality = request.POST['locality']
        city = request.POST['city']
        mobile = request.POST['mobile']
        email = request.POST['email']
        is_old_worker = new_applicants.objects.filter(email=email)
        if is_old_worker.count() != 0:
            return render(request, 'join_us.html', {'error_message':'A Field worker with that e-mail already exist.'})
        new_worker = new_applicants(name=name,
                                    street=street,
                                    locality=locality,
                                    city=city,
                                    mobile=mobile,
                                    email=email,
                                    is_a_member=False)
        new_worker.save()
        return render(request, 'index.html', {'info_message':'Your information is with us. We will contact you shortly.'})

    except:
        render(request, 'join_us.html', {'error_message':'Some internal issues. Try again after some time'})
    return render(request, 'join_us.html')


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        'form': form
    }
    return render(request, 'index.html',
                              {'success_message': 'Successfully Logged Out'})

@csrf_exempt
def save_donation(request):

    username = request.POST['username']
    foodImage = request.FILES['food_image']
    street = request.POST['street']
    locality = request.POST['locality']
    city = request.POST['city']
    contact = request.POST['contact']
    fs = FileSystemStorage()
    filename = fs.save(foodImage.name, foodImage)
    donation_instance = donate_info(user_name=username,
                                    is_resolved=False,
                                    request_date=timezone.now(),
                                    food_image=filename,
                                    street=street,
                                    locality=locality,
                                    city=city,
                                    mobile=contact)
    donation_instance.save()
    for i in range(1,2000000):
        try:
            request_id = donate_info.objects.latest('user_name')
            item_name = 'food' + str(i)
            item_weight = 'item_weight' + str(i)
            item_expiry = 'food_expiry' + str(i)
            food_name = request.POST[item_name]
            food_weight = request.POST[item_weight]
            food_expiry = request.POST[item_expiry]
            food_instance = food_info(user_name=username,
                                      food_name=food_name,
                                      item_amount=food_weight,
                                      expiry_date=food_expiry,
                                      request_id=request_id)
            food_instance.save()
        except:
            break
    return render(request, 'index.html', {'success_message' : 'Your request is submitted successfully. A field worker will contact you shortly.'})

def account(request):
    if not request.user.is_active:
       return render(request, 'login_user.html', {'error_message': 'Login to continue'})
    username = request.user.username
    food_instance = []
    account_instance = donate_info.objects.filter(user_name=username).order_by('-request_date')
    for donation in account_instance:
        try:
            food = food_info.objects.filter(request_id=int(donation.request_id))
            donation.request_id = int(donation.request_id)
            for item in food:
                item.request_id = int(item.request_id)
            food_instance.append(food)
        except:
            food_instance.append(None)
    return render(request, 'account.html', {'donation':account_instance, 'food':food_instance})

class UserFormView(View):
    form_class = UserForm
    template_name = 'registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form':form})
    @csrf_exempt
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            #insert email
            email = form.cleaned_data['email']
            is_user_existing = user_info.objects.filter(username = username)

            if is_user_existing.count() != 0:
                return render(request, 'registration_form.html',
                              {'error_message': 'User Already Registered!'})
            is_email_existing = user_info.objects.filter(email = email)
            #if email is already used
            if is_email_existing.count() != 0:
                return render(request, 'registration_form.html', {'form': form, 'error_message': 'This E-Mail is already registered'})
            #random token generation
            #expiry date is 1 day after current time
            try:
                expiry_date = timedelta(days=1)
                token = randint(10000, 99999)
                user_instance = user_info.objects.create(username = username,
                                                     email = email,
                                                     is_verified = False,
                                                     token = token,
                                                     register_date = timezone.now(),
                                                     expiry_date = timezone.now() + expiry_date)
                #Email Code
                subject = "Food Army Confirmation Code"
                message = "Thank you for registering to Food Army. Your Confirmation code is: " + str(token) + ". Do not " \
                        "share this with anyone. This code expires in a day."
                e_mail = EmailMessage(subject, message, to=[str(email)])
                e_mail.send()
                user.save()
                user_instance.save()
                return render(request, 'index.html', {'info_message' : 'Check your mail for a confirmation code. The code expires in a day.'})
            except:
                return render(request, 'index.html', {'error_message': 'Some internal issues. Sorry for inconvenience. Try again later.'})

        return render(request, self.template_name, {'form':form})
