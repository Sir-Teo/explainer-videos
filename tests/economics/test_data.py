"""The Data Room: the frozen extracts load, match their sources' known values, and are all registered."""

import math
import re
from pathlib import Path

from explainer.economics import data
from explainer.economics.data import tables

HERE = Path(data.__file__).parent


def test_maddison():
    w = data.maddison_world()
    i1820, i2022 = w["year"].index(1820), w["year"].index(2022)
    assert abs(w["World"][i1820] - 1127.73) < 0.01 and abs(w["World"][i2022] - 16676.75) < 0.01
    uk = data.maddison_country("GBR")
    assert uk["year"][0] == 1000 and 1252 in uk["year"] and uk["year"][-1] == 2022
    assert len(data.maddison_year(2022)) == 169


def test_fred_and_spf():
    g = data.fred("GDPCA")
    assert g["date"][0] == "1929-01-01" and abs(g["value"][0] - 1191.124) < 1e-6
    u = data.fred("M0892AUSM156SNBR")
    assert max(u["value"]) > 25
    rows = {(r["year"], r["quarter"]): r for r in data.spf()}
    aug = rows[(2008, 3)]
    assert abs(aug["rgdp_b"] / aug["rgdp_a"] - 1 - 0.01547) < 1e-4
    assert aug["recess"][1] == 45


def test_pinksheet_and_psd():
    a = data.pinksheet("arabica")
    assert a["month"][0] == "1960-01" and a["month"][-1] == "2026-10"
    i = a["month"].index("1975-06")
    assert a["value"][i] == 1.23 and a["value"][a["month"].index("1977-04")] > 5 * a["value"][i]
    assert data.pinksheet("tin")["units"] == "$/mt"
    c = data.psd_coffee()
    y = c["year"].index(1976)
    assert c["Brazil"]["production"][y - 1:y + 1] == [23000.0, 9300.0]
    assert abs(c["world"]["production"][y] - 61162) < 1


def test_every_file_is_registered():
    listed = {f for d in data.DATASETS.values() for f in d["files"]}
    on_disk = {p.name for p in HERE.glob("*.csv")}
    assert listed == on_disk
    sources = (HERE / "SOURCES.md").read_text()
    for f in on_disk:
        assert f"`{f}`" in sources, f
    for t in tables.ALL.values():
        assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", t.checked) and t.cite and t.tag
        assert f"`{t.key}`" in sources, t.key


def test_the_fine_transcription():
    g = tables.GNEEZY_RUSTICHINI_2000.data
    for c, means in g["table2"].items():
        x = g["centres"][c][1]
        assert len(x) == 20
        mine = (sum(x[0:4]) / 4, sum(x[4:8]) / 4, sum(x[4:16]) / 12, sum(x[16:20]) / 4)
        for a, b in zip(mine, means):  # the paper truncates its twelve-week means to one decimal
            assert abs(a - b) < 1e-9 or abs(math.floor(a * 10 + 1e-9) / 10 - b) < 1e-9


def test_part3_accounts_and_surveys():
    gdp = dict(zip(data.fred("GDPA")["date"], data.fred("GDPA")["value"]))["2025-01-01"]
    parts = [dict(zip(data.fred(s)["date"], data.fred(s)["value"]))["2025-01-01"]
             for s in ("PCECA", "GPDIA", "GCEA", "EXPGSA", "IMPGSA")]
    assert abs(parts[0] + parts[1] + parts[2] + parts[3] - parts[4] - gdp) < 0.01   # C + I + G + X - M = GDP
    assert data.fred("GDIA")["retrieved"] == "2026-11-19" and data.fred("GDPCA")["retrieved"] == "2026-11-18"
    u = data.fred("UNRATE")
    missing = [d for d, v in zip(u["date"], u["value"]) if not v == v]
    assert missing == ["2025-10-01"]                                        # the one month never collected
    chn = next(r for r in data.wdi(2024) if r["code"] == "CHN")
    assert 18e12 < chn["gdp_usd"] < 19e12 and 38e12 < chn["gdp_ppp"] < 39e12
    assert len(data.hdr()) == 195
    fl = {r["quarter"]: r for r in data.rtdsm()["first_latest"]}
    assert abs(fl["2008:Q4"]["first"] + 3.804) < 1e-3 and abs(fl["2008:Q4"]["latest"] + 8.472) < 1e-3


def test_kuznets_tables_add_up():
    k = tables.KUZNETS_1934.data
    for i in range(4):
        # income produced = income paid out + business savings (table 1)
        assert k["paid_out"][i] + k["business_savings"][i] == k["produced"][i]
        # labour + property + entrepreneurial income = income paid out (table 2), to the report's rounding
        total = k["labour"][i] + k["property"][i] + k["entrepreneurial"][i]
        assert abs(total - k["paid_out"][i]) <= 2
    p = tables.PETTY_1665.data
    assert p["stock_yields"] + p["labour_yields"] == p["expense"]
    b = tables.CPI_BIAS.data
    assert abs(sum(b["boskin_1996"]) - b["boskin_total"]) < 1e-9
    assert abs(sum(b["lebow_rudd_2003"]) - b["lebow_rudd_total"]) < 1e-9
    assert abs(sum(b["moulton_2018"]) - b["moulton_total"]) < 1e-9
