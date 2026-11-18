from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs55.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load


def tile(title, body, col, w=4.2, h=2.7):
    frame = RoundedRectangle(width=w, height=h, corner_radius=0.15, stroke_color=col, stroke_width=2, fill_color=BG,
                             fill_opacity=1)
    t = label(title, font_size=21, color=col)
    b = wrapped_label(body, w - 0.4, font_size=17, color=GREY_A)
    VGroup(t, b).arrange(DOWN, buff=0.25).move_to(frame)
    return VGroup(frame, t, b)


class Frontier(WatchScene):
    def construct(self):
        self.card()
        self.sky()

    def card(self):
        self.chapter(14, r"Frontier: \ the open problems of the series", r"What did we meet that nobody knows?", lit=(1971, 2024), extra=((1971, r"Cook: \ P versus NP"), (2024, r"BB(5) proved")), part=PART, said="Chapter fourteen, the frontier. What did this series meet that nobody knows?")

    def sky(self):
        self.ask(r"P versus NP; whether one-way functions exist. \\ Settled?", [r"one of them", r"neither"], 1,
                 say="P versus NP, and whether one-way functions exist. Has either been settled?",
                 reveal="Neither. The security of Parts 29 and 30 rests on an open question.")
        rows = load("open")["rows"]
        head = label(r"Questions the degree left open", font_size=36).to_edge(UP, buff=0.3)
        cells = VGroup()
        cols = (NO, HEAD, YES, DATA, LAM, KERN)
        for i, r in enumerate(rows):
            parts = ", ".join(str(p) for p in r["parts"])
            box = RoundedRectangle(width=6.2, height=0.72, corner_radius=0.1, stroke_color=cols[i % 6],
                                   stroke_width=1.5, fill_color=BG, fill_opacity=1)
            t = label(rf"{r['problem']} \ (Part{'s' if len(r['parts']) > 1 else ''} {parts})", font_size=17,
                      color=cols[i % 6])
            d = label(r["record"], font_size=14, color=GREY_A)
            for x in (t, d):
                if x.width > 5.9:
                    x.width = 5.9
            g = VGroup(t, d).arrange(DOWN, buff=0.06).move_to(box)
            cells.add(VGroup(box, g))
        cells.arrange_in_grid(cols=2, buff=(0.25, 0.14), flow_order="dr").next_to(head, DOWN, buff=0.3)
        if cells.height > 6.4:
            cells.height = 6.4
            cells.next_to(head, DOWN, buff=0.3)
        with self.voiceover(
            "Along the way this series met questions that nobody can answer. <bookmark mark='a'/> Whether P equals "
            "NP, and whether one-way functions, and with them all of modern cryptography, exist at all. How fast "
            "matrices can be multiplied. The sixth Busy Beaver number, now that the fifth was finally proved in "
            "2024. Whether splay trees are optimal. The unique games conjecture. Whether randomness ever really "
            "helps. Why we cannot prove that any explicit function needs many gates. <bookmark mark='b'/> And the "
            "practical ones: a memory model for C, quantum computers that do something useful, and verified software "
            "at the scale people actually build. Part 61 returns to each of these, as research."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in cells[:8]], lag_ratio=0.25), run_time=5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c) for c in cells[8:]], lag_ratio=0.3), run_time=2)
        self.wait(0.4)
        self.clear_scene()




_ = (DATA, KERN, LAM, NO, YES)
