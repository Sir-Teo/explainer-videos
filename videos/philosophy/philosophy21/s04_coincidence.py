from __future__ import annotations

from videos.philosophy.philosophy21.common import *  # noqa: F403


class Coincidence(VoiceoverScene):
    def construct(self):
        card = chapter_card(3, r"The statue and the lump", r"Can two things be in the same place at once?",
                            lit=(1975, 2000), part=PART)
        with self.voiceover("Chapter three. The statue and the lump."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.puzzle()
        self.views()
        self.profiles()
        self.grounding()

    def puzzle(self):
        hc = history_card(1975, r"Allan Gibbard", r"`Contingent Identity': \ Lumpl and Goliath", width=6.4,
                          color=HIST).to_corner(UL, buff=0.3)
        lump = Polygon([-5.6, -2.0, 0], [-5.2, -0.6, 0], [-4.4, -0.3, 0], [-3.6, -0.7, 0], [-3.3, -2.0, 0],
                       color=WHOLE, fill_opacity=0.5)
        statue = VGroup(Circle(radius=0.32, color=NOM, fill_opacity=0.3).move_to([-1.4, 0.3, 0]),
                        Polygon([-1.9, -0.1, 0], [-0.9, -0.1, 0], [-0.7, -2.0, 0], [-2.1, -2.0, 0], color=NOM,
                                fill_opacity=0.3))
        ar = Arrow([-3.1, -1.1, 0], [-2.2, -1.1, 0], buff=0.05, color=GREY_B)
        hd = [r"", r"\text{the lump}", r"\text{the statue}"]
        rows = [[MathTex(r"\text{same matter, place, shape now}", font_size=20), MathTex(r"\checkmark", font_size=24,
                                                                                         color=OK),
                 MathTex(r"\checkmark", font_size=24, color=OK)],
                [MathTex(r"\text{could survive being squashed}", font_size=20), MathTex(r"\checkmark", font_size=24,
                                                                                        color=OK),
                 MathTex(r"\times", font_size=24, color=BAD)],
                [MathTex(r"\text{existed yesterday, before sculpting}", font_size=20),
                 MathTex(r"\checkmark", font_size=24, color=OK), MathTex(r"\times", font_size=24, color=BAD)]]
        grid = ValueGrid(hd, rows, col_w=[4.6, 1.6, 1.6], cell_h=0.6, font_size=19).move_to([2.8, 0.4, 0])
        concl = label(r"by Leibniz's law, \ the lump is not the statue: \ two things in one place", font_size=20,
                      color=GOAL).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "A sculptor takes a lump of clay on Monday and on Tuesday shapes it into a statue. "
            "<bookmark mark='a'/>Now the statue and the lump occupy the same place, with the same matter and the same "
            "shape. <bookmark mark='b'/>But the lump could survive being squashed into a ball, and the statue could "
            "not. <bookmark mark='c'/>And the lump existed on Monday, before the statue did. <bookmark mark='d'/>So by "
            "Leibniz's law the statue and the lump differ in properties, and are two things in one place. Allan "
            "Gibbard made it harder: a clay statue made all at once, and destroyed all at once, so that the two share "
            "their whole history, and still differ in what could have happened to them."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(lump))
            vo.wait_until("a")
            self.play(GrowArrow(ar), FadeIn(statue), FadeIn(grid.head), Create(grid.rule), FadeIn(VGroup(*grid.cell[0])))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*grid.cell[1])))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*grid.cell[2])))
            vo.wait_until("d")
            self.play(FadeIn(concl))
        self.clear_scene()

    def views(self):
        head = label(r"Pluralists and monists", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"pluralism", r"two objects, \ one place: \ the statue is \textit{constituted by} the lump, \ not "
                           r"identical to it \ (Wiggins; \ Baker, \ 2000)", NOM),
            (r"its cost", r"classical mereology says same parts, \ same thing \ (Part 20's strong supplementation)",
             BAD),
            (r"monism", r"one object: \ `statue' and `lump' are two ways of describing it", WHOLE),
            (r"its cost", r"then what of the modal difference? \ Lewis \ (1971): \ different counterpart relations, \ "
                          r"selected by the sortal \ (Part 22)", ABS),
            (r"nihilism", r"Part 20's van Inwagen: \ there is no statue and no lump, \ only simples arranged statue-wise",
             GREY_A),
        ]
        g = rows_table(rows, top=1.6, gap=0.5, width=8.8, x_text=-2.4, label_size=21)
        with self.voiceover(
            "Two families of answer. <bookmark mark='a'/>Pluralists accept two objects in one place: the statue is "
            "constituted by the lump without being identical to it. David Wiggins and Lynne Rudder Baker defend this. "
            "<bookmark mark='b'/>The cost is that classical mereology, from Part 20, says that things with the same "
            "parts are the same thing. <bookmark mark='c'/>Monists say there is one object, and statue and lump are "
            "two ways of describing it. <bookmark mark='d'/>Their cost is to explain the modal difference. David Lewis "
            "said that different words call up different counterpart relations, a theory we meet in Part 22. "
            "<bookmark mark='e'/>And Part 20's nihilist says there is neither statue nor lump, only simples arranged "
            "statue-wise."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def grounding(self):
        head = label(r"The grounding problem", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = stack([(r"the statue and the lump are alike in every physical respect, \ at every moment", WHITE),
                      (r"so what makes it true that one could survive squashing and the other could not?", GOAL),
                      (r"Bennett \ (2004); \ Zimmerman: \ the modal difference seems to float free", BAD),
                      (r"answers: \ sortal essences; \ the sculptor's intentions; \ conventions of description", UNIV),
                      (r"a test case for grounding \ (Part 20): \ must every difference have a base?", ABS)],
                     font_size=21, aligned_edge=LEFT, width=11.4).to_edge(DOWN, buff=0.4)
        rng = np.random.default_rng(21)
        pts = [[rng.uniform(-0.42, 0.42), rng.uniform(-1.35, 0.2), 0] for _ in range(22)] + \
              [[0.18 * np.cos(t), 0.75 + 0.18 * np.sin(t), 0] for t in np.linspace(0, 2 * PI, 5)[:-1]]

        def figure(col, name):
            sil = VGroup(Circle(radius=0.32, color=col, fill_opacity=0.12).move_to([0, 0.75, 0]),
                         Polygon([-0.5, 0.35, 0], [0.5, 0.35, 0], [0.7, -1.5, 0], [-0.7, -1.5, 0], color=col,
                                 fill_opacity=0.12))
            dots = VGroup(*[Dot(p_, radius=0.045, color=GREY_A) for p_ in pts])
            nm = label(name, font_size=20, color=col).next_to(sil, DOWN, buff=0.15)
            return VGroup(sil, dots, nm)

        fl = figure(WHOLE, r"the lump").scale(0.85).move_to([-2.6, 1.3, 0])
        fs = figure(NOM, r"the statue").scale(0.85).move_to([2.6, 1.3, 0])
        same = VGroup(MathTex(r"=", font_size=48, color=OK), label(r"every particle, \ every moment", font_size=18,
                                                                    color=OK)).arrange(DOWN, buff=0.1).move_to(
            [0, 1.6, 0])
        diff = VGroup(MathTex(r"\ne", font_size=40, color=BAD), label(r"what each could survive", font_size=18,
                                                                       color=BAD)).arrange(DOWN, buff=0.1).move_to(
            [0, 0.5, 0])
        with self.voiceover(
            "The pluralist faces a further problem. <bookmark mark='a'/>The statue and the lump are alike in every "
            "physical respect, at every moment of their existence. <bookmark mark='b'/>So what grounds the difference "
            "in what could happen to them? <bookmark mark='c'/>Karen Bennett and Dean Zimmerman pressed this "
            "grounding problem: the modal difference seems to float free of everything else. <bookmark mark='d'/>"
            "Answers appeal to sortal essences, to the sculptor's intentions, or to conventions of description. "
            "<bookmark mark='e'/>It is a test case for Part 20's grounding: must every difference rest on some "
            "difference beneath it?"
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(fl), FadeIn(fs), FadeIn(same), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(diff), FadeIn(rows[1]))
            for mk, r in zip("cde", rows[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def profiles(self):
        d = load("modal")
        head = label(r"Same now, \ different modal profiles", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        hd = [r"\text{scenario}", r"\text{the lump}", r"\text{the statue}"]
        rows = []
        for sc in d["scenarios"]:
            rows.append([MathTex(r"\text{" + sc["case"] + "}", font_size=21),
                         MathTex(r"\text{exists}" if sc["lump"] else r"\text{gone}", font_size=21,
                                 color=OK if sc["lump"] else BAD),
                         MathTex(r"\text{exists}" if sc["statue"] else r"\text{gone}", font_size=21,
                                 color=OK if sc["statue"] else BAD)])
        grid = ValueGrid(hd, rows, col_w=[5.6, 1.8, 1.8], cell_h=0.55, font_size=20).move_to([-0.6, 0.4, 0])
        notes = stack([(r"they differ in " + f"{d['differ']}" + r" of " + f"{len(d['scenarios'])}" +
                        r" scenarios, \ though alike in every actual respect", GOAL),
                       (r"persistence conditions are modal: \ what a thing could survive", UNIV)], font_size=19,
                      width=11.0).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "The Reasoner tabulates the two objects across possible scenarios. <bookmark mark='a'/>In the actual "
            "world both exist. <bookmark mark='b'/>Squash the clay into a ball, and the lump survives while the statue "
            "is destroyed. <bookmark mark='c'/>Replace one arm with new clay, and the statue survives, repaired, while "
            "the original lump is no longer all there. <bookmark mark='d'/>Had it never been sculpted, the lump would "
            "exist without the statue; melted down, neither survives. <bookmark mark='e'/>Alike in every actual "
            "respect, they differ in three of five scenarios. Persistence conditions are modal: they concern what a "
            "thing could survive."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            for mk, i in zip("abcd", range(4)):
                vo.wait_until(mk)
                self.play(FadeIn(VGroup(*grid.cell[i])))
                if i == 3:
                    self.play(FadeIn(VGroup(*grid.cell[4])))
            vo.wait_until("e")
            self.play(FadeIn(notes))
        self.clear_scene()
