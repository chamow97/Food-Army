from django.conf.urls import url
from fms import views

app_name='fms'

urlpatterns = [
    url(r'^$', views.index, name='base'),
    url(r'^register$', views.UserFormView.as_view(), name='register'),
    url(r'^login_user$', views.login_user, name='login_user'),
    url(r'^logout_user$', views.logout_user, name='logout_user'),
    url(r'^donate$', views.donate, name='donate'),
    url(r'^confirm$', views.confirm_account, name='confirm_account'),
    url(r'^reconfirm$', views.reconfirm_account, name='reconfirm_account'),
    url(r'^confirmation$', views.confirmation, name='confirmation'),
]