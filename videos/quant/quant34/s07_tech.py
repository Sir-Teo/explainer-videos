from __future__ import annotations

import json
import math
from pathlib import Path

from explainer.quant import *  # noqa: F403
from videos.quant.quant34.common import BAD, FIRM_C, GOOD, HURDLE, PART, TECH_C, fit_right

# approximate coordinates of the two exchange data centres (degrees)
AURORA = (41.76, -88.32)      # CME Group's data centre, Aurora, Illinois
CARTERET = (40.58, -74.23)    # Nasdaq's data centre, Carteret, New Jersey
C_KM_MS = 299.792458          # km per millisecond in vacuum


def great_circle(a, b) -> float:
    la1, lo1, la2, lo2 = map(math.radians, (*a, *b))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * 6371.0 * math.asin(math.sqrt(h))


class Tech(VoiceoverScene):
    def construct(self):
        self.card()
        self.stack()
        self.languages()
        self.data()
        self.latency()
        self.colo()
        self.research()
        self.repro()
        self.question()

    def card(self):
        c = chapter_card(6, r"Technology", r"What does a quant firm build, and how fast must it be?", part=PART)
        with self.voiceover("Chapter six. A quant firm is a software company that happens to trade. What it builds "
                            "depends on its horizon: a fund rebalancing monthly needs clean data and careful research "
                            "code; a market maker needs every microsecond."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def stack(self):
        rows = [cmath(r"\text{data}", r":", r"\text{ticks, fundamentals, alternative; point in time, versioned}",
                      font_size=30, colors={r"\text{data}": TECH_C}),
                cmath(r"\text{research}", r":", r"\text{notebooks, clusters, GPUs; every trial logged}", font_size=30,
                      colors={r"\text{research}": TECH_C}),
                cmath(r"\text{production}", r":", r"\text{signals, portfolio, orders; the same code as research}",
                      font_size=30, colors={r"\text{production}": TECH_C}),
                cmath(r"\text{execution}", r":", r"\text{gateways, risk checks, exchange connections}", font_size=30,
                      colors={r"\text{execution}": TECH_C})]
        whys = [why(r"what the firm knew and when: a revised number used before its release is look-ahead (Part 26)"),
                why(r"where the trial counter lives; the House's caches and checksums are a small version of it"),
                why(r"a strategy that is reimplemented for production is a different strategy; firms run one code base"),
                why(r"Chapter 5's pre-trade checks, and the network to the exchange")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.45, edge=6.9)
        with self.voiceover(
            "The stack. <bookmark mark='a'/> Data, stored point in time, so the firm can say what it knew and when. "
            "<bookmark mark='b'/> Research: notebooks, clusters and GPUs, with every trial logged. "
            "<bookmark mark='c'/> Production, ideally the same code as research, because a strategy reimplemented for "
            "production is a different strategy. <bookmark mark='d'/> And execution: gateways, Chapter five's checks, "
            "and the connections to the exchanges."
        ) as vo:
            step(0)
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def languages(self):
        cards = VGroup(
            desk_question(r"OCaml at Jane Street", r"Yaron Minsky's \textit{OCaml for the Masses} (ACM Queue, 2011) "
                          r"explained why the firm writes its trading systems in a typed functional language: the "
                          r"compiler catches errors that would otherwise be found by losing money", width=12.4,
                          font_size=19),
            desk_question(r"C++ and hardware", r"where latency decides who trades, firms write C++ close to the "
                          r"hardware, bypass the operating system's network stack, and put logic on FPGAs", width=12.4,
                          font_size=19),
            desk_question(r"Python for research", r"most research is written in Python on top of compiled libraries, "
                          r"as in this series; the question is how it reaches production unchanged", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Languages, from the public record. <bookmark mark='a'/> Jane Street writes its systems in OCaml, and Yaron "
            "Minsky explained why in 2011: a strict type system catches errors before they cost money. "
            "<bookmark mark='b'/> Where latency decides who gets the trade, firms write C++ close to the hardware, "
            "bypass the operating system's network stack, and put logic on programmable chips. "
            "<bookmark mark='c'/> And most research is Python on compiled libraries, like this series; the hard part is "
            "getting it to production unchanged."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def data(self):
        rows = [cmath(r"\text{a day of US equity ticks}", r"\approx", r"\text{billions of messages}", font_size=32),
                cmath(r"\text{column stores}", r":", r"\text{kdb+/q and its successors}", font_size=32,
                      colors={r"\text{column stores}": TECH_C}),
                cmath(r"\text{point in time}", r":", r"\text{every value with the time it became known}", font_size=32,
                      colors={r"\text{point in time}": GOOD})]
        whys = [why(r"every quote and trade on every venue, time-stamped to the microsecond or nanosecond"),
                why(r"time-series data are stored by column, so a query over one field across a year reads only that "
                    r"field; Kx's kdb+ is the classic example"),
                why(r"Part 3's restated accounts and Part 28's revised text: the database keeps every version")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Data. <bookmark mark='a'/> A day of American equity quotes and trades runs to billions of messages, time-"
            "stamped to the microsecond. <bookmark mark='b'/> They are stored by column, so a question about one field "
            "over a year reads only that field: Kx's kdb+ is the classic example. <bookmark mark='c'/> And every value "
            "is stored with the time it became known, so restated accounts and revised numbers never leak into a "
            "backtest."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def latency(self):
        km = great_circle(AURORA, CARTERET)
        vac = km / C_KM_MS
        fib = vac * 1.47
        rows = [cmath(r"\text{Aurora, IL} \to \text{Carteret, NJ}", r"\approx", rf"{km:,.0f}\ \text{{km}}".replace(",", "{,}"),
                      font_size=32),
                cmath(r"\text{light in vacuum}", r":", rf"{vac:.2f}\ \text{{ms one way}}", font_size=34,
                      colors={r"\text{light in vacuum}": GOOD}),
                cmath(r"\text{light in fibre}", r":", rf"\times 1.47 = {fib:.2f}\ \text{{ms}}", font_size=34,
                      colors={r"\text{light in fibre}": BAD})]
        whys = [why(r"the great-circle distance between the futures exchange's data centre near Chicago and an equity "
                    r"exchange's in New Jersey"),
                why(r"the floor no technology can beat: the speed of light along the straightest path"),
                why(r"glass slows light by its refractive index, and cables do not run straight; signals through air, by "
                    r"microwave, travel at nearly the vacuum speed")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "How fast is fast? <bookmark mark='a'/> The futures that lead the American stock market trade in a data "
            f"centre near Chicago; the stocks, in New Jersey, about {km:.0f} kilometres away. "
            f"<bookmark mark='b'/> Light in vacuum covers that in {vac:.2f} milliseconds: the floor no technology can "
            f"beat. <bookmark mark='c'/> In glass fibre, slower by its refractive index, at least {fib:.1f}. In 2010 a "
            "firm dug a straighter fibre route between the two, and others then built microwave links, because signals "
            "through air travel at nearly the vacuum speed. The race is against physics, and it has nearly been won."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def colo(self):
        cards = VGroup(
            desk_question(r"colocation", r"exchanges rent space beside their matching engines, with equal cable lengths "
                          r"to every customer, so distance inside the building is the same for all", width=12.4,
                          font_size=19),
            desk_question(r"why speed is worth paying for", r"a market maker whose quote is stale when news arrives is "
                          r"picked off; speed is protection against adverse selection, as much as a way to take it "
                          r"(Part 38)", width=12.4, font_size=19),
            desk_question(r"the arms race, and its critics", r"Budish, Cramton and Shim (2015) argued that continuous "
                          r"markets reward tiny speed advantages, and proposed frequent batch auctions instead",
                          width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Inside the exchange's building. <bookmark mark='a'/> Exchanges rent space beside their matching engines, "
            "with equal cable lengths to every customer. <bookmark mark='b'/> Speed is worth paying for because a market "
            "maker whose quote is stale when news arrives gets picked off: speed is protection as much as attack. "
            "<bookmark mark='c'/> And critics, Eric Budish, Peter Cramton and John Shim, argued that continuous markets "
            "reward tiny speed advantages wastefully, and proposed auctions held many times a second instead. Part "
            "thirty-eight returns to this."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def research(self):
        rows = [cmath(r"\text{compute}", r":", r"\text{CPU clusters for backtests; GPUs for networks}", font_size=32),
                cmath(r"\text{a trial}", r"=", r"(\text{code},\ \text{data version},\ \text{parameters},\ \text{result})",
                      font_size=30, colors={r"\text{a trial}": FIRM_C}),
                cmath(r"\text{cheaper trials}", r"\Rightarrow", r"\text{more trials} \Rightarrow \text{a higher bar}",
                      font_size=32, colors={r"\text{a higher bar}": BAD})]
        whys = [why(r"backtests are embarrassingly parallel; training networks on market data needs GPUs (Parts 17, 27)"),
                why(r"a research platform records each trial completely, so any result can be rerun and every trial "
                    r"counted"),
                why(r"Part 29's lesson at the scale of a firm: computing power makes the multiple-testing problem worse, "
                    r"not better")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Research computing. <bookmark mark='a'/> Clusters of processors for backtests, which run in parallel "
            "trivially, and GPUs for networks. <bookmark mark='b'/> A good research platform records each trial "
            "completely: the code, the version of the data, the parameters and the result. <bookmark mark='c'/> And the "
            "lesson of Part twenty-nine, at the scale of a firm: cheaper trials mean more of them, and a higher bar for "
            "every result."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def repro(self):
        try:
            man = json.loads(Path("videos/quant/data/manifest.json").read_text())
            n_files = len(man.get("files", man)) if isinstance(man, dict) else len(man)
        except (OSError, ValueError):
            n_files = 0
        cards = VGroup(
            desk_question(r"the House's version", rf"every data file this series downloads is checked against a SHA-256 "
                          rf"digest in a manifest ({n_files} entries); every computed number is cached by name and "
                          r"recomputed from source on demand", width=12.4, font_size=19),
            desk_question(r"why it matters", r"a result that cannot be rerun cannot be reviewed, and a number that "
                          r"changed silently is a trial that was never counted", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.3)
        with self.voiceover(
            "And reproducibility. <bookmark mark='a'/> In the House, every data file is checked against a digest in a "
            f"manifest of {n_files} entries, and every number on screen is computed by named code and cached. "
            "<bookmark mark='b'/> That is not tidiness. A result that cannot be rerun cannot be reviewed, and a number "
            "that changed silently is a trial nobody counted."
        ) as vo:
            for k, mk in enumerate(("a", "b")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a microwave link saves 3 ms over fibre on a route. A futures move predicts a stock's move with an "
                       r"edge of 0.5 bp per trade. What is the speed worth, and to whom?")
        with self.voiceover(
            "Pause and predict. A microwave link saves three milliseconds over fibre. A futures move predicts a stock's "
            "next move with an edge of half a basis point a trade. What is the speed worth, and to whom?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
