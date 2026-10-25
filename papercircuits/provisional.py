"""Tags for page text that waits on an open decision in docs/page-standard.md.

Keep every tagged choice in a constant at the top of its sheet module, so settling a
decision is a one-line change per page.
"""

_TAG = '<font color="#b87333"><b>[{}]</b></font>'

T0 = _TAG.format("T0")    # waits on the T0 contact tests
POWER = _TAG.format("P")  # waits on the power decision, standard §7
T1 = _TAG.format("T1")    # waits on the T1 pencil tests
T3 = _TAG.format("T3")    # waits on the first T3 copper oxide wafer

TAG_NOTE = (
    f"{T0} and {POWER} mark choices that may change: {T0} after the contact tests, "
    f"{POWER} once the power supply is settled."
)
TAG_NOTE_WITH_T1 = (
    f"{T0}, {T1} and {POWER} mark choices that may change: {T0} after the contact tests, "
    f"{T1} after the pencil tests, {POWER} once the power supply is settled."
)
HEADER_STATUS = "Draft: tagged steps may change"

