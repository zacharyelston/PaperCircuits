"""Tags for page text that waits on an open decision in docs/page-standard.md.

Keep every tagged choice in a constant at the top of its sheet module, so settling a
decision is a one-line change per page.
"""

_TAG = '<font color="#b87333"><b>[{}]</b></font>'

T0 = _TAG.format("T0")    # waits on the T0 contact tests
POWER = _TAG.format("P")  # waits on the power decision, standard §7

TAG_NOTE = (
    f"{T0} and {POWER} mark choices that may change: {T0} after the contact tests, "
    f"{POWER} once the power supply is settled."
)
HEADER_STATUS = "Draft: tagged steps may change"

HOLE_STEP = f"Punch the holes and set eyelets in H2 and H3. {T0}"
