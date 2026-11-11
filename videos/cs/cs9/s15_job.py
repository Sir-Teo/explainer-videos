from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs9.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, NO, PART, REFERENCE_GHZ, YES, bar_chart, fmt,
                                  load, sci, size_label)


class Job(VoiceoverScene):
    def construct(self):
        self.card()
        self.scans()
        self.without()
        self.price()
        self.ledger()

    def card(self):
        card = chapter_card(14, r"The Job meets memory", "What does the sampled memory model project?", part=PART)
        with self.voiceover(
            "Chapter fourteen. The Job meets memory."
        ):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def scans(self):
        sc = load("scans")
        head = label("Table-length prefix stream: \\ exact LRU counting within this model", font_size=34).to_edge(UP, buff=0.3)
        idea = VGroup(
            label(r"nonempty length-field scan: \ lines $0,1,\dots,e$; \ empty scan: no lines", font_size=23, color=GREY_A),
            label("repeated line $\\ell$ hits FA-LRU \\ $\\iff$ \\ previous covering scan had at most $C$ lines", font_size=24, color=HEAD),
            label(rf"so {sc['words'] / 1e6:.1f} million scans give all {sc['line_reads'] / 1e9:.1f} billion line reads' "
                  r"fates, \ in seconds", font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.18).next_to(head, DOWN, buff=0.3)
        rows = sc["rows"]
        ax = Axes(x_range=[0, len(rows) - 1, 1], y_range=[0, 1, 0.25], x_length=8.0, y_length=2.8, tips=False,
                  axis_config={"color": GREY_C, "font_size": 16}).to_edge(DOWN, buff=0.75)
        ax.y_axis.add_numbers([0, 0.5, 1], font_size=16, num_decimal_places=1)
        xt = VGroup(*[label(size_label(r["kb"] * 1024), font_size=15, color=GREY_B).next_to(ax.c2p(k, 0), DOWN,
                                                                                           buff=0.1)
                      for k, r in enumerate(rows)])
        lru = VMobject(color=NO, stroke_width=4).set_points_as_corners([ax.c2p(k, r["lru"]) for k, r in enumerate(rows)])
        front = VMobject(color=YES, stroke_width=4).set_points_as_corners(
            [ax.c2p(k, r["keep_front"]) for k, r in enumerate(rows)])
        ll = label(r"LRU", font_size=20, color=NO).next_to(ax.c2p(3, rows[3]["lru"]), UP, buff=0.1)
        lf = label("pin $C-1$ lines; \\ one transient slot", font_size=20, color=YES).next_to(ax.c2p(5, rows[5]["keep_front"]),
                                                                                   LEFT, buff=0.1)
        with self.voiceover(
            "The table-only prefix model allows exact LRU counting without expanding billions of visits. <bookmark "
            "mark='a'/> A scan touches lines zero through its end index. This is an abstract line stream, excluding "
            "letter traffic and stores. <bookmark mark='b'/> Between two references to line l, let e be the end "
            "index of the latest earlier scan that reached l. Exactly e distinct other lines intervene. A repeated "
            "reference therefore hits a fully associative C-line LRU cache if e is less than C, equivalently if that "
            "earlier covering scan had at most C lines. <bookmark mark='c'/> The cached-prefix method evaluates this model "
            "over all recorded scan ends. <bookmark mark='d'/> The green comparator pins C minus one front lines and "
            "uses one transient slot. Its achievable miss count upper-bounds MIN under matching forced-insertion "
            "rules; it is not MIN's exact miss count."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abc", idea):
                if mk != 'a':
                    vo.wait_until(mk)
                self.play(FadeIn(it))
                if mk == 'a':
                    vo.wait_until(mk)
            vo.wait_until("d")
            self.play(Create(ax), FadeIn(xt))
            self.play(Create(lru), FadeIn(ll), run_time=1.5)
            self.play(Create(front), FadeIn(lf), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def without(self):
        sc = load("scans")
        j = load("job")
        lat = j["clocks"]["pebble"]["latencies"]
        dram_s = sc["line_reads"] * lat[3] / (884.9557522123894e6)
        head = label(r"And with no cache at all?", font_size=36).to_edge(UP, buff=0.4)
        lines = VGroup(
            label(rf"{sc['line_reads'] / 1e9:.1f} billion table-line visits \ $\times$ \ {lat[3]}-cycle large-set proxy",
                  font_size=26, color=NO),
            label(rf"$\approx$ {dram_s / 60:.0f} serial-delay minutes; \ compare with a separate fitted projection", font_size=25,
                  color=HEAD),
            label("serial waiting budget, \\ not a measured no-cache corpus runtime", font_size=24,
                  color=YES),
        ).arrange(DOWN, buff=0.4).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is a deliberately serialized waiting-budget calculation. <bookmark mark='a'/> Assign the selected "
            "large-working-set delay to every abstract table-line visit, convert it at the assumed Pebble clock, and "
            "allow no overlap. <bookmark mark='b'/> The product is the displayed number of minutes. It is neither a "
            "measured no-cache corpus execution nor a general lower or upper bound for actual runtime: real transfer "
            "size, reuse, bandwidth, parallelism and instruction work all matter. <bookmark mark='c'/> Compare it "
            "with the fitted ledger only as an illustration of how assumptions change the apparent cost. The later "
            "projection uses separate sampled events and simplified microbenchmarks; it does not prove that a "
            "physical hierarchy makes this entire waiting budget disappear."
        ) as vo:
            self.play(FadeIn(head))
            for mk, l in zip("abc", lines):
                if mk != 'a':
                    vo.wait_until(mk)
                self.play(FadeIn(l, shift=UP * 0.1))
                if mk == 'a':
                    vo.wait_until(mk)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def price(self):
        j = load("job")
        head = label(r"What the misses cost", font_size=36).to_edge(UP, buff=0.35)
        p = j["clocks"]["pebble"]
        n = j["clocks"]["comparison clock"]
        lines = VGroup(
            label(rf"sampled events: \ {100 * j['m_table']:.0f}\% table and {100 * j['m_pool']:.0f}\% first-letter "
                  r"events miss modeled L1", font_size=24, color=GREY_A),
            label(rf"assumed 885 MHz \ (cumulative proxies {', '.join(map(str, p['latencies']))} cycles): \ "
                  rf"fitted increment $+{100 * j['change']:.2f}\%$", font_size=23, color=YES),
            label(rf"turn off the prefetcher: \ $+{100 * j['no_prefetch_change']:.1f}\%$", font_size=24, color=CTRL),
            label(rf"illustrative {REFERENCE_GHZ:g} GHz \ ({', '.join(map(str, n['latencies']))} cycles): \ "
                  rf"$+{100 * n['prefetch']['extra_cycles'] / j['row2']['cycles']:.0f}\%$", font_size=24, color=NO),
        ).arrange(DOWN, buff=0.35).move_to(DOWN * 0.1)
        with self.voiceover(
            "This projection combines four sampled corpus windows with synthetic scan and first-letter benchmarks on "
            "the functional core. The abstract corpus table and pool are relocated into disjoint regions; this is "
            "not a full execution of the unchanged Pebble memory image. <bookmark mark='a'/> The fractions describe "
            "coalesced table events and first-letter pool events in those windows. Later matching bytes, target "
            "reads and stores are omitted from that sampling model. <bookmark mark='b'/> Weight the measured model "
            "increments at the assumed Pebble clock to obtain the displayed extra cycles. <bookmark mark='c'/> "
            "Disabling the immediate free prefetch rule gives a separate projection. <bookmark mark='d'/> Repricing "
            "the same timing proxies at an illustrative faster clock changes the cycle costs. Bandwidth, prefetch "
            "lead time, queuing and complete write traffic are absent, so small fitted overheads are conditional "
            "model results, not hardware guarantees."
        ) as vo:
            self.play(FadeIn(head))
            for mk, l in zip("abcd", lines):
                if mk != 'a':
                    vo.wait_until(mk)
                self.play(FadeIn(l, shift=UP * 0.1))
                if mk == 'a':
                    vo.wait_until(mk)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ledger(self):
        j = load("job")
        head = label(r"Ledger row 3", font_size=38).to_edge(UP, buff=0.35)
        rows = j["ledger"] + [{"part": p_, "label": t} for p_, t in ((10, r"four cores"), (13, r"an optimizing compiler"),
                                                                     (16, r"sort, then count"), (17, r"a hash table"))]
        led = ledger_table(rows, shown=4, highlight=(3,), font_size=21, row_h=0.4, label_width=4.8).move_to(DOWN * 0.3)
        res = label(rf"{human_time(j['ledger'][2]['seconds'])} $\to$ {human_time(j['ledger'][3]['seconds'])}: \ "
                    r"conditional model increment; \ no full-corpus run or error bound", font_size=24,
                    color=COST).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Row three adds the modeled memory increments to Part 8's fitted corpus cycle estimate and divides by "
            "the same assumed clock. It remains a projection from counts, samples and short benchmarks, without a "
            "full-corpus run or an error bound. <bookmark mark='a'/> The abstract table-only stream still exposes a "
            "large amount of scanning work. Caching, overlap and prefetching affect the cost of that work under "
            "different assumptions; they do not change how many table entries the algorithm examines. Better data "
            "structures can reduce the work itself, which later parts investigate. Pointer-heavy programs, different "
            "clocks and finite-bandwidth memory systems require their own models and measurements. The near-equal "
            "ledger rows should motivate that investigation, not a conclusion that real memory is generally free."
        ) as vo:
            self.play(FadeIn(head), FadeIn(led.axis), LaggedStart(*[FadeIn(r) for r in led.rows], lag_ratio=0.1))
            vo.wait_until("a")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()
