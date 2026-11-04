"""Shared instruments for the computer-science series (videos/cs/cs1 ... cs61), *Computer Science, Built*.

    from explainer.cs import *

Everything of *AI, Built*'s visual language is reused (``explainer.ai``: the colour-linked derivations ``cmath`` and
``morph``, ``LiveBars``, ``glow_dot``, camera framing, the lecture cards, ``reference_card``, ``cite``, ``gloss``)
and so are the analysis series' text helpers and derivation ladder (``label``, ``note``, ``why``, ``ladder``).  Here,
the devices that hold this series together (videos/cs/SYLLABUS.md, section 2):

* :func:`chapter_card`, with the **tower** of abstractions (the part's layer lit) and the **timeline strip**,
  1800-2030 (the chapter's years lit);
* :func:`tower`, the stack itself, drawn large when a part talks about where it sits;
* :func:`series_map`, the sixty-one parts in eleven acts, the current one lit;
* :func:`ledger_table`, the Job's running record (the cost of counting the words of thirty novels, one row per part
  that changes it; ``.cache/cs*/ledger.json``);
* :func:`payoff_card` ("where this comes back") and :func:`practice_card` ("in practice").

The series' own visual instruments (tapes, rule tables, bitmaps, ...) are in :mod:`explainer.cs.viz`, exported here.
"""

from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F401,F403
from explainer.ai import _zh, label, note, wrapped_label, zh  # noqa: F401
from explainer.cs.viz import *  # noqa: F401,F403,E402

SERIES_EN = "Computer Science, Built"
SERIES_ZH = "计算机科学，从零搭建"

# ---------------------------------------------------------------------------
# The sixty-one parts in eleven acts: a degree (I-X) and the research frontier (XI)
# ---------------------------------------------------------------------------
ACTS = [
    (r"I.\ The Machine", (1, 6)),
    (r"II.\ Making It Fast", (7, 10)),
    (r"III.\ Speaking to the Machine", (11, 15)),
    (r"IV.\ Algorithms", (16, 24)),
    (r"V.\ Limits and Secrets", (25, 30)),
    (r"VI.\ One Machine, Many Programs", (31, 35)),
    (r"VII.\ Many Machines", (36, 39)),
    (r"VIII.\ Building Software", (40, 44)),
    (r"IX.\ Systems at Scale", (45, 50)),
    (r"X.\ Horizons and Trust", (51, 55)),
    (r"XI.\ The Research Frontier", (56, 61)),
]
PARTS = {
    1: r"What Is a Computation?", 2: r"Proof and Counting", 3: r"Logic from Switches", 4: r"Arithmetic",
    5: r"Memory and Time", 6: r"The Stored-Program Computer",
    7: r"Pipelines", 8: r"Out of Order", 9: r"The Memory Hierarchy", 10: r"Parallel Machines",
    11: r"The Running Program", 12: r"Languages and Automata", 13: r"The Compiler", 14: r"Lambda and Types",
    15: r"Runtimes",
    16: r"Counting Steps", 17: r"Data Structures", 18: r"Graphs", 19: r"The Great Paradigms",
    20: r"Randomness as a Resource", 21: r"Strings", 22: r"Geometry", 23: r"Optimization",
    24: r"Algorithms in Practice",
    25: r"Undecidable", 26: r"P versus NP", 27: r"Proofs and Randomness", 28: r"Error-Correcting Codes",
    29: r"Secrets", 30: r"Public Keys",
    31: r"The Kernel", 32: r"Virtual Memory", 33: r"Concurrency", 34: r"Storage", 35: r"Databases",
    36: r"Networks I: Moving Bits", 37: r"Networks II: Reliable Conversation", 38: r"Agreement", 39: r"Scale",
    40: r"Software Engineering", 41: r"Version Control, Builds and Dependencies", 42: r"The Browser and the Web",
    43: r"APIs and Services", 44: r"People and Products",
    45: r"The Cloud", 46: r"Logs, Streams and Warehouses", 47: r"Search Engines",
    48: r"System Design I: Building Blocks", 49: r"System Design II: Case Studies", 50: r"Keeping It Running",
    51: r"Light and Pixels", 52: r"Computing with Real Numbers", 53: r"Quantum Computation",
    54: r"Proving Programs Correct", 55: r"Trusting Trust",
    56: r"Spectral Graphs and Expanders", 57: r"Learning Theory", 58: r"Semantics",
    59: r"Distributed Computing Theory", 60: r"Domain-Specific Hardware", 61: r"Doing Research",
}
# Short names, for the series map (five columns of a frame)
SHORT = dict(PARTS)
SHORT.update({1: r"What Is Computation?", 6: r"Stored Programs", 9: r"Memory Hierarchy", 11: r"Running Programs",
              12: r"Languages, Automata", 19: r"Great Paradigms", 20: r"Randomness", 24: r"Algorithms in Practice",
              28: r"Codes", 36: r"Networks I", 37: r"Networks II", 40: r"Software Engineering",
              41: r"Version Control, Builds", 42: r"Browser and Web", 43: r"APIs and Services",
              44: r"People, Products", 46: r"Logs and Streams", 48: r"System Design I", 49: r"System Design II",
              50: r"Keeping It Running", 52: r"Real Numbers", 53: r"Quantum", 54: r"Proving Programs",
              56: r"Spectral Graphs", 59: r"Distributed Theory", 60: r"Domain-Specific Hardware"})


