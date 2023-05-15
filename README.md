# Instashare "description"

## The project

The project was built with Connexion framework, which is a flask-based framework that allows describing an API using OpenAPI (or swagger) specification.

### Swagger file

into swagger folder from root folder of code, you can find the swagger file, which is the specification of the API. This file is used by Connexion to build the API. Here you can find the definition of the endpoints, the parameters, the responses, and the models.

### Bussiness logic

The exercise  is simple, register users, and upload files. So we have the followings endpoints:

- /users/register: POST
- /users/login: POST
- /upload_files: POST
- /files: GET (not implemented)

Once a user is registered, the user can log in and upload files. The files are stored in the designed storage (Google Storage in this case), and the information of the files is stored in a database (PostgreSQL). The files are stored in a folder with the name (id of the user) of its owner. The file is stored and compressed by the requirement of the exercise. If this was not a requirement the main logic to upload a file would be:

- The client tells the API need to upload a file with all its parameters.
- The API generates a pre-signed URL to upload the file to the storage.
- The client uploads the file to the storage using the pre-signed URL.

>Note: The author removed the steps of explanation to keep the document short.

This resolve the problem of API to process the file, and the problem of the client to upload the file. The API only needs to store the information of the file in the database. The client can upload the file directly to the storage. This is a very common solution to upload files to the cloud.

## Async upload

Generally, Python allows async requests using libraries such as **asyncio**, **aiohttp**, or **request-async** among others. But has a significant limitation known as Global Interpreter lock (GIL, by English acronyms), this limitation does not permit two (or more) threads access to the same object at the same time. Other technologies like NodeJS for example, are built-in in C++ and based on the v8 Engine of Google, use a model based on **event loops**, and manage efficiently the async operations without blocking the main thread. Also, NodeJS can use **workers** to execute parallel code and communicate it by throwing messages. To all of this, NodeJS implement an “artifact” called Promise, which is an elegant and powerful way to evade the called callback hell this happens when many callback functions are nested. In this context, an attractive solution to solve the async requests in Python is the use of **workers** (imitating the functionalities of NodeJS), many libraries are implemented to do that, the author chose Celery. Celery needs a message broker or a message manager to send and receive messages between tasks to the **workers**, the author chose Redis. This specific code has it own container to be deployed.

## Tests

The test are implemented using pytest, and hypotesis to generate random data to test the endpoints. The tests are implemented in the folder tests, and the test files are named with the prefix test_.

## Validation

The author tried to validate all levels of API. For example in the swagger file, the parameters are validated using a kind of JSON -schema of this kind of file, in the code using JSON-schema one more time, and in the definition of models using sqlalchemy. Much of the data was validated using Regular Expressions.

## Github Actions

### Build Workflow

The build workflow is configured to build and push into his repository the docker image of the application. The workflow is triggered when a push is made into the master, develop or tag. The nomenclature for tagging the container is ```<branch>:<short hash of commit>```The build workflow is configured to build and push into his repository the docker image of the application. The workflow is triggered when a push is made into the master, develop or tag. The nomenclature for tagging the container is ```instashare:<branch>-<short hash of commit>```, but if the container is master the configuration will push two tags, the first is ```instashare:<short hash of commit>``` (without branch) and ```instashare:latest``` (to keep continuously updated the last commit on latest tag). The same logic is fallowed with the worker container.

### Python test workflow

The test workflow prepares code to be tested, the only added here is the use of Ruff, which is a very fast and comprehensive static code analysis tool for Python written in Rust (is faster than other tools).

### GOOGLE CREDENTIALS

The author used Google Storage, so they created a service account in Google Cloud, and downloaded the credentials in a JSON file. This file is used by the application to connect to Google Storage. It is a bad practice to store this file in the repository, so the author used Github Secrets to store the file for test. To check the corect work of the API the author can share with the reviewer his credentials, or get access to his Google Cloud account.

### Docker-compose

The author used docker-compose to deploy the application in a local environment. The docker-compose file is in the root folder of the code. The docker-compose file is configured to deploy the application and the worker. The code of worker is in a subfolder ot project, and are specified in docker-compose file.