from channels.db import database_sync_to_async
import json
import pytest
from pytest import mark
from channels.testing import WebsocketCommunicator

from trace_project.routing import application
from trace.models import Trace


@mark.integration
class TraceIntegrationTests:

    @database_sync_to_async
    def trace_exists(self, trace_id):
        return Trace.objects.filter(id=trace_id).exists()

    @database_sync_to_async
    def delete_trace(self, trace_id):
        Trace.objects.get(id=trace_id).delete()

    @pytest.mark.asyncio
    async def test_empty_trace_id(self):
        communicator = WebsocketCommunicator(application, "ws/trace/1az")

        with pytest.raises(Exception) as _:
            await communicator.connect()

    @pytest.mark.asyncio
    @pytest.mark.django_db()
    async def test_insert_one_message_trace(self, complete_trace):
        trace_id = 1
        communicator = WebsocketCommunicator(
            application, f"ws/trace/{trace_id}")
        connected, subprotocol = await communicator.connect()
        assert connected is True
        await communicator.send_to(text_data=json.dumps(complete_trace))

        await communicator.receive_from()

        assert await self.trace_exists(trace_id)

    @pytest.mark.asyncio
    @pytest.mark.django_db()
    async def test_insert_two_messages_trace(self, complete_trace):
        trace_id = 2
        communicator = WebsocketCommunicator(
            application, f"ws/trace/{trace_id}")
        connected, subprotocol = await communicator.connect()
        assert connected is True
        part_1 = complete_trace[:len(complete_trace)//2]
        part_2 = complete_trace[len(complete_trace)//2:]
        await communicator.send_to(text_data=json.dumps(part_1))
        await communicator.send_to(text_data=json.dumps(part_2))

        await communicator.receive_from()

        assert await self.trace_exists(trace_id)

    @pytest.mark.asyncio
    @pytest.mark.django_db()
    async def test_incomplete_message_trace(self, complete_trace):
        trace_id = 3
        communicator = WebsocketCommunicator(
            application, f"ws/trace/{trace_id}")
        connected, subprotocol = await communicator.connect()
        assert connected is True

        part_1 = complete_trace[:len(complete_trace)//2]
        await communicator.send_to(text_data=json.dumps(part_1))

        assert await communicator.receive_nothing()

        await communicator.disconnect()

        assert await self.trace_exists(trace_id) is False

    @pytest.mark.django_db()
    def test_retrieve_trace_rest_endpoint(self, client):
        trace_id = 4
        Trace.objects.create(id=trace_id)
        response = client.get(f"/api/trace/{trace_id}/")
        assert response.status_code == 200

    @pytest.mark.django_db()
    def test_fail_retrieve_trace_rest_endpoint(self, client):
        trace_id = 5  # unexistent trace
        response = client.get(f"/api/trace/{trace_id}/")
        assert response.status_code == 404
