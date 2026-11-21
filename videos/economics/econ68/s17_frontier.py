from __future__ import annotations

from videos.economics.econ68.common import *  # noqa: F403

PROBLEMS = [
    (r"I \ $\cdot$ \ The Question", r"measure welfare when goods are free and digital"),
    (r"II \ $\cdot$ \ Choosing", r"read welfare from choices that are not consistent"),
    (r"III \ $\cdot$ \ Markets", r"tell when pricing algorithms collude"),
    (r"IV \ $\cdot$ \ Failure and Design", r"design markets for data and privacy"),
    (r"V \ $\cdot$ \ The Long Run", r"explain the productivity slowdown since the mid-2000s"),
    (r"VI \ $\cdot$ \ Money and the Cycle", r"find the neutral rate, \ and what large balance sheets do"),
    (r"VII \ $\cdot$ \ The World Economy", r"price a world split into blocs, \ ideas included"),
    (r"VIII \ $\cdot$ \ Work and the State", r"tax wealth that moves, \ and insure work that changes"),
    (r"IX \ $\cdot$ \ The Fields", r"value climate risks with tipping points and fat tails"),
    (r"X \ $\cdot$ \ The Graduate Core", r"solve many-agent models with aggregate risk, \ at scale"),
    (r"XI \ $\cdot$ \ Economics at Work", r"keep forecasts and policy scores honest in real time"),
    (r"XII \ $\cdot$ \ The Frontier", r"explain firm sizes, \ long expansions and inverted curves"),
]


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 15, r"Frontier: \ twelve open problems", r"Where should the next generation start?",
             "Chapter fifteen. Frontier: twelve open problems.", scale=("world",), horizon=("a century",))
        self.grid()

    def grid(self):
        cols = (DATA, FIRST, TRUE, ROW, MODEL, TOLL)
        cards = VGroup()
        for k, (act, txt) in enumerate(PROBLEMS):
            col = cols[k % len(cols)]
            box = RoundedRectangle(width=4.1, height=1.25, corner_radius=0.1, stroke_color=col, stroke_width=2,
                                   fill_color=col, fill_opacity=0.07)
            a = label(act, font_size=15, color=col)
            t = label(txt, font_size=16, color=WHITE)
            if t.width > 3.8:
                t.scale_to_fit_width(3.8)
            VGroup(a, t).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to(box)
            cards.add(VGroup(box, a, t))
        cards.arrange_in_grid(rows=4, cols=3, buff=(0.25, 0.22)).move_to(DOWN * 0.15)
        head = label(r"one open problem from each act", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.35)
        with self.voiceover(
            "One open problem from each act, for whoever comes next. <bookmark mark='a'/> Measure welfare when the "
            "goods are free and digital. Read welfare from choices that are not consistent. Tell when pricing "
            "algorithms collude. Design markets for data and privacy. <bookmark mark='b'/> Explain why productivity "
            "growth slowed in the rich world from the mid-2000s. Find the neutral interest rate, and learn what "
            "large central-bank balance sheets do. Price a world split into blocs, counting the ideas that stop "
            "crossing. Tax wealth that can move, and insure work that keeps changing. <bookmark mark='c'/> Value "
            "climate risks that have tipping points and fat tails. Solve models of many different agents with "
            "aggregate risk, at the scale of real economies. Keep forecasts and policy scores honest in real time. "
            "And close the three Facts this series could not: firm sizes, long expansions, and the yield curve. "
            "<bookmark mark='d'/> Each is a dissertation, and none needs anything this series did not show you how "
            "to start."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.05) for c in cards[:4]], lag_ratio=0.4), run_time=3.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.05) for c in cards[4:8]], lag_ratio=0.4), run_time=3.0)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.05) for c in cards[8:]], lag_ratio=0.4), run_time=3.0)
            vo.wait_until("d")
            self.play(Indicate(cards, color=WHITE, scale_factor=1.01))
        self.clear_scene()
