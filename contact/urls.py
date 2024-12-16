from django.urls import path
from contact.views import contact, detail

app_name = 'contact'

urlpatterns = [
    path('', contact, name='new'),
    path('<int:pk>/', detail, name='detail'),
]