# Requirements to run this with docker
1. Internet connection
2. Docker and Docker Compose

Everything should work without anything else. Docker compose should handle most of it

## Steps to start

Just run 

    `docker compose up`

and that should be enough


## Note
By default, the setup is made in this way that it will drop and recreate the database at each restart of docker container, and seed it.

To stop this, open deploy/run-server.sh and remove the invocation of create_db and seed_db 


# Requirements to run this on local machine
1. Internet connection
2. UV with python 3.13
3. PostgreSQL v18

Steps to start:
1. clone the project and run

    `uv sync`

2. set env variables in .env.docker.rc  and source them.
On mac/linux

   `source .env.docker.rc`


3. Run following commands to setup and seed db

    `python3 create_db.py`

    `python3 seed_db.py`


4. Then start the server with

    `uv dev src/app`



By default, server listens on port 8000.

# Usage:

there is a postman collection provided. named `hospital-serch.json`
The auth for this project is just one hardcoded API_KEY in headers, set via ENV variables, default value is 1234

Here are example curl requests, assuming db is seeded.


1. for creating patient

    `curl --request POST \
    --url http://127.0.0.1:8000/patients \
    --header 'content-type: application/json' \
    --header 'x-api-key: 1234' \
    --data '{
    "name": "manish",
    "age": 24
    }'`

2. for creating notes

    `curl --request POST \
    --url http://127.0.0.1:8000/add_note \
    --header 'content-type: application/json' \
    --header 'x-api-key: 1234' \
    --data '{
    "text": "patient has cold and fever and cough",
    "patient_id": 2
    }'`

3. for searching notes

    curl --request GET \
    --url 'http://127.0.0.1:8000/search_notes/?search_text=diabetes' \
    --header 'x-api-key: 1234'




