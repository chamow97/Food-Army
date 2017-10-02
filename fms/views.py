from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .forms import UserForm
from .models import user_info
from random import randint
from django.core.mail import EmailMessage
from datetime import timedelta


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
    return render(request, 'donate.html')

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

def reconfirm_account(request):
    return render(request, 'reconfirm_account.html')

def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        'form': form
    }
    return render(request, 'index.html',
                              {'success_message': 'Successfully Logged Out'})


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

        return render(request, self.template_name, {'form':form})
