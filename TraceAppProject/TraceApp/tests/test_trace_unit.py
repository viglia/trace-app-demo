from pytest import mark

from TraceApp.models import Span, Event


@mark.unit
class TraceTests:

    def test_span_included(self):
        s1 = Span(start=2, end=5)
        s2 = Span(start=2, end=5)
        s3 = Span(start=3, end=4)

        # edge case exact inclusion
        assert s2.included_in_span(s1) == True

        # normal inclusion
        assert s3.included_in_span(s1)

    def test_span_not_included(self):
        s1 = Span(start=2, end=5)
        s2 = Span(start=2, end=6)
        s3 = Span(start=1, end=2)

        assert s2.included_in_span(s1) is False
        assert s3.included_in_span(s1) is False

    def test_event_included(self):
        s1 = Span(start=2, end=5)
        e1 = Event("event_1", 2)
        e2 = Event("event_2", 5)
        e3 = Event("event_3", 3)

        assert e1.included_in_span(s1) is True
        assert e2.included_in_span(s1) is True
        assert e3.included_in_span(s1) is True

    def test_event_not_included(self):
        s1 = Span(start=2, end=5)
        e1 = Event("event_1", 6)

        assert e1.included_in_span(s1) is False
