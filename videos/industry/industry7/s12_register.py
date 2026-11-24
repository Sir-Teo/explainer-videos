from __future__ import annotations

from explainer.industry.register import row, rows
from videos.industry.industry7.common import *  # noqa: F403


class Register(VoiceoverScene):
    def construct(self):
        card(self, 12, "The Register", "How does this series keep its own numbers honest?",
             "Chapter twelve. The Register.", lit=("unit",))
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
