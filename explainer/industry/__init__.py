"""*Industry, Built*: shared code for the series (videos/industry/README.md, videos/industry/SYLLABUS.md).

    from explainer.industry.kit import *        # scenes: text, cards, palette, money formatting
    from explainer.industry import viz          # the instruments: the phone, the Dollar, the Map, ...
    from explainer.industry.register import get # every figure a film shows, with its source and date
    from explainer.industry.works import chain  # the model companies' arithmetic (numpy only)

The register and the works are importable without manim (labs and tests use them).
"""

from __future__ import annotations

SERIES_EN = "Industry, Built"
SERIES_ZH = "产业，从零搭建"

# (label, name, first part, last part), as in the README's "The acts".
ACTS = [
    ("I", "Reading an Industry", 1, 7),
    ("II", "Out of the Ground", 8, 14),
    ("III", "Making", 15, 23),
    ("IV", "Building", 24, 26),
    ("V", "Moving", 27, 30),
    ("VI", "Selling and Serving", 31, 35),
    ("VII", "Information", 36, 42),
    ("VIII", "Money", 43, 49),
    ("IX", "People", 50, 55),
    ("X", "Systems", 56, 61),
    ("XI", "The Job", 62, 64),
]

PARTS = {
    1: "Where the Money Goes", 2: "The Economy on One Page", 3: "The Accounts", 4: "The Cost Curve", 5: "The Moat",
    6: "The Cycle", 7: "Sizing a Market", 8: "Oil and Gas", 9: "Mining and Metals", 10: "Farming and Food",
    11: "Heavy Materials", 12: "Chemicals", 13: "Electricity", 14: "Water and Waste", 15: "Semiconductors",
    16: "Electronics", 17: "Automobiles", 18: "Aerospace and Defence", 19: "Machinery", 20: "Pharmaceuticals",
    21: "Medical Technology", 22: "Consumer Goods", 23: "Fashion and Luxury", 24: "Construction", 25: "Homes",
    26: "Property", 27: "Shipping and Ports", 28: "Airlines", 29: "Rail, Trucks and Parcels", 30: "Telecoms",
    31: "Grocery and Mass Retail", 32: "E-commerce", 33: "The Middlemen", 34: "Restaurants and Franchising",
    35: "Travel and Hotels", 36: "Software", 37: "Cloud and Data Centres", 38: "Advertising",
    39: "Media and Streaming", 40: "Video Games", 41: "Music, Books and Creators", 42: "Artificial Intelligence",
    43: "Banks", 44: "Investment Banks and Markets", 45: "Insurance", 46: "Asset Management",
    47: "Private Equity and Venture Capital", 48: "Payments", 49: "The Toll Collectors", 50: "Hospitals and Doctors",
    51: "Health Insurance and the Drug Channel", 52: "Education", 53: "Professional Services",
    54: "Outsourcing and Staffing", 55: "Sports and Live Entertainment", 56: "The Energy Transition",
    57: "Chokepoints", 58: "The Giants", 59: "Birth", 60: "Decline", 61: "One Industry, Five Countries",
    62: "The Analyst", 63: "Due Diligence", 64: "The Report",
}

# The five questions every part answers (README, "The story"), in the order the films take them.
QUESTIONS = (
    ("unit", "What is sold?"),
    ("make", "How is it made, and what does one more cost?"),
    ("dollar", "Where does the dollar go?"),
    ("moat", "Why does it stay there?"),
    ("change", "What moves it?"),
)
QUESTION_SHORT = {"unit": "What is sold", "make": "How it is made", "dollar": "Where the dollar goes",
                  "moat": "Why it stays", "change": "What moves it"}


def act_of(part: int) -> tuple:
    for a in ACTS:
        if a[2] <= part <= a[3]:
            return a
    raise ValueError(part)
