# Django backend

We are using Django to run a REST API for the app.

## Setup

Install the following packages with pip:
```shell
pip install django
pip install djangorestframework
pip install djangorestframework-simplejwt
```

## Running

To run the server, run the following command in the `drivingsim` directory:
```shell
python manage.py runserver
```

## REST API Documentation

Authentication is done using JWTs. The following endpoints are available:

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

Request body

```json
{
  "refresh":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY3MDkzODE3NywiaWF0IjoxNjcwODUxNzc3LCJqdGkiOiI1YjBmZmQxYjMi35HJMjJlYmE4ODY0YWQ5OGZlODY5NyIsInVzZXJfaWQiOjF9.olPIMFyiE9YiEL_Xsyw9S27nppgKy227Qgo5g8gF9ks"
}
```

Response body

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjcwODUyNjc2LCJpYXQiOjE2NzA4NTIzNjgsImp0aSI6Ijg3MmU0YzBiMmM2ZDQ3NWU5ZDlkYjNhZWQyNTNhMzcxIiwidIelcl9pZCI6MX0.QXi_e7tqICU1SlKMOwOlXirejUXm7fyHuRqQa_T87J0"
}
```


