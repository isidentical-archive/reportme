from contextlib import AbstractContextManager, contextmanager
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from functools import partial
from typing import List, Optional


@dataclass
class ReqType:
    _type: str
    requirement: Optional[str] = None
    message: Optional[str] = None

    def __str__(self):
        return f"{self.requirement}: {self.message}"

    def __getattr__(self, requirement):
        if not requirement.startswith("__"):
            return partial(self.__class__, self._type, requirement)
        raise AttributeError(requirement)

@dataclass
class Requirement:
    file: str
    line: int
    report: ReqType


@dataclass
class Node:
    name: str
    requirements: List[Requirement] = field(default_factory=list)

    def add_requirement(self, file, line, report):
        req = Requirement(file, line, report)
        self.requirements.append(req)
        return req


@dataclass
class Category:
    name: str
    nodes: List[Node] = field(default_factory=list)

    @contextmanager
    def add_node(self, name):
        node = Node(name)
        self.nodes.append(node)
        yield node


@dataclass
class Report(AbstractContextManager):
    name: Optional[str] = None
    version: Optional[str] = None
    description: Optional[str] = None
    date: datetime = datetime.now()

    categories: List[Category] = field(default_factory=list)

    @contextmanager
    def add_category(self, name):
        category = Category(name)
        self.categories.append(category)
        yield category

    def __exit__(self, *exc_info):
        return None
