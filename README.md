# DocHUB CRUD app API WITH DJANGO REST FRAMEWORK
[Django REST framework](http://www.django-rest-framework.org/) is a powerful and flexible toolkit for building Web APIs.

## Requirements
- Python 3.6
- Django 3.1
- Django REST Framework

## Structure
In a RESTful API, endpoints (URLs) define the structure of the API and how end users access data from our application using the HTTP methods - GET, POST, PUT, DELETE. Endpoints should be logically organized around _collections_ and _elements_, both of which are resources.

In our case, we have one single resource, `api`, so we will use the following URLS - `api/v1/auth/register/`, `api/v1/auth/login/`, `api/v1/patient/`, and `api/v1/patient/<str:pk>/` for collections and elements, respectively:

Endpoint |HTTP Method | CRUD Method | Result
-- | -- |-- |--
`api/v1/auth/register/` | POST | CREATE | Register an user
`api/v1/auth/login/` | POST | CREATE | User login
`api/v1/patient/`| POST | CREATE | Add a patient data
`api/v1/patient/`| GET | READ | Get all patients data
`api/v1/patient/<str:pk>/` | PUT | UPDATE | Update a patient data
`api/v1/patient/<str:pk>/` | DELETE | DELETE | Delete a patient data

## Use
We can test the API using [heroku](https://doc-hub-app.herokuapp.com/) or we can use [Postman](https://www.postman.com/)
