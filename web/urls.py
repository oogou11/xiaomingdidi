from django.conf.urls import url 
from .views.index import index
from .views.contact import email

urlpatterns = [   
    url(r'^$',index, name='index'), 
    url(r'^index',index, name='index'),  
    url(r'^contact/email',email, name='email'),
]