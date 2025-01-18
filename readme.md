# Django Project Setup

Table of Contents

- Prerequisites
- Installation
- Running the Project
- APIs

==================================

# Prerequisites

Ensure the following are installed:

- Python 3.8+
- Django 4.2+
- pip (Python package manager)
- Virtualenv
- Git (for cloning the repository)

==================================

# Installation

Follow these steps to set up the project:

- Clone the repository:

        git clone https://github.com/rohitprasain99/djangoDrfInterview.git

- Navigate to the project directory:

  cd project-name

- Create a virtual environment:

  python -m venv venv

- Activate the virtual environment:

  Windows:

        venv\Scripts\activate

  macOS/Linux:

        source venv/bin/activate

- Install dependencies:

        pip install -r requirements.txt

- Apply database migrations:

        python manage.py migrate

==================================

# Running the Project

Start the development server with the following command:

    python manage.py runserver

Access the application in your browser at:

    http://127.0.0.1:8000/

==================================

# APIs

baseUrl:

    http://127.0.0.1:8000/api

# User Registration

Endpoint: [POST]

    {{baseurl}}/register/

Request:

    {
        "email": "abmalla19@gmail.com",
        "password": "ab@123"
    }

Response:

    {
        "data": {
            "email": "abmalla19@gmail.com"
         },
        "message": "user registered successfully"
    }

# User Login

Endpoint: [POST]

    {{baseurl}}/token/

Request:

    {
        "email": "abmalla19@gmail.com",
        "password": "ab@123"
    }

Response:

    {
        "data": {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM3MTkxNTMxLCJpYXQiOjE3MzcxOTAwMzEsImp0aSI6IjI2OWQ5ZDc4MjgwYjRlNjJhNGU0NjQwZmY4MDFmOTc5IiwidXNlcl9pZCI6IjgwYjJhOTU2LWJkNDEtNDYxMC04N2Y0LTY5M2U3MDQ4OTNhMSJ9.QuUVDu6GQFwElJYt1zrJujeBOVSH1yIcESCPu-NAosk",
            "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczNzI3NjQzMSwiaWF0IjoxNzM3MTkwMDMxLCJqdGkiOiJjMjFlMTViNzI2MmM0MGI2OGI5NDdlYmEwNTQ4MTk0YiIsInVzZXJfaWQiOiI4MGIyYTk1Ni1iZDQxLTQ2MTAtODdmNC02OTNlNzA0ODkzYTEifQ.Bo9RgYURCgnzDS161t0GPMQdTKq3ET2CwCOCsxHuyYg",
        "message": "logged in successfully"
        }
    }

==================================

# Generate access token from refresh token

Endpoint: [GET]

    {{baseurl}}/token/refresh/

Request:

    {
         "refresh_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczNzIzOTY0MiwiaWF0IjoxNzM3MTUzMjQyLCJqdGkiOiJhMDQ2MmE2ZmE2ZGM0OWM0OGRlOWQ0OTRiOTYyNmNjZCIsInVzZXJfaWQiOiI4YzM3N2E3OS1kZDNmLTQ2NWItYmQxMC04MzEwODk1YjVlNmQifQ.svCEmvqWuFOgZnGL29KYq29SMdyGN7yIEXK-Cp3207M"
    }

Response:

    {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM3MTkxNzA4LCJpYXQiOjE3MzcxOTAwMzEsImp0aSI6ImZmOWM0NjEwMzFmYTQwNDBhYTRjNzljMjM3N2Q5NjMxIiwidXNlcl9pZCI6IjgwYjJhOTU2LWJkNDEtNDYxMC04N2Y0LTY5M2U3MDQ4OTNhMSJ9.QruoETyWtOcTcQrdg44QTVlFq2blVvDJp6vJqnH1JI8"
    }

==================================

# Jwt blacklist for logout functionality

Endpoint: [POST]

    {{baseurl}}/logout/

Request:

    {
        "refresh_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczNzI3NjQzMSwiaWF0IjoxNzM3MTkwMDMxLCJqdGkiOiJjMjFlMTViNzI2MmM0MGI2OGI5NDdlYmEwNTQ4MTk0YiIsInVzZXJfaWQiOiI4MGIyYTk1Ni1iZDQxLTQ2MTAtODdmNC02OTNlNzA0ODkzYTEifQ.Bo9RgYURCgnzDS161t0GPMQdTKq3ET2CwCOCsxHuyYg"
    }

Response:

    {
        "message": "Token successfully blacklisted"
    }

# Reset Password

1.  Endpoint: [GET] - generate OTP

        {{baseurl}}/forget_password/

Request:

    {
        "email":"abmalla19@gmail.com"
    }

Response:

    {
        "message": "please check mail for OTP code. It expires in 5 minute",
        "otp": "688952"
    }

2.  Endpoint: [POST] - update password

        {{baseurl}}/new_password_otp/

Request:

    {
        "otp":"493868",
        "new_password":"ab@12345"
    }

Response:

    {
        "message": "Password changed successfully"
    }

# Change Password

Endpoint: [POST]

    {{baseurl}}/change_password/

Authentication Header (Required):

    Bearer {{access_token}}

Request:

    {
        "current_password": "ab@12345",
        "new_password": "ab@12"
    }

Response:

    {
        "message": "Password updated successfully"
    }

# User Profile

Authentication Header (Required) for all endpoints:

    Bearer {{access_token}}

Endpoint: [POST]

    {{baseurl}}/create_profile/

Request:

    {
        "first_name":"abhushan",
        "last_name" : "malla",
        "country" : "nepal",
        "contact" : "+447813241324"
    }

Response:

    {
        "data": {
            "first_name": "abhushan",
            "last_name": "malla",
            "country": "nepal",
            "contact": "+447813241324"
        },
        "message": "User created successfully"
    }

Endpoint: [GET]

    {{baseurl}}/get_profile/

Request:

    {

    }

Response:

    {
        "data": {
            "first_name": "abhushan",
            "last_name": "malla",
            "country": "nepal",
            "contact": "+447813241324",
            "email": "abmalla19@gmail.com"
        },
        "message": "User profile updated successfully"
    }

Endpoint: [PATCH]

    {{baseurl}}/update_profile/

Request:

    {
        "first_name": "abhushann",
        "last_name": "mallaaaa"
    }

Response:

    {
        "data": {
            "first_name": "abhushann",
            "last_name": "mallaaaa",
            "country": "nepal",
            "contact": "+447813241324",
            "email": "abmalla19@gmail.com"
        },
        "message": "User profile updated successfully"
    }

Endpoint: [DELETE]

    {{baseurl}}/delete_profile/

Request:

    {

    }

Response:

    {
        "message": "User detail deleted successfully"
    }

# Contact

For questions, contact:

Email: prasainrohit@gmail.com

GitHub: https://github.com/rohitprasain99
