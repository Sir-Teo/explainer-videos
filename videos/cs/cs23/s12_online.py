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
            label(r"no deterministic rule does better: \\ an adversary ends the season the day after you buy",
                  font_size=21, color=GREY_A),
            label(rf"randomized \ (Karlin et al., 1994): \\ $e/(e - 1) \approx {o['e_ratio']:.3f}$ in expectation",
                  font_size=21, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        if side.width > 5.6:
            side.width = 5.6
            side.to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "So far every algorithm saw its whole input. Many real decisions are made before the future arrives. "
            "<bookmark mark='a'/> Skis cost ten to buy, or one a day to rent, and you don't know how many days of snow "
            "there will be. <bookmark mark='b'/> Judge a strategy by its competitive ratio: in the worst case, how "
            "much more it pays than someone who knew the future, who would rent for short seasons and buy at once "
            "for long ones. <bookmark mark='c'/> Rent for nine days, then buy. If the season is short you paid what "
            "the clairvoyant paid; if it is long you paid nineteen instead of ten. Never more than twice. <bookmark "
            "mark='d'/> No deterministic rule does better, because an adversary who knows your rule can end the season "
            "the day after you buy. <bookmark mark='e'/> But if you buy on a random day, with the right "
            "probabilities, the adversary cannot aim, and the expected ratio falls to e over e minus one, about one "
            "point five eight. Our simulation of that rule paid fifteen point four for long seasons, against ten."
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
            label(r"LRU: \ 1.2 to 6.9 times the clairvoyant; \ randomized policies win once the cache is large",
                  font_size=21, color=DATA),
            label(r"marking: \ evict a random unmarked page; \ $2H_k$-competitive \ (Fiat et al., 1991)", font_size=21,
                  color=LAM),
        ).arrange(DOWN, buff=0.24).next_to(tab, DOWN, buff=0.4)
        with self.voiceover(
            "Caches face the same problem every nanosecond: when the cache is full and a new line arrives, which old "
            "one should go? <bookmark mark='a'/> We replayed the Job's memory trace from Part 9, a hundred and "
            "fifty-five thousand accesses to ninety-two distinct lines, through caches of eight to ninety-six lines, "
            "under several policies. <bookmark mark='b'/> Laszlo Belady showed in 1966 that the optimal policy evicts "
            "the line whose next use is furthest in the future. It is perfect, and impossible online, but it measures "
            "everyone else. <bookmark mark='c'/> Least recently used stays within a factor of about one and a "
            "fifth to seven of the clairvoyant here, and FIFO is close behind. <bookmark mark='d'/> Once the cache "
            "is large, the randomized policies win: the marking algorithm, which evicts a random page not used since "
            "the current phase began, and even plain random eviction. The Job sweeps through its tables in loops, "
            "and loops are exactly where LRU is weakest, as the next example shows."
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
            label(r"Sleator and Tarjan (1985): \ LRU and FIFO are $k$-competitive, \ and no deterministic policy is "
                  r"better \ (proved by this adversary)", font_size=21, color=HEAD),
            label(r"OPT evicts the page needed furthest away: \ about one fault per $k$ requests", font_size=21,
                  color=YES),
            label(r"yet real traces have locality, \ and LRU's approximations rule every cache \ (Parts 9 and 32)",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "How bad can least recently used be? <bookmark mark='a'/> Use a cache of four pages and request five "
            "pages in a cycle. The page LRU evicts is always the very next one requested, so every request is a "
            "fault. <bookmark mark='b'/> The clairvoyant evicts the page needed furthest away and faults about once "
            "every four requests. <bookmark mark='c'/> Daniel Sleator and Robert Tarjan founded competitive analysis "
            "with this example in 1985: LRU and FIFO are k-competitive, and the same adversary forces every "
            "deterministic policy to fault on every request, so none does better. Randomized marking cannot be "
            "trapped like this and pays a logarithmic factor, two H k. <bookmark mark='d'/> Real programs are kinder "
            "than adversaries, which is why approximations of LRU run every cache from Part 9 to Part 32."
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
