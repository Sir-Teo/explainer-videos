from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs37.common import (CCC, DATA, HEAD, KERN, LAM, NO, PART, WIN, YES, axes, grid_table, load)


class Mathis(VoiceoverScene):
    def construct(self):
        self.card()
        self.derive()
        self.measured()
        self.unfair()

    def card(self):
        card = chapter_card(8, r"The Mathis formula", r"How fast can a TCP go, given its loss rate?",
                            lit=(1997, 1998), extra=((1997, r"Mathis, Semke, \\ Mahdavi and Ott"),
                                                     (1998, r"Padhye et al.: \ with timeouts")), part=PART)
        with self.voiceover("Chapter eight. The Mathis formula."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def derive(self):
        head = label(r"One tooth of the sawtooth", font_size=36).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 3.2, 1], y_range=[0, 1.15, 0.5], x_length=6.0, y_length=3.4,
                  axis_config={"color": GREY_D, "include_numbers": False, "include_ticks": False}).move_to(
            [-3.4, -0.4, 0])
        W = 1.0
        pts = []
        for k in range(3):
            pts += [(k, W / 2), (k + 1, W)]
        tooth = VMobject(color=CCC["reno"], stroke_width=3).set_points_as_corners([ax.c2p(*p) for p in pts])
        drops = VGroup(*[DashedLine(ax.c2p(k + 1, W), ax.c2p(k + 1, W / 2), color=NO, dash_length=0.06)
                         for k in range(2)])
        wl = MathTex(r"W", font_size=28, color=WIN).next_to(ax.c2p(0, W), LEFT, buff=0.1)
        w2 = MathTex(r"W/2", font_size=28, color=WIN).next_to(ax.c2p(0, W / 2), LEFT, buff=0.1)
        span = Brace(Line(ax.c2p(1, 0), ax.c2p(2, 0)), DOWN, color=GREY_B)
        sl = MathTex(r"W/2 \text{ round trips}", font_size=24, color=GREY_B).next_to(span, DOWN, buff=0.08)
        steps = VGroup(
            MathTex(r"\text{packets per tooth} = \text{area} = \tfrac{W}{2}\cdot\tfrac34 W = \tfrac38 W^2",
                    font_size=30, color=WHITE),
            MathTex(r"\text{one loss per tooth} \Rightarrow \tfrac38 W^2 = \tfrac1p \Rightarrow W = "
                    r"\sqrt{\tfrac{8}{3p}}", font_size=30, color=NO),
            MathTex(r"\text{rate} = \frac{\tfrac34 W \cdot \text{MSS}}{\text{RTT}} = \frac{\text{MSS}}{\text{RTT}}"
                    r"\sqrt{\frac{3}{2p}}", font_size=34, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([3.3, -0.3, 0])
        for s in steps:
            if s.width > 6.4:
                s.width = 6.4
        with self.voiceover(
            "In 1997 Matt Mathis and his colleagues asked how fast a Reno flow can go if the network drops a "
            "fraction p of its packets at random. <bookmark mark='a'/> In steady state, the window climbs from half "
            "of some peak W to W, one packet per round trip, then a loss halves it. Each tooth lasts W over two "
            "round trips. <bookmark mark='b'/> The packets sent in one tooth are the area under it: W over two round "
            "trips, at an average window of three quarters of W. That is three eighths of W squared. "
            "<bookmark mark='c'/> One of those packets is the loss, so three eighths W squared is one over p, and W "
            "is the square root of eight over three p. <bookmark mark='d'/> The rate is the average window, a "
            "packet's size each, per round trip. Out comes the Mathis formula: the packet size over the round "
            "trip, times the square root of three over two p. Throughput falls only as the square root of the loss "
            "rate, and directly as the round trip."
        ) as vo:
            self.play(FadeIn(head), Create(ax))
            vo.wait_until("a")
            self.play(Create(tooth), FadeIn(drops), FadeIn(wl), FadeIn(w2), run_time=2)
            self.play(GrowFromCenter(span), FadeIn(sl))
            vo.wait_until("b")
            self.play(FadeIn(steps[0]))
            vo.wait_until("c")
            self.play(FadeIn(steps[1]))
            vo.wait_until("d")
            self.play(FadeIn(steps[2]))
        self.wait(0.4)
        self.clear_scene()

    def measured(self):
        s = load("sawtooth")
        head = label(r"Measured on our TCP", font_size=36).to_edge(UP, buff=0.3)
        g = axes([0, 2, 1], [0, 2, 1], x_length=6.2, y_length=3.8, x_label=r"loss rate $p$ \ (log scale)",
                 y_label=r"throughput, \ Mb/s \ (log scale)", xticks=(0, 1, 2), yticks=(0, 1, 2),
                 fx=lambda v: rf"$10^{{{int(v) - 4}}}$", fy=lambda v: rf"$10^{{{int(v)}}}$").move_to([-3.0, -0.5, 0])
        ax = g.ax
        f = ax.plot(lambda x: math.log10(1460 * 8 / 0.1 * math.sqrt(1.5 / 10 ** (x - 4)) / 1e6), x_range=[0, 2],
                    color=YES, stroke_width=2.5)
        dots = VGroup(*[Dot(ax.c2p(math.log10(r["p"]) + 4, math.log10(r["measured"])), radius=0.07,
                            color=CCC["reno"]) for r in s["mathis"]])
        rows = [[f"{r['p']:g}", f"{r['measured']:.2f}", f"{r['mathis']:.2f}",
                 f"{r['measured'] / r['mathis']:.2f}"] for r in s["mathis"]]
        tab = grid_table([r"$p$", r"measured", r"Mathis", r"ratio"], rows, widths=[1.3, 1.5, 1.5, 1.1], row_h=0.4,
                         font_size=19, mono_cols=())
        tab.move_to([3.6, 0.6, 0])
        for k in range(1, len(rows) + 1):
            tab.cells[k][1].set_color(CCC["reno"])
            tab.cells[k][2].set_color(YES)
        foot = wrapped_label(r"RTT 100 ms, \ a 200 Mb/s link that is never the limit: \ only random loss holds the "
                             r"flow back. \ At high loss our TCP beats the formula slightly: \ it acknowledges every "
                             r"packet, \ like SACK, \ so it recovers several losses in one round trip", 5.6,
                             font_size=18, color=GREY_A).move_to([3.6, -2.0, 0])
        with self.voiceover(
            "We tested the formula on our own TCP: a single Reno flow, a hundred-millisecond round trip, a link far "
            "faster than it can use, and random losses at five rates. <bookmark mark='a'/> On logarithmic axes the "
            "formula is a straight line of slope minus a half, and the measurements sit on it. At one loss in ten "
            "thousand, fourteen point three megabits a second, against fourteen point three predicted. "
            "<bookmark mark='b'/> At higher loss rates our flow does slightly better than the formula, because it "
            "learns about every lost packet at once, as selective acknowledgements allow, and recovers several in a "
            "single round trip. Padhye and colleagues extended the formula in 1998 to include timeouts, which "
            "matter when losses come in bursts. <bookmark mark='c'/> Look at what it says about long distance. "
            "Across the Atlantic, at a hundred and eight milliseconds and one loss in a thousand, Reno is limited to "
            "four megabits a second, on a link of a hundred. That is why Reno, in the hook, took thirty-five seconds."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), Create(f))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.2), FadeIn(tab))
            vo.wait_until("b")
            self.play(FadeIn(foot))
            vo.wait_until("c")
            self.play(Indicate(tab.cells[3][1], color=NO))
        self.wait(0.4)
        self.clear_scene()

    def unfair(self):
        s = load("sawtooth")
        head = label(r"RTT unfairness", font_size=36).to_edge(UP, buff=0.3)
        rows = [[f"{r['rtt2'] * 1000:.0f} ms", f"{r['short']:.1f}", f"{r['long']:.1f}", f"{r['ratio']:.1f}",
                 f"{r['rtt2'] / 0.02:.1f}"] for r in s["unfair"]]
        tab = grid_table([r"long flow's RTT", r"20 ms flow, \ Mb/s", r"long flow, \ Mb/s", r"ratio",
                          r"RTT ratio"], rows, widths=[2.5, 2.4, 2.4, 1.3, 1.6], row_h=0.44, font_size=20,
                         mono_cols=())
        tab.next_to(head, DOWN, buff=0.5).set_x(0)
        for k in range(1, len(rows) + 1):
            tab.cells[k][1].set_color(DATA)
            tab.cells[k][2].set_color(KERN)
            tab.cells[k][3].set_color(NO)
        lines = VGroup(
            wrapped_label(r"two Reno flows share a 20 Mb/s link; \ one has a 20 ms round trip, \ the other longer",
                          12.4, font_size=21, color=GREY_A),
            wrapped_label(r"windows grow by one packet \textit{per round trip}: \ the short flow grows ten times as "
                          r"often, \ and both see the same drops", 12.4, font_size=21, color=WHITE),
            wrapped_label(r"with a shared drop-tail queue the penalty is worse than $1/\text{RTT}$: \ it approaches "
                          r"$1/\text{RTT}^2$ \ (Lakshman and Madhow, 1997)", 12.4, font_size=21, color=NO),
            wrapped_label(r"so a user far away gets a smaller share of the same link: \ one of the reasons for "
                          r"CUBIC, \ whose growth depends on time, \ not round trips", 12.4, font_size=21,
                          color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(tab, DOWN, buff=0.5)
        with self.voiceover(
            "The formula has a consequence nobody designed. <bookmark mark='a'/> Put two Reno flows on a "
            "twenty-megabit link, one with a twenty-millisecond round trip and the other further away. With equal "
            "round trips they split the link evenly. <bookmark mark='b'/> But a window grows by one packet per "
            "round trip, so the nearby flow grows ten times as often as one with ten times its round trip, while "
            "both suffer the same drops. <bookmark mark='c'/> At five times the round trip, the near flow gets two "
            "point three times as much. At ten times, thirty-two times as much: worse than one over the round trip, "
            "approaching one over its square, as Lakshman and Madhow showed for a shared drop-tail queue. "
            "<bookmark mark='d'/> AIMD is fair between equals. Between a user next door and a user across an ocean, "
            "it is not, and this is one of the reasons the next generation of algorithms grows with the clock, not "
            "with round trips."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines[0]))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*tab.cells[0])), Create(tab.rule), FadeIn(VGroup(*tab.cells[1])))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(VGroup(*tab.cells[k])) for k in range(2, len(rows) + 1)],
                                  lag_ratio=0.3))
            self.play(FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.wait(0.4)
        self.clear_scene()


_ = (HEAD,)
