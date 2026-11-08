from __future__ import annotations

from videos.philosophy.philosophy24.common import *  # noqa: F403


class Regularity(VoiceoverScene):
    def construct(self):
        card = chapter_card(1, r"Laws as regularities", r"What makes a law more than a pattern?",
                            lit=(1748, 1989), part=PART)
        with self.voiceover("Chapter one. Laws as regularities."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.naive()
        self.spheres()
        self.tests()
        self.mosaic()

    def naive(self):
        head = label(r"The regularity view", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        f = MathTex(r"\text{law} \;=\; \text{a true generalization}\quad \forall x\,(Fx \to Gx)", font_size=40,
                    color=LAW).move_to([0, 1.4, 0])
        rows = stack([(r"Hume: \ we never observe necessity, \ only constant conjunction", HIST),
                      (r"so a law is just a pattern that holds everywhere and always", LAW),
                      (r"`all copper conducts electricity', \ `all ravens are black' \ (Part 15)", WHITE),
                      (r"the trouble: \ many true generalizations are no laws at all", BAD)], font_size=22,
                     aligned_edge=LEFT, width=11.0, buff=0.32).move_to([0, -0.9, 0])
        with self.voiceover(
            "Start with the simplest answer. <bookmark mark='a'/>A law of nature is a true generalization: everything "
            "that is F is G. <bookmark mark='b'/>Hume is the source. When one billiard ball strikes another, we see "
            "the first move and then the second, but never a necessity connecting them; all experience shows is "
            "constant conjunction. <bookmark mark='c'/>So, on the regularity view, a law is nothing more than a "
            "pattern that holds everywhere and always. <bookmark mark='d'/>All copper conducts electricity; every "
            "massive body attracts every other. <bookmark mark='e'/>The trouble is that a great many true "
            "generalizations are not laws at all."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
            vo.wait_until("e")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def spheres(self):
        head = label(r"Two spheres", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        g_ball = Circle(radius=1.0, color=DATA, fill_color=DATA, fill_opacity=0.35, stroke_width=3).move_to(
            [-3.6, 0.7, 0])
        u_ball = Circle(radius=0.35, color=OK, fill_color=OK, fill_opacity=0.35, stroke_width=3).move_to(
            [3.6, 0.7, 0])
        g_txt = label(r"`every sphere of gold is less than a mile across'", font_size=21, color=DATA).next_to(
            g_ball, DOWN, buff=0.35)
        u_txt = label(r"`every sphere of uranium-235 is less than a mile across'", font_size=21,
                      color=OK).next_to(u_ball, DOWN, buff=1.0)
        g_why = wrapped_label(r"true, \ but an accident: \ there is not enough gold in one place, \ and nothing "
                              r"forbids it", 5.6, 20, WHITE).next_to(g_txt, DOWN, buff=0.3)
        u_why = wrapped_label(r"true, \ and no accident: \ about 52 kg of it, \ a sphere some 17 cm across, \ is "
                              r"critical, \ and a larger one explodes", 5.6, 20, WHITE).next_to(u_txt, DOWN, buff=0.3)
        same = label(r"the same logical form, \ $\forall x\,(Sx \to Lx)$; \ the difference is not in the form",
                     font_size=22, color=GOAL).to_edge(DOWN, buff=0.45)
        grow = Circle(radius=0.35, color=BAD, stroke_width=3).move_to(u_ball)
        with self.voiceover(
            "Bas van Fraassen made the point with a famous pair of sentences. <bookmark mark='a'/>Every sphere of "
            "gold is less than a mile across. True, as far as anyone knows: there is not that much gold gathered in "
            "one place. But it is an accident. Nothing in nature forbids a golden sphere a mile wide; the world "
            "simply never made one. <bookmark mark='b'/>Every sphere of uranium-235 is less than a mile across. "
            "Also true, and no accident. <bookmark mark='c'/>Gather about fifty-two kilograms of uranium-235 into a "
            "sphere some seventeen centimetres across, and it is critical: a chain reaction runs away, and a larger "
            "sphere cannot hold together. <bookmark mark='d'/>The two sentences have exactly the same logical form. "
            "Whatever makes the second a law and the first an accident, it is not the form of the sentence."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(GrowFromCenter(g_ball), FadeIn(g_txt))
            self.play(FadeIn(g_why))
            vo.wait_until("b")
            self.play(GrowFromCenter(u_ball), FadeIn(u_txt))
            vo.wait_until("c")
            self.play(FadeIn(u_why), Create(grow))
            self.play(grow.animate.scale(1.6).set_stroke(opacity=0), run_time=1.2)
            vo.wait_until("d")
            self.play(FadeIn(same))
        self.clear_scene()

    def tests(self):
        head = label(r"What laws do that accidents do not", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        hd = [r"\text{test}", r"\text{uranium}", r"\text{gold}"]
        tests = [(r"\text{supports counterfactuals}", True, False),
                 (r"\text{explains its instances}", True, False),
                 (r"\text{confirmed by its instances}", True, False),
                 (r"\text{true}", True, True)]
        rows = [[MathTex(a, font_size=24), mark(b), mark(c)] for a, b, c in tests]
        grid = ValueGrid(hd, rows, col_w=[4.6, 1.8, 1.8], cell_h=0.6, font_size=22).move_to([-2.4, 0.2, 0])
        side = stack([(r"`if this were a mile-wide sphere of uranium, \ it would have exploded': \ true", OK),
                      (r"`if this were a mile-wide sphere of gold, \dots': \ no law forbids it", DATA),
                      (r"and laws can be vacuous or uninstantiated: \ Newton's first law; \ Tooley's particles",
                       ABS)], font_size=20, aligned_edge=LEFT, width=4.6, buff=0.35).move_to([4.6, 0.2, 0])
        with self.voiceover(
            "Laws do jobs that accidents cannot. <bookmark mark='a'/>A law supports counterfactuals: if this were a "
            "mile-wide sphere of uranium, it would have exploded. Nothing similar holds for gold. "
            "<bookmark mark='b'/>A law explains its instances: this sphere is small because larger ones go critical. "
            "The gold sphere is small for no reason in particular. <bookmark mark='c'/>And a law is confirmed by its "
            "instances, as Part 15 found when Goodman separated lawlike from accidental predicates. "
            "<bookmark mark='d'/>Both sentences are true. Truth alone does not separate them. <bookmark mark='e'/>"
            "Worse, some laws have no instances at all. Newton's first law describes bodies on which no force acts, "
            "and there may be none. Michael Tooley imagined ten kinds of fundamental particle, with laws for every "
            "pair that meets, and one pair that never does: surely there is still a fact about how they would "
            "interact. On the regularity view every vacuous generalization is true, so every one would be a law."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            for mk, r in zip("abcd", range(4)):
                vo.wait_until(mk)
                self.play(*[FadeIn(c) for c in grid.cell[r]])
                if r < 2:
                    self.play(FadeIn(side[r]))
            vo.wait_until("e")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def mosaic(self):
        q = quote_card(r"All there is to the world is a vast mosaic of local matters of particular fact, \ just one "
                       r"little thing and then another.", r"David Lewis",
                       r"\textit{Philosophical Papers}, \ volume II \ (1986), \ introduction", width=10.4,
                       font_size=24).to_edge(UP, buff=0.4)
        rng = np.random.default_rng(1986)
        cells = VGroup()
        cols, rws, s = 24, 6, 0.36
        for i in range(cols):
            for j in range(rws):
                v = (i + 2 * j) % 5 == 0 or rng.random() < 0.06
                sq = Square(side_length=s * 0.9, stroke_width=0, fill_color=LAW if v else GREY_E,
                            fill_opacity=0.9 if v else 0.6)
                sq.move_to([(i - cols / 2 + 0.5) * s, -0.8 + (j - rws / 2 + 0.5) * s, 0])
                cells.add(sq)
        lab = label(r"the laws: \ the best summary of the pattern \ (chapter 2)", font_size=22,
                    color=GOAL).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "David Lewis kept Hume's picture and repaired it. <bookmark mark='a'/>All there is to the world, he "
            "wrote, is a vast mosaic of local matters of particular fact, just one little thing and then another. "
            "This is Humean supervenience: no necessary connections, only the mosaic. <bookmark mark='b'/>Here is a "
            "toy mosaic, a strip of cells, some lit. There is a pattern in it, with a few cells that break it. "
            "<bookmark mark='c'/>For Lewis the laws are not extra ingredients in the mosaic. They are the best "
            "summary of it. The next chapter builds that idea and puts a number on what best means."
        ) as vo:
            self.play(FadeIn(q))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.005), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(lab))
        self.clear_scene()
