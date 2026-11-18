from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs7.common import CODE, COST, DATA, HEAD, NO, PART, YES, fmt, load, mono


def bars(values, width=5.6, height=1.5, color_hi=YES, color_lo=GREY_C, threshold=128):
    """The array as bars: values at least ``threshold`` (the ones the loop adds) lit."""
    n = len(values)
    dx = width / n
    g = VGroup()
    for k, v in enumerate(values):
        h = 0.06 + height * v / 255
        g.add(Rectangle(width=dx * 0.78, height=h, stroke_width=0, fill_color=color_hi if v >= threshold else color_lo,
                        fill_opacity=0.9).move_to([-width / 2 + dx * (k + 0.5), h / 2, 0]))
    return g


class Hook(WatchScene):
    """The cold open: the same loop over the same numbers, twelve times slower when they are shuffled."""

    def construct(self):
        self.race()
        self.why()
        self.title(PART)
        self.route()

    # ------------------------------------------------------------------
    def race(self):
        s = load("sorted")
        host = s["host"]
        code = VGroup(*[mono(t, 26) for t in ("for (i = 0; i < n; i++)", "    if (data[i] >= 128)",
                                              "        sum += data[i];")]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        code.move_to(UP * 2.55)
        rng = np.random.default_rng(3)
        vals = rng.integers(0, 256, 48)
        a = bars(vals).move_to(LEFT * 3.4 + DOWN * 0.35)
        b = bars(vals).move_to(RIGHT * 3.4 + DOWN * 0.35)
        order = np.argsort(vals, kind="stable")
        la = label(r"shuffled", font_size=28, color=NO).next_to(a, DOWN, buff=0.25)
        lb = label(r"sorted", font_size=28, color=YES).next_to(b, DOWN, buff=0.25)
        n = host["n"]
        with self.voiceover(
            "Here are three lines of C. <bookmark mark='a'/> Walk an array, and add up every value of at least a "
            "hundred and twenty-eight. <bookmark mark='b'/> Give it two copies of the same numbers. Leave one "
            "shuffled. <bookmark mark='c'/> Sort the other. Same values, same sum, the same additions, in a "
            "different order."
        ) as vo:
            self.play(LaggedStart(*[Write(c) for c in code], lag_ratio=0.4), run_time=2.2)
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(r, DOWN) for r in a], lag_ratio=0.02), FadeIn(la), run_time=1.6)
            vo.wait_until("c")
            src = a.copy()
            self.add(src)
            targets = [b[j] for j in range(len(vals))]
            # every bar of the shuffled copy flies to its place in the sorted one
            sorted_b = VGroup(*[targets[k].copy() for k in range(len(vals))])
            for k, j in enumerate(order):
                sorted_b[k].stretch_to_fit_height(a[j].height).set_fill(a[j].get_fill_color()).move_to(
                    [targets[k].get_center()[0], b.get_bottom()[1] + a[j].height / 2, 0])
            self.play(*[Transform(src[j], sorted_b[k], path_arc=-0.5) for k, j in enumerate(order)], FadeIn(lb),
                      run_time=2.4)
        card = self.predict(r"Which copy does this computer add up faster?",
                            [r"the shuffled one", r"the sorted one", r"neither: same work, same time"],
                            narration="Run the loop over each copy. Which finishes first: the shuffled one, the "
                                      "sorted one, or neither, because it's the same work?",
                            where="right", room=VGroup(code, a, src, la, lb))
        self.unpin(card)
        card.room = None
        self.play(FadeOut(VGroup(code, a, src, la, lb)), card.animate.scale(0.62).to_corner(UR, buff=0.3),
                  run_time=0.8)
        race = Race([(r"sorted", host["sorted"], YES), (r"shuffled", host["random"], NO)], unit="ms", scale=1e3,
                    fmt="{:.1f}", width=7.4, lane_h=0.62, gap=0.6, font_size=30).move_to(LEFT * 0.6 + DOWN * 0.9)
        what = tag("measured", rf"{n // 1024}K values, {host['reps']} passes").next_to(race, DOWN, buff=0.7)
        self.play(FadeIn(race.lanes), FadeIn(what), *[FadeIn(c) for c in race.clocks])
        self.add(*race.bars)
        self.mark("run")
        race.go(self, seconds=7.0)
        race.freeze()
        ratio = host["ratio"]
        verdict = label(rf"{ratio:.0f}$\times$ slower, \ for the same additions", font_size=38, color=HEAD).next_to(
            race, UP, buff=0.55)
        self.reveal(card, 1, narration=(
            f"The sorted copy finishes in {host['sorted'] * 1e3:.1f} milliseconds. The shuffled one takes "
            f"{host['random'] * 1e3:.0f}."))
        with self.voiceover(f"That's {ratio:.0f} times slower, for exactly the same additions."):
            self.play(Write(verdict), *[Indicate(c, color=HEAD) for c in race.clocks], run_time=1.2)
        self.clear_scene()

    # ------------------------------------------------------------------
    def why(self):
        s = load("sorted")["pebble"]
        r, so = s["random"], s["sorted"]
        guess = label(r"the processor doesn't wait for the \texttt{if}: \ it guesses", font_size=34).to_edge(
            UP, buff=0.5)
        # a branch fork: one path taken, the other abandoned
        start = Dot(LEFT * 4.6 + DOWN * 0.2, color=HEAD, radius=0.1)
        fork = Dot(LEFT * 1.6 + DOWN * 0.2, color=HEAD, radius=0.1)
        up = Line(fork.get_center(), RIGHT * 3.6 + UP * 1.3, color=YES, stroke_width=6)
        dn = Line(fork.get_center(), RIGHT * 3.6 + DOWN * 1.7, color=NO, stroke_width=6)
        trunk = Line(start.get_center(), fork.get_center(), color=HEAD, stroke_width=6)
        tl = label(r"guess right: \ keep going", font_size=26, color=YES).next_to(up.get_end(), UP, buff=0.15)
        dl = label(r"guess wrong: \ throw the work away", font_size=26, color=NO).next_to(dn.get_end(), DOWN,
                                                                                         buff=0.15)
        work = VGroup(*[RoundedRectangle(width=0.5, height=0.3, corner_radius=0.06, stroke_width=0, fill_color=DATA,
                                         fill_opacity=0.8) for _ in range(5)])
        tracker = ValueTracker(0.0)
        meters = VGroup(
            Meter(r"wrong guesses, \ shuffled", tracker, values=np.linspace(0, r["mispredicts"], 101), fmt="{:,.0f}",
                  color=NO, font_size=30),
            Meter(r"wrong guesses, \ sorted", tracker, values=np.linspace(0, so["mispredicts"], 101), fmt="{:,.0f}",
                  color=YES, font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(DOWN, buff=0.55)
        src = tag("simulated", r"Pebble's pipeline, the same loop").next_to(meters, RIGHT, buff=0.6)
        with self.voiceover(
            "Nothing in the C code explains that. The answer is inside the processor. <bookmark mark='a'/> It doesn't "
            "wait to learn which way the if will go. It guesses, and races ahead. <bookmark mark='b'/> Guess right, "
            "and the work it did early is kept. <bookmark mark='c'/> Guess wrong, and that work is thrown away. "
            "<bookmark mark='d'/> Run the same loop on Pebble, the computer we built from gates, and count the wrong "
            f"guesses. Shuffled: {r['mispredicts']:,}. Sorted: {so['mispredicts']}."
        ) as vo:
            self.play(FadeIn(guess, shift=DOWN * 0.1))
            vo.wait_until("a")
            self.play(GrowFromCenter(start), Create(trunk), GrowFromCenter(fork), run_time=0.9)
            work.arrange(RIGHT, buff=0.12).move_to(trunk)
            self.play(LaggedStart(*[FadeIn(w, shift=RIGHT * 0.3) for w in work], lag_ratio=0.15), run_time=0.8)
            vo.wait_until("b")
            self.play(Create(up), FadeIn(tl), work.animate.move_to(up.point_from_proportion(0.55)).rotate(
                np.arctan2(1.5, 5.2)), run_time=1.2)
            vo.wait_until("c")
            ghost = work.copy().set_fill(NO, 0.8).rotate(-np.arctan2(1.5, 5.2))
            ghost.move_to(trunk)
            self.play(Create(dn), FadeIn(dl), ghost.animate.move_to(dn.point_from_proportion(0.55)).rotate(
                -np.arctan2(1.9, 5.2)), run_time=1.2)
            self.play(ghost.animate.set_opacity(0).shift(DOWN * 0.6), run_time=0.6)
            vo.wait_until("d")
            self.play(FadeIn(meters), FadeIn(src))
            self.play(tracker.animate.set_value(100), run_time=2.5, rate_func=smooth)
        with self.voiceover(
            "By the end of this film you'll know what a wrong guess costs, to the cycle, on a machine we built. To "
            "get there, we turn Part 6's computer into an assembly line."
        ):
            self.play(Indicate(meters[0], color=NO), run_time=1.2)
        self.clear_scene()

    # ------------------------------------------------------------------
    def route(self):
        d = load("charts")["ideal"]
        flow = PipelineFlow(d).scale(0.95).move_to(DOWN * 0.2)
        steps = VGroup(*[chip(t, c, font_size=20, height=0.46) for t, c in (
            ("the iron law", COST), ("the assembly line", DATA), ("hazards", NO), ("guesses", HEAD),
            ("the Job", CODE))]).arrange(RIGHT, buff=0.3).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Part 6's Pebble works on one instruction at a time. <bookmark mark='a'/> Today it works on five at once. "
            "<bookmark mark='b'/> We'll define speed, build the assembly line, break it with hazards, repair it with "
            "guesses, and run the Job on it."
        ) as vo:
            self.play(FadeIn(flow.boxes), FadeIn(flow.regs), FadeIn(flow.readouts))
            vo.wait_until("a")
            flow.run(self, 0, 7, per_cycle=0.45, flash=False)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in steps], lag_ratio=0.25), run_time=1.6)
        flow.run(self, 7, len(flow.chart), per_cycle=0.4, flash=False)
        self.clear_scene()
