"""Part 2's arithmetic on the Filing Room's extracts: value added adds up, the table balances, the inverse is the
sum of the rounds of buying, and upstreamness is at least one."""

import numpy as np

from explainer.industry.data.fetch import IO_CODES, read
from videos.industry.industry2.compute import results


def test_value_added_adds_up():
    R = results()
    total, *sectors = R["va"]
    assert abs(sum(d["va"] for d in sectors) - total["va"]) / total["va"] < 0.002
    for d in R["va"]:
        assert abs(d["comp"] + d["tax"] + d["gos"] - 100) < 0.5, d["sector"]


def test_table_balances_and_inverse_is_the_rounds():
    io = results()["io"]
    A, L = np.array(io["A"]), np.array(io["L"])
    assert (A >= 0).all() and (A.sum(axis=0) < 1).all()  # every industry adds some value
    S, P = np.eye(len(A)), np.eye(len(A))
    for _ in range(200):
        P = P @ A
        S += P
    assert np.allclose(S, L, atol=1e-9)
    # industry output is intermediate inputs plus value added, column by column
    rows = read("bea_io_2023")
    Z = np.array([[r[c] for c in IO_CODES] for r in rows if r["code"] in IO_CODES])
    va = np.array([sum(r[c] or 0 for r in rows if r["code"] in ("V001", "V002", "V003")) for c in IO_CODES])
    used = np.array([sum(r[c] or 0 for r in rows if r["code"] in ("Used", "Other")) for c in IO_CODES])
    x = np.array(io["output"]) * 1e6
    assert np.allclose(Z.sum(axis=0) + used + va, x, rtol=1e-6)
    assert 1.6 < io["output_total"] / io["va_total"] < 1.9


def test_upstreamness():
    io = results()["io"]
    U = dict(zip(io["names"], io["upstream"]))
    assert min(U.values()) >= 1 - 1e-9
    assert U["Farms"] > U["Manufacturing"] > U["Retail"]
