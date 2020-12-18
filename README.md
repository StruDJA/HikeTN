# Full Stack HikeTN API Backend

### Discover your next hike from hikers like you.

## Live app at [Heroku](https://hiketn.herokuapp.com)

## Getting Started

### Installing Dependencies

#### Backend

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

## ENV Variables Setup
Set your app, database and Auth0 variables within the `config.py` file.

## Running the server

From within the main directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app
flask run --reload
```

Using `--reload` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `app` directs flask to use the `app` directory and the `__init__.py` file to find the application. 


## Testing
In order to run tests use the following command:

```bash
python test_app.py
```

All tests are kept in that file and should be maintained as updates are made to app functionality.

## Authentication

The authentication system used for this project is Auth0.

The `/login` endpoint will redirect you to Auth0 login page then to the `/auth` endpoint where you will get your JWT access token for the API after retrieving it upon successful callback from `/callback` endpoint.

```bash
{
  "success":true, "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Imc2TktBSHp5b094TWRMNzRGcWlKNyJ9.eyJpc3MiOiJodHRwczovL3N0cnVkZXYtdG4uZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmZGJmZjI4NGQ2ZTViMDA2Y2Y2OGNlNyIsImF1ZCI6Ikhpa2VUTkFQSSIsImlhdCI6MTYwODI2ODE0NiwiZXhwIjoxNjA4Mjc1MzQ2LCJhenAiOiJXNm5INnZLNXpnOVR2ZWVEWlFhQVA4dHliR3JFZVAzZCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOnJlZ2lvbnMiLCJkZWxldGU6cmV2aWV3cyIsImRlbGV0ZTp0cmFpbHMiLCJnZXQ6cmV2aWV3cyIsInBhdGNoOnJlZ2lvbnMiLCJwYXRjaDpyZXZpZXdzIiwicGF0Y2g6dHJhaWxzIiwicG9zdDpyZWdpb25zIiwicG9zdDpyZXZpZXdzIiwicG9zdDp0cmFpbHMiXX0.dwKtaGp-SU6x8yvqD1A-so07sD0aGncuVnAZSk97jFxod3UoEFK38-4KagBtwZmkMdPpKQCO7vOULkH-fNlex4vFB-QNBmcRJOKwGeZkHW8njQCQhHtUTROR7Jt_2ypoGe3EdbyKGYGcyUYskZ0lY6-fO8eiaqssxCCsd2E-CBrg_UAkMJTza-oqCMtNuWqyvQlMctsGkBte5o7_57lbVIC5h5iofYVF9VvDGn7EzWAeT4v8y059v1dXyXjfgGpMMW6lDxcqRVZY334YmmsCWbBwdUN8W6U1x6EehJZr-uGcWoFwUZ7dLCDimGWAfd_S8r4AKQBFy-8DIHwk95qtKw",
  "token_type": "Bearer"
}
```

## Authorization

The Auth0 JWT includes claims for permissions based on the user's role within the Auth0 system. 

You can use `postman` or the command line tool `curl` after copying your JWT token like the following:

```bash
export TOKEN='type_your_token_here'
```

Then:

```bash
curl -d '{"rating":4,"comment":"star wars","trail_id":17}' -H "Content-type: application/json" -X POST 'http://127.0.0.1:5000/api/reviews' -H "Authorization: Bearer ${TOKEN}" | jq .

```

## API Reference

### Getting Started
- Base URL: The app can be run locally or from its base URL at Heroku. The backend app is hosted at `https://hiketn.herokuapp.com`.

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return these error types when requests fail:
- 400: Bad Request
- 401: Authorization is expected
- 403: Access denied
- 404: Resource Not Found
- 405: Method not allowed
- 422: Not Processable 
- 500: Internal server error

### Endpoints 
#### GET /api/regions
- General:
    - Returns a list of region objects, success value, and total number of regions.
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
    
- Sample: `curl http://127.0.0.1:5000/api/regions?page=1`

