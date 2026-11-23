"""Every Register row has a source, a URL (unless it is an assumption), an ISO date and a sane range."""

from explainer.industry import register


def test_rows_are_complete():
    assert register.rows(1), "no rows for Part 1"
    assert register.problems() == []


def test_get_and_span():
    assert register.get("apple.iphone_sales.fy2026") > 200
    lo, hi = register.span("bom.17pro")
    assert lo < register.get("bom.17pro") < hi
