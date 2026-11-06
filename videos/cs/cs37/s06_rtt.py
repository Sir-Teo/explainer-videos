from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs37.common import (ACKC, DATA, HEAD, KERN, LAM, NO, PART, SEG, YES, axes, grid_table, load,
                                   seq_diagram, trace)


class Rtt(VoiceoverScene):
    def construct(self):
        self.card()
        self.samples()
        self.estimators()
        self.karn()

    def card(self):
        card = chapter_card(5, r"Timers that learn", r"How long should a sender wait before resending?",
                            lit=(1981, 1988), extra=((1981, r"RFC 793: \ $\beta \cdot$ SRTT"),
                                                     (1987, r"Karn and Partridge"), (1988, r"Jacobson and Karels")),
                            part=PART)
        with self.voiceover("Chapter five. Timers that learn."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def samples(self):
        r = load("rtt")
        head = label(r"Round trips are not constant", font_size=36).to_edge(UP, buff=0.3)
        pts = r["samples"]
        t0 = pts[0][0]
        g = axes([0, 40, 5], [0, 0.4, 0.1], x_length=10.5, y_length=4.2, x_label=r"seconds",
                 y_label=r"measured round trip", xticks=range(0, 41, 5), yticks=(0.1, 0.2, 0.3, 0.4),
                 fy=lambda v: f"{v * 1000:.0f} ms").move_to(DOWN * 0.4)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(t, y), radius=0.03, color=SEG) for t, y in pts])
        base = DashedLine(ax.c2p(0, 0.108), ax.c2p(40, 0.108), color=GREY_B, dash_length=0.1)
        bl = label(r"propagation: \ 108 ms", font_size=17, color=GREY_B).next_to(ax.c2p(40, 0.108), DOWN,
                                                                               buff=0.08).shift(LEFT * 1.1)
        foot = label(rf"one flow among six sharing a 20 Mb/s bottleneck: \ {r['n'] + 1} samples from "
                     rf"{r['min'] * 1000:.0f} to {r['max'] * 1000:.0f} ms", font_size=20, color=GREY_A).to_edge(
            DOWN, buff=0.25)
        with self.voiceover(
            "A sender that retransmits must decide how long to wait. Too short, and it resends packets that were "
            "only delayed, adding traffic to a network that is already slow. Too long, and every loss costs a long "
            "silence. <bookmark mark='a'/> The right wait depends on the round trip, and the round trip is not a "
            "constant. Here is one flow from San Francisco to Frankfurt, sharing a bottleneck with five others that "
            "join over time. Its round trips start at the hundred and eight milliseconds of light in fibre and "
            "climb, as queues build, past three hundred. The timer must learn this, from samples, as it goes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), Create(base), FadeIn(bl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.004), run_time=3)
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()
        _ = t0

    def estimators(self):
        r = load("rtt")
        head = label(r"Two estimators", font_size=36).to_edge(UP, buff=0.3)
        eqs = VGroup(
            MathTex(r"\text{RFC 793:}\quad \text{SRTT} \leftarrow \tfrac78\,\text{SRTT} + \tfrac18 R, \qquad "
                    r"\text{RTO} = \beta\cdot\text{SRTT}", font_size=30, color=KERN),
            MathTex(r"\text{Jacobson:}\quad \text{RTTVAR} \leftarrow \tfrac34\,\text{RTTVAR} + \tfrac14 |\text{SRTT} "
                    r"- R|, \qquad \text{RTO} = \text{SRTT} + 4\,\text{RTTVAR}", font_size=30, color=YES),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT).next_to(head, DOWN, buff=0.3)
        for e in eqs:
            if e.width > 12.8:
                e.width = 12.8
        pts = r["samples"]
        g = axes([0, 40, 10], [0, 0.8, 0.2], x_length=7.2, y_length=3.4, x_label=r"seconds",
                 xticks=range(0, 41, 10), yticks=(0.2, 0.4, 0.6, 0.8), fy=lambda v: f"{v * 1000:.0f} ms").move_to(
            [-2.6, -1.6, 0])
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(t, y), radius=0.025, color=SEG) for t, y in pts])
        ts = [p[0] for p in pts[1:]]
        tr2 = trace(ax, list(zip(ts, r["rfc793_2.0"]["trace"])), KERN, width=2)
        trj = trace(ax, list(zip(ts, r["jacobson"]["trace"])), YES, width=2)
        rows = [[r"$\beta = 1.3$", f"{r['rfc793_1.3']['spurious']}", f"{r['rfc793_1.3']['mean'] * 1000:.0f} ms"],
                [r"$\beta = 2$", f"{r['rfc793_2.0']['spurious']}", f"{r['rfc793_2.0']['mean'] * 1000:.0f} ms"],
                [r"Jacobson", f"{r['jacobson']['spurious']}", f"{r['jacobson']['mean'] * 1000:.0f} ms"]]
        tab = grid_table([r"timer", r"would fire early", r"mean wait"], rows, widths=[1.8, 2.2, 1.8], row_h=0.42,
                         font_size=19, mono_cols=())
        tab.move_to([3.9, -0.9, 0])
        for k, c in ((1, NO), (2, KERN), (3, YES)):
            for j in range(3):
                tab.cells[k][j].set_color(c)
        foot = wrapped_label(rf"mean round trip {r['mean_rtt'] * 1000:.0f} ms. \ A fixed multiple is either "
                             r"trigger-happy or slow; \ tracking the \textit{variation} is both safe and quick", 5.6,
                             font_size=19, color=WHITE).move_to([3.9, -2.6, 0])
        with self.voiceover(
            "The original TCP specification kept a smoothed average of the samples, and waited a fixed multiple, "
            "beta, of it, with beta between one point three and two. <bookmark mark='a'/> Van Jacobson and Mike "
            "Karels, in 1988, also kept a smoothed average of how far each sample strays from the mean, and waited "
            "the mean plus four of those deviations. <bookmark mark='b'/> Here are the two timers over our samples. "
            "The fixed multiple of two stays far above the samples, all the time. Jacobson's hugs them when they are "
            "steady and opens up when they swing. <bookmark mark='c'/> Count the samples that arrived after the "
            "timer would have fired, each a needless retransmission. With beta one point three, fifteen. With beta "
            "two, none, but it waits almost half a second on average before recovering a real loss. Jacobson's "
            "timer fires early once, and waits a third less. Measuring the variance is what makes a timer both safe "
            "and quick, and the same estimator still runs in every TCP today."
        ) as vo:
            self.play(FadeIn(head), FadeIn(eqs[0]))
            vo.wait_until("a")
            self.play(FadeIn(eqs[1]))
            vo.wait_until("b")
            self.play(FadeIn(g), FadeIn(dots))
            self.play(Create(tr2), run_time=1.5)
            self.play(Create(trj), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(tab), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def karn(self):
        head = label(r"Karn's rule: \ which ACK is this?", font_size=36).to_edge(UP, buff=0.3)
        ev = [(0.0, None, r"segment", True, SEG), (3.0, 4.0, r"segment \ (again)", True, SEG),
              (4.0, 5.0, r"ACK", False, ACKC)]
        sd = seq_diagram(ev, t_max=5.6, height=4.4, gap=5.0).move_to([-3.2, -0.6, 0])
        b1 = Brace(Line(sd.arrows[0][0].get_start(), sd.arrows[0][0].get_start() + DOWN * (5.0 / 5.6 * 4.4)),
                   LEFT, color=NO)
        b1l = label(r"from the first send?", font_size=17, color=NO).next_to(b1, LEFT, buff=0.08)
        side = VGroup(
            wrapped_label(r"an ACK for a retransmitted segment could belong to either copy: \ the sample is "
                          r"\textbf{ambiguous}", 5.4, font_size=21, color=WHITE),
            wrapped_label(r"\textbf{Karn's rule} \ (1987): \ take no samples from retransmitted segments, \ and "
                          r"after a timeout \textbf{double} the timer until a fresh sample arrives", 5.4,
                          font_size=21, color=YES),
            wrapped_label(r"exponential backoff again \ (Ethernet, Part 36): \ the more the network fails to answer, "
                          r"\ the more patiently we ask", 5.4, font_size=20, color=KERN),
            wrapped_label(r"today the timestamp option tags each segment, \ so even retransmissions give "
                          r"unambiguous samples", 5.4, font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([3.5, -0.4, 0])
        with self.voiceover(
            "One trap remains. <bookmark mark='a'/> A segment is lost, the timer fires, and it is sent again. An ACK "
            "arrives. Did it answer the first copy, or the second? If we guess wrong, we measure a round trip that "
            "is far too long or far too short. <bookmark mark='b'/> Phil Karn, writing amateur radio packet "
            "software, proposed the fix with Craig Partridge in 1987: take no samples from a segment that was "
            "retransmitted, and each time the timer fires, double it, until a clean sample arrives. "
            "<bookmark mark='c'/> It is Ethernet's exponential backoff once more. A network that keeps failing to "
            "answer is asked more and more patiently. <bookmark mark='d'/> Modern TCPs also stamp each segment with "
            "the time it was sent, and the receiver echoes the stamp, which removes the ambiguity entirely."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sd[:4]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(a) for a in sd.arrows], lag_ratio=0.4))
            self.play(GrowFromCenter(b1), FadeIn(b1l), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()


_ = (DATA, HEAD, LAM)
