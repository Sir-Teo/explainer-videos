from __future__ import annotations

from videos.philosophy.philosophy29.common import *  # noqa: F403

VCOL = {"2a": ACT, "2b": BAD, "3a": BODY, "3b": WORLD}
VNAME = {"2a": r"2a: \ uncrossed, \ excited \ (`fear')", "2b": r"2b: \ crossed, \ excited \ (`aggression')",
         "3a": r"3a: \ uncrossed, \ inhibited \ (`love')", "3b": r"3b: \ crossed, \ inhibited \ (`exploration')"}


class Body(VoiceoverScene):
    def construct(self):
        card = chapter_card(7, r"The lived body", r"Do we think with our bodies?", lit=(1945, 1998), part=PART)
        with self.voiceover("Chapter seven. The lived body."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.merleau()
        self.vehicles()
        self.four_e()

    def merleau(self):
        hc = history_card(1945, r"Maurice Merleau-Ponty", r"\textit{Phenomenology of Perception}", width=6.4,
                          color=HIST).to_corner(UL, buff=0.3)
        rows = [
            (r"the body schema", r"not an object I have, \ but my hold on the world: \ I know where my hand is "
                                 r"without looking", BODY),
            (r"`I can'", r"consciousness is first `I can', \ not `I think': \ motor intentionality", ACT),
            (r"Schneider", r"a patient who could grasp his nose, \ but not point to it on command \ (Gelb and "
                           r"Goldstein)", OBJ),
            (r"the blind man's cane", r"with practice the cane's tip becomes the place where he feels the "
                                      r"pavement", WORLD),
            (r"the phantom limb", r"an arm that is gone, \ still reaching: \ the body schema outlives its organ", BAD),
        ]
        g = rows_table(rows, top=0.8, gap=0.4)
        with self.voiceover(
            "For Maurice Merleau-Ponty, in 1945, the subject of perception is not a mind but a body. "
            "<bookmark mark='a'/>The body schema is not an object I have, but my hold on the world: I know where my "
            "hand is without looking, and can reach a cup in the dark. <bookmark mark='b'/>Consciousness is "
            "originally not I think but I can: motor intentionality, directed at things as things to do. "
            "<bookmark mark='c'/>His evidence included a patient, Schneider, studied by Adhémar Gelb and Kurt "
            "Goldstein, who after a war wound could grasp his nose to blow it, but could not point to it on command. "
            "Concrete action survived; abstract movement did not. <bookmark mark='d'/>A blind man's cane, with "
            "practice, stops being an object in his hand: its tip becomes the place where he feels the pavement. "
            "<bookmark mark='e'/>And the phantom limb, an arm that is gone but still reaches for things, shows the "
            "body schema outliving its organ."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def vehicles(self):
        d = load("vehicles")
        head = label(r"Braitenberg's vehicles, \ simulated", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        V = d["vehicles"]
        assert V["2a"]["min_dist"] > 1.5 and V["2b"]["min_dist"] < 0.5 and abs(V["3a"]["final_dist"] - 1.294) < 1e-3
        assert V["3b"]["final_dist"] > 20 and d["start"] == [-3.0, -1.2, 0.0]
        sc, cx, cy = 0.62, -2.3, -0.6

        def P(p):
            return np.array([cx + sc * p[0], cy + sc * p[1], 0])

        lamp = VGroup(*[Circle(radius=r, color=SIGN, stroke_width=0, fill_opacity=0.12).move_to(P(d["light"]))
                        for r in (0.9, 0.6, 0.35)], Dot(P(d["light"]), radius=0.12, color=SIGN))
        frame = Rectangle(width=7.4, height=5.6, color=GREY_D, stroke_width=1).move_to([cx, cy, 0])
        paths, tags = VGroup(), VGroup()
        for k in ("2a", "2b", "3a", "3b"):
            pts = [P(p) for p in V[k]["path"]]
            pts = [p for p in pts if abs(p[0] - cx) < 3.65 and abs(p[1] - cy) < 2.75]
            paths.add(VMobject(color=VCOL[k], stroke_width=5 if k == "3a" else 3).set_points_as_corners(pts))
        start = Dot(P(d["start"][:2]), radius=0.1, color=WHITE)
        rest = Dot(P(V["3a"]["final"]), radius=0.1, color=VCOL["3a"])
        rl = label(r"comes to rest", font_size=16, color=VCOL["3a"]).next_to(rest, DOWN, buff=0.1)
        key = VGroup(*[label(VNAME[k], font_size=18, color=VCOL[k]) for k in ("2a", "2b", "3a", "3b")]).arrange(
            DOWN, buff=0.25, aligned_edge=LEFT).move_to([4.4, 1.0, 0])
        car = VGroup(Rectangle(width=0.9, height=0.6, color=WHITE), Dot([0.45, 0.22, 0], color=SIGN),
                     Dot([0.45, -0.22, 0], color=SIGN), Rectangle(width=0.3, height=0.12, color=GREY_B).move_to(
                [-0.2, 0.36, 0]), Rectangle(width=0.3, height=0.12, color=GREY_B).move_to([-0.2, -0.36, 0])
                     ).scale(0.9).move_to([4.4, -1.4, 0])
        cl = label(r"two light sensors, \ two wheels, \ two wires", font_size=17, color=GREY_A).next_to(car, DOWN,
                                                                                                    buff=0.15)
        foot = label(r"nothing inside represents the light: \ the behaviour is in the coupling of body and world",
                     font_size=20, color=GOAL).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "In 1984 the neuroscientist Valentino Braitenberg imagined the simplest possible bodies. "
            "<bookmark mark='a'/>A vehicle with two light sensors at the front and two wheels at the back, and a "
            "wire from each sensor to a wheel. More light, and the wheel turns faster, or, with an inhibiting wire, "
            "slower. <bookmark mark='b'/>The Reasoner simulates four of them from the same start. Wire each sensor "
            "to the wheel on its own side, and the vehicle turns away from the light and leaves: Braitenberg called "
            "it fear. <bookmark mark='c'/>Cross the wires, and it turns toward the light and rushes at it, passing "
            "within half a unit: aggression. <bookmark mark='d'/>Make the wires inhibiting, uncrossed, and it turns "
            "toward the light and slows, coming to rest facing it, a little over one unit away: love. Inhibiting "
            "and crossed, it approaches, then veers off and away: exploration. <bookmark mark='e'/>Nothing inside "
            "any of them represents the light, or has a goal. The behaviour, which an observer cannot help describing "
            "in the language of feeling, lives in the coupling of a body with its world."
        ) as vo:
            self.play(FadeIn(head), Create(frame), FadeIn(lamp))
            vo.wait_until("a")
            self.play(FadeIn(car), FadeIn(cl), FadeIn(start))
            vo.wait_until("b")
            self.play(Create(paths[0]), FadeIn(key[0]), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(paths[1]), FadeIn(key[1]), run_time=2.5)
            vo.wait_until("d")
            self.play(Create(paths[3]), FadeIn(key[3]), run_time=2.0)
            self.play(Create(paths[2]), FadeIn(key[2]), run_time=2.0)
            self.play(FadeIn(rest), FadeIn(rl))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def four_e(self):
        head = label(r"4E cognition", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"embodied", r"cognition depends on the body's form and skills \ (Varela, \ Thompson and Rosch, \ "
                          r"\textit{The Embodied Mind}, \ 1991)", BODY),
            (r"embedded", r"we offload work onto the world: \ Tetris players rotate pieces on screen to think \ "
                          r"(Kirsh and Maglio, \ 1994)", WORLD),
            (r"enactive", r"perceiving is knowing how sensations change as we move \ (O'Regan and No\"e, \ 2001)", ACT),
            (r"extended", r"Otto's notebook plays the role of Inga's memory, \ so it is part of his mind \ (Clark and "
                          r"Chalmers, \ 1998)", OBJ),
            (r"the critics", r"coupling is not constitution: \ a notebook \textit{causes} thinking, \ it does not "
                             r"\textit{think} \ (Adams and Aizawa, \ 2008)", BAD),
        ]
        g = rows_table(rows, top=1.6, gap=0.42)
        with self.voiceover(
            "Merleau-Ponty's body returned to cognitive science as four E's. <bookmark mark='a'/>Embodied: cognition "
            "depends on the form and skills of the body, the thesis of Francisco Varela, Evan Thompson and Eleanor "
            "Rosch's book The Embodied Mind, in 1991. <bookmark mark='b'/>Embedded: we offload work onto the world. "
            "David Kirsh and Paul Maglio found that Tetris players rotate pieces on the screen to help them decide "
            "where they fit, faster than they could rotate them in their heads. <bookmark mark='c'/>Enactive: "
            "perceiving is knowing how sensations change as we move, in Kevin O'Regan and Alva Noë's sensorimotor "
            "account. <bookmark mark='d'/>Extended: Andy Clark and David Chalmers argued in 1998 that Otto, who has "
            "Alzheimer's and relies on a notebook, has a mind that includes it, because the notebook plays the role "
            "that memory plays for Inga. <bookmark mark='e'/>The critics, Fred Adams and Ken Aizawa among them, reply "
            "that this confuses coupling with constitution: a notebook can cause thinking without itself thinking."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
