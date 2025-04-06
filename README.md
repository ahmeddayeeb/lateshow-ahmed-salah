# Late Show API

This is a Flask API for managing episodes, guests, and appearances on a late show.

## Setup

1.  Clone the repository.
2.  Create a virtual environment: `python3 -m venv venv`
3.  Activate the virtual environment: `source venv/bin/activate`
4.  Install the dependencies: `pip install flask flask-sqlalchemy flask-migrate`
5.  Initialize the database: `flask db init`
6.  Run the migrations: `flask db migrate -m "Create tables"`
7.  Apply the migrations: `flask db upgrade`
8.  Seed the database: `python seed.py`

## Running the application

1.  Run the application: `python app.py`

## Testing the application

1.  Run the application: `python app.py`
2.  Use a tool like Postman to send requests to the following endpoints:
    *   `GET /episodes`: Returns a list of all episodes in the format:
        ```json
        [
          {
            "id": 1,
            "date": "1/11/99",
            "number": 1
          },
          {
            "id": 2,
            "date": "1/12/99",
            "number": 2
          }
        ]
        ```
    *   `GET /episodes/:id`: Returns a specific episode in the format:
        ```json
        {
          "id": 1,
          "date": "1/11/99",
          "number": 1,
          "appearances": [
            {
              "episode_id": 1,
              "guest": {
                "id": 1,
                "name": "Michael J. Fox",
                "occupation": "actor"
              },
              "guest_id": 1,
              "id": 1,
              "rating": 4
            }
          ]
        }
        ```
    *   `GET /guests`: Returns a list of all guests in the format:
        ```json
        [
          {
            "id": 1,
            "name": "Michael J. Fox",
            "occupation": "actor"
          },
          {
            "id": 2,
            "name": "Sandra Bernhard",
            "occupation": "Comedian"
          },
          {
            "id": 3,
            "name": "Tracey Ullman",
            "occupation": "television actress"
          }
        ]
        ```
    *   `POST /appearances`: Creates a new appearance. Send a request with the following data:
        ```json
        {
          "rating": 5,
          "episode_id": 1,
          "guest_id": 1
        }
        ```
        The response should be in the format:
        ```json
        {
          "id": 162,
          "rating": 5,
          "guest_id": 3,
          "episode_id": 2,
          "episode": {
            "date": "1/12/99",
            "id": 2,
            "number": 2
          },
          "guest": {
            "id": 3,
            "name": "Tracey Ullman",
            "occupation": "television actress"
          }
        }
        ```
2.  Verify that the responses are in the correct format and contain the expected data.
