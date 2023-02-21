# P&O driving simulator backend

We are using Django to run a REST API. 

## Table of contents

1. [Setup](#setup)
2. [Initialising or updating after pull](#initialising-or-updating-after-pull)
3. [Testing](#testing)
4. [REST API Documentation](#rest-api-documentation)
    1. [Create an account](#create-an-account)
    2. [Login by generating a JWT](#login-by-generating-a-jwt)
    3. [Refresh an access token](#refresh-an-access-token)
    4. [View your user information](#view-your-user-information)
    5. [View other user's information](#view-other-users-information)
    6. [Send a friend request](#send-a-friend-request)
    7. [Accept a friend request](#accept-a-friend-request)
    8. [Decline a friend request](#decline-a-friend-request)
    9. [Remove a friend or friend request](#remove-a-friend-or-friend-request)
   10. [View your received friend requests](#view-your-received-friend-requests)
   11. [View your friends](#view-your-friends)

## Setup

You can install all necessary packages at once with `pip`:
```shell
pip install -r requirements.txt
```

Or you can install the packages one by one with `pip`:
```shell
pip install django
pip install djangorestframework
pip install djangorestframework-simplejwt
pip install django-cors-headers
pip install django-extensions
```

## Initialising or updating after pull

Run the following commands to update the database with the latest models:
```shell
python manage.py makemigrations
python manage.py migrate
```

## Testing

To run the server, run the following command in the `drivingsim` directory:
```shell
python manage.py runserver
```

You may want to create a superuser to access the admin panel or to use as a dummy account:
```shell
python manage.py createsuperuser --username=test --email=test@test.com
````

If you want to play around with user models, you can use the Django shell:
```shell
python manage.py shell
```

To create 4 dummy accounts, run the following command:
```shell
python manage.py runscript scripts.creation_script
````

The following accounts will be added to the database:
```js
testUser1 = {
    "username": "testuser1",
    "password1": "TestPass8263",
    "password2": "TestPass8263",
    "email": "testuser1@domain.com",
    "national_registration_number": "01.20.07-050.90",
    "is_learner": True,
    "is_instructor": False,
    "has_drivers_license": True,
    "is_shareable": True
}

testUser2 = {
    "username": "testuser2",
    "password1": "TestPass8264",
    "password2": "TestPass8264",
    "email": "testuser2@domain.com",
    "national_registration_number": "12.00.05-030.00",
    "is_learner": True,
    "is_instructor": False,
    "has_drivers_license": False,
    "is_shareable": True
}

testInstructor1 = {
    "username": "testinstructor1",
    "password1": "TestPass8265",
    "password2": "TestPass8265",
    "email": "testinstructor1@domain.com",
    "national_registration_number": "60.60.06-060.00",
    "is_learner": False,
    "is_instructor": True,
    "has_drivers_license": True,
    "is_shareable": True        
}

testInstructor2 = {
    "username": "testinstructor2",
    "password1": "TestPass8266",
    "password2": "TestPass8266",
    "email": "testinstructor2@domain.com",
    "national_registration_number": "09.30.70-210.10",
    "is_learner": False,
    "is_instructor": True,
    "has_drivers_license": True,
    "is_shareable": True
}
````

## REST API Documentation

Authentication is done using JWTs. All requests use the `application/json` content type, unless stated otherwise. All request bodies and responses are in JSON format.

### Create an account

```
POST /api/user/
```

```json
{
    "username": "username",
    "password1": "password",
    "password2": "password",
    "email": "email@domain.com",
    "national_registration_number": "00.00.00-000.00",
    "is_learner": false,
    "is_instructor": false,
    "has_drivers_license": false,
    "is_shareable": false
}
```

If `is_shareable` is set to `true`, the user's details will be viewable by other users.

Response body:

```json
{
    "user": {
        "username": "username",
        "email": "email@domain.com",
        "is_learner": false,
        "is_instructor": false,
        "has_drivers_license": false,
        "is_shareable": false
    },
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY3MzQ1Mzk2MCwiaWF0IjoxNjcwODYxOTYwLCJqdGkiOiJiMTMzYjdhYTgzNjU0ZDdjYjc4MGFhODgyYWZiZmVhNiIsInVzZXJfaWQiOjh9.20JI1zrBf4PS936Klqdw4S9n-KcglC-Jd6kBBkBw67M",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjcxMjkzOTYwLCJpYXQiOjE2NzA4NjE5NjAsImp0aSI6IjViZDZkNDY0NDYxYTRjYmViN2QwMTMwMWE0MmUxYTc4IiwidXNlcl9pZCI6OH0.LTdHxXOrdJjQNZvFrvVlF_tE0jfaWvrR8i5dluij3Ng"
}
```

The `access` token can be used for requests that require authentication, while the `refresh` token can be used to refresh the `access` token.

### Login by generating a JWT

```
POST /api/token/
```

Request body:

```json
{
    "username": "username",
    "password": "password"
}
```

Response body:

```json
{
    "refresh":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY3MDkzODE3NywiaWF0IjoxNjcwODUxNzc3LCJqdGkiOiI1YjBmZmQxYjMi35HJMjJlYmE4ODY0YWQ5OGZlODY5NyIsInVzZXJfaWQiOjF9.olPIMFyiE9YiEL_Xsyw9S27nppgKy227Qgo5g8gF9ks","access":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZxhWeIjoxNjcwODUyMDc3LCJpYXQiOjE2NzA4NTE3NzcsImp0aSI6IjQ5YTJkZjI0YWI2MjRhM2NiODAxZWY2OGExMGI0NzEwIiwidXNlcl9pZCI6MX0.yK265VBj99YwGJI8Jsxskclo_Qu3NiWlI76tHmBsHYI"
}
```

The `access` JWT will be used in requests that require user authentication. You can use the `access` token in an `Authorization` header like so:

```http request
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZxhWeIjoxNjcwODUyMDc3LCJpYXQiOjE2NzA4NTE3NzcsImp0aSI6IjQ5YTJkZjI0YWI2MjRhM2NiODAxZWY2OGExMGI0NzEwIiwidXNlcl9pZCI6MX0.yK265VBj99YwGJI8Jsxskclo_Qu3NiWlI76tHmBsHYI
```

This will become clear in future examples.

An access token is valid for 5 days. Once this time has passed, you will need to generate a new access token using the refresh token which is valid for 30 days.

### Refresh an access token

```
POST /api/token/refresh/
```

Request body:

```json
{
    "refresh":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY3MDkzODE3NywiaWF0IjoxNjcwODUxNzc3LCJqdGkiOiI1YjBmZmQxYjMi35HJMjJlYmE4ODY0YWQ5OGZlODY5NyIsInVzZXJfaWQiOjF9.olPIMFyiE9YiEL_Xsyw9S27nppgKy227Qgo5g8gF9ks"
}
```

Response body:

```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjcwODUyNjc2LCJpYXQiOjE2NzA4NTIzNjgsImp0aSI6Ijg3MmU0YzBiMmM2ZDQ3NWU5ZDlkYjNhZWQyNTNhMzcxIiwidIelcl9pZCI6MX0.QXi_e7tqICU1SlKMOwOlXirejUXm7fyHuRqQa_T87J0"
}
```

This access token will also be valid for 5 days and can be used in the same way as the previous access token.

### View your user information

```
GET /api/user/
```

Headers:

```
Authorization: Bearer <access token>
```

Response body:

```json
{
    "username": "username",
    "email": "email@domain.com",
    "is_learner": false,
    "is_instructor": false,
    "has_drivers_license": false,
    "is_shareable": false
}
```

### View other user's information

```
GET /api/user/<username>/
```

Headers:

```
Authorization: Bearer <access token>
```

Response body:

```json
{
    "username": "username",
    "email": "email@domain.com",
    "is_learner": false,
    "is_instructor": false,
    "has_drivers_license": false,
    "is_shareable": false
}
```

If the user is set to private, the response will be an error message and the status code will be `403`.

### Send a friend request

```
POST /api/friend/request/<to_username>/send/
```

Headers:

```
Authorization: Bearer <access token>
```

Response body:
```
{
    "message": "User does not exist/Friend request already sent/Friend request already received/Friend request sent"
}
```

If the user is not found, the response code is `404`. If the friend request fails, the response code is `400`. If the friend request is sent, the response code is `200`.

### Accept a friend request

```
POST /api/friend/request/<from_username>/accept/
```

Headers:

```
Authorization: Bearer <access token>
```

Response body:

```
{
    "message": "User does not exist/Friend request does not exist/Friend request accepted"
}
```

If the user or friend request does not exist, the response code is `404`. If the friend request fails, the response code is `400`. If the friend request is accepted, the response code is `200`.

### Decline a friend request

```
POST /api/friend/request/<from_username>/decline/
```

Headers:

```
Authorization: Bearer <access token>
```

Response body:

```
{
    "message": "User does not exist/Friend request does not exist/Friend request declined"
}
```

### Remove a friend or friend request

```
POST /api/friend/<from_username>/remove/
```

Headers:

```
Authorization: Bearer <access token>
```

Response body:

```
{
    "message": "User does not exist/Friend does not exist/Friend removed"
}
```

### View your received friend requests

```
GET /api/friend/request/
```

Headers:

```
Authorization: Bearer <access token>
```

Response body:

```json
[
  {
    "from_user": {
      "username": "test1",
      "email": "test1@test.com",
      "is_learner": false,
      "is_instructor": false,
      "has_drivers_license": false,
      "is_shareable": false
    },
    "to_user": {
      "username": "test2",
      "email": "test2@test.com",
      "is_learner": false,
      "is_instructor": false,
      "has_drivers_license": false,
      "is_shareable": false
    },
    "accepted": true
  }
]
```

### View your friends

```
GET /api/friend/
```

Headers:

```
Authorization: Bearer <access token>
```

Response body:

```json
[
  {
    "from_user": {
      "username": "test1",
      "email": "test1@test.com",
      "is_learner": false,
      "is_instructor": false,
      "has_drivers_license": false,
      "is_shareable": false
    },
    "to_user": {
      "username": "test2",
      "email": "test2@test.com",
      "is_learner": false,
      "is_instructor": false,
      "has_drivers_license": false,
      "is_shareable": false
    },
    "accepted": true
  }
]
```
