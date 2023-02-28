# Welcome to FOHIspital

## A completely digital hospital experience on FHIR

Step-by-step we will build a digital hospital and many of its interactions with fileformats in healthcare. We will build a full-stack web application with a modern stack using FastAPI, Vue.js, PostgreSQL and Docker.

## 0. Hello World - Let's Get started

- Install FastAPI

    pip -r install requirements.txt

## 1. Routes and Patients - Our first FHIR interaction

### Add router folder and reorganize code

Run the local dev server. Beware, we now need to start uvicorn with the folder name "app":

    uvicorn app.main:app --reload


### 1.1. Serving and Accepting FHIR Resources

- Get a patient resource from the latest FHIR spec
    -> https://docs.smarthealthit.org/dstu2-examples/

- Add a new route and accept get and post requests

    -> see file routers/patients.py

- Make sure you validate the inputs
    -> add fhir.resources which comes with a Pydantic Type Definition and a Class for each FHIR Resource


- Retrieve the list of patients

- Create a set of patients by posting to the route
    -> How to set the id? How to store the data?
    -> UUID, Postgres bjson

- Retrieve the individual Patient by id


### Synthesis

Let's Analyze what we did:
    - We imported modules to allow for separating out routers to submodules of our app
    - We looked at types and their validation
    - We introduced FHIR and its resources
    - We create routes for listing all or individual patients (GET)
    - We created a route to create new patient (POST)
    - We worked with the operating systems and files in Python
    - We worked with the JSON File Format

What could be improved:
    - User ids are still weird and non-systematic
    - Storing our Resources on the file server is difficult, e.g. if multiple users want to change the same patient
    - Our code has some areas with duplications or lacks extensibility
    - No 'real' user interface

## 2. FHIR Validation in depth

### 2.1. Create a generic FHIR Validator

What about accepting any valid FHIR resource after testing it on upload? How might we implement that?

'''

    from fhir.resources import construct_fhir_element

    construct_fhir_element(resource["resourceType"], resource)

'''

Test it with resource from hapi.fhir.org

### Dockerize your Backend

Since we started out using a requirements.txt file the next steps should be easy. Create a file called "Dockerfile" in the root of your project and put these contents:


'''

#
FROM python:3.10-slim

#
WORKDIR /code

#
COPY ./requirements.txt /code/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
COPY ./app /code/app

#
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

'''

Then run:

'''

    docker build -t backend .

'''

Then start your container with:


'''

docker run -d --name fhir_backend -p 80:80 backend

'''

Navigate your browser to 'localhost' and you should see the entry message of our service. More info via: https://fastapi.tiangolo.com/deployment/docker/


## 3. Postgres Persistence

One major flaw of our system ist the lack of proper persistence, i.e. storage of data outside of memory. Currently, we use file which are easy to use and share. However, this approach is only sensible as long as the amount of interactions with the data and especiallu update operations is low. In addition, if you wanted to update only one field it would mean a complete loading of the file and then exchanging of the value based on its dictionary key. This might be ok for one operation, but absolutely inefficient for large numbers of edits.

Databases are great tools to persist data an efficient and extensible way. There are many types of database systems and approaches to modeling data for them. Which one is right for FHIR?

### 3.1. Document vs. Relational Databases

### 3.2. Postsgres BJSON as middleground

### 3.3 CRUD operations in Fastapi with SQLMODEL and Postgres BJSON

### 3.4 Dockerizing the database

### Synthesis