def act_of(part: int) -> int:
    """The act (1-11) a part belongs to."""
    for i, (_, (a, b)) in enumerate(ACTS, 1):
        if a <= part <= b:
            return i
    raise ValueError(part)


def series_map(current: int | None = None, done: int = 0, font_size=17, width=13.4, height=7.3) -> VGroup:
    """The acts in a grid of two rows (six columns for eleven acts); each part a row.  Parts up to ``done`` are white,
    ``current`` is lit and boxed, the rest are dim.  ``.part[p]`` is the row of part p; ``.cols[i]`` act i+1."""
    cols = VGroup()
    for act, (a, b) in ACTS:
        head = label(act, font_size=font_size + 3, color=GREY_A)
        rows = VGroup()
        for p in range(a, b + 1):
            color = C.CS_HEAD if p == current else (WHITE if p <= done else GREY_C)
            rows.add(label(rf"{p}.\ {SHORT[p]}", font_size=font_size, color=color))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        if head.width > 2.75:
            head.width = 2.75
        col = VGroup(head, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        col.head, col.rows = head, rows
        cols.add(col)
    cols.arrange_in_grid(rows=2, cols=(len(ACTS) + 1) // 2, buff=(0.32, 0.42), cell_alignment=UL)
    if cols.width > width:
        cols.width = width
    if cols.height > height:
        cols.height = height
    g = VGroup(cols)
    g.cols = cols
    g.part = {}
    for col, (_, (a, b)) in zip(cols, ACTS):
        for p, row in zip(range(a, b + 1), col.rows):
            g.part[p] = row
    if current is not None:
        box = SurroundingRectangle(g.part[current], color=C.CS_HEAD, buff=0.07, corner_radius=0.06, stroke_width=2)
        g.add(box)
        g.box = box
    return g.move_to(ORIGIN)


# ---------------------------------------------------------------------------
# The tower of abstractions
# ---------------------------------------------------------------------------
LAYERS = [  # bottom to top: (key, name)
    ("math", r"mathematics and logic"),
    ("physics", r"switches"),
    ("gates", r"gates"),
    ("arith", r"arithmetic and memory"),
    ("isa", r"instruction set"),
    ("uarch", r"microarchitecture"),
    ("code", r"machine code"),
    ("lang", r"languages"),
    ("algo", r"algorithms"),
    ("os", r"operating system"),
    ("data", r"storage and data"),
    ("net", r"networks"),
    ("dist", r"distributed systems"),
    ("cloud", r"services and the cloud"),
    ("apps", r"applications"),
]
COLUMNS = [("limits", r"the limits", C.CS_LIMIT), ("practice", r"the practice", C.CS_PRACTICE)]
LAYER_COLOR = {"math": C.CS_INF, "physics": "#C2A26B", "gates": "#E8C547", "arith": "#F2A541", "isa": "#FF9F45",
               "uarch": "#FF8A65", "code": "#F28B82", "lang": "#E37BD3", "algo": "#B39DDB", "os": "#7C7FE0",
               "data": "#58A6FF", "net": "#2EC4B6", "dist": "#5BD17A", "cloud": "#9BE37B", "apps": "#D4E157"}
# the layers each part lights by default (chapter cards may override)
PART_LAYERS = {1: ("math", "limits"), 2: ("math",), 3: ("physics", "gates"), 4: ("arith",), 5: ("arith",),
               6: ("isa",), 7: ("uarch",), 8: ("uarch",), 9: ("uarch",), 10: ("uarch",), 11: ("code",),
               **{p: ("lang",) for p in range(12, 16)}, **{p: ("algo",) for p in range(16, 25)},
               25: ("limits",), 26: ("limits",), 27: ("limits",), 28: ("limits", "net"), 29: ("limits",),
               30: ("limits",), 31: ("os",), 32: ("os",), 33: ("os",), 34: ("os", "data"), 35: ("data",),
               36: ("net",), 37: ("net",), 38: ("dist",), 39: ("dist",), 40: ("practice",), 41: ("practice",),
               42: ("apps", "practice"), 43: ("cloud",), 44: ("apps", "practice"), 45: ("cloud",),
               46: ("data", "cloud"), 47: ("apps",), 48: ("cloud", "dist"), 49: ("cloud", "dist"),
               50: ("cloud", "practice"), 51: ("apps",), 52: ("algo",), 53: ("physics", "limits"),
               54: ("lang", "practice"), 55: tuple(k for k, _ in LAYERS) + ("limits", "practice"),
               56: ("algo", "math"), 57: ("algo", "limits"), 58: ("lang", "math"), 59: ("dist", "limits"),
               60: ("uarch", "gates"), 61: tuple(k for k, _ in LAYERS) + ("limits", "practice")}


def tower(lit=(), height=5.4, width=2.3, font_size=15, labels="lit", lit_color=None) -> VGroup:
    """The stack of abstractions, bottom (mathematics and logic) to top (applications), with two side columns: the
    limits and the practice.  Layers in ``lit`` glow in their colours; ``labels`` is "lit" (only lit layers are
    named, beside the stack), "all" (every layer named, inside its slab) or "none".  ``.layer[key]`` is a layer's slab
    (a VGroup of the rectangle and, with labels, its name); ``.column[key]`` a side column."""
    n = len(LAYERS)
    gap = 0.05
    h = (height - gap * (n - 1)) / n
    g = VGroup()
    g.layer, g.column = {}, {}
    slabs = VGroup()
    for i, (key, name) in enumerate(LAYERS):
        on = key in lit
        col = lit_color or LAYER_COLOR[key]
        w = width + (0.5 if key == "math" else 0.0)
        r = RoundedRectangle(width=w, height=h, corner_radius=min(0.06, h / 3), stroke_width=1.6 if on else 1.0,
                             stroke_color=col if on else GREY_C, fill_color=col, fill_opacity=0.85 if on else 0.13)
        if not on:
            r.set_stroke(opacity=0.55)
        r.move_to([0, -height / 2 + h / 2 + i * (h + gap), 0])
        slab = VGroup(r)
        if labels == "all":
            t = label(name, font_size=font_size, color=BLACK if on else GREY_B)
            if t.width > w - 0.12:
                t.width = w - 0.12
            if t.height > h * 0.8:
                t.height = h * 0.8
            slab.add(t.move_to(r))
        elif labels == "lit" and on:
            t = label(name, font_size=font_size, color=col).next_to(r, LEFT, buff=0.15)
            slab.add(t)
        slab.key = key
        g.layer[key] = slab
        slabs.add(slab)
    g.add(slabs)
    for j, (key, name, col) in enumerate(COLUMNS):
        on = key in lit
        bar = RoundedRectangle(width=0.22, height=height - h - gap, corner_radius=0.06,
                               stroke_width=1.6 if on else 1.0, stroke_color=col if on else GREY_C, fill_color=col,
                               fill_opacity=0.85 if on else 0.13)
        if not on:
            bar.set_stroke(opacity=0.55)
        bar.move_to([width / 2 + 0.22 + j * 0.34, (h + gap) / 2, 0])
        column = VGroup(bar)
        if on and labels != "none":
            t = label(name, font_size=font_size, color=col).rotate(PI / 2)
            if t.height > bar.height:
                t.height = bar.height
            column.add(t.next_to(bar, RIGHT, buff=0.08))
        column.key = key
        g.column[key] = column
        g.add(column)
    return g


# ---------------------------------------------------------------------------
# The timeline strip
# ---------------------------------------------------------------------------
TIMELINE = [
    (1801, r"Jacquard's punched cards"),
    (1822, r"Babbage's Difference Engine"),
    (1837, r"the Analytical Engine"),
    (1843, r"Lovelace's Note G"),
    (1854, r"Boole's \textit{Laws of Thought}"),
    (1874, r"Cantor: $\mathbb{R}$ is uncountable"),
    (1879, r"Frege's \textit{Begriffsschrift}"),
    (1890, r"Hollerith's tabulator"),
    (1891, r"Cantor's diagonal argument"),
    (1900, r"Hilbert's problems"),
    (1928, r"the Entscheidungsproblem"),
    (1931, r"G\"odel's incompleteness"),
    (1936, r"Church and Turing"),
    (1937, r"Shannon: relays are logic"),
    (1941, r"Zuse's Z3"),
    (1944, r"Colossus"),
    (1945, r"ENIAC; von Neumann's report"),
    (1947, r"the transistor"),
    (1948, r"the Manchester Baby; information theory"),
    (1949, r"EDSAC; Shannon on secrecy"),
    (1950, r"Hamming's codes"),
    (1951, r"Kleene's regular events"),
    (1952, r"Hopper's A-0"),
    (1956, r"Chomsky's hierarchy"),
    (1957, r"FORTRAN"),
    (1958, r"the integrated circuit"),
    (1959, r"Dijkstra's shortest paths"),
    (1960, r"LISP; ALGOL 60"),
    (1961, r"time-sharing"),
    (1962, r"Rad\'o's busy beaver"),
    (1963, r"Sketchpad"),
    (1965, r"Moore's law; polynomial time"),
    (1967, r"Minsky's counter machines"),
    (1968, r"software engineering"),
    (1969, r"Unix; ARPANET"),
    (1970, r"Codd's relations; Conway's Life"),
    (1971, r"Cook's theorem"),
    (1972, r"Karp's 21 problems"),
    (1974, r"Cerf and Kahn's TCP"),
    (1976, r"Diffie--Hellman"),
    (1977, r"RSA"),
    (1978, r"Lamport's clocks"),
    (1983, r"TCP/IP"),
    (1984, r"Trusting Trust"),
    (1985, r"FLP; IEEE 754"),
    (1989, r"Paxos"),
    (1991, r"the Web; Linux"),
    (1994, r"Shor's algorithm"),
    (1998, r"Google"),
    (2004, r"Rule 110 is universal; MapReduce"),
    (2005, r"git"),
    (2006, r"EC2 and S3"),
    (2011, r"Kafka"),
    (2014, r"Raft; Kubernetes"),
    (2018, r"Spectre"),
    (2024, r"BB(5) proved; ML-KEM"),
]
T0, T1 = 1800, 2030


def timeline(lit=(), width=12.0, show_labels=True, font_size=18, extra=()) -> VGroup:
    """The strip from 1800 to 2030; years in ``lit`` glow and get their names.  ``extra``: (year, name) pairs a part
    adds for its own chapter cards."""
    x0 = -width / 2

    def X(y):
        return x0 + width * (y - T0) / (T1 - T0)

    events = dict(TIMELINE)
    events.update(dict(extra))
    g = VGroup(Line([X(T0), 0, 0], [X(T1), 0, 0], color=GREY_D, stroke_width=2))
    for yr in (1800, 1850, 1900, 1950, 2000):
        g.add(Line([X(yr), -0.06, 0], [X(yr), 0.06, 0], color=GREY_D, stroke_width=1.5))
        g.add(Text(str(yr), font_size=14, color=GREY_D).next_to([X(yr), 0, 0], DOWN, buff=0.12))
    labels, anchors = VGroup(), []
    side = 1
    for yr in sorted(events):
        on = yr in lit
        d = Dot([X(yr), 0, 0], radius=0.065 if on else 0.035, color=C.CS_HEAD if on else GREY_C)
        g.add(d)
        if on and show_labels:
            t = label(rf"{yr}\; {events[yr]}", font_size=font_size, color=C.CS_HEAD)
            t.next_to(d, UP if side > 0 else DOWN, buff=0.14 if side > 0 else 0.4)
            side = -side
            labels.add(t)
            anchors.append(d)
    for row in (1, -1):  # keep the lit labels apart and inside the frame
        same = sorted([t for t in labels if np.sign(t.get_y()) == row], key=lambda t: t.get_x())
        for a, b in zip(same, same[1:]):
            gap = b.get_left()[0] - a.get_right()[0]
            if gap < 0.2:
                b.shift(RIGHT * (0.2 - gap))
        if same and same[-1].get_right()[0] > 6.9:
            same[-1].shift(LEFT * (same[-1].get_right()[0] - 6.9))
            for i in range(len(same) - 2, -1, -1):
                gap = same[i + 1].get_left()[0] - same[i].get_right()[0]
                if gap < 0.2:
                    same[i].shift(LEFT * (0.2 - gap))
        if same and same[0].get_left()[0] < -6.9:
            same[0].shift(RIGHT * (-6.9 - same[0].get_left()[0]))
    leaders = VGroup()  # a displaced label keeps a thin line to its own year
    for t, d in zip(labels, anchors):
        if abs(t.get_x() - d.get_x()) > 0.1:
            above = t.get_y() > 0
            leaders.add(Line(d.get_top() if above else d.get_bottom(), t.get_bottom() if above else t.get_top(),
                             color=C.CS_HEAD, stroke_width=1, stroke_opacity=0.4))
    g.add(leaders, labels)
    g.labels, g.leaders = labels, leaders
    return g


def chapter_card(number, title: str, question: str = "", lit=(), part: int | None = None, layers=None,
                 extra=()) -> VGroup:
    """Chapter title and the question it answers; the timeline strip with this chapter's years lit; and, on the left,
    the tower with the part's layers lit (``layers`` overrides the part's default).  ``card[0]`` is the title group,
    ``card[1]`` the strip, ``card[2]`` the tower."""
    if zh():
        head_text = (rf"第{part}部分 \textperiodcentered\ " if part else "") + f"第{number}章"
    else:
        head_text = (rf"Part {part} \textperiodcentered\ " if part else "") + f"Chapter {number}"
    head = label(head_text, font_size=28, color=GREY_B)
    t = label(title, font_size=54)
    if t.width > 10.6:
        t.width = 10.6
    g = VGroup(head, t)
    if question:
        q = label(question, font_size=30, color=GREY_A)
        if q.width > 10.6:
            q.width = 10.6
        g.add(q)
    g.arrange(DOWN, buff=0.3).move_to([0.75, 0.75, 0])
    strip = timeline(lit=lit, extra=extra).to_edge(DOWN, buff=0.9)
    lay = PART_LAYERS.get(part, ()) if layers is None else layers
    tw = tower(lit=lay, height=3.4, width=1.0, labels="none")
    names = dict(LAYERS) | {k: n for k, n, _ in COLUMNS}
    colors = LAYER_COLOR | {k: c for k, _, c in COLUMNS}
    keys = [k for k in [k for k, _ in LAYERS][::-1] + [k for k, _, _ in COLUMNS] if k in lay]
    if len(keys) > 3:
        caption = VGroup(label(r"the whole tower", font_size=18, color=GREY_A))
    else:
        caption = VGroup(*[label(names[k], font_size=18, color=colors[k]) for k in keys])
    caption.arrange(DOWN, buff=0.08, aligned_edge=LEFT).next_to(tw, DOWN, buff=0.22).align_to(tw, LEFT)
    side = VGroup(tw, caption).to_corner(UL, buff=0.45)
    side.tower, side.caption = tw, caption
    return VGroup(g, strip, side)


# ---------------------------------------------------------------------------
# The ledger: the cost of the Job, one row per part that changes it
# ---------------------------------------------------------------------------
def ledger_table(rows: list[dict], shown: int | None = None, highlight=(), lo=-9.0, hi=12.0, bar_width=6.0,
                 row_h=0.4, font_size=20, label_width=5.0) -> VGroup:
    """One row per entry: ``part``, ``label`` (what changed) and ``seconds`` (the projected time to count the words
    of all thirty novels), drawn as a bar on a log scale from 10^lo to 10^hi seconds.  A row without ``seconds`` is
    one a later part fills (a dim question mark).  Only the first ``shown`` rows are filled.  The axis is marked with
    human time scales (a second, a day, a year, the age of the universe) so the logarithm reads as a story."""
    shown = len(rows) if shown is None else shown
    x0 = -bar_width / 2 + label_width / 2 + 0.4
    scale = bar_width / (hi - lo)
    out = VGroup()
    for i, r in enumerate(rows):
        y = -i * row_h
        on = i < shown
        name = label(rf"{r['part']}\quad {r['label']}", font_size=font_size, color=WHITE if on else GREY_D)
        if name.width > label_width:
            name.width = label_width
        name.move_to([x0 - 0.25 - name.width / 2, y, 0])
        if "seconds" in r and r["seconds"]:
            e = float(np.clip(np.log10(r["seconds"]), lo, hi))
            w = max((e - lo) * scale, 0.02)
            bar = Rectangle(width=w, height=row_h * 0.6, stroke_width=0, fill_color=C.CS_COST,
                            fill_opacity=0.9 if on else 0).move_to([x0 + w / 2, y, 0])
            value = label(human_time(r["seconds"]), font_size=font_size - 1, color=C.CS_COST if on else GREY_D)
            value.next_to(bar, RIGHT, buff=0.12)
            if not on:
                value.set_opacity(0)
        else:
            bar = VectorizedPoint([x0, y, 0])
            value = MathTex(r"?", font_size=font_size + 2, color=GREY_D).move_to([x0 + 0.25, y, 0])
        row = VGroup(name, bar, value)
        row.name, row.bar, row.value, row.data = name, bar, value, r
        if i in highlight:
            row.add_to_back(Rectangle(width=label_width + bar_width + 1.8, height=row_h * 0.95, stroke_width=0,
                                      fill_color=C.CS_HEAD, fill_opacity=0.1).move_to(
                [x0 + (bar_width - label_width) / 2 + 0.3, y, 0]))
        out.add(row)
    bottom = -(len(rows) - 1) * row_h - 0.35
    axis = VGroup(Line([x0, 0.4, 0], [x0, bottom, 0], color=GREY_C, stroke_width=1.5))
    for sec, name in ((1e-6, r"$\mu$s"), (1.0, r"second"), (86400.0, r"day"), (3.15e7, r"year"),
                      (3.15e9, r"century"), (4.35e17, r"age of the universe")):
        e = np.log10(sec)
        if lo <= e <= hi:
            x = x0 + (e - lo) * scale
            axis.add(DashedLine([x, 0.4, 0], [x, bottom, 0], color=GREY_D, stroke_width=1, dash_length=0.06))
            axis.add(label(name, font_size=15, color=GREY_B).move_to([x, bottom - 0.22, 0]))
    g = VGroup(axis, out)
    g.rows, g.axis = out, axis
    return g.move_to(ORIGIN)


def human_time(s: float) -> str:
    """Seconds as a readable Tex quantity: 3.2 ms, 4.1 hours, 2,300 years."""
    units = [(3.15e7, r"years"), (86400.0, r"days"), (3600.0, r"hours"), (60.0, r"min"), (1.0, r"s"),
             (1e-3, r"ms"), (1e-6, r"$\mu$s"), (1e-9, r"ns")]
    for u, name in units:
        if s >= u or u == 1e-9:
            v = s / u
            txt = f"{v:,.0f}" if v >= 100 else (f"{v:.1f}" if v >= 10 else f"{v:.2f}")
            return rf"{txt} {name}"
    return f"{s:g} s"


# ---------------------------------------------------------------------------
# Payoffs and practice
# ---------------------------------------------------------------------------
def payoff_card(items, font_size=24, title=r"Where this comes back") -> VGroup:
    """``items``: (idea, [part numbers]).  Each row: the idea, an arrow, the parts that use it (number and name)."""
    head = label(title, font_size=font_size + 12)
    rows = VGroup()
    for idea, parts in items:
        left = label(idea, font_size=font_size, color=C.CS_HEAD)
        right = label(r",\ ".join(rf"{p}\ \textit{{{SHORT[p]}}}" for p in parts), font_size=font_size - 2,
                      color=GREY_A)
        rows.add(VGroup(left, right))
    lw = max(r[0].width for r in rows)
    for r in rows:
        r[0].align_to(ORIGIN, LEFT)
        arrow = MathTex(r"\longrightarrow", font_size=font_size + 4, color=GREY_C)
        r.insert(1, arrow)
        arrow.next_to(ORIGIN, RIGHT, buff=0).shift(RIGHT * (lw + 0.3))
        r[2].next_to(arrow, RIGHT, buff=0.3)
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
    for r in rows:
        r[1].set_y(r[0].get_y())
        r[2].set_y(r[0].get_y())
    g = VGroup(head, rows).arrange(DOWN, buff=0.5)
    if g.width > 13.4:
        g.width = 13.4
    g.head, g.rows = head, rows
    return g.move_to(ORIGIN)


def practice_card(items, title=r"In practice", font_size=24, width=12.6) -> VGroup:
    """Where the part's ideas live in industry: ``items`` are (where, what) pairs, e.g.
    (r"emulators", r"QEMU, game consoles, the JVM: universal machines")."""
    head = label(title, font_size=font_size + 12, color=C.CS_PRACTICE)
    rows = VGroup()
    for where, what in items:
        a = label(where, font_size=font_size, color=WHITE)
        b = wrapped_label(what, width - 4.2, font_size - 2, GREY_A)
        rows.add(VGroup(a, b))
    lw = max(r[0].width for r in rows)
    for r in rows:
        r[0].align_to(ORIGIN, LEFT)
        r[1].next_to(ORIGIN, RIGHT, buff=0).shift(RIGHT * (lw + 0.45)).align_to(r[0], UP)
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.28)
    g = VGroup(head, rows).arrange(DOWN, buff=0.5)
    if g.width > 13.4:
        g.width = 13.4
    if g.height > 7.2:
        g.height = 7.2
    g.head, g.rows = head, rows
    return g.move_to(ORIGIN)
