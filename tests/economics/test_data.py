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
