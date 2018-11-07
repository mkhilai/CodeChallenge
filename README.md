# CodeChallenge

The CodeChallenge project

Python 3, Django 2.1, Django Rest 3.9

API has the following endpoints:

- localhost:8000/login/ Accepts POST requests. In order to create a user the following object needs to be sent.

```json
{
  "username": "testuser",
  "email": "testuser@test.com",
  "password": "testpassword",
  "name": "testname"
}
```

- localhost:8000/companies/ Accepts POST and GET reguests. In order to create a user (or a list of users) the following list of objects needs to be sent. GET returns a list of all companies, related to the currently logged in user.

```json
[{
  "name": "Test Company",
  "email": "test_company@test.com",
  "phone": "+49 123 4567890",
  "country": "Country",
  "city": "City",
  "streetAddress": "City 123 00 B",
  "userID": 1
}]
```


- localhost:8000/companies/companyID/ Accepts GET, PUT, PATCH and DELETE requests.

- localhost:8000/companies/companyID/ Accepts POST requests. In order to get a token of the user the username and password needs to be sent. Later the token is used in order to get access to the user's data.

```json
{
  "username": "testuser",
  "password": "testpassword"
}
```
```json

{
    "token": "f95c7d5c3005db2a610a9e609dba0a70376adec3"
}
```
