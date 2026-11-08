from __future__ import annotations

from videos.philosophy.philosophy20.common import *  # noqa: F403


class Vagueness(VoiceoverScene):
    def construct(self):
        card = chapter_card(8, r"Vagueness, and composition as identity", r"Can it be vague whether something "
                            r"exists?", lit=(1986, 2001), part=PART)
        with self.voiceover("Chapter eight. Vagueness, and composition as identity."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.sorites()
        self.argument()
        self.brick()
        self.identity()

    def sorites(self):
        head = label(r"A sorites series of compositions", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        frames = VGroup()
        gaps = [0.0, 0.15, 0.45, 0.9, 1.5, 2.4]
        for k, gpx in enumerate(gaps):
            cx = -5.6 + 2.25 * k
            a = Square(side_length=0.45, color=PARTC, fill_opacity=0.7).move_to([cx - 0.25 - gpx / 4, 0.6, 0])
            b = Square(side_length=0.45, color=PARTC, fill_opacity=0.7).move_to([cx + 0.25 + gpx / 4, 0.6, 0])
            t = label(r"case " + f"{k + 1}", font_size=16, color=GREY_A).move_to([cx, -0.1, 0])
            frames.add(VGroup(a, b, t))
        arrow = Arrow([-6.0, -0.6, 0], [6.0, -0.6, 0], buff=0, color=GREY_B, stroke_width=2)
        al = VGroup(label(r"clearly compose", font_size=16, color=OK).move_to([-5.3, -0.95, 0]),
                    label(r"clearly do not", font_size=16, color=BAD).move_to([5.4, -0.95, 0]))
        rows = stack([(r"glued, \ touching, \ nearly touching, \ \dots, \ a metre apart, \ a mile apart", WHITE),
                      (r"if composition is restricted, \ somewhere it stops", GOAL),
                      (r"a sharp cut-off between two neighbouring cases seems arbitrary", BAD)], font_size=20,
                     width=12.0).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Moderate answers face a challenge from vagueness. <bookmark mark='a'/>Line up cases. Two blocks glued "
            "together; touching; nearly touching; a little apart; a metre apart; a mile apart. "
            "<bookmark mark='b'/>At one end they clearly compose something; at the other, on any moderate view, they "
            "clearly do not. So composition must stop somewhere along the series. <bookmark mark='c'/>But any sharp "
            "cut-off between two neighbouring cases, differing by a hair, seems arbitrary."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(f) for f in frames], lag_ratio=0.25), GrowArrow(arrow), FadeIn(al),
                      FadeIn(rows[0]), run_time=2.5)
            for mk, r in zip("bc", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def argument(self):
        head = label(r"Lewis and Sider's argument from vagueness", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        steps = [
            (r"1. \ if composition is restricted, \ there is a sorites series from composing to not composing", WHITE),
            (r"2. \ no case in the series is a sharp cut-off", GREY_A),
            (r"3. \ so if restricted, \ composition is sometimes vague", GOAL),
            (r"4. \ but if composition is vague, \ the number of things that exist is vague", BAD),
            (r"5. \ and a numerical sentence has no vague words in it:", BAD),
        ]
        g = stack(steps, font_size=21, aligned_edge=LEFT, width=11.6, buff=0.25).move_to([0, 0.8, 0])
        f = MathTex(r"\exists x \, \exists y \, \big(x \ne y \land \forall z \,(z = x \lor z = y)\big)",
                    font_size=36, color=UNIV).next_to(g, DOWN, buff=0.35)
        fl = label(r"`there are exactly two things': \ only quantifiers, \ identity and connectives", font_size=18,
                   color=GREY_A).next_to(f, DOWN, buff=0.12)
        concl = label(r"6. \ so composition is not restricted: \ it always happens \ (or, \ for the nihilist, \ never)", font_size=22,
                      color=OK).next_to(fl, DOWN, buff=0.35)
        with self.voiceover(
            "David Lewis and Ted Sider turned this into an argument. <bookmark mark='a'/>If composition is "
            "restricted, there is a series of cases running from composition to its absence. "
            "<bookmark mark='b'/>No case in the series is a sharp cut-off. <bookmark mark='c'/>So composition is "
            "sometimes vague: it is indeterminate whether some things compose anything. <bookmark mark='d'/>But then "
            "it is indeterminate how many things exist. <bookmark mark='e'/>And how many things exist can be said in "
            "pure logic. There are exactly two things: there is an x and a y, distinct, and everything is one or the "
            "other. Quantifiers, identity and connectives are not vague. <bookmark mark='f'/>So composition is not "
            "restricted after all: it is unrestricted, or, for the nihilist, it never happens."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            self.play(Write(f), FadeIn(fl))
            vo.wait_until("f")
            self.play(FadeIn(concl))
        self.clear_scene()

    def brick(self):
        w = wall(upto=20, current=20).scale(0.44).to_edge(LEFT, buff=0.3).shift(DOWN * 0.3)
        card = wall_card(20, width=6.2, font_size=22).to_edge(RIGHT, buff=0.3)
        rows = card[1][1]
        with self.voiceover(
            "This is the twentieth brick in the Wall. <bookmark mark='a'/>The dream: a principled answer to when "
            "parts make a whole, one that counts tables and organisms but not the sum of my nose and the Eiffel "
            "Tower. <bookmark mark='b'/>The wall: van Inwagen's special composition question, sharpened by the "
            "argument from vagueness: every moderate answer seems to need a sharp cut-off, or vague existence. "
            "<bookmark mark='c'/>What it forces: a choice between nihilism, universalism, or accepting that it can be "
            "vague what exists."
        ) as vo:
            self.play(FadeIn(w))
            vo.wait_until("a")
            self.play(Indicate(w.brick[20], color=P.CONCL, scale_factor=1.08), FadeIn(card[0]), FadeIn(card[1][0]),
                      FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def identity(self):
        head = label(r"Composition as identity", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        h = hasse(7, [(0, 3), (1, 3), (0, 4), (2, 4), (1, 5), (2, 5), (3, 6), (4, 6), (5, 6)],
                  names=[r"$a$", r"$b$", r"$c$", r"$ab$", r"$ac$", r"$bc$", r"$abc$"], center=[-3.8, -0.4, 0],
                  width=3.2, height=2.8)
        rows = stack([(r"Baxter \ (1988); \ Lewis \ (1991): \ the whole \textit{is} the parts, \ taken together", WHOLE),
                      (r"so the sums are `no addition to being': \ universalism comes free", OK),
                      (r"count the atoms: \ 3; \ count everything: \ 7; \ which is the number of things?", GOAL),
                      (r"Leibniz's law: \ the parts are many, \ the whole is one: \ how can they be identical?", BAD),
                      (r"Sider \ (2007), \ Cotnoir \ (2013): \ a plural identity, \ with its own logic", UNIV)],
                     font_size=20, aligned_edge=LEFT, width=7.0).move_to([3.0, -0.4, 0])
        with self.voiceover(
            "Universalism seems profligate: every scattered collection is one more thing. "
            "<bookmark mark='a'/>Donald Baxter and David Lewis replied with composition as identity: a whole is "
            "nothing over and above its parts; it is the parts, taken together. <bookmark mark='b'/>Then the sums "
            "are no addition to being, and universalism comes for free. <bookmark mark='c'/>But count. Three atoms "
            "and their sums: are there three things here, or seven? <bookmark mark='d'/>And Leibniz's law: the parts "
            "are three, the whole is one, so how can they be identical? <bookmark mark='e'/>Ted Sider and Aaron "
            "Cotnoir have developed identity between one thing and many things, with its own logic, to make the "
            "view coherent."
        ) as vo:
            self.play(FadeIn(head), FadeIn(h))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