#### GET /api/trails
- General:
    - Returns a list of trail objects, success value, and total number of trails.
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
- Sample: `curl http://127.0.0.1:5000/api/trails?page=1`

#### GET /api/reviews
- General:
    - Returns a list of review objects, success value, and total number of reviews.
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
    - Authentication & authorization needed.
- Sample: `curl 'http://127.0.0.1:5000/api/reviews' -H "Authorization: Bearer ${TOKEN}"`

#### POST /api/regions
- General:
    - Creates a new region object using the submitted name and reg_type. Returns the id of the created region, success value and total regions.
    - Authentication & authorization needed.
- Sample: `curl http://127.0.0.1:5000/api/regions -X POST -H "Content-Type: application/json" -H "Authorization: Bearer ${TOKEN}" -d '{"name":"Tunis", "reg_type": "Cold"}'`

#### POST /api/trails
- General:
    - Creates a new trail object using the submitted name, distance, elevation, difficulty, coordination, parking. Returns the id of the created trail, success value and total trails.
    - Authentication & authorization needed.
- Sample: `curl http://127.0.0.1:5000/api/regions -X POST -H "Content-Type: application/json" -H "Authorization: Bearer ${TOKEN}" -d '{name": "Chenini2","distance": 5,"elevation": 200,"difficulty": "intermediate","coordination": {"region": "Tataouine", "lat": 32.9232228504901, "lon": 10.260753677963038},"parking": false}'`

#### POST /api/reviews
- General:
    - Creates a new review object using the submitted rating, comment and trail_id. Returns the id of the created review, success value and total reviews.
    - Authentication & authorization needed.
- Sample: `curl http://127.0.0.1:5000/api/regions -X POST -H "Content-Type: application/json" -H "Authorization: Bearer ${TOKEN}" -d '{"rating":4, "comment": "Natural park with a large variety of mediterranean trees and plants", "trail_id": 17}'`

#### DELETE /api/regions/{region_id}
- General:
    - Deletes the region object of the given ID if it exists. Returns the id of the deleted region, success value and total regions.
    - Authentication & authorization needed.
- Sample: `curl -X DELETE http://127.0.0.1:5000/api/regions/38 -H "Authorization: Bearer ${TOKEN}"`

#### DELETE /api/trails/{trail_id}
- General:
    - Deletes the trail object of the given ID if it exists. Returns the id of the deleted trail, success value and total trails.
    - Authentication & authorization needed.
- Sample: `curl -X DELETE http://127.0.0.1:5000/api/trails/38 -H "Authorization: Bearer ${TOKEN}"`

#### DELETE /api/reviews/{review_id}
- General:
    - Deletes the review object of the given ID if it exists. Returns the id of the deleted review, success value and total reviews.
    - Authentication & authorization needed.
- Sample: `curl -X DELETE http://127.0.0.1:5000/api/reviews/38 -H "Authorization: Bearer ${TOKEN}"`

#### PATCH /api/regions/{region_id}
- General:
    - Updates the region object of the given ID if it exists. Returns success value and the whole region object.
    - Authentication & authorization needed.
- Sample: `curl http://127.0.0.1:5000/api/regions/38 -X PATCH -H "Content-Type: application/json" -d '{"reg_type": "Warm"}' -H "Authorization: Bearer ${TOKEN}"`

#### PATCH /api/trails/{trail_id}
- General:
    - Updates the trail object of the given ID if it exists. Returns success value and the whole trail object.
    - Authentication & authorization needed.
- Sample: `curl http://127.0.0.1:5000/api/trails/38 -X PATCH -H "Content-Type: application/json" -d '{"name": "Nahli Park"}' -H "Authorization: Bearer ${TOKEN}"`

#### PATCH /api/reviews/{review_id}
- General:
    - Updates the review object of the given ID if it exists. Returns success value and the whole review object.
    - Authentication & authorization needed.
- Sample: `curl http://127.0.0.1:5000/api/trails/38 -X PATCH -H "Content-Type: application/json" -d '{"rating": 3}' -H "Authorization: Bearer ${TOKEN}"`