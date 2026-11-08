from __future__ import annotations

from videos.philosophy.philosophy15.common import *  # noqa: F403

VCOL = {"good": OK, "contradictory": BAD, "inconclusive": GREY_B}


class Wheel(VoiceoverScene):
    def construct(self):
        card = chapter_card(3, r"Inference in India", r"When is a reason a good reason?", lit=(150, 480),
                            part=PART)
        with self.voiceover("Chapter three. Inference in India."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.five()
        self.wheel()
        self.carvaka()

    def five(self):
        head = label(r"The Nyāya inference \ (\textit{Nyāya Sūtra}, \ c.\ 150)", font_size=30, color=CONN).to_edge(
            UP, buff=0.35)
        steps = [(r"thesis", r"the hill has fire"), (r"reason", r"because it has smoke"),
                 (r"example", r"wherever there is smoke there is fire, \ as in a kitchen"),
                 (r"application", r"this hill has smoke, \ which goes with fire"),
                 (r"conclusion", r"so the hill has fire")]
        g = VGroup()
        for i, (a, b) in enumerate(steps):
            x = label(a, font_size=22, color=PAST)
            y = label(b, font_size=23, color=FUT if i == 2 else WHITE)
            x.move_to([-4.6, 1.7 - i * 0.7, 0])
            y.move_to([-2.8 + y.width / 2, 1.7 - i * 0.7, 0])
            g.add(VGroup(x, y))
        vy = stack([(r"\textit{vyāpti}: \ `pervasion', \ invariable concomitance: \ smoke is pervaded by fire", GOAL),
                    (r"the example carries the general rule \textit{and} an instance of it", GREY_A)],
                   font_size=22).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Indian logicians faced the problem of induction more than a thousand years before Hume. "
            "<bookmark mark='a'/>The Nyāya school's standard inference has five members. The thesis: the hill has "
            "fire. <bookmark mark='b'/>The reason: because it has smoke. <bookmark mark='c'/>The example: wherever "
            "there is smoke there is fire, as in a kitchen. <bookmark mark='d'/>The application: this hill has smoke, "
            "which goes with fire. <bookmark mark='e'/>And the conclusion. <bookmark mark='f'/>The heart of it is "
            "vyāpti, pervasion: the invariable concomitance of smoke with fire. The example both states the general "
            "rule and shows an instance of it."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("f")
            self.play(FadeIn(vy))
        self.clear_scene()

    def wheel(self):
        d = load("wheel")["cells"]
        hc = history_card(480, r"Dignāga", r"\textit{Hetucakra}, \ the wheel of reasons", width=5.0,
                          color=HIST).to_corner(UL, buff=0.35)
        conds = stack([(r"a good reason must be:", WHITE),
                       (r"1. \ present in the subject \ (the hill)", GREY_A),
                       (r"2. \ present in similar cases \ (\textit{sapakṣa}: \ places with fire)", PAST),
                       (r"3. \ absent from dissimilar cases \ (\textit{vipakṣa}: \ places without)", FUT)],
                      font_size=21, aligned_edge=LEFT, width=6.0).move_to([3.6, 1.6, 0])
        cell = 1.25
        grid = VGroup()
        cells = {}
        for r_ in d:
            i = ["all", "some", "none"].index(r_["similar"])
            j = ["all", "some", "none"].index(r_["dissimilar"])
            pos = np.array([-4.4 + j * cell, -0.1 - i * cell, 0])
            sq = Square(side_length=cell - 0.08, stroke_color=GREY_C, stroke_width=2, fill_color=VCOL[r_["verdict"]],
                        fill_opacity=0.0).move_to(pos)
            t = label(r_["verdict"], font_size=15, color=WHITE).move_to(pos)
            cells[(i, j)] = (sq, t, r_)
            grid.add(VGroup(sq, t))
        rlab = VGroup(*[label(t, font_size=18, color=PAST).move_to([-5.55 - 0.35, -0.1 - i * cell, 0])
                        for i, t in enumerate((r"all", r"some", r"none"))])
        clab = VGroup(*[label(t, font_size=18, color=FUT).move_to([-4.4 + j * cell, 0.75, 0])
                        for j, t in enumerate((r"all", r"some", r"none"))])
        rt = label(r"in similar cases", font_size=18, color=PAST).rotate(PI / 2).move_to([-6.55, -1.35, 0])
        ct = label(r"in dissimilar cases", font_size=18, color=FUT).move_to([-3.15, 1.15, 0])
        res = stack([
            (r"the Reasoner checks each case: \ any counterexample? \ found with fire?", WHITE),
            (r"good: \ 2 \ \ (all or some similar, \ no dissimilar)", OK),
            (r"contradictory: \ 2 \ \ (found only where fire is absent)", BAD),
            (r"inconclusive: \ the other 5", GREY_B),
        ], font_size=21, aligned_edge=LEFT, width=6.0).move_to([3.6, -1.4, 0])
        with self.voiceover(
            "Dignāga, around 480, systematized the conditions in his wheel of reasons. <bookmark mark='a'/>A good "
            "reason must be present in the subject, present in similar cases, places with fire, and absent from "
            "dissimilar cases, places without. <bookmark mark='b'/>A reason can occur in all, some or none of the "
            "similar cases, and in all, some or none of the dissimilar ones: nine combinations, a wheel of three by "
            "three. <bookmark mark='c'/>The Reasoner builds a small universe for each and checks the two things that "
            "matter: the reason never occurs without the property, and it does occur with it. "
            "<bookmark mark='d'/>Exactly two cells are good: present in all or some similar cases, and in no "
            "dissimilar case. <bookmark mark='e'/>Two are contradictory: they support the opposite conclusion. "
            "<bookmark mark='f'/>The other five are inconclusive, which is Dignāga's classification exactly."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in conds], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*[g[0] for g in grid])), FadeIn(rlab), FadeIn(clab), FadeIn(rt), FadeIn(ct))
            vo.wait_until("c")
            self.play(FadeIn(res[0]))
            for mk, verdict in zip("def", ("good", "contradictory", "inconclusive")):
                vo.wait_until(mk)
                sel = [c for c in cells.values() if c[2]["verdict"] == verdict]
                self.play(*[c[0].animate.set_fill(VCOL[verdict], opacity=0.45) for c in sel],
                          *[FadeIn(c[1]) for c in sel], FadeIn(res["def".index(mk) + 1]))
        self.clear_scene()

    def carvaka(self):
        head = label(r"But how is pervasion known?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"the Cārvāka skeptic", r"perception shows only these smokes and these fires; \ inference needs "
                                     r"pervasion, \ and pervasion would need inference: \ a circle", BAD),
            (r"Dharmakīrti \ (7th c.)", r"pervasion rests on real relations: \ identity of nature, \ or cause and "
                                        r"effect: \ smoke is fire's effect", OK),
            (r"Gaṅgeśa \ (14th c.)", r"we perceive the universal: \ seeing smoke, \ we see \textit{smokeness}, \ "
                                     r"and so all smoke", OK),
            (r"Hume, \ 1748", r"the same circle, \ in the same place", GOAL),
        ]
        g = VGroup()
        top = 1.9
        for a, b, c in rows:
            x = label(a, font_size=22, color=c)
            y = wrapped_label(b, 8.8, 21, WHITE)
            x.move_to([-6.5 + x.width / 2, top - x.height / 2, 0])
            y.move_to([-3.0 + y.width / 2, top - y.height / 2, 0])
            g.add(VGroup(x, y))
            top -= max(x.height, y.height) + 0.45
        with self.voiceover(
            "How is pervasion known? <bookmark mark='a'/>The Cārvāka materialists pressed exactly Hume's objection. "
            "Perception shows us only these smokes and these fires, never all of them. Inference needs pervasion, and "
            "establishing pervasion would need inference: a circle. <bookmark mark='b'/>Dharmakīrti, in the seventh "
            "century, answered that pervasion rests on real relations: identity of nature, or cause and effect. Smoke "
            "is the effect of fire, so it cannot occur without it. <bookmark mark='c'/>Gaṅgeśa, founder of the new "
            "Nyāya in the fourteenth century, held that in seeing smoke we perceive smokeness, the universal, and so, "
            "in a way, all smoke. <bookmark mark='d'/>Hume rediscovered the circle, and the debate over what could "
            "break it, in the same place."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r[0]), FadeIn(r[1], shift=LEFT * 0.1))
        self.clear_scene()
