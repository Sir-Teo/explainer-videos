from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs5.common import (BG, CLOCK, CODE, COST, CTRL, DATA, FUNC, HEAD, INF, NO, PART, WIRE, YES, load, sci,
                                  wave)


def box(w, h, text, color=CTRL, font_size=24):
    b = RoundedRectangle(width=w, height=h, corner_radius=0.1, stroke_color=color, stroke_width=2.5, fill_color=BG,
                         fill_opacity=1)
    return VGroup(b, MathTex(text, font_size=font_size, color=color).move_to(b))


class Meta(VoiceoverScene):
    def construct(self):
        self.card()
        self.violation()
        self.histogram()
        self.mtbf()
        self.synchronizer()
        self.buridan()

    def card(self):
        card = chapter_card(5, r"Metastability", r"What happens when the outside world ignores the clock?",
                            lit=(1973,), part=PART)
        with self.voiceover("Chapter five. Metastability."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def violation(self):
        d = load("latch")["violation"]
        head = label(r"Change $D$ exactly at the edge", font_size=38).to_edge(UP, buff=0.35)
        n = len(d["C"])
        dx = 11.0 / n
        x0 = -5.2
        ws = VGroup(wave(d["C"], x0=x0, y=1.0, dx=dx, color=CLOCK, name=r"\text{clk}"),
                    wave(d["D"], x0=x0, y=0.1, dx=dx, color=DATA, name="D"),
                    wave(d["M"], x0=x0, y=-0.8, dx=dx, color=GREY_B, name="M"),
                    wave(d["Q"], x0=x0, y=-1.7, dx=dx, color=NO, name="Q"))
        e = DashedLine([x0 + dx * 6, 1.8, 0], [x0 + dx * 6, -1.9, 0], color=CLOCK, stroke_width=2)
        txt = VGroup(label(r"the same flip-flop as chapter 3, \ simulated gate by gate", font_size=24, color=GREY_A),
                     label(r"the master oscillates before it settles: \ $Q$ is neither 0 nor 1 for several gate delays",
                           font_size=26, color=NO)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.5)
        rng = np.random.default_rng(5)
        ck = wave([k % 2 for k in range(22)], x0=-5.5, y=1.2, dx=0.5, h=0.5, color=CLOCK, name=r"\text{clk}")
        edges = [-5.5 + 0.5 * k for k in range(1, 22, 2)]
        arr = sorted(rng.uniform(-5.4, 5.4, 14))
        ticks, hot = VGroup(), []
        for xx in arr:
            near = min(abs(xx - e) for e in edges) < 0.12
            if near:
                hot.append(len(ticks))
            ticks.add(Line([xx, -0.2, 0], [xx, 0.5, 0], color=NO if near else DATA, stroke_width=4 if near else 2.5))
        tl = label(r"changes from outside, \ at arbitrary times: \ some land right on an edge", font_size=24,
                   color=GREY_A).next_to(ticks, DOWN, buff=0.4)
        tl.set_x(0)
        intro = VGroup(ck, ticks, tl)
        with self.voiceover(
            "Inside a single clocked circuit, setup and hold can always be met: the designer controls every path. "
            "But signals from outside, a key press, a network packet, a sensor, arrive whenever they like. "
            "<bookmark mark='a'/> Here is the flip-flop of chapter three again, simulated gate by gate, with D "
            "changing on the very tick of the clock edge. <bookmark mark='b'/> The master latch is caught half shut, "
            "with its two halves fighting, and in this model they oscillate for several gate delays before the slave "
            "copies out a value. For that time, Q is not a valid zero or one. In a real circuit the voltages hover "
            "near the saddle instead of oscillating, but the effect is the same: an output that is late by an amount "
            "nobody chose."
        ) as vo:
            self.play(FadeIn(head), Create(ck))
            self.play(LaggedStart(*[GrowFromPoint(t, t.get_bottom()) for t in ticks], lag_ratio=0.25), run_time=3.5)
            self.play(FadeIn(tl), *[Indicate(ticks[i], color=NO, scale_factor=1.5) for i in hot])
            vo.wait_until("a")
            self.play(FadeOut(intro))
            self.play(LaggedStart(*[Create(w) for w in ws[:2]], lag_ratio=0.2), Create(e), FadeIn(txt[0]))
            vo.wait_until("b")
            self.play(Create(ws[2]), Create(ws[3]), run_time=2.0)
            self.play(FadeIn(txt[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def histogram(self):
        d = load("meta")
        head = label(r"How long does it take to decide?", font_size=36).to_edge(UP, buff=0.3)
        hist, edges = d["hist"], d["edges"]
        ax = Axes(x_range=[0, 12, 2], y_range=[0, 14000, 3500], x_length=5.8, y_length=4.0, tips=False,
                  axis_config={"color": GREY_C, "font_size": 18, "include_numbers": True}).move_to(LEFT * 3.2 + DOWN * 0.4)
        bars = VGroup()
        for h, a, b in zip(hist, edges[:-1], edges[1:]):
            if h == 0:
                continue
            r = Rectangle(width=ax.c2p(b, 0)[0] - ax.c2p(a, 0)[0], height=ax.c2p(0, h)[1] - ax.c2p(0, 0)[1],
                          stroke_width=0.5, stroke_color=BG, fill_color=HEAD, fill_opacity=0.8)
            bars.add(r.move_to(ax.c2p((a + b) / 2, 0), aligned_edge=DOWN))
        xl = note(r"resolution time \ (units of $\tau$)", font_size=20).next_to(ax, DOWN, buff=0.35)
        yl = note(r"40{,}000 random arrivals", font_size=20).next_to(ax, UP, buff=0.1)
        # survival on a log scale
        ax2 = Axes(x_range=[0, 12, 2], y_range=[-5, 0, 1], x_length=5.0, y_length=4.0, tips=False,
                   axis_config={"color": GREY_C, "font_size": 18}).move_to(RIGHT * 3.6 + DOWN * 0.4)
        yl2 = VGroup(*[MathTex(rf"10^{{{k}}}", font_size=20, color=GREY_B).next_to(ax2.c2p(0, k), LEFT, buff=0.1)
                       for k in range(-5, 1)])
        sv = [(t, p) for t, p in d["surv"] if p > 0]
        curve = VMobject(color=NO, stroke_width=3).set_points_as_corners([ax2.c2p(t, np.log10(p)) for t, p in sv])
        l2 = MathTex(r"P(t > T) \propto e^{-\lambda T}", font_size=32, color=NO).next_to(ax2.c2p(5, -1), UR, buff=0.1)
        t2 = note(r"fraction still undecided \ (log scale)", font_size=20).next_to(ax2, UP, buff=0.1)
        with self.voiceover(
            "How late? Use the dynamical system of chapter two. <bookmark mark='a'/> A data edge arrives at a random "
            "moment near the clock edge and leaves the latch with a small random imbalance. Here are forty thousand "
            "such arrivals, each integrated until the latch reaches a clean value. Most decide quickly. But the "
            "histogram has a long tail. <bookmark mark='b'/> Plot the fraction still undecided on a logarithmic "
            "scale, and the tail is a straight line: the probability of taking longer than T falls like e to the "
            "minus lambda T, with lambda the saddle's unstable eigenvalue. Waiting one more unit of time makes failure "
            "e squared, about seven, times less likely; but no amount of waiting makes it impossible."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.04), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(ax2), FadeIn(yl2), FadeIn(t2))
            self.play(Create(curve), FadeIn(l2), run_time=1.6)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mtbf(self):
        m = load("meta")["mtbf"]
        head = label(r"Mean time between failures", font_size=38).to_edge(UP, buff=0.35)
        f = MathTex(r"\mathrm{MTBF} = \frac{e^{\,t_r / \tau}}{T_0\, f_{clk}\, f_{data}}", font_size=48, color=CODE).move_to(
            UP * 1.5)
        terms = VGroup(
            label(r"$t_r$: \ the time allowed to resolve", font_size=22, color=GREY_A),
            label(r"$\tau$: \ the latch's time constant", font_size=22, color=GREY_A),
            label(r"$T_0 f_{clk} f_{data}$: \ how often data lands \\ inside the dangerous window", font_size=22,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(f, DOWN, buff=0.35)
        ex = VGroup(
            label(rf"$\tau = T_0 = 20$ ps, \ 1 GHz clock, \ data changing at 100 MHz", font_size=26, color=GREY_B),
            label(rf"one flip-flop, \ $t_r = 0.5$ ns: \ a failure every {m['one_hours']:.0f} hours", font_size=30,
                  color=NO),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.35)
        f.move_to(UP * 1.9 + LEFT * 3.0).scale(0.85)
        terms.next_to(f, DOWN, buff=0.35)
        tau, rate = 20e-12, 20e-12 * 1e9 * 1e8
        ax = Axes(x_range=[0, 1.6, 0.4], y_range=[-6, 30, 6], x_length=5.4, y_length=3.6, tips=False,
                  axis_config={"color": GREY_C, "font_size": 18}).move_to(RIGHT * 3.3 + UP * 0.45)
        ax.x_axis.add_numbers([0.4, 0.8, 1.2, 1.6], font_size=18)
        ylab = VGroup(*[MathTex(rf"10^{{{k}}}", font_size=18, color=GREY_B).next_to(ax.c2p(0, k), LEFT, buff=0.08)
                        for k in (0, 12, 24)])
        axl = VGroup(note(r"$t_r$ (ns)", font_size=20).next_to(ax.x_axis, DOWN, buff=0.35),
                     note(r"MTBF in seconds \ (log scale)", font_size=20).next_to(ax, UP, buff=0.08))

        def lg(t_ns):
            return (t_ns * 1e-9 / tau) / np.log(10) - np.log10(rate)

        curve = ax.plot(lg, x_range=[0, 1.6], color=YES, stroke_width=3)
        refs = VGroup()
        for val, name in ((np.log10(86400), r"a day"), (np.log10(4.35e17), r"age of the universe")):
            refs.add(VGroup(DashedLine(ax.c2p(0, val), ax.c2p(1.6, val), color=GREY_D, stroke_width=1.5),
                            note(name, font_size=18).next_to(ax.c2p(0.02, val), UR, buff=0.04)))
        p1 = Dot(ax.c2p(0.5, lg(0.5)), color=NO, radius=0.08)
        p1l = note(r"10 hours", font_size=18).next_to(p1, RIGHT, buff=0.1)
        slope = label(r"every extra $\tau$ \ multiplies it by $e$", font_size=20, color=HEAD).next_to(
            ax.c2p(0.9, lg(0.9)), RIGHT, buff=0.2)
        with self.voiceover(
            "Engineers turn this into a single number. <bookmark mark='a'/> The mean time between failures grows "
            "exponentially with the time t r allowed for resolving, divided by the latch's time constant tau, and "
            "falls with how often the data changes inside the dangerous window around the clock edge. "
            "<bookmark mark='b'/> With typical numbers, twenty-picosecond constants, a one gigahertz clock and data "
            "changing a hundred million times a second, a single flip-flop given half a nanosecond to settle fails "
            "about once every ten hours. For a chip that runs for years, that is a disaster."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f), FadeIn(terms))
            self.play(Create(ax), FadeIn(ylab), FadeIn(axl), FadeIn(refs))
            self.play(Create(curve), FadeIn(slope), run_time=1.6)
            vo.wait_until("b")
            self.play(FadeIn(ex[0]))
            self.play(FadeIn(ex[1]), FadeIn(p1, scale=2), FadeIn(p1l))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def synchronizer(self):
        m = load("meta")["mtbf"]
        head = label(r"The two-flip-flop synchronizer", font_size=38).to_edge(UP, buff=0.35)
        f1 = box(1.4, 1.0, r"\text{FF}_1", NO).move_to(LEFT * 2.2 + UP * 1.2)
        f2 = box(1.4, 1.0, r"\text{FF}_2", YES).move_to(RIGHT * 1.0 + UP * 1.2)
        a0 = Arrow(f1.get_left() + LEFT * 1.6, f1.get_left(), buff=0, color=DATA, stroke_width=3)
        a1 = Arrow(f1.get_right(), f2.get_left(), buff=0.08, color=WIRE, stroke_width=3)
        a2 = Arrow(f2.get_right(), f2.get_right() + RIGHT * 1.6, buff=0, color=WIRE, stroke_width=3)
        l0 = label(r"from outside", font_size=22, color=DATA).next_to(a0, UP, buff=0.1)
        l1 = label(r"may hover \\ for a while", font_size=20, color=NO).next_to(a1, UP, buff=0.1)
        l2 = label(r"safe", font_size=22, color=YES).next_to(a2, UP, buff=0.1)
        res = VGroup(
            label(rf"a whole extra clock cycle to resolve: \ $t_r = 1.5$ ns", font_size=26, color=GREY_A),
            MathTex(rf"e^{{1.5\,\text{{ns}} / 20\,\text{{ps}}}} = e^{{75}} \quad \Rightarrow \quad \text{{MTBF}} \approx "
                    rf"{sci(m['two_years'], 1)} \ \text{{years}}", font_size=34, color=YES),
            label(r"hundreds of millions of times the age of the universe, \ for one cycle of latency", font_size=26,
                  color=HEAD),
            note(r"every clock-domain crossing on every chip is built this way; \ getting it wrong is a classic, \\ "
                 r"rare, \ unreproducible hardware bug", font_size=22),
        ).arrange(DOWN, buff=0.28).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "The cure is cheap. <bookmark mark='a'/> Send the outside signal through two flip-flops in a row. The "
            "first one may go metastable. But nobody looks at its output until the next clock edge, a whole cycle "
            "later, and only the second flip-flop does. <bookmark mark='b'/> That extra cycle multiplies the time "
            "allowed to resolve, and because the failure rate falls exponentially with that time, the mean time "
            "between failures becomes about ten to the eighteen years, hundreds of millions of times the age of the "
            "universe, for the price of one cycle of delay. <bookmark mark='c'/> Every place where signals cross from one clock to "
            "another on every chip uses a synchronizer like this. Thomas Chaney and Charles Molnar measured the "
            "effect convincingly in 1973, after years in which many engineers refused to believe in it; forgetting "
            "it still produces the rarest and most maddening hardware bugs."
        ) as vo:
            self.play(FadeIn(head), FadeIn(f1), FadeIn(f2), GrowArrow(a0), GrowArrow(a1), GrowArrow(a2), FadeIn(l0))
            vo.wait_until("a")
            self.play(FadeIn(l1), FadeIn(l2))
            vo.wait_until("b")
            self.play(FadeIn(res[0]))
            self.play(Write(res[1]), FadeIn(res[2]))
            vo.wait_until("c")
            self.play(FadeIn(res[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def buridan(self):
        head = label(r"Not a bad design: \ a theorem", font_size=38).to_edge(UP, buff=0.35)
        lam = load("meta")["lambda"]
        ax = Axes(x_range=[0, 1, 0.25], y_range=[0, 8, 2], x_length=5.2, y_length=3.8, tips=False,
                  axis_config={"color": GREY_C, "font_size": 18, "include_numbers": True}).move_to(LEFT * 3.6 + DOWN * 0.5)
        xs = np.concatenate([0.5 - np.geomspace(0.5, 1e-9, 200), 0.5 + np.geomspace(1e-9, 0.5, 200)])
        ys = np.minimum(np.log(0.9 / np.maximum(np.abs(xs - 0.5), 1e-9)) / lam + 1.8, 8)
        left = VMobject(color=HEAD, stroke_width=3).set_points_as_corners([ax.c2p(x, y) for x, y in zip(xs[:200], ys[:200])])
        right = VMobject(color=HEAD, stroke_width=3).set_points_as_corners([ax.c2p(x, y) for x, y in zip(xs[200:], ys[200:])])
        xl = note(r"when the input changed, \ relative to the clock edge", font_size=20).next_to(ax, DOWN, buff=0.35)
        yl = note(r"time to decide", font_size=20).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        q = VGroup(
            label(r"Buridan's principle \ (Lamport, 1984):", font_size=26, color=HEAD),
            label(r"a discrete decision \ based on an input \\ with a continuous range of values \\ cannot be made "
                  r"within a bounded time", font_size=26, color=GREY_A),
            label(r"the decision time is a continuous function of the input; \\ if it jumps from 0 to 1, \ somewhere "
                  r"in between \\ it must take arbitrarily long", font_size=22, color=GREY_B),
            label(r"synchronizers, \ arbiters \ and every network card \\ live with it; \ they cannot remove it",
                  font_size=24, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(RIGHT * 3.0 + DOWN * 0.2)
        with self.voiceover(
            "It is tempting to think a better flip-flop could eliminate metastability. It cannot, and the reason is "
            "a theorem. <bookmark mark='a'/> Plot the time a latch takes to decide against the moment the input "
            "changed, relative to the clock. Far from the edge it decides quickly. Near the edge it takes longer, and "
            "right at one critical moment, the time is unbounded. <bookmark mark='b'/> Leslie Lamport called this "
            "Buridan's principle, after the donkey that starved halfway between two bales of hay: a discrete decision "
            "based on an input with a continuous range of values cannot always be made in a bounded time. The "
            "argument is continuity. The physical state of any device depends continuously on its input, so if one "
            "input leads to zero and another to one, some input in between leads to a state that is neither, for as "
            "long as you care to wait. <bookmark mark='c'/> Engineers cannot remove the risk, only make it "
            "astronomically small, and that is exactly what the synchronizer does."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(left), Create(right), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x) for x in q[:3]], lag_ratio=0.4), run_time=2.4)
            vo.wait_until("c")
            self.play(FadeIn(q[3]))
        self.wait(0.3)
        self.clear_scene()

