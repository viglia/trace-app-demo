## Setup the environment

Required **Python Version**: >= `3.7.3`

1. Clone the repository
2. `cd` into the repository and create a new virtuan environment with `python3 -m venv env`
3. activate the `env` with `source env/bin/activate`
4. install the requirements with `pip install -r requirements.txt`
5. `cd` into the root directory of the project with `cd trace_project`
6. run `python manage.py migrate`

## Run the app
From the root folder (*trace_project*) run `python manage.py runserver`

## Run the tests

From the root folder (*trace_project*) run `python -m pytest`

#### Run only the unit tests
From the root folder (*trace_project*) run `python -m pytest -m unit`

#### Run only the integration tests
From the root folder (*trace_project*) run `python -m pytest -m integration`

## How to manually interact with the app

#### Sending Trace messages

The endpoint for sending the trace message is: `/ws/trace/<trace_id:int>`
Where the trace id is an integer that needs to be unique for each new *Trace*.

There are different ways to interact with the app. The quickest one would probably be just open a console in the browser and use the native support with Javascript.

If you want to use *Python* you can use the `websocket-client` library.

Here a quick example:

first install the package
`pip install websocket_client`

```
from websocket import create_connection
import json

ws = create_connection("ws://localhost:8000/ws/trace/1")

message = [
    {
        "timestamp": 1569972082,
        "type": "TRACE_START",
        "group_id": "e6fa79ca-d142-4046-a134-5134f16a0b5e"
    },
    {
        "timestamp": 1569972090,
        "type": "SPAN_END",
        "group_id": "dbed4e4e-8ec6-40dd-ae35-b118abf1ab69"
    },
    {
        "timestamp": 1569972084,
        "type": "SPAN_START",
        "group_id": "1ff14a38-55ff-431a-a6ca-a86c82d8ed46",
        "name": "movies_network_load"
    },
    {
        "timestamp": 1569972090,
        "type": "SPAN_END",
        "group_id": "1ff14a38-55ff-431a-a6ca-a86c82d8ed46"
    },
    {
        "timestamp": 1569972083,
        "type": "EVENT",
        "name": "movies_cache_content_rendered"
    },
    {
        "timestamp": 1569972082,
        "type": "SPAN_START",
        "group_id": "dbed4e4e-8ec6-40dd-ae35-b118abf1ab69",
        "name": "movies_load"
    },  
    {
        "timestamp": 1569972090,
        "type": "TRACE_END",
        "group_id": "e6fa79ca-d142-4046-a134-5134f16a0b5e"
    }
]

ws.send(json.dumps(message))
msg =  ws.recv()
print(msg)
```

#### Retrieving a Trace

The endpoint for retrieving (GET) or deleting (DELETE) a trace is
`/api/trace/{trace_id:int}/`

You can use any client you want to interact with it but since the project is currently in DEBUG mode you can just take advantage of the *django_rest* browsable api.