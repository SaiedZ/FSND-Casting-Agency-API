# Casting Agency API
</br>

[![CircleCI](https://dl.circleci.com/status-badge/img/gh/SaiedZ/FSND-Casting-Agency-API/tree/master.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/SaiedZ/FSND-Casting-Agency-API/tree/master)
</br>

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)    ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)    ![Heroku](https://img.shields.io/badge/Heroku-430098?style=for-the-badge&logo=heroku&logoColor=white)    ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
</br>

<p align="center">
  <img src="https://user-images.githubusercontent.com/90851774/207030729-d479ea20-2388-4549-a6c8-4369ab3399b9.jpg"
       alt="Casting agency API illustration"
       width="600"/>
</p>
</br>
</br>

## 🔎 About the project

The Casting Agency API  is responsible for creating movies and managing and assigning actors to those movies.

## 💪 Motivation for project

This is the capstone project of Udacity fullstack nanodegree program. It demonstrates our skills to develop and deploy a RESTful API.

## 👉 What I have built ?

- **Backend**
  - Fully functionnal API to manage Actors and Movies
  - Applying software system risk and compliance principles
  - SQLAlchemy
  - Migrations

- **Securing The REST API**
  - Implementing authentication and authorization in Flask using the [Auth0 API](https://auth0.com/)
  - Designing against key security principals
  - Implementing role-based control design patterns

- **Testing**
  - Testing endpoints with **Postman** and **Pytest**

- **Devops**
  - CircleCI pipline to automate tests after commit
  - Docker
  - Deploying the API to Heroku


## ✨ Deployed API

- **URL** : [https://agency-casting-api.herokuapp.com/](https://agency-casting-api.herokuapp.com/)
- **API V1 URL**: [https://agency-casting-api.herokuapp.com/api/v1](https://agency-casting-api.herokuapp.com/api/v1)
- **health check**: [https://agency-casting-api.herokuapp.com/api/v1/health](https://agency-casting-api.herokuapp.com/api/v1/health)

## 🤓 Getting Started (local)

### Installing Dependencies

#### Python 3.10

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## 💻 Running the server (local)

First ensure you are working using your created virtual environment.

You will need to add envirement variables, either to the ` setup.sh ` or to ` .env ` file:

> If added to setup.sh, please add ` export ` at the begining of each line.

```
AUTH0_CLIENT_ID=""
AUTH0_CLIENT_SECRET=""
AUTH0_DOMAIN=""
ALGORITHMS=['RS256']
API_AUDIENCE=""
```

Each time you open a new terminal session, run:

```bash
source ./setup.sh
```

Then run the server:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.


## ✅ Running the tests (local)

### Pytest

To run tests:

```bash
coverage run -m pytest
```

To get the coverage report:

```bash
coverage report -m
```


**Coverage report example**

<img src="https://user-images.githubusercontent.com/90851774/207088816-4e13cf11-7769-4024-9633-34ef1f94a0e1.png"
     alt="Coverage report"
     width="400"/>
     

### Postman

First you need to start the server, import postman collectoion from postman folder and run tests.

![image](https://user-images.githubusercontent.com/90851774/207124182-cc632b39-3848-41f5-92a9-56d6e19a451f.png)


## 📖 API Reference

### Getting Started

- **Base URL**:
  - local app: the default url is http://127.0.0.1:5000/api/v1/
  - deployed app: https://agency-casting-api.herokuapp.com/api/v1/

- **Authentication**: Endpoints need a JWT token generated by the Auth0 after user's login.
  - Bearer {token} 
- **Permission**: All endpoints need a specific permission (see bellow for more detail). They are included in the JWT Token from Auth0.
- **Headers**: 
  - "Content-Type": "application/json"
  - "Accept": "application/json"


### Auth0 roles

- Casting Assistant
    - Can view actors and movies
- Casting Director
    - All permissions a Casting Assistant has and…
    - Add or delete an actor from the database
    - Modify actors or movies
- Executive Producer
    - All permissions a Casting Director has and…
    - Add or delete a movie from the database

### Postman request examples

A postman collection with request examples could be found in the postman folder: "FSND-Casting-Agency.postman_collection.json"

### Error Handling

Errors are returned as JSON objects in the following format:
```json
{
    "success": false, 
    "error": 400,
    "message": "bad request",
}
```

The API will return three error types when requests fail:

- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Resource Not Found
- 422: Not Processable
- 500: Internal Server Error

### 🧝‍♂️ Actors endpoints

#### GET ` /actors `

    Gets all actors

    Request Arguments
    -------    
    None
    
    Permissions
    -------
    get:actors

    Returns
    -------
    JSON:
        sucess: bool
            will be True if the request was successfully handled.
        actors: list of json objects
            description of actors.
        page: int
            the current page number.
        pages: int
            the total number of pages.
        next_page: int or False
            the next page number or False if there is no next page.
        next_page_url: str or False
            the url for the next page or False if there is no next page.
        total_actors: int
            the total number of actors.
    Response code: int
        200.

    Raises
    -------
    500: server error
        if fetching actors from db fails.

    Response example:
    -------
    
```json
  {
  "actors": [
      {
          "age": 35,
          "gender": "Female",
          "id": 1,
          "movies": [
              {
                  "description": null,
                  "genre": "Action",
                  "id": 2,
                  "release_date": "Tue, 01 Jan 2002 00:00:00 GMT",
                  "title": "Die Hard 2"
              }
          ],
          "name": "Jannet",
          "number_movies": 1
      },
      {
          "age": 3,
          "gender": "Male",
          "id": 2,
          "movies": [],
          "name": "Jammy",
          "number_movies": 0
      },
      {
          "age": 3,
          "gender": "Male",
          "id": 3,
          "movies": [],
          "name": "Jammy",
          "number_movies": 0
      }
  ],
  "next_page": 2,
  "next_page_url": "http://127.0.0.1:5000/api/v1/actors?page=2",
  "page": 1,
  "pages": 5,
  "success": true,
  "total_actors": 15
}

```
  
#### POST ` /actors`

    Creates a new actor.

    Permissions
    -------
    create:actor

    Returns
    -------
    JSON:
        success: bool
            will be True if the request was successfully handled.
        actor: JSON
            a formatted representation of the created actor.
    Response code: int
        201

    Notes
    -------
    See errors section for more information about the errors that can be raised.


    Response example:
    -------
    
```json
{
"actor": {
    "age": 3,
    "gender": "Male",
    "id": 18,
    "movies": [],
    "name": "Jammy",
    "number_movies": 0
},
"success": true
}
```
    
#### PATCH ` /actors/$id`

    Updates an existing actor.

    Permissions
    -------
    patch:actor

    Parameters
    -------
    id: int
        the id of the actor to be updated.

    Returns
    -------
    JSON:
        success: bool
            will be True if the request was successfully handled.
        actor: JSON
            a formatted representation of the updated actor.
    Response code: int
        200

    Notes
    -------
    See errors section for more information about the errors that can be raised.
    
    
    Response example:
    -------
    
```json
{
    "actor": {
        "age": 3,
        "gender": "Female",
        "id": 18,
        "movies": [],
        "name": "Jannet",
        "number_movies": 0
    },
    "success": true
}
```
  
#### DELETE ` /actors/$id`

   Deletes an existing actor.

    Permissions
    -------
    delete:actor

    Parameters
    -------
    id: int
        the id of the actor to be deleted.

    Returns
    -------
    JSON:
        success: bool
            will be True if the request was successfully handled.
        detele: int
            the id of the deleted actor.
    Response code: int
        200
    
    Raises
    -------
    500: server error
        if deleting actor from db fails.
        
    Response example:
    -------
    
```json
{
    "delete": 18,
    "success": true
}
```
    
### 🎬 Movies endpoints

#### GET ` /movies `

    Gets all movies

    Permissions
    -------
    get:movies

    Returns
    -------
    JSON:
        sucess: bool
            will be True if the request was successfully handled.
        movies: list of json objects
            description of movies.
        page: int
            the current page number.
        pages: int
            the total number of pages.
        next_page: int or False
            the next page number or False if there is no next page.
        next_page_url: str or False
            the url for the next page or False if there is no next page.
        total_movies: int
            the total number of movies.
    Response code: int
        200.

    Raises
    -------
    500: server error
        if fetching movies from db fails.

    Response example:
    -------
    
```json
{
"movies": [
    {
        "actors": [],
        "description": null,
        "genre": "Action",
        "id": 1,
        "num_actors": 0,
        "release_date": "Fri, 01 Jan 1999 00:00:00 GMT",
        "title": "Die Hard 1"
    },
    {
        "actors": [
            {
                "age": 35,
                "gender": "Female",
                "id": 1,
                "name": "Jannet"
            }
        ],
        "description": null,
        "genre": "Action",
        "id": 2,
        "num_actors": 1,
        "release_date": "Tue, 01 Jan 2002 00:00:00 GMT",
        "title": "Die Hard 2"
    }
    ],
    "next_page": false,
    "next_page_url": false,
    "page": 1,
    "pages": 1,
    "success": true,
    "total_movies": 2
}
```
    
#### POST ` /movies`

    Creates a new movie.
    
    Permissions
    -------
    create:movies

    Returns
    -------
    JSON:
        success: bool
            will be True if the request was successfully handled.
        movie: JSON
            description of the created movie.
    Response code: int
        201.

    Notes
    -------
    See errors section for more information about the errors that can be raised.
    
    Response example:
    -------
    
```json
{
    "movie": {
        "actors": [
            {
                "age": 35,
                "gender": "Female",
                "id": 1,
                "name": "Jannet"
            }
        ],
        "description": null,
        "genre": "Action",
        "id": 3,
        "num_actors": 1,
        "release_date": "Sat, 01 Jan 2005 00:00:00 GMT",
        "title": "Die Hard 3"
    },
    "success": true
}
```

#### PATCH ` /movies/$id`

    Updates an existing movie.

    Permissions
    -------
    patch:movie

    Parameters
    -------
    id: int
        id of the movie to update.

    Returns
    -------
    JSON:
        success: bool
            will be True if the request was successfully handled.
        movie: JSON
            description of the updated movie.
    Response code: int
        200.

    Notes
    -------
    See errors section for more information about the errors that can be raised.

    Response example:
    -------
    
```json
{
    "movie": {
        "actors": [
            {
                "age": 35,
                "gender": "Female",
                "id": 1,
                "name": "Jannet"
            }
        ],
        "description": null,
        "genre": "Action",
        "id": 3,
        "num_actors": 1,
        "release_date": "Sat, 01 Jan 2005 00:00:00 GMT",
        "title": "Die Hard 3"
    },
    "success": true
}
```

#### DELETE ` /movies/$id`

   Deletes an existing movie.

    Permissions
    -------
    delete:movie

    Parameters
    -------
    id: int
        id of the movie to delete.

    Returns
    -------
    JSON:
        success: bool
            will be True if the request was successfully handled.
        delete: int
            id of the deleted movie.
    Response code: int
        200.
    
    Raises
    -------
    500: server error
        if deleting actor from db fails.
        
    Response example:
    -------
    
```json
{
    "delete": 3,
    "success": true
}
```
