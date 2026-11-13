"""Lab 43: count increments over a network that loses and duplicates messages under three delivery promises, model-check deduplication, and measure varints."""

from videos.coursekit import labs  # noqa: I001  (must stay first: it lets explainer.cs import without manim)

import numpy as np

from explainer.cs.api import delivery as dl
from explainer.cs.api import wire

TITLE = "At most once, at least once, exactly once"
GOAL = ("Send 4,000 increments to a counter through the series' lossy, duplicating network under the three delivery "
        "promises and compare each count with its expected value; explore every execution of two retried "
        "increments with and without deduplication; and check the varint's length against one byte per seven bits.")
TASKS = [
    "Set dup to 0 and compare 'at least once' with 'exactly once' again. Where do the extra counts come from when the network never duplicates?",
    "Call dl.model_check(False, n_msgs=1, retries=1, max_dups=0) and read the trace: what is the shortest execution that counts one increment twice?",
    "Encode -1 with wire.varint and with wire.varint(wire.zigzag(-1)), then find the largest magnitude that zigzag still fits in two bytes.",
]


def expected(loss, dup):
    """Expected count per increment: at most once, and at least once (retry until an acknowledgement arrives)."""
    delivered = (1 - loss) * (1 + dup)  # copies of one send that arrive
    acked = (1 - loss) * ((1 - dup) * (1 - loss) + dup * (1 - loss ** 2))  # some copy arrives and some ack returns
    return delivered, delivered / acked


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    n, dup = 4000, 0.02

    # 1. three promises over the same network, at several loss rates
    losses = [0.0, 0.05, 0.1, 0.2, 0.3]
    got = {p: [] for p in ("at most once", "at least once", "exactly once")}
    for k, loss in enumerate(losses):
        r = dl.semantics(n=n, loss=loss, dup=dup, seed=seed * 100 + k)["policies"]
        for p in got:
            got[p].append(r[p]["count"])
        most, least = expected(loss, dup)
        assert r["exactly once"]["count"] == n, "deduplication makes the count exact at every loss rate"
        assert r["exactly once"]["messages"] == r["at least once"]["messages"], "and costs no extra traffic"
        assert abs(r["at most once"]["count"] / n - most) < 0.03, "at most once: (1 - loss)(1 + dup) per increment"
        assert abs(r["at least once"]["count"] / n - least) < 0.04, "at least once: deliveries per acknowledged send"
        if loss > 0:
            assert r["at most once"]["count"] < n < r["at least once"]["count"]
        if loss == 0.05:
            lab.row("loss 5%, dup 2%: at most once", f"{r['at most once']['count']:,} of {n:,}   (expected {most * n:,.0f})")
            lab.row("loss 5%, dup 2%: at least once", f"{r['at least once']['count']:,} of {n:,}   (expected {least * n:,.0f})")
            lab.row("loss 5%, dup 2%: exactly once", f"{r['exactly once']['count']:,} of {n:,}   with the same "
                                                    f"{r['exactly once']['messages']:,} messages")

    # 2. every execution of two increments, each sent up to three times
    safe, unsafe = dl.model_check(True, 2, 2), dl.model_check(False, 2, 2)
    assert not safe["violation"] and unsafe["violation"] and unsafe["counter_at_violation"] > 2
    lab.row("model check, with dedup", f"{safe['states']:,} states, the counter never exceeds 2")
    lab.row("model check, without", f"{unsafe['states']:,} states; counter {unsafe['counter_at_violation']} after: "
                                    + ", ".join(unsafe["trace"]))

    # 3. the varint: one byte per seven bits, and zigzag for small negatives
    assert wire.varint(150) == bytes([0x96, 0x01]), "the encoding guide's example"
    bits = np.arange(1, 65)
    sizes = []
    for b in bits:
        v = (1 << int(b - 1)) + int(rng.integers(0, 1 << min(int(b - 1), 62)))  # a random value with exactly b bits
        enc = wire.varint(v)
        assert wire.read_varint(enc) == (v, len(enc)) and len(enc) == -(-int(b) // 7)
        sizes.append(len(enc))
    for v in [int(x) for x in rng.integers(-10 ** 6, 10 ** 6, 200)] + [-1, 0, 1, -2 ** 63, 2 ** 63 - 1]:
        z = wire.zigzag(v)
        assert z >= 0 and wire.unzigzag(z) == v and z == (2 * v if v >= 0 else -2 * v - 1)
    lab.row("varint", f"150 is 96 01; -2 takes {len(wire.varint(-2))} bytes as an int, "
                      f"{len(wire.varint(wire.zigzag(-2)))} after zigzag")
    lab.note = ("Losing messages makes a counter too low, retrying makes it too high, and remembering which ids were "
                "applied makes it exact with the same traffic: exactly-once processing is at-least-once delivery "
                "plus deduplication.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    grid = np.linspace(0, 0.3, 61)
    x = [100 * v for v in losses]
    ax[0].plot(100 * grid, [expected(v, dup)[1] for v in grid], color=labs.RED, lw=1, ls="--")
    ax[0].plot(100 * grid, [expected(v, dup)[0] for v in grid], color=labs.BLUE, lw=1, ls="--", label="expected (dashed)")
    ax[0].plot(x, np.array(got["at least once"]) / n, "o", color=labs.RED, label="at least once")
    ax[0].plot(x, np.array(got["exactly once"]) / n, "o", color=labs.GREEN, label="exactly once (with dedup)")
    ax[0].plot(x, np.array(got["at most once"]) / n, "o", color=labs.BLUE, label="at most once")
    ax[0].set(title="Counter after 4,000 increments, as a share of the truth", xlabel="messages lost (%), 2% duplicated",
              ylabel="count / increments sent")
    ax[0].legend(loc="upper left")
    ax[1].step(bits, sizes, where="mid", color=labs.GOLD, label="bytes of wire.varint")
    ax[1].plot(bits, bits / 7, color=labs.MUTED, ls="--", label="bits / 7")
    ax[1].set(title="A varint spends one byte per seven bits", xlabel="bits in the value", ylabel="bytes on the wire")
    ax[1].legend(loc="upper left")
    lab.fig = fig
    return lab
