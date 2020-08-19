from __future__ import annotations
from django.db import models
from typing import List, Union


# Create your models here.
class Span():
    def __init__(self, name: str = None, start: int = None, end: int = None):
        self.name: str = name
        self.start: int = start
        self.end: int = end
        self.type: str = "SPAN"
        self.children: List[Span] = []

    def included_in_span(self, span: Span) -> bool:
        return self.start >= span.start and self.end <= span.end

    def __repr__(self):
        return f"({self.name} -> {self.start},{self.end})"


class Event():
    def __init__(self, name: str, timestamp: int = None):
        self.name: str = name
        self.timestamp: int = timestamp
        self.type: str = "EVENT"

    def included_in_span(self, span: Span) -> bool:
        return self.timestamp >= span.start and self.timestamp <= span.end

    @property
    def start(self):
        return self.timestamp

    def __repr__(self):
        return f"({self.name} -> {self.timestamp})"


class TraceUtility():

    def __init__(self):
        self.start: int = None
        self.end: int = None
        self.type: str = "TRACE"
        # initially add a 'root span' for utility
        self.children: List[Union[Span, Event]] = [Span(
            "root_span", float('-inf'), float('inf'))]
        self.__map = {}
        self.__group_id = None

    def process_message(self, message: List):
        for obj in message:
            obj_type = obj["type"]
            obj_timestamp = obj["timestamp"]

            if obj_type.startswith("SPAN"):
                group_id = obj["group_id"]

                if group_id not in self.__map:
                    self.__map[group_id] = Span()
                    self.__map[group_id].type = "SPAN"

                if obj_type == "SPAN_START":
                    self.__map[group_id].start = obj_timestamp
                    self.__map[group_id].name = obj["name"]

                else:
                    self.__map[group_id].end = obj_timestamp

            if obj_type.startswith("TRACE"):

                if obj_type == "TRACE_START":
                    self.__group_id = obj["group_id"]
                    self.start = obj_timestamp
                else:
                    if self.__group_id == obj["group_id"]:
                        self.end = obj_timestamp
                    self.children = self.children + [v for k, v in
                                                     self.__map.items()]

            if obj_type == "EVENT":
                event = Event(name=obj["name"], timestamp=obj["timestamp"])
                self.children.append(event)

    def transform_data(self):
        if not self.__check_integrity():
            raise Exception("Error: the trace is not consistent! " +
                            "Some events might be incomplete or out of trace.")
        self.children.sort(key=lambda s: s.start)

        for i in reversed(range(len(self.children))):
            for j in reversed(range(i)):
                if (isinstance(self.children[j], Span) and
                   self.children[i].included_in_span(self.children[j])):

                    self.children[j].children.insert(0, self.children[i])
                    break

        if self.children[0].children != []:
            self.children = self.children[0].children

    def __check_integrity(self):
        # the integrity of the data is False when:
        # 1. an event is incomplete (either start or end are missing)
        # 2. the event occurred in a time outside of a trace time span
        if self.start is None or self.end is None:
            return False
        # here we skip the first one as it's a fake span created for utility
        for obj in self.children[1:]:
            if not isinstance(obj, Event):
                if obj.start is None or obj.end is None:
                    return False
                if not self.__inside_trace(obj.start, obj.end):
                    return False
            else:
                if not self.__inside_trace(obj.start):
                    return False
        return True

    def __inside_trace(self, start: int, end: int = None):
        if end is None:
            end = start
        return start >= self.start and end <= self.end
