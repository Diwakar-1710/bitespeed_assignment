from django.urls import path
from .views import identify,get_all_contacts,delete_contact


urlpatterns = [
    path('identify/', identify, name = 'identify'),
    path('get_all_contacts/', get_all_contacts, name='get_all_contacts'),
    path('delete_contact/<int:contact_id>/', delete_contact, name='delete_contact'),
]