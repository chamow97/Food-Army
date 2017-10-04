from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import user_info
from .models import food_info
from .models import donate_info
from .models import gallery_info
from .models import new_applicants

admin.site.register(user_info)
admin.site.register(donate_info)
admin.site.register(food_info)
admin.site.register(gallery_info)
admin.site.register(new_applicants)