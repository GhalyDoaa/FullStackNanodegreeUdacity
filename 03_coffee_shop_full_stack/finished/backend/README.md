# Coffee Shop Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

$ cd YOUR_PROJECT_DIRECTORY_PATH/
$ virtualenv --no-site-packages env
$ source env/bin/activate
```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```

### Running the server

From within the ./src directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:
```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.


### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `get:drinks-detail`
    - `post:drinks`
    - `patch:drinks`
    - `delete:drinks`
6. Create new roles for:
    - Barista
        - can `get:drinks-detail`
    - Manager
        - can perform all actions
##Testing
Just like the 2nd Project, I used Test-Driven-Development to implement all Endpoints.

I used Postman Collections to test all my Endpoints for expected behaviour & correct permission execution.

To execute the tests, follow these steps:

Install Postman
Download the Postman Collection in this Repo (udacity-fsnd-udaspicelatte.postman_collection.json)
Open Postman and click on "Import" on the upper-left corner
Select udacity-fsnd-udaspicelatte.postman_collection.json
Once uploaded, you can simple click on "Runner" (right next to "Import") and start all tests.
tip: Dont forget to have flask running before testing!

Please note that tests have been made with (possibly) invalid tokens, so some of them won´t pass anymore.
