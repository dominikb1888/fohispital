# Welcome to FOHIspital

## A completely digital hospital experience on FHIR

Step-by-step we will build a digital hospital and many of its interactions with fileformats in healthcare. We will build a full-stack web application with a modern stack using FastAPI, Vue.js, PostgreSQL and Docker.

## 0. Hello World - Let's Get started

- Install FastAPI

```{python}

pip -r install requirements.txt


```

## 1. Routes and Patients - Our first FHIR interaction

### Add router folder and reorganize code

Run the local dev server. Beware, we now need to start uvicorn with the folder name "app":

```{python}

uvicorn app.main:app --reload

```

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

```{python}

    from fhir.resources import construct_fhir_element

    construct_fhir_element(resource["resourceType"], resource)

```

Test it with resource from hapi.fhir.org

### Dockerize your Backend

Since we started out using a requirements.txt file the next steps should be easy. Create a file called "Dockerfile" in the root of your project and put these contents:


```{docker}

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

```

Then run:

```{bash}

docker build -t backend .

```

Then start your container with:


```{bash}

docker run -d --name fhir_backend -p 80:80 backend

```

Navigate your browser to 'localhost' and you should see the entry message of our service. More info via: https://fastapi.tiangolo.com/deployment/docker/


## 3. Postgres Persistence

One major flaw of our system ist the lack of proper persistence, i.e. storage of data outside of memory. Currently, we use file which are easy to use and share. However, this approach is only sensible as long as the amount of interactions with the data and especiallu update operations is low. In addition, if you wanted to update only one field it would mean a complete loading of the file and then exchanging of the value based on its dictionary key. This might be ok for one operation, but absolutely inefficient for large numbers of edits.

Databases are great tools to persist data an efficient and extensible way. There are many types of database systems and approaches to modeling data for them. Which one is right for FHIR?



### 3.1. Document vs. Relational Databases



### 3.2. Postsgres BJSON as middleground


1. Installing Postgres

Simple solution running nix means adding postgresql to pkgs.mkShell:


```{python}

{ pkgs ? import <nixpkgs> {} }:

let
  pythonEnv = with pkgs.python310Packages; [
    # Data Science Basics
    ipython
    jupyter
    fastapi
    uvicorn

    (
    buildPythonPackage rec {
      pname = "fhir.resources";
      version = "6.5.0";
      src = fetchPypi {
        inherit pname version;
        sha256 = "1d02ff2547e5b6323543c8ce9916e0c9e5536847b3b2171acb1f51a86efba16e";
      };
      doCheck = false;
      propagatedBuildInputs = [
          pytest-runner
          pydantic
      ];
    }
    )

  ];

in pkgs.mkShell {
  buildInputs = with pkgs; [
    pythonEnv
    postgresql
    # keep this line if you use bash
    pkgs.bashInteractive
  ];
}

```


Using Docker means using a docker template. Just make sure to store a dump of the db locally before initial push.



2. Setting up Postgres



```{python}

# Create a database with the data stored in the current directory
initdb -D .tmp/db

# Start PostgreSQL running as the current user
# and with the Unix socket in the current directory
pg_ctl -D .tmp/db -l logfile -o "--unix_socket_directories='$PWD'" start

# Create a database
createdb -h $PWD fohispital


```




3. Using Postgres with Python

Let's do it directly using ipython to see what we are getting :-)

```{python}
from sqlalchemy import create_engine

import os

engine = create_engine(
    f"postgresql://:@/fohispital?host={os.getcwd()}")

engine.table_names()


```

This should connect to a Postgres Instance on a local socket and return an empty list ('[]') as we did not create any tables so far. So, let's add a fake table to throw away later just to get some feel of using postgres in Python.


```{python}
# Import all Dependencies

import sqlalchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy import Table
from sqlalchemy.orm import declarative_base


# Define the Table as a Class
Base = declarative_base

class MyTable(Base):
   __tablename__ = 'myTable'
   time_id = Column(String(), primary_key=True)
   customer_id = Column(String())
   inventory_id = Column(String())

   def toJSON(self):
       json = {
          "time_id":self.alert_id,
          "customer_id":self.customer_id,
          "inventory_id":self.inventory_id,
      }
      return json

# Create the table
Base.metadata.create_all(engine)

# List tables in our DB
engine.table_names()

```

This will create the following output in ipython or the console:

```

$> ['MyTable']

```

4. Using Postgres with FASTapi

Currently we are create a separate model for our Database Table. Ideally this exactly matches the json data we output via our API


5. Using Postgress with SQLmodel and FHIR.resources in FASTapi




### 3.3 CRUD operations in Fastapi with SQLMODEL and Postgres BJSON

Implementation of Patient Resource in Fastapi and Postgresql

https://amercader.net/blog/beware-of-json-fields-in-sqlalchemy/

Creating the model for our object

```{python}

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer
from sqlalchemy_json import mutable_json_type
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Resource(Base):

    __tablename__ = 'document'

    id = Column(Integer, primary_key=True)
    config = Column(mutable_json_type(dbtype=JSONB, nested=True))

Base.metadata.create_all(engine)

```

Create a new session to query our newly created and populated database.

```{python}

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind = engine)
session = Session()

```


Loading and Querying a JSONB Record in our table.

```{python}

import json

with open('app/routers/fhir_resources/patient-example-a.canonical.json') as f:
    fhir_json = json.load(f)

session.add(Resource(config=fhir_json)) # Add a new Insert Object
session.commit() # Write to DB

```

Query the database for records and select only the name from our JSONB records

```{python}
names = session.query(Resource.config['name']).all()

for name in names:
    name  = name._data[0]
    print(f"{name[0]['given'][0]} {name[0]['family']}")

```

Output:

```{bash}

Pieter van de Heuvel
Duck Donald

```


Updating a record:
- https://www.arundhaj.com/blog/sqlalchemy-expression-partial-json-update.html


### 3.4 Using FHIR.resources to populate the database

Required Reading:
- https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8050750/
- https://github.com/juliangruendner/criteria-based-selection-fhir

Case Study:
- https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6776354/
- https://github.com/dominikb1888/ketos_develop

Optional Tutorials:
- https://roman.pt/posts/pydantic-in-sqlalchemy-fields/
- https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSONB
- https://medium.com/fhirbase-dojo/should-you-use-fhir-resources-as-your-storage-format-62dd25977a85


Partial Updates of pydantic models:
- https://medium.com/@david.danier/how-to-handle-patch-requests-with-fastapi-c9a47ac51f04
- PATCH on FHIR: https://fhirblog.com/2019/08/13/updating-a-resource-using-patch/
-


### 3.5 Connect to FASTapi and Dockerizing the database

- Single Page Example: https://github.com/tiangolo/fastapi/issues/211

In order to push this environment to a cloud service at some point we will create a Docker for Postgres and Docker Coompose file which orchstrates our container. At the moment this is only the database and our backend, later we will add a frontend and maybe more services like a load balancer or a cache.


### Synthesis
