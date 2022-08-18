# FastAPI Simple To-Do List Mock

A simple mock To-Do List API using FastAPI and Mongita.

![todo-list-api-swagger-screenshot](assets/images/todo-list-api-swagger-screenshot.png)

## Table of Contents

- [About](#about)
  - [Built With](#built-with)
- [Getting Started](#getting-started)
  - [Installation](#installation)
- [Usage](#usage)
  - [Run the Server](#run-the-server)
  - [Interact From the Browser (Swagger UI)](#interact-from-the-browser-swagger-ui)
  - [Interact From the Command Line (HTTPie)](#interact-from-the-command-line-httpie)
- [Acknowledgements](#acknowledgements)
- [Licence](#licence)

## About

A simple mock To-Do List API using FastAPI and Mongita, with basic CRUD operations allowing you to create, update and delete tasks.

### Built With

- [Python](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Mongita](https://github.com/scottrogowski/mongita)

## Getting Started

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/TomJGooding/fastapi-simple-todo-mock.git
   ```
2. Install the requirements. It is recommended to first [create a virtual environment](https://packaging.python.org/en/latest/tutorials/installing-packages/#creating-virtual-environments).
   ```sh
   python3 -m pip install -r requirements.txt
   ```

## Usage

### Run the Server

Run the [Uvicorn](https://www.uvicorn.org/) server with:

```sh
uvicorn main:app
```

### Interact From the Browser (Swagger UI)

[Swagger UI](https://github.com/swagger-api/swagger-ui) is a browser-based tool for interacting with REST APIs, and FastAPI creates this user interface for the API automatically.

Open your browser at [http://localhost:8000/docs](http://localhost:8000/docs)

For example, to create a new task:

1. Expand the **POST /todos Create Task** item.
2. Click the **Try it out** button, which will allow you to fill the parameters.
3. Then click the **Execute** button. The user interface will communicate with your API, send the parameters, get the results and show them on the screen.

### Interact From the Command Line (HTTPie)

[HTTPie](https://httpie.io/docs/cli) is a command-line HTTP client for interacting with APIs & HTTP servers.

You will need to have the FastAPI server running in the background.

For example, create a new task with:

```sh
http POST localhost:8000/todos id=1 title="Water the plants" complete=False
```

## Acknowledgements

- The [Python REST APIs With FastAPI](https://realpython.com/courses/python-rest-apis-with-fastapi/) video course by Real Python for getting started with FastAPI

## Licence

Licensed under the [GNU General Public License v3.0](LICENSE).

