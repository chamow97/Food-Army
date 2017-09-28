from django.conf.urls import url
from fms import views

app_name='fms'

urlpatterns = [
    url(r'^$', views.index, name='base'),
    url(r'^register$', views.UserFormView.as_view(), name='register'),
    url(r'^login_user$', views.login_user, name='login_user'),
    url(r'^logout_user$', views.logout_user, name='logout_user'),
    url(r'^donate$', views.donate, name='donate')
]