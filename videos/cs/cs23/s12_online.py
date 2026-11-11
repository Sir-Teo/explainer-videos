from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs23.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono, words)


class Online(VoiceoverScene):
    def construct(self):
        self.card()
        self.ski()
        self.paging()
        self.lower()

    def card(self):
        card = chapter_card(11, r"Online: \ deciding without the future", r"How well can you do if you can't see "
                            r"ahead?", lit=(1985,), extra=((1985, r"Sleator--Tarjan competitive analysis"),),
                            part=PART)
        with self.voiceover("Chapter eleven. Online: deciding without the future."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def ski(self):
        o = load("online")
        B = o["B"]
        head = label(r"Ski rental", font_size=34).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 30, 5], y_range=[0, 22, 5], x_length=6.4, y_length=3.8,
                  axis_config={"color": GREY_D, "include_numbers": True, "font_size": 18}).to_edge(LEFT, buff=0.9)
        ax.shift(DOWN * 0.3)
        xl = label(r"days the season lasts", font_size=18, color=GREY_A).next_to(ax, DOWN, buff=0.1)
        yl = label(r"cost", font_size=18, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        opt = ax.plot_line_graph([r["days"] for r in o["det"]], [r["opt"] for r in o["det"]], line_color=YES,
                                 add_vertex_dots=False, stroke_width=3)
        det = ax.plot_line_graph([r["days"] for r in o["det"]], [r["cost"] for r in o["det"]], line_color=NO,
                                 add_vertex_dots=False, stroke_width=3)
        rnd = ax.plot_line_graph([r["days"] for r in o["rnd"]], [r["cost"] for r in o["rnd"]], line_color=LAM,
                                 add_vertex_dots=False, stroke_width=3)
        keys = VGroup(label(r"knowing the future: \ $\min(d, B)$", font_size=18, color=YES),
                      label(r"rent until day $B$, \ then buy", font_size=18, color=NO),
                      label(r"buy on a random day \ (expected)", font_size=18, color=LAM)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).next_to(ax, UP, buff=0.4).align_to(ax, LEFT)
        side = VGroup(
            label(rf"renting costs 1 a day; \ buying costs $B = {B}$; \\ you don't know how long the snow lasts",
                  font_size=21, color=WHITE),
            label(r"\textbf{competitive ratio}: \ the worst case of \\ your cost $/$ the clairvoyant's cost", font_size=21,
                  color=HEAD),
            label(r"break-even: \ rent $B - 1$ days, \ then buy: \\ never more than $2 - 1/B$ times the best", font_size=21,
                  color=NO),
            label('no deterministic rule improves this ratio: \\\\ end the season on its purchase day',
                  font_size=21, color=GREY_A),
            label(rf"discrete $B=10$: \ ratio {o['discrete_ratio']:.3f}; \\ continuous/large-$B$ limit $e/(e-1)\approx{o['e_ratio']:.3f}$; \\ season fixed before the random draw",
                  font_size=21, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        if side.width > 5.6:
            side.width = 5.6
            side.to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            (
            "Online decisions arrive before their future is known. <bookmark mark='a'/> Rent skis for one per "
            'day or buy for ten. The discrete convention charges rental only on days before purchase. <bookmark '
            "mark='b'/> Compare cost with the clairvoyant optimum, the smaller of season length and ten. For "
            "randomized rules the season must be fixed independently of the random buy day. <bookmark mark='c'/> "
            "Rent nine days, then buy: the worst ratio is nineteen over ten. <bookmark mark='d'/> A "
            'deterministic lower-bound adversary ends the season on the purchase day. This gives the required '
            "ratio even for a rule that buys early. <bookmark mark='e'/> For our buy-day distribution the exact "
            'discrete ratio is one over one minus nine tenths to the tenth power, about one point five three '
            'five. The familiar e over e minus one is the continuous or large-buy-price limit, about one point '
            'five eight two. The sampled curve estimates the separately calculated exact expectation.'
        )
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), Create(opt), FadeIn(keys[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), Create(det), FadeIn(keys[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]), Create(rnd), FadeIn(keys[2]))
        self.wait(0.3)
        self.clear_scene()

    def paging(self):
        o = load("online")
        head = label(r"Paging: \ the Job's memory trace \ (Part 9)", font_size=32).to_edge(UP, buff=0.35)
        rows = [[str(r["k"]), words(r["lru"]), words(r["fifo"]), words(r["marking"]), words(r["random"]),
                 words(r["opt"]), f"{r['lru'] / r['opt']:.2f}"] for r in o["rows"]]
        tab = grid_table([r"cache $k$ lines", r"LRU", r"FIFO", r"marking", r"random", r"OPT \ (Belady)",
                          r"LRU $/$ OPT"], rows, widths=[2.2, 1.4, 1.4, 1.6, 1.5, 2.2, 1.7], row_h=0.46, font_size=21,
                         mono_cols=(), colors=[[WHITE, DATA, GREY_A, LAM, GREY_A, YES, HEAD]] * len(rows))
        tab.next_to(head, DOWN, buff=0.45).set_x(0)
        notes = VGroup(
            label(rf"{words(o['requests'])} accesses to {o['distinct']} distinct 64-byte lines; \ faults when the cache "
                  r"holds $k$ of them", font_size=21, color=WHITE),
            label(r"Belady (1966): \ evict the line used \textbf{furthest in the future}: \ optimal, \ and impossible "
                  r"online", font_size=21, color=YES),
            label('finite trace outcomes for these capacities and separate seeds; \\ no universal winner',
                  font_size=21, color=DATA),
            label('marking: \\ expected $2H_k$ competitiveness for oblivious requests, \\ plus an initial additive term', font_size=21,
                  color=LAM),
        ).arrange(DOWN, buff=0.24).next_to(tab, DOWN, buff=0.4)
        with self.voiceover(
            (
            "We replay only the Job's data accesses, excluding instruction fetches. <bookmark mark='a'/> Its one "
            'hundred fifty-five thousand two hundred sixty-six accesses map to ninety-two distinct '
            'sixty-four-byte lines. The model is an initially empty fully associative cache with unit miss cost, '
            "not a hardware latency simulation. <bookmark mark='b'/> Belady evicts the page whose next use lies "
            'furthest ahead; offline next-use preprocessing is separate from online policy work. An independent '
            "full-trace simulator checks every displayed result. <bookmark mark='c'/> The table shows finite "
            'outcomes for these capacities and seeds, including least recently used, first in first out and '
            "random policies. <bookmark mark='d'/> Marking clears marks at a new phase and evicts a random "
            'unmarked resident. Its two-H-k expected competitive theorem assumes an oblivious request sequence '
            'and allows an additive initial term. These particular random outcomes establish no universal winner.'
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.25))
            for mk, n_ in zip("abcd", notes):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()

    def lower(self):
        o = load("online")
        head = label(r"Why $k$ is the best a deterministic cache can promise", font_size=30).to_edge(UP, buff=0.35)
        k = 4
        seq = list(range(k + 1)) * 3
        cells = VGroup(*[VGroup(Square(side_length=0.48, stroke_color=GREY_B, stroke_width=1.5), mono(str(p), 20, WHITE))
                         for p in seq]).arrange(RIGHT, buff=0.05)
        for c in cells:
            c[1].move_to(c[0])
        cells.next_to(head, DOWN, buff=0.5)
        cap = label(rf"$k = {k}$: \ cycle through $k + 1$ pages; \ LRU always evicts the next one needed", font_size=21,
                    color=NO).next_to(cells, DOWN, buff=0.2)
        rows = [[str(a["k"]), words(a["requests"]), words(a["lru"]), words(a["marking"]), words(a["opt"]),
                 f"{a['lru'] / a['opt']:.1f}"] for a in o["adv"]]
        tab = grid_table([r"$k$", r"requests", r"LRU faults", r"marking", r"OPT", r"LRU $/$ OPT"], rows,
                         widths=[0.9, 1.8, 2.0, 1.6, 1.4, 1.9], row_h=0.44, font_size=21, mono_cols=(),
                         colors=[[WHITE, GREY_A, NO, LAM, YES, HEAD]] * len(rows))
        tab.next_to(cap, DOWN, buff=0.4).set_x(0)
        notes = VGroup(
            label('LRU/FIFO: \\ $k$-competitive up to an additive term; \\\\ general deterministic lower bound uses a policy-adaptive request, \\ not this fixed cycle', font_size=21, color=HEAD),
            label(r"OPT evicts the page needed furthest away: \ about one fault per $k$ requests", font_size=21,
                  color=YES),
            label('model: \\ initially empty, \\ fully associative, \\ unit misses; \\ data accesses only',
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            (
            "A cyclic trace exposes one weakness of least recently used. <bookmark mark='a'/> Cycle over five "
            "pages with capacity four: every request misses under LRU. <bookmark mark='b'/> Offline OPT misses "
            'roughly once per four requests after its initial fills; the exact finite counts appear here. '
            "<bookmark mark='c'/> This fixed cycle alone does not defeat every deterministic policy. The general "
            "lower bound uses an adaptive request to a page absent from that policy's cache. LRU and FIFO are "
            "k-competitive with the usual additive constant. Randomized marking's expected two-H-k upper bound "
            "concerns oblivious sequences, not that adaptive adversary. <bookmark mark='d'/> Locality, capacity, "
            'associativity and replacement cost determine which model helps explain a real cache. This unit-cost '
            'trace study isolates only one part of that behavior.'
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(cells))
            vo.wait_until("a")
            self.play(FadeIn(cap), LaggedStart(*[c[0].animate.set_fill(NO, 0.4) for c in cells], lag_ratio=0.08))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.25), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[0]))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()
