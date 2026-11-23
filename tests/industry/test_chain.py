"""The Works' chain arithmetic (explainer/industry/works/chain.py) and Part 1's numbers."""

import pytest

from explainer.industry.works import chain


@pytest.mark.parametrize("price,bom", [(1099, 520), (1199, 718), (299, 144.4)])
def test_dollar_slices_sum_to_price(price, bom):
    d = chain.dollar(price, bom, indirect_share=0.6, channel_margin=0.1, assembly=30, other_cogs=40,
                     opex_ratio=0.15, tax_rate=0.16)
    assert d.total() == pytest.approx(price)
    assert d.group("parts") == pytest.approx(bom)


def test_memory_override_keeps_the_bill():
    d = chain.dollar(1199, 718, memory=244, indirect_share=0.6, channel_margin=0.1, assembly=30, other_cogs=40,
                     opex_ratio=0.15, tax_rate=0.16)
    assert d.get("memory").amount == pytest.approx(244)
    assert d.group("parts") == pytest.approx(718)


def test_value_added_sums_to_final_price_and_sales_double_count():
    links = [("wafer", 10), ("chip", 83), ("phone", 1033), ("shop", 1099)]
    out = chain.value_added(links)
    assert sum(a for _, _, a in out) == pytest.approx(1099)
    assert sum(s for _, s, _ in out) > 1099


def test_tier_passthrough():
    (gb, dp, dm, absorbed), = chain.tier_passthrough([1024], [1599], [1899], 39, 145, 13 / 256, 250 / 1024)
    assert dp == 300
    assert dm == pytest.approx(106 + 1024 * (250 / 1024 - 13 / 256))
    assert absorbed == pytest.approx(dm - 300)


def test_part1_numbers():
    from videos.industry.industry1.compute import results

    R = results()
    assert sum(s["amount"] for s in R["dollar17"]["slices"]) == pytest.approx(R["dollar17"]["price"], abs=0.05)
    assert sum(s["amount"] for s in R["dollar18"]["slices"]) == pytest.approx(R["dollar18"]["price"], abs=0.05)
    lo, hi = R["dollar17"]["profit_range"]
    assert lo < R["dollar17"]["profit"] < hi
    assert R["memory"]["kept18"] > 5 * R["memory"]["kept17"]          # the memory shock, per phone
    ipod = R["ipod"]
    assert ipod["apple"] + ipod["retail"] + ipod["distribution"] + ipod["inputs"] == pytest.approx(ipod["price"], abs=0.5)
