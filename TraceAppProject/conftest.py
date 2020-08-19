from pytest import fixture


@fixture(scope='session')
def complete_trace():
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
    yield message
