from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs7.common import HEAD, NO, PART, YES, chapter, fmt, load, mono


def two_bit(outcomes):
    """A 2-bit saturating counter's guesses for a branch's outcomes (state 0-3, taken if >= 2), starting weakly
    not taken."""
    s, guesses = 1, []
    for t in outcomes:
        guesses.append(s >= 2)
        s = min(3, s + 1) if t else max(0, s - 1)
    return guesses


class Sorted(WatchScene):
    def construct(self):
        chapter(self, 14, r"The puzzle, solved", r"Why does sorting the data make a loop faster?", lit=(2012,),
                extra=((2012, r"the sorted-array question"),))
        self.replay()
        self.stream()
        self.pebble()
        self.branchless()

    # ------------------------------------------------------------------
    def replay(self):
        h = load("sorted")["host"]
        race = Race([(r"sorted", h["sorted"], YES), (r"shuffled", h["random"], NO)], unit="ms", scale=1e3,
                    fmt="{:.1f}", width=7.6, lane_h=0.6, gap=0.55, font_size=30).move_to(UP * 0.3)
        q = label(r"the same additions, \ in a different order", font_size=30, color=GREY_A).next_to(race, UP,
                                                                                                  buff=0.7)
        with self.voiceover(
            f"Back to where we started. The same loop, {h['ratio']:.0f} times slower on shuffled data. You now "
            "have everything you need to explain it."
        ):
            self.play(FadeIn(q), FadeIn(race.lanes), *[FadeIn(c) for c in race.clocks])
            self.add(*race.bars)
            race.go(self, seconds=3.0)
        race.freeze()
        self.clear_scene()

    # ------------------------------------------------------------------
    def stream(self):
        rng = np.random.default_rng(3)
        data = rng.integers(0, 256, 3000)  # the values compute_sorted scans
        n = 56
        rows = []
        srt = np.sort(data)
        cross = int(np.searchsorted(srt, 128))  # where the sorted outcomes switch from not taken to taken
        for vals in (data, srt[cross - 30:]):
            out = [bool(v >= 128) for v in vals[:n]]
            g = two_bit(out)
            rows.append(([(YES if t else GREY_C, None) for t in out],
                         [((NO, "x") if a != t else (GREY_E, None)) for a, t in zip(g, out)], sum(a != t for a, t in
                                                                                             zip(g, out))))
        strips = VGroup()
        for k, (o, m, _) in enumerate(rows):
            st = EventStrip([o, m], names=[r"\texttt{if} taken?", r"2-bit miss"], window=24, cell=0.32)
            strips.add(st)
        strips.arrange(DOWN, buff=1.1).move_to(LEFT * 0.2 + DOWN * 0.1)
        heads = VGroup(label(r"shuffled", font_size=30, color=NO).next_to(strips[0], UP, buff=0.2),
                       label(r"sorted", font_size=30, color=YES).next_to(strips[1], UP, buff=0.2))
        t = strips[0].t
        strips[1].t = t
        miss = [np.cumsum([1 if c[1] else 0 for c in r[1]]) for r in rows]
        meters = VGroup(*[Meter(r"misses", t, values=np.concatenate([[0], m_]), fmt="{:.0f}", color=c, font_size=26)
                          .next_to(s_, RIGHT, buff=0.35) for m_, c, s_ in zip(miss, (NO, YES), strips)])
        src = tag("illustrative", rf"the first {n} values; a 2-bit counter").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Watch the branch inside the loop, one value at a time. <bookmark mark='a'/> On shuffled data, taken or "
            "not is a coin flip. A predictor learns nothing, and misses about half the time. <bookmark mark='b'/> On "
            "sorted data it's one long run of not taken, then one long run of taken. The predictor misses once at the "
            "switch, and that's it."
        ) as vo:
            self.play(FadeIn(heads), FadeIn(strips[0].labels), FadeIn(strips[1].labels), FadeIn(src))
            self.add(strips, meters)
            vo.wait_until("a")
            strips[0].advance(self, 30, per_step=0.16)
            vo.wait_until("b")
            strips[0].advance(self, n - 30, per_step=0.12)
        for m in meters:
            m.num.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def pebble(self):
        p = load("sorted")["pebble"]
        h = load("sorted")["host"]
        ratio = p["random"]["cycles"] / p["sorted"]["cycles"]
        race = Race([(r"sorted", p["sorted"]["cycles"], YES), (r"shuffled", p["random"]["cycles"], NO)],
                    unit="cycles", fmt="{:,.0f}", width=5.8, lane_h=0.55, gap=0.5, font_size=28).move_to(
            LEFT * 0.9 + DOWN * 0.4)
        src = tag("simulated", r"Pebble's pipeline: 3,000 values, scanned twice").to_corner(DR, buff=0.3)
        mis = label(rf"misses: \ {fmt(p['random']['mispredicts'])} \ against \ {p['sorted']['mispredicts']}",
                    font_size=30, color=HEAD).next_to(race, UP, buff=0.7)
        self.play(FadeIn(mis), FadeIn(src))
        card = self.predict(rf"Pebble misses {fmt(p['random']['mispredicts'])} times against "
                            rf"{p['sorted']['mispredicts']}. \\ How much slower is the shuffled run?",
                            [r"about $1.1\times$", r"about $2\times$", rf"about ${h['ratio']:.0f}\times$, like this "
                                                                        r"computer"],
                            narration="Same experiment on Pebble's pipeline. Three thousand misses against fourteen. "
                                      "How much slower is the shuffled run? Barely? Twice? Or "
                                      f"{h['ratio']:.0f} times, like the real computer?", room=mis)
        self.park(card)
        self.play(FadeIn(race.lanes), *[FadeIn(c) for c in race.clocks])
        self.add(*race.bars)
        race.go(self, seconds=3.5)
        race.freeze()
        self.reveal(card, 0 if ratio < 1.5 else 1, narration=(
            f"Only {ratio:.2f} times. A wrong guess costs Pebble two cycles: it's a short pipe, and it does one thing "
            "at a time. A modern core is deep and wide. On each wrong guess it throws away many cycles of work for "
            "several instructions at once, and the rest of this loop is nearly free. So the misses are almost all "
            "of the time."))
        self.clear_scene()

    # ------------------------------------------------------------------
    def branchless(self):
        h = load("sorted")["host"]
        code = VGroup(mono("sltiu t3, t2, 128     # 1 if small", 24), mono("addi  t3, t3, -1      # all ones if big", 24),
                      mono("and   t3, t3, t2", 24), mono("add   a0, a0, t3      # adds x, or 0", 24)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).move_to(UP * 0.4)
        with self.voiceover(
            "Or remove the branch altogether. Compare, and turn the answer into a mask: all ones "
            "for a big value, zeros for a small one. AND it with x, and add. Nothing to guess."
        ):
            self.play(LaggedStart(*[Write(c) for c in code], lag_ratio=0.35), run_time=2.4)
        card = self.predict(r"Without the branch, \ the shuffled loop takes...",
                            [rf"still about {h['random'] * 1e3:.0f} ms", rf"about {h['random_branchless'] * 1e3:.0f} ms",
                             r"under 1 ms"],
                            narration="On this computer, the shuffled loop took "
                                      f"{h['random'] * 1e3:.0f} milliseconds. Without the branch, how long?",
                            room=code)
        self.park(card)
        self.play(FadeOut(code))
        race = Race([(r"sorted", h["sorted"], YES), (r"branchless, \ sorted", h["sorted_branchless"], HEAD),
                     (r"branchless, \ shuffled", h["random_branchless"], HEAD), (r"shuffled", h["random"], NO)],
                    unit="ms", scale=1e3, fmt="{:.1f}", width=6.8, lane_h=0.45, gap=0.38, font_size=24,
                    name_width=3.2).move_to(DOWN * 0.5 + RIGHT * 0.4)
        src = tag("measured", rf"{h['reps']} passes, median of five").to_corner(DL, buff=0.3)
        self.play(FadeIn(race.lanes), *[FadeIn(c) for c in race.clocks], FadeIn(src))
        self.add(*race.bars)
        race.go(self, seconds=6.0)
        race.freeze()
        self.reveal(card, 1, narration=(
            f"About {h['random_branchless'] * 1e3:.0f} milliseconds, and the order no longer matters. It's a little "
            "slower than the lucky sorted run, because it always does both halves of the work. Compilers make this "
            "trade with conditional moves, and databases, codecs and trading systems write branch-free inner loops "
            "on purpose."))
        self.clear_scene()
