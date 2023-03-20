# FOHIspital v0.0

## Installation

- Install a recent version of Python and pip on your local system (3.8 or later)

Install FASTapi and uvicorn by running. (Be aware that this is a global install. We will look at better methods next time):

```
pip install fastapi uvicorn[standard]
```

Run the server by typing:

```
uvicorn main:app --reload
```

This will start a uvicorn server that looks for a FASTapi object called 'app' in the file main.py in the same directory.

You should see a list of 3 FHIR/JSON encoded patient objects as a list of dictionaries in your browser after opening the URL that the prompt will show.


## Takeaways

1. What did we achieve?

- A very simple way to load and display FHIR json on the web


2. What can do better?

- Store the data for simultaneous access (aka. database -> Postgres)
- Validate the imported JSON data so we can make sure it is actually FHIR

