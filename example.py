from reportme.publisher import ReportBuffer
from reportme.reporter import Report
from reportme.reports import Approach, Reimplement, Style

report = Report(
    name="Demo",
    version="0.1.0",
    description=(
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        "Cras quis justo risus. Phasellus velit orci, congue sed."
        "Vivamus sed enim mollis, pulvinar quam quis, blandit ta."
    ),
)

pythonicity = report.add_category(name="Pythonicity")

pep8 = pythonicity.add_node("PEP8")
pep8.add_requirement("xxx.py", 32, Style.E331("BLA BLA"))
pep8.add_requirement("yyy.py", 321, Style.W551("TLA TLA"))
pep8.add_requirement("zzz.py", 543, Style.Z771("TLA TLA"))

approachs = pythonicity.add_node("Approachs")
approachs.add_requirement("aaa.py", 432, Approach.WITH_USE("TLA TLA"))
approachs.add_requirement("bbb.py", 2432, Approach.STLIB_USE("ZLA ZLA"))

optimizations = report.add_category(name="Optimizations")

reimplements = optimizations.add_node("Reimplements")
reimplements.add_requirement("zzz.py", 322, Reimplement.STDLIB_FUNC("ZZZ, TTT"))
reimplements.add_requirement("aaa.py", 323, Reimplement.BUILTIN_FUNC("TAD ZZZ"))

buf = ReportBuffer()
buf.render(report)
buf.print()
