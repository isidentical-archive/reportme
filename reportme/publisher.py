from contextlib import contextmanager
from dataclasses import dataclass
from io import StringIO
from textwrap import wrap


class ReportBuffer:
    def __init__(self, width=160):
        self.width = width
        self.buf = StringIO()

    def add_line(self, content=None):
        if content is not None:
            self.buf.write("\n".join(wrap(content, self.width)))
        self.buf.write("\n")

    @contextmanager
    def area(self, padder="="):
        self.add_line(padder * (self.width))
        yield
        self.add_line(padder * (self.width))

    def render(self, report):
        with self.area():
            self.add_line(f"{f'{report.name} (v{report.version})':^{self.width}}")
            self.add_line()
            self.add_line(f"Date: {report.date}")
            self.add_line(f"Description: {report.description}")
            for category in report.categories:
                with self.area(padder="-"):
                    self.add_line(f"{category.name:^{self.width}}")

    def print(self):
        print(self.buf.getvalue())
