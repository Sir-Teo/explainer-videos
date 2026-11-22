from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs46.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load


def node(name, color, w=2.2, h=0.6, size=18):
    r = RoundedRectangle(width=w, height=h, corner_radius=0.1, stroke_color=color, stroke_width=2, fill_color=BG,
                         fill_opacity=1)
    return VGroup(r, label(name, font_size=size, color=color).move_to(r))


class Frontier(WatchScene):
    def construct(self):
        self.card()
        self.incremental()
        self.time_()

    def card(self):
        self.chapter(14, r"Frontier: \ streams, \ tables and their limits", r"Can every query be kept up to date cheaply?", lit=(2013, 2023), extra=((2013, r"differential dataflow"), (2023, r"DBSP")), part=PART, said="Chapter fourteen, the frontier. Can every query be kept up to date, cheaply?")

    def incremental(self):
        head = label(r"Queries that update themselves", font_size=36).to_edge(UP, buff=0.3)
        ops = [(r"orders", DATA), (r"join users", HEAD), (r"filter: \ country", LAM), (r"count by day", YES)]
        chain = VGroup(*[node(t, c, w=2.6) for t, c in ops]).arrange(RIGHT, buff=0.6).next_to(head, DOWN, buff=0.6)
        arrows = VGroup(*[Arrow(chain[i].get_right(), chain[i + 1].get_left(), buff=0.05, color=GREY_B,
                                stroke_width=2) for i in range(3)])
        deltas = VGroup(*[label(t, font_size=18, color=c).next_to(chain[i], DOWN, buff=0.25) for i, (t, c) in
                          enumerate(((r"$+1$ order", DATA), (r"$+1$ joined row", HEAD), (r"$+1$ or nothing", LAM),
                                     (r"one count $+1$", YES)))])
        lines = VGroup(
            wrapped_label(r"\textbf{incremental view maintenance}: \ push each change through the query as a delta, "
                          r"\ doing work proportional to the change, \ not the data", 12.4, font_size=20,
                          color=WHITE),
            wrapped_label(r"\textbf{differential dataflow} \ (McSherry et al., \ 2013) \ handles iteration and "
                          r"recursion; \ \textbf{DBSP} \ (Budiu et al., \ 2023) \ turns any query over streams "
                          r"into an incremental one by algebra", 12.4, font_size=20, color=YES),
            wrapped_label(r"open: \ which queries can be maintained in time proportional to the change, \ and with "
                          r"how much state? \ some joins provably cannot", 12.4, font_size=20, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Streams and tables are converging. <bookmark mark='a'/> Take a query over a table, joins, filters, "
            "counts, and ask that its answer stay current as rows arrive. <bookmark mark='b'/> Rather than rerun it, "
            "push each change through the plan as a delta: one new order becomes one joined row, which passes the "
            "filter or not, and changes one count by one. That is incremental view maintenance, and its promise is "
            "work in proportion to the change, not the data. <bookmark mark='c'/> Differential dataflow, from Frank "
            "McSherry and colleagues in 2013, extended it to iterative and recursive computations, and DBSP, by "
            "Mihai Budiu and colleagues in 2023, gave an algebra that makes any streaming query incremental. "
            "<bookmark mark='d'/> Which queries can be maintained cheaply, and with how much state, is open; for "
            "some joins, provably, they cannot."
        ) as vo:
            self.play(FadeIn(head), FadeIn(chain), *[GrowArrow(a) for a in arrows])
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d, shift=DOWN * 0.1) for d in deltas], lag_ratio=0.4), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(lines[1]))
            vo.wait_until("d")
            self.play(FadeIn(lines[2]))
        self.wait(0.4)
        self.clear_scene()


    def time_(self):
        self.ask(r"Can a stream processor ever \emph{know} \\ that no older event will arrive?", [r"yes", r"no"], 1,
                 say="Can a stream processor ever know for certain that no older event is still on its way?",
                 reveal="No. A watermark is a guess, trading completeness against latency.")
        w = load("watermark")
        head = label(r"Time is a guess", font_size=36).to_edge(UP, buff=0.3)
        rows = w["rows"]
        x0, y0, xw, yh = -6.0, -1.6, 6.2, 3.4
        import math
        lx = [math.log10(r["mean_latency"]) for r in rows]

        def pt(r):
            return [x0 + (math.log10(r["mean_latency"]) - lx[0]) / (lx[-1] - lx[0]) * xw,
                    y0 + (r["complete"] - 0.8) / 0.2 * yh, 0]
        ax = VGroup(Line([x0, y0, 0], [x0 + xw, y0, 0], color=GREY_C), Line([x0, y0, 0], [x0, y0 + yh, 0],
                                                                              color=GREY_C))
        curve = VMobject(color=HEAD, stroke_width=3).set_points_as_corners([pt(r) for r in rows])
        dots = VGroup(*[Dot(pt(r), radius=0.06, color=HEAD) for r in rows])
        lab = VGroup(*[label(rf"{r['lag']:.0f} s", font_size=15, color=GREY_B).next_to(d, DOWN, buff=0.08)
                       for r, d in zip(rows, dots)])
        al = w["allowed_lateness"]
        star = Star(n=5, outer_radius=0.15, color=YES, fill_opacity=1).move_to(pt(al))
        sl = label(rf"5 s watermark $+$ 60 s allowed lateness: \ {al['refinements']} refinements", font_size=17,
                   color=YES).next_to(star, LEFT, buff=0.15)
        xl = label(r"mean latency of a window's first answer \ (log)", font_size=17, color=GREY_B).next_to(ax[0], DOWN,
                                                                                                    buff=0.35)
        yl = label(r"share of events counted", font_size=17, color=GREY_B).next_to(ax[1], UP, buff=0.1)
        side = VGroup(
            wrapped_label(r"a watermark is a heuristic claim that no older events will come; \ every choice of lag "
                          r"trades completeness for latency \ (chapter 4)", 5.4, font_size=19, color=WHITE),
            wrapped_label(r"allowed lateness and retractions escape the trade by answering early and correcting, \ "
                          r"at the price of state and of consumers that must accept corrections", 5.4, font_size=19,
                          color=YES),
            wrapped_label(r"open: \ watermarks with guarantees, \ from measured delay distributions; \ semantics of "
                          r"streaming SQL that every engine agrees on", 5.4, font_size=19, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "The deepest limit is time. <bookmark mark='a'/> A watermark is a guess that no older events will "
            "arrive, and every choice of how long to wait trades completeness for latency: from four fifths of the "
            "events within two seconds to all but one of them after a minute. <bookmark mark='b'/> Answering early and then "
            f"correcting escapes the trade: a five-second watermark with a minute of allowed lateness fired "
            f"{al['refinements']} refinements and ended with every window exact. The price is state, and consumers "
            "that must accept corrections. <bookmark mark='c'/> Watermarks with guarantees, derived from measured "
            "delays, and a semantics of streaming SQL that every engine agrees on, are open problems."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(curve), FadeIn(dots), FadeIn(lab), FadeIn(side[0]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(star), FadeIn(sl), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()



_ = (DATA, KERN, LAM, NO, YES)
