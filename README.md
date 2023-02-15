# Django backend

We are using Django to run a REST API for the app.

## Setup

Install the following packages with pip:
```shell
pip install django
pip install djangorestframework
pip install djangorestframework-simplejwt
```

## Initialising or updating after pull

Run the following commands to update the database with the latest models:
```shell
python manage.py makemigrations
python manage.py migrate
```

## Running

To run the server, run the following command in the `drivingsim` directory:
```shell
python manage.py runserver
```

## REST API Documentation

Authentication is done using JWTs. All requests use the `application/json` content type, unless stated otherwise.

### Create an account

```
POST /api/user
```

Request body in `x-www-form-urlencoded`:

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

Response body:

```json
{
    "username": "test"
}
```

### View other user's information

```
GET /api/user/<username>/
```

Response body:

```json
{
    "username": "test"
}
```

If the user is set to private, the response will be an error message and the status code will be `403`.

### Send a friend request

```
POST api/friend/<str:username>/send/
```

Response body:

User doesn't exist:
```json
{
    "error": "User does not exist"
}
```

Friend request already sent:
```json
{
    "error": "Friend request already sent"
}
```

Friend request already received:
```json
{
    "error": "Friend request already received"
}
```

Friend request succesfully sent:
```json
{
    "success": "Friend request sent"
}
```

### Accept a friend request

```
POST api/friend/<str:username>/accept
```

Response body:


User does not exist:
```json
{
    "error": "User does not exist"
}
```

Friend request does not exist:
```json
{
    "error": "Friend request does not exist"
}
```

Friend request succesfully accepted:
```json
{
    "success": "Friend request accepted"
}
```

### View your friends

```
GET api/friend/
```

Response body:
```json
{
    "friends": "test"
}
```
