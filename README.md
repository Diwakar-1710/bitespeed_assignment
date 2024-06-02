# Contact Identity Reconciliation Service

This Django project provides a web service for reconciling customer identities across multiple purchases based on email and phone number information.

## Features

- **Identity Reconciliation**: Identify and keep track of customer identities across multiple purchases.
- **Primary and Secondary Contacts**: Maintain primary and secondary contact information in the database.
- **RESTful API**: Expose an endpoint `/identify` to receive HTTP POST requests for identity reconciliation.
                 :Expose an endpoint `/get_all_contacts` to receive HTTP GET requests that return all contact data

## Getting Started

To run this project locally, follow these steps:

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd <repository-name>

2. **Install dependencies**:

   ```bash
   pip install django

3. **Run migrations**:

   ```bash
   python manage.py makemigrations
   python manage.py migrate

4. **Start the development server**:

    ```bash
    python manage.py runserver

 
