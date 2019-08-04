from contextlib import contextmanager
from dataclasses import asdict, dataclass
from io import StringIO
from itertools import repeat
from textwrap import wrap

CELL_WIDTHS = {"file": 40, "line": 10, "report": 100}


class ReportBuffer:
    def __init__(self, width=160):
        self.width = width
        self.buf = StringIO()

    def add_line(self, content=None):
        if content is not None:
            self.buf.write("\n".join(wrap(content, self.width)))
        self.buf.write("\n")

    def add_report(self, report):
        self._nodes.append(asdict(report))

    @contextmanager
    def add_table(self, columns):
        try:
            self._nodes = []
            yield
        finally:
            self.add_line()

            template = "|" + " {} |" * len(columns)

            padded_headers = [column.ljust(CELL_WIDTHS[column]) for column in columns]
            header = template.format(*padded_headers)
            sep = "|" + "-" * (len(header) - 2) + "|"

            rows = []
            for node in self._nodes:
                _, requirement, message = node["report"].values()
                if message:
                    requirement += f" {message}"
                node["report"] = requirement
                fields = [
                    str(node[column]).ljust(CELL_WIDTHS[column]) for column in columns
                ]
                rows.append(template.format(*fields))

            output = [sep, header, sep, *rows, sep]
            for line in output:
                self.add_line(line)
            self.add_line()

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
                with self.area(padder=" "):
                    self.add_line(f"{category.name:^{self.width}}")
                    self.add_line()
                    for segment, node in enumerate(category.nodes):
                        self.add_line(f"Segment {segment}: {node.name}")
                        with self.add_table(["file", "line", "report"]):
                            for report in node.requirements:
                                self.add_report(report)

    def print(self):
        print(self.buf.getvalue())
