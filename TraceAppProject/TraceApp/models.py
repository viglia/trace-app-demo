from __future__ import annotations
from django.db import models
from typing import List


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
