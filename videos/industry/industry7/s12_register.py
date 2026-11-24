from __future__ import annotations

from explainer.industry.register import row, rows
from videos.industry.industry7.common import *  # noqa: F403


class Register(VoiceoverScene):
    def construct(self):
        card(self, 13, "The Register", "How does this series keep its own numbers honest?",
             "Chapter thirteen. The Register.", lit=("unit",))
        rw = row("water.primo.2023")
        box = RoundedRectangle(corner_radius=0.12, width=11.0, height=4.6, stroke_color=GOLD, stroke_width=2,
                               fill_color="#141A24", fill_opacity=1).move_to([0, -0.2, 0])
        fields = [("key", rw.key), ("value", f"{rw.value:g} {rw.unit}"),
                  ("what it is", rw.definition[:92] + ("..." if len(rw.definition) > 92 else "")),
                  ("source", rw.source), ("the figure describes", rw.fact), ("read from the source on", rw.checked),
                  ("kind", f"{rw.kind}: a company's own filing"), ("note", rw.note)]
        lines = VGroup()
        for k, (name, val) in enumerate(fields):
            ln = VGroup(tx(name, 17, GOLD), tx(val, 17, WHITE))
            ln[1].next_to(ln[0], RIGHT, buff=0.3)
            lines.add(ln)
        lines.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(box)
        for ln in lines:
            if ln.width > 10.4:
                ln.scale_to_fit_width(10.4)
        for ln in lines:
            ln[1].align_to(lines[0][0], LEFT).shift(RIGHT * 3.0)
        lines.move_to(box)
        stamp = VGroup(RoundedRectangle(corner_radius=0.08, width=2.6, height=0.8, stroke_color="#E8554E", stroke_width=3,
                                        fill_opacity=0),
                       tx(f"as of {rw.checked}", 20, "#E8554E", bold=True)).rotate(0.15).move_to([4.4, 1.6, 0])
        kinds = VGroup(*[tx(k, 17, c) for k, c in (("filing", RETAIL), ("official", FACTORY), ("tracker", GUESS),
                                                     ("study", UNITS), ("press", "#E8554E"), ("assumption", GREY_B))]
                       ).arrange(RIGHT, buff=0.5).to_edge(DOWN, buff=0.45)
        n = sum(len(rows(p)) for p in range(1, 8))
        src = source("this series' Register: explainer/industry/register.py and data/rows_pNN.py", size=13)
        with self.voiceover(
            "Every number in this series has an entry like this one, in what we call the Register. "
            "<bookmark mark='a'/> A key, and the value. <bookmark mark='b'/> What exactly it measures, in words, "
            "because, as this part has shown, the definition is most of a number. <bookmark mark='c'/> Where it came "
            "from, and the address to check it. <bookmark mark='d'/> Two dates, and they are different: the period "
            "the figure describes, and the day we read it. Markets move; a figure read today about 2023 says so. "
            "<bookmark mark='e'/> And what kind of figure it is: a company's own filing, a statistical office, a "
            "commercial tracker's estimate, a study, a press report we could not check against its source, or this "
            "series' own assumption, labelled as one. <bookmark mark='f'/> Here, a note too: Primo does not say where "
            f"its number comes from. Seven parts in, the Register holds {n} entries, and a check refuses to build a "
            "film that shows a number without one."
        ) as vo:
            self.play(FadeIn(src), DrawBorderThenFill(box))
            for k, m in enumerate("abcdef"):
                vo.wait_until(m)
                grp = {"a": (0, 1), "b": (2,), "c": (3,), "d": (4, 5), "e": (6,), "f": (7,)}[m]
                self.play(*[FadeIn(lines[i], shift=RIGHT * 0.15) for i in grp], run_time=0.8)
                if m == "d":
                    self.play(FadeIn(stamp, scale=1.4))
                if m == "e":
                    self.play(LaggedStart(*[FadeIn(k_) for k_ in kinds], lag_ratio=0.15))
        self.clear_scene()
        self.holdings()

    def holdings(self):
        import collections
        seen = {}
        for p in range(1, PART + 1):
            for r_ in rows(p):
                seen[r_.key] = r_
        cnt = collections.Counter(r_.kind for r_ in seen.values())
        order = [("filing", "companies' own filings", RETAIL), ("official", "statistical offices and regulators", FACTORY),
                 ("study", "studies", UNITS), ("tracker", "commercial trackers", GUESS),
                 ("press", "press reports", "#E8554E"), ("assumption", "this series' assumptions", GREY_B)]
        n = sum(cnt.values())
        top = max(cnt.values())
        bars = VGroup()
        for k, (kd, name, col) in enumerate(order):
            v = cnt.get(kd, 0)
            lab = tx(name, 19, col, bold=True).move_to([-1.6, 1.6 - 0.72 * k, 0], aligned_edge=RIGHT)
            bar = Rectangle(width=max(6.2 * v / top, 0.04), height=0.46, stroke_width=0, fill_color=col,
                            fill_opacity=0.9).next_to(lab, RIGHT, buff=0.3).align_to([-1.3, 0, 0], LEFT)
            val = tx(f"{v}", 19, WHITE, bold=True).next_to(bar, RIGHT, buff=0.15)
            bars.add(VGroup(lab, bar, val))
        head = tx(f"The Register after seven parts: {n} entries", 24, GOLD, bold=True).to_edge(UP, buff=0.5)
        uber = row("uber.tam.eats")
        stale = VGroup(tx(f"Uber Eats' $2.8tn: describes {uber.fact}, read {uber.checked[:4]}", 18, GREY_A),
                       tx("old figures stay, labelled with their year; they are history, not news", 18, GREY_A)
                       ).arrange(DOWN, buff=0.06).to_edge(DOWN, buff=0.6)
        src = source("this series' Register, counted when this film was built", size=13)
        with self.voiceover(
            f"Here is what the Register holds, seven parts in. <bookmark mark='a'/> More than half of its {n} entries "
            f"come from companies' own filings: {cnt['filing']} of them, read from annual reports and prospectuses "
            f"lodged with regulators. <bookmark mark='b'/> Then {cnt['official']} from statistical offices and "
            f"regulators. <bookmark mark='c'/> Then studies, commercial trackers and press reports, each labelled "
            f"as such, and {cnt['assumption']} assumptions of our own. <bookmark mark='d'/> Before each part is "
            "built, every number it shows is read again from its source, and the dates are kept. An entry about "
            "2017 read in 2026 is not wrong; it is history, and the film says so. That is the whole discipline: "
            "never a number without a source, a definition and a date."
        ) as vo:
            self.play(FadeIn(src), FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(bars[0][0]), GrowFromEdge(bars[0][1], LEFT), FadeIn(bars[0][2]))
            vo.wait_until("b")
            self.play(FadeIn(bars[1][0]), GrowFromEdge(bars[1][1], LEFT), FadeIn(bars[1][2]))
            vo.wait_until("c")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(g[0]), GrowFromEdge(g[1], LEFT), FadeIn(g[2]))
                                    for g in bars[2:]], lag_ratio=0.3), run_time=2.4)
            vo.wait_until("d")
            self.play(FadeIn(stale, shift=UP * 0.1))
        self.clear_scene()
