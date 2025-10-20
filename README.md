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



# Design Decisions
1. Database
    I picked postgreSQL with pgvector extension. Reason being I'm familiar with postgres and it's a battle tested database

2. Embedding model
    I used SentenceTransformer("multi-qa-MiniLM-L6-cos-v1"), it was the suggested model for semantic search.
    OpenAI or Ollama API would probably give better results because of bigger model with better vocabulary, but to keep things simple for this project, I decided to use an smaller open source model.

3. DB Design
    I have create a patients table and notes table, with notes table referencing patients.patient_id as foreign key to not allow notes for patients which don't exist, with `ONCASCADE DELETE` to avoid having redundant entries in db.
    Have created a `ivfflat` Index on notes.embedding, for faster searching.

4. Architecture patterns used
    It's a simple client server application, to keep things simple. Tradeoff being, because we are calculating embedding on each note creation/updation/search, those operations are slower.

# Project Metadata

1. Estimated time spent on the task
    About 6 hours. 
    The MVP part of searching notes via embeddings was done in 2 hours, it was quite simple.
    I spent about 1-2 hour for setting up unit tests, but async sqlalchemy give me headache.
    Then I spend remaining time to dockerize whole project to start with just one command, and handing some edge cases.

2. Bonus features
    Docker Containerization, with Persistent Production Database. I have also added some seed values to database, can be removed easily if wanted. Couldn't add unit tests because of one issue.

3. Known limitations
    There might be some edge cases missing in CRUD for patients and notes.
    I haven't tested note search on large scale data, not sure of it's performance.
    