from __future__ import annotations

from videos.psychology.psych37.common import *  # noqa: F403


class Lonely(VoiceoverScene):
    def construct(self):
        self.card()
        self.mortality()
        self.causal()

    def card(self):
        card = chapter_card(11, r"Loneliness and health", r"Do relationships keep people alive?",
                            lit={2010: r"Holt-Lunstad et al.", 2015: r"Holt-Lunstad et al."}, part=PART,
                            scale=("body", "person"), marr=("what",))
        with self.voiceover("Chapter eleven. Loneliness and health."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def mortality(self):
        head = heading(r"148 studies")
        A = axes([-0.6, 3.6], [1.0, 2.0], x_length=5.6, y_length=3.4, xticks=None, yticks=[1.0, 1.5, 2.0],
                 yfmt=lambda v: f"{v:.1f}", ylabel=r"odds ratio", center=[-3.2, -0.3, 0], font_size=15)
        vals = [(1.50, r"social relationships, \ overall", GOOD), (1.91, r"complex measures of integration", GOOD),
                (1.29, r"social isolation", AUTH), (1.26, r"loneliness", AUTH)]
        b = VGroup(*[bars(A.ax, [k], [v], c, width=0.6) for k, (v, _, c) in enumerate(vals)])
        names = VGroup(*[wrapped_label(t, 1.3, 13, c).next_to(A.ax.c2p(k, 1.0), DOWN, buff=0.12)
                         for k, (_, t, c) in enumerate(vals)])
        tops = VGroup(*[label(f"{v:.2f}", font_size=15, color=c).next_to(A.ax.c2p(k, v), UP, buff=0.08)
                        for k, (v, _, c) in enumerate(vals)])
        rows = rows_of([
            (r"Holt-Lunstad, \ Smith and Layton, \ 2010: \ 148 studies, \ 308{,}849 people: \ stronger social "
             r"relationships, \ 1.5 times the odds of survival over the follow-up; \ 1.91 for complex measures of "
             r"social integration", GOOD),
            (r"Holt-Lunstad and colleagues, \ 2015: \ the odds of death were 1.29 times higher with social isolation "
             r"and 1.26 with loneliness", AUTH),
            (r"these are associations of a size comparable to familiar health risks", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.3, 0])
        tag = published_tag(r"Holt-Lunstad et al.\ (2010, \ 2015)")
        with self.voiceover(
            "The last question in this part is about health. <bookmark mark='a'/> In 2010 Julianne Holt-Lunstad "
            "and colleagues pooled a hundred and forty-eight studies of three hundred thousand people. Those with "
            "stronger social relationships had one and a half times the odds of surviving the follow-up, and nearly "
            "twice the odds for the most complete measures of social integration. <bookmark mark='b'/> In 2015 "
            "they reported that social isolation raised the odds of death by twenty-nine percent, and loneliness "
            "by twenty-six. <bookmark mark='c'/> These are associations of a size comparable to familiar health "
            "risks."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(*[GrowFromEdge(x[0], DOWN) for x in b[:2]], FadeIn(tops[:2]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(*[GrowFromEdge(x[0], DOWN) for x in b[2:]], FadeIn(tops[2:]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def causal(self):
        head = heading(r"Association, \ or cause?")
        nodes = VGroup(*[word_chip(t, color=c, font_size=20, width=2.6) for t, c in (
            (r"social ties", GOOD), (r"health", PERSON), (r"illness, \ poverty, \ depression", AUTH))])
        nodes[0].move_to([-5.0, 1.2, 0])
        nodes[1].move_to([-1.9, 1.2, 0])
        nodes[2].move_to([-3.45, -0.6, 0])
        a1 = Arrow(nodes[0].get_right(), nodes[1].get_left(), buff=0.1, color=GOOD)
        a2 = CurvedArrow(nodes[1].get_bottom() + DOWN * 0.05, nodes[0].get_bottom() + DOWN * 0.05, angle=-0.8,
                         color=GREY_B)
        a3 = VGroup(Arrow(nodes[2].get_top(), nodes[0].get_bottom(), buff=0.1, color=AUTH),
                    Arrow(nodes[2].get_top(), nodes[1].get_bottom(), buff=0.1, color=AUTH))
        rows = rows_of([
            (r"the studies are observational: \ ties may protect health", GOOD),
            (r"or poor health may cut people off: \ reverse causation", GREY_A),
            (r"or illness, \ poverty and depression may do both: \ confounding", AUTH),
            (r"the association held across people's health at the start, \ but observation cannot rule out every "
             r"alternative; \ randomized tests of connection on mortality do not exist", YOU),
        ], 5.6, 20, 0.38).move_to([3.6, -0.2, 0])
        with self.voiceover(
            "But association isn't cause. <bookmark mark='a'/> The studies are observational. Ties may protect "
            "health. <bookmark mark='b'/> Or poor health may cut people off, which is reverse causation. "
            "<bookmark mark='c'/> Or illness, poverty and depression may do both, which is confounding. "
            "<bookmark mark='d'/> The association held across people's health at the start, but observation can't "
            "rule out every alternative, and randomized tests of social connection on mortality don't exist. The "
            "frontier asks what could stand in for them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(nodes[:2]))
            vo.wait_until("a")
            self.play(GrowArrow(a1), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(a2), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(nodes[2]), GrowArrow(a3[0]), GrowArrow(a3[1]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
