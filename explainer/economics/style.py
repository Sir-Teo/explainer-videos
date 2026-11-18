"""The colours of *Economics, Built*: one meaning per colour, for the whole series (videos/economics/SYLLABUS.md,
section 3).

    from explainer.economics import E
    curve.set_color(E.DEMAND)      # demand is blue in every part; supply is amber

Data are white, Agora (the model) is orange, and the Island's planted truth is a dashed green line, so a glance tells
data from model from truth.  The five sectors of the Tableau keep one colour each from the first part to the last
balance sheet.  Parts add names for their own objects in ``common.py``, built from these where the meaning is the
same.
"""

from types import SimpleNamespace

from manim import GREY_A, GREY_B, GREY_C, GREY_D, WHITE

E = SimpleNamespace(
    # who produced the numbers
    DATA=WHITE,  # data: the Data Room, transcribed tables
    AGORA="#FF9F5A",  # Agora, the model economy: its predictions and simulations
    TRUTH="#7BD88F",  # the Island's planted truth (drawn dashed)
    ISLAND="#8FA8D9",  # the Island: simulated people and data (always tagged)
    # a market
    DEMAND="#5DADEC",  # demand, buyers, willingness to pay
    SUPPLY="#F2B84B",  # supply, sellers, cost
    PRICE="#F7F3E3",  # a price, a transaction
    CS="#5DADEC",  # consumer surplus (filled, faint)
    PS="#F2B84B",  # producer surplus
    DWL="#F26D6D",  # deadweight loss, a loss
    # the five sectors of the Tableau
    HOUSEHOLDS="#4FD1C5",
    FIRMS="#F2B84B",
    BANKS="#B48EF0",
    GOVERNMENT="#F26D6D",
    WORLD="#8FA8D9",
    # goods on the Island
    FISH="#6FB7E8",
    COCONUT="#C89B6D",
    # evidence
    TREAT="#FF7F6E",  # a treated unit (filled)
    CTRL="#7EC8F5",  # a control (hollow)
    PRED="#C9A0FF",  # a prediction, a forecast
    MISS="#F25F5C",  # its miss, an error
    GAIN="#7BD88F",  # a gain
    # bookkeeping
    ACCENT="#F6C453",  # the series' accent: chapter cards, the lit timeline, Play it
    SOURCE="#E3B98A",  # a data or publication tag
    OUGHT="#E9A3C9",  # the normative step (the is/ought card)
    GRID=GREY_D,
    DIM=GREY_C,
    TEXT_DIM=GREY_A,
    MUTED=GREY_B,
)

# The Dials' statuses (explainer.economics.dials.STATUSES)
DIAL_STATUS = {
    "settled within a range": "#5BD18B",
    "depends on the setting": "#F2C14E",
    "contested": "#F28C5C",
    "not identified": GREY_B,
}

# The Dials' designs: a tick on a dial card is coloured by how the estimate was identified
DESIGN_COLOR = {
    "RCT": "#7BD88F",
    "IV": "#5DADEC",
    "RD": "#4FD1C5",
    "DiD": "#B48EF0",
    "event study": "#C9A0FF",
    "structural": "#FF9F5A",
    "calibration": "#F2B84B",
    "survey": GREY_A,
    "narrative": "#E9A3C9",
    "lab": "#F7D154",
}
