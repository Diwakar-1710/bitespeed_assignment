from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Contact
from .serializers import ContactSerializer

@api_view(['POST'])
def identify(request):
    email = request.data.get('email')
    phone_number = request.data.get('phone_number')

    if not email and not phone_number:
        return Response({"error": "Email or phoneNumber must be provided."}, status=status.HTTP_400_BAD_REQUEST)

    contacts = Contact.objects.filter(Q(email=email) | Q(phone_number=phone_number))
    print(contacts)
    if not contacts.exists():
        print('No matching contacts found. Creating a new primary contact.')
        new_contact = Contact.objects.create(
            email=email,
            phone_number=phone_number,
            link_precedence='primary'
        )
        return Response({
            "contact": {
                "primaryContactId": new_contact.id,
                "emails": [new_contact.email] if new_contact.email else [],
                "phoneNumbers": [new_contact.phone_number] if new_contact.phone_number else [],
                "secondaryContactIds": []
            }
        }, status=status.HTTP_201_CREATED)

    primary_contact = None
    emails = set()
    phone_numbers = set()
    secondary_ids = []

    for contact in contacts:
        print(contact)
        if contact.link_precedence == 'primary':
            primary_contact = contact
        
        secondary_ids.append(contact.id)
        if contact.email:
            emails.add(contact.email)
        if contact.phone_number:
            phone_numbers.add(contact.phone_number)

    print(email) 
    print(emails)
    print(phone_number not in phone_numbers)
    print(phone_numbers)  

    if (email is not None and email not in emails) or (phone_number is not None and phone_number not in phone_numbers):
        # Create a new secondary contact with the new details
        new_secondary_contact = Contact.objects.create(
            email=email,
            phone_number=phone_number,
            linked_id=primary_contact.id,
            link_precedence='secondary'
        )
        secondary_ids.append(new_secondary_contact.id)
        if new_secondary_contact.email:
            emails.add(new_secondary_contact.email)
        if new_secondary_contact.phone_number:
            phone_numbers.add(new_secondary_contact.phone_number)
     #Create a list of Q objects for email and phone number queries
    email_queries = Q()
    phone_number_queries = Q()

    for email in emails:
        email_queries |= Q(email=email)

    for phone_number in phone_numbers:
        phone_number_queries |= Q(phone_number=phone_number)

    # Combine email and phone number queries using OR operator
    all_contacts = Contact.objects.filter(email_queries | phone_number_queries)
    primary_contact = None
    emails = set()
    phone_numbers = set()
    secondary_ids = []

    for contact in all_contacts:
        print(contact)
        if contact.link_precedence == 'primary':
            primary_contact = contact
        
        secondary_ids.append(contact.id)
        if contact.email:
            emails.add(contact.email)
        if contact.phone_number:
            phone_numbers.add(contact.phone_number)

    # Remove primary contact's details from sets to avoid duplication
    secondary_ids.remove(primary_contact.id)
    emails.discard(primary_contact.email)
    phone_numbers.discard(primary_contact.phone_number)

    response_data = {
        "contact": {
            "primaryContactId": primary_contact.id,
            "emails": [primary_contact.email] + list(emails),
            "phoneNumbers": [primary_contact.phone_number] + list(phone_numbers),
            "secondaryContactIds": secondary_ids
        }
    }

    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_all_contacts(request):
    contacts = Contact.objects.all()
    serializer = ContactSerializer(contacts,many = True)
    return Response(serializer.data)


@api_view(['DELETE'])
def delete_contact(request, contact_id):
    try:
        contact = Contact.objects.get(id=contact_id)
    except Contact.DoesNotExist:
        return Response({"error": "Contact does not exist"}, status=status.HTTP_404_NOT_FOUND)

    contact.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)