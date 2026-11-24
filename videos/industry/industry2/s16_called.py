from __future__ import annotations

from explainer.industry.calls import calls
from videos.industry.industry2.common import *  # noqa: F403


class Called(VoiceoverScene):
    def construct(self):
        card(self, 18, "Called it?", "Did machines replace people, as Leontief feared?",
             "Chapter eighteen. Called it?", lit=("change",))
        self.leontief()
        self.ours()

    def leontief(self):
        L = R["leontief"]
        q = VGroup(T("“The role of humans as the most important factor of production is bound to diminish", 24,
                     I.TEXT), T("in the same way that the role of horses in agricultural production was first", 24,
                                I.TEXT),
                   T("diminished and then eliminated by the introduction of tractors.”", 24, I.TEXT),
                   T("Wassily Leontief, 1983", 20, I.DIM)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_edge(UP,
                                                                                                      buff=0.6)
        after = VGroup(T("American payroll jobs", 22, I.DIM),
                       TB(f"{L['j1983']:.0f} million in 1983  →  {L['j2025']:.0f} million in 2025", 34, I.PROFIT)
                       ).arrange(DOWN, buff=0.12).move_to(DOWN * 0.8)
        tail = T("So far, people have not gone the way of horses. Part 42 asks whether AI changes the answer.", 22,
                 I.ACCENT).to_edge(DOWN, buff=0.6)
        src = source("Leontief (1983), National Academy of Engineering; BLS via FRED", corner=DR)
        with self.voiceover(
            "Every part ends with a forecast. This one comes from Leontief himself. <bookmark mark='a'/> In 1983, "
            "looking at computers and robots, he wrote that the role of humans as the most important factor of "
            "production is bound to diminish, the way the role of horses in farming was first diminished and then "
            "eliminated by tractors. <bookmark mark='b'/> In 1983 American employers had 90 million people on their "
            "payrolls. In 2025 they had 158 million. <bookmark mark='c'/> So far, people have not gone the way of "
            "horses: the work moved, from factories to offices, hospitals and shops, as this part has shown. "
            "Whether artificial intelligence changes that is a question Part 42 takes up."
        ) as vo:
            people = VGroup(*[draw.person(0.42) for _ in range(16)]).arrange(RIGHT, buff=0.12).move_to(DOWN * 2.05)
            key = T("each figure: 10 million payroll jobs", 15, I.DIM).next_to(people, DOWN, buff=0.1)
            self.play(FadeIn(src), LaggedStart(*[FadeIn(p_, shift=UP * 0.2) for p_ in people[:9]], lag_ratio=0.1),
                      FadeIn(key), run_time=1.6)
            vo.wait_until("a")
            self.play(FadeIn(q, shift=DOWN * 0.1), run_time=1.6)
            vo.wait_until("b")
            self.play(FadeIn(after, shift=UP * 0.1),
                      LaggedStart(*[FadeIn(p_, shift=UP * 0.2) for p_ in people[9:]], lag_ratio=0.15), run_time=1.6)
            vo.wait_until("c")
            self.play(FadeIn(tail))
        self.clear_scene()

    def ours(self):
        c = calls(2, ours=True)[0]
        box = RoundedRectangle(corner_radius=0.16, width=12.0, height=3.4, stroke_color=I.ACCENT, stroke_width=2,
                               fill_color=I.PANEL, fill_opacity=1)
        body = VGroup(TB("This series' call", 26, I.ACCENT), T(f"logged {c.made}", 18, I.DIM),
                      T("In 2030, health care and social assistance will employ", 28, I.TEXT),
                      TB("more people than manufacturing and retail combined", 32, I.MONEY),
                      T("our probability: 40%  ·  2025: 23.3 million against 28.1 million  ·  scored on BLS annual "
                        "averages", 17, I.DIM)).arrange(DOWN, buff=0.16).move_to(box)
        with self.voiceover(
            "And this series' own call, logged today. <bookmark mark='a'/> In 2030, health care and social "
            "assistance will employ more Americans than manufacturing and retail put together. In 2025 the counts "
            "were 23.3 million against 28.1 million. <bookmark mark='b'/> Health care has been adding about three "
            "quarters of a million jobs a year, and factories and shops have been flat, so it is close. We put the "
            "chance at forty percent, and we will score it on the Bureau of Labor Statistics' averages for 2030."
        ) as vo:
            self.play(FadeIn(box), FadeIn(body[0]))
            vo.wait_until("a")
            self.play(FadeIn(body[1:4], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(body[4]))
        self.clear_scene()
