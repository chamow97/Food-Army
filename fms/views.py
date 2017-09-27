from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, render_to_response
from django.template.context_processors import csrf
from django.contrib.auth.models import User
from django.views import View
from .forms import UserForm
from .models import user_info


def index(request):
    return render(request, 'index.html')

def login_user(request):
    if not request.user.is_authenticated():
        if request.method == 'POST':
            username = request.POST["username"]
            password = request.POST["password"]

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/')
                else:
                    return render(request, 'login_user.html',
                                  {'error_message' : 'Your account has been disabled!'})
            else:
                return render(request, 'login_user.html',
                              {'error_message': 'Incorrect Username / Password!'})

    return render(request, 'login_user.html')


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

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            #insert phone number
            email = form.cleaned_data['email']
            print(email)
            # is_user_existing = user_info.objects.filter(username = username)
            # if is_user_existing.count() != 0:
            #     return render(request, 'registration_form.html',
            #                   {'error_message': 'User Already Registered!'})
            # is_email_existing = user_info.objects.filter(email = email)
            # if is_email_existing.count() != 0:
            #     return render(request, 'registration_form.html', {'form': form, 'error_message': 'This E-Mail is already registered'})
            user_instance = user_info.objects.create(username = username,
                                                     email = email,
                                                     is_verified = False,
                                                     token = 100)
            user.save()
            user_instance.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/')

        return render(request, self.template_name, {'form':form})
