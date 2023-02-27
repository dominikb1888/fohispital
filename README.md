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

