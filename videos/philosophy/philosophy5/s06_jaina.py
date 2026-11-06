from __future__ import annotations

from videos.philosophy.philosophy5.common import *  # noqa: F403

SKT = {("t",): r"\textit{syād asti}", ("f",): r"\textit{syān nāsti}", ("t", "f"): r"\textit{syād asti nāsti}",
       ("i",): r"\textit{syād avaktavya}", ("t", "i"): r"\textit{syād asti avaktavya}",
       ("f", "i"): r"\textit{syān nāsti avaktavya}", ("t", "f", "i"): r"\textit{syād asti nāsti avaktavya}"}
EN = {"t": r"it is", "f": r"it is not", "i": r"it is inexpressible"}
COL = {"t": OK, "f": BAD, "i": BOTH}


def elephant(center=ORIGIN, s=1.0) -> VGroup:
    """A simple elephant from ellipses and lines."""
    c = np.asarray(center, float)
    body = Ellipse(width=3.0 * s, height=1.8 * s, stroke_color=GREY_B, stroke_width=2.5).move_to(c)
    head = Circle(radius=0.62 * s, stroke_color=GREY_B, stroke_width=2.5).move_to(c + np.array([1.75, 0.45, 0]) * s)
    ear = Ellipse(width=0.7 * s, height=0.95 * s, stroke_color=GREY_B, stroke_width=2.5).move_to(
        c + np.array([1.45, 0.45, 0]) * s)
    trunk = VMobject(stroke_color=GREY_B, stroke_width=3).set_points_smoothly(
        [c + np.array([2.25, 0.25, 0]) * s, c + np.array([2.6, -0.3, 0]) * s, c + np.array([2.55, -0.95, 0]) * s,
         c + np.array([2.35, -1.2, 0]) * s])
    tusk = Line(c + np.array([2.05, 0.0, 0]) * s, c + np.array([2.45, -0.35, 0]) * s, color=GREY_A, stroke_width=3)
    legs = VGroup(*[Rectangle(width=0.32 * s, height=0.85 * s, stroke_color=GREY_B, stroke_width=2.5).move_to(
        c + np.array([x, -1.15, 0]) * s) for x in (-1.0, -0.45, 0.55, 1.05)])
    tail = Line(c + np.array([-1.5, 0.2, 0]) * s, c + np.array([-1.85, -0.55, 0]) * s, color=GREY_B, stroke_width=2.5)
    g = VGroup(body, legs, head, ear, trunk, tusk, tail)
    g.parts = {"trunk": trunk, "tusk": tusk, "ear": ear, "leg": legs[0], "side": body, "tail": tail}
    return g


class Jaina(VoiceoverScene):
    def construct(self):
        card = chapter_card(5, r"Seven ways of saying", r"Why did the Jainas count exactly seven?", lit=(1292,),
                            part=PART)
        with self.voiceover("Chapter five. Seven ways of saying."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.elephant_()
        self.seven()
        self.count()
        self.jar()

    def elephant_(self):
        el = elephant(center=[-0.4, -0.3, 0], s=1.15)
        claims = [("trunk", r"`a snake'", [3.9, -1.6, 0]), ("tusk", r"`a spear'", [4.6, 0.3, 0]),
                  ("ear", r"`a fan'", [2.3, 2.5, 0]), ("leg", r"`a pillar'", [-2.4, -2.9, 0]),
                  ("side", r"`a wall'", [0.4, 2.6, 0]), ("tail", r"`a rope'", [-4.7, -1.2, 0])]
        labs, lines = VGroup(), VGroup()
        for part, txt, pos in claims:
            t = label(txt, font_size=26, color=GOAL).move_to(pos)
            labs.add(t)
            lines.add(DashedLine(t.get_center(), el.parts[part].get_center(), buff=0.35, color=GREY_C,
                                 dash_length=0.08))
        hc = history_card(r"6th--5th c.\ BCE", r"Mahāvīra and the Jainas", r"\textit{anekāntavāda}: \ reality is "
                          r"many-sided", width=6.2, color=HIST).to_corner(UL, buff=0.35)
        moral = label(r"each is right from where he stands, \ and wrong if he says it is the whole truth",
                      font_size=24, color=OK).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The Jaina tradition, going back to Mahāvīra, a contemporary of the Buddha, holds that reality is "
            "many-sided: anekāntavāda. <bookmark mark='a'/>Its emblem is the story of the blind men and the "
            "elephant. <bookmark mark='b'/>One feels the trunk and says it is a snake; one the tusk, a spear; one "
            "the ear, a fan; one a leg, a pillar; one the side, a wall; one the tail, a rope. "
            "<bookmark mark='c'/>Each is right from where he stands, and wrong only in claiming the whole truth."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Create(el), run_time=2)
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(Create(ln), FadeIn(t)) for ln, t in zip(lines, labs)],
                                  lag_ratio=0.35), run_time=4)
            vo.wait_until("c")
            self.play(FadeIn(moral))
        self.clear_scene()

    def seven(self):
        d = load("jaina")
        head = label(r"\textit{saptabhaṅgī}: \ every claim is qualified by \textit{syāt}, `in some respect'",
                     font_size=28, color=CONN).to_edge(UP, buff=0.4)
        rows = VGroup()
        for i, b in enumerate(d["bhangas"]):
            b = tuple(b)
            num = label(rf"{i + 1}.", font_size=24, color=GREY_B)
            skt = label(SKT[b], font_size=24, color=GREY_A)
            en = label(r"in some respect " + r", \ and ".join(EN[x] for x in b), font_size=24)
            dots = VGroup(*[Dot(radius=0.09, color=COL[x]) for x in b]).arrange(RIGHT, buff=0.08)
            rows.add(VGroup(num, dots, en, skt))
        for i, r in enumerate(rows):
            y = 2.3 - 0.66 * i
            r[0].move_to([-4.6 + r[0].width / 2, y, 0])
            r[1].move_to([-3.9 + r[1].width / 2, y, 0])
            r[2].move_to([-2.9 + r[2].width / 2, y + 0.13, 0])
            r[3].move_to([-2.9 + r[3].width / 2, y - 0.17, 0])
        src = label(r"Kundakunda; \ Samantabhadra; \ Mallisena's \textit{Syādvādamañjarī} (1292)", font_size=20,
                    color=GREY_B).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "From many-sidedness came a doctrine of predication, syādvāda, 'the doctrine of maybe'. Every claim is "
            "qualified by syāt: in some respect. <bookmark mark='a'/>In some respect it is. In some respect it is "
            "not. In some respect it is, and it is not. <bookmark mark='b'/>In some respect it is inexpressible. "
            "<bookmark mark='c'/>And three more that combine the inexpressible with the first three. "
            "<bookmark mark='d'/>The seven, the saptabhaṅgī, were worked out by Kundakunda and Samantabhadra in the "
            "first millennium, and given their classic statement in Mallisena's commentary of 1292."
        ) as vo:
            self.play(FadeIn(head))
            for mk, idx in (("a", [0, 1, 2]), ("b", [3]), ("c", [4, 5, 6])):
                vo.wait_until(mk)
                self.play(LaggedStart(*[FadeIn(rows[i], shift=RIGHT * 0.15) for i in idx], lag_ratio=0.3))
            vo.wait_until("d")
            self.play(FadeIn(src))
        self.clear_scene()

    def count(self):
        d = load("jaina")
        head = label(r"Why seven?", font_size=36, color=CONN).to_edge(UP, buff=0.5)
        base = VGroup(*[VGroup(Dot(radius=0.14, color=COL[x]), label(EN[x], font_size=24)).arrange(RIGHT, buff=0.2)
                        for x in "tfi"]).arrange(RIGHT, buff=0.8).next_to(head, DOWN, buff=0.5)
        bl = label(r"from each standpoint, a claim gets one of three values", font_size=24, color=GREY_A).next_to(
            base, DOWN, buff=0.25)
        subsets = VGroup()
        for b in d["bhangas"]:
            dots = VGroup(*[Dot(radius=0.13, color=COL[x]) for x in b]).arrange(RIGHT, buff=0.1)
            box = SurroundingRectangle(dots, buff=0.15, color=GREY_C, corner_radius=0.08)
            subsets.add(VGroup(box, dots))
        subsets.arrange(RIGHT, buff=0.35).next_to(bl, DOWN, buff=0.7)
        eq = MathTex(r"2^3 - 1 = 7", font_size=48, color=GOAL).next_to(subsets, DOWN, buff=0.5)
        expl = label(r"a predication is the \textit{set} of values a claim takes across standpoints: \ any nonempty "
                     r"subset of three", font_size=24).next_to(eq, DOWN, buff=0.3)
        who = label(r"Priest, `Jaina logic: a contemporary perspective' (2008); \ Ganeri (2002)", font_size=20,
                    color=GREY_B).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Why exactly seven? There is a precise answer. <bookmark mark='a'/>From any one standpoint, a claim "
            "takes one of three basic values: it is, it is not, or it is inexpressible. <bookmark mark='b'/>Across "
            "all the standpoints, what we can truly say is the set of values the claim takes. "
            "<bookmark mark='c'/>A set of values drawn from three, not empty: there are two to the third, minus "
            "one, and that is seven. The Reasoner lists them, and they come out in the traditional order. "
            "<bookmark mark='d'/>This reconstruction is Graham Priest's, building on Jonardon Ganeri. On it, the "
            "seven predications are not mystical. They are the complete list."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(base), FadeIn(bl))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s_, scale=0.8) for s_ in subsets], lag_ratio=0.2), run_time=2.5)
            vo.wait_until("c")
            self.play(Write(eq), FadeIn(expl))
            vo.wait_until("d")
            self.play(FadeIn(who))
        self.clear_scene()

    def jar(self):
        head = label(r"`The jar exists', \ from four standpoints", font_size=32, color=CONN).to_edge(UP, buff=0.5)
        st = [(r"as a jar \ (its own substance)", "t"), (r"as cloth \ (another substance)", "f"),
              (r"here, in this room", "t"), (r"as both at once: \ it is, and it is not", "i")]
        rows = VGroup()
        for txt, v in st:
            rows.add(VGroup(label(txt, font_size=26), Dot(radius=0.13, color=COL[v]),
                            label(EN[v], font_size=24, color=COL[v])))
        for i, r in enumerate(rows):
            y = 1.4 - 0.75 * i
            r[0].move_to([-5.8 + r[0].width / 2, y, 0])
            r[1].move_to([0.4, y, 0])
            r[2].move_to([0.8 + r[2].width / 2, y, 0])
        res = VGroup(label(r"the set of values:", font_size=26, color=GOAL),
                     VGroup(*[Dot(radius=0.13, color=COL[x]) for x in "tfi"]).arrange(RIGHT, buff=0.1),
                     label(r"predication 7: \ \textit{syād asti nāsti avaktavya}", font_size=26, color=GOAL)
                     ).arrange(RIGHT, buff=0.3).to_edge(DOWN, buff=0.9)
        moral = label(r"no contradiction: \ each value belongs to a different standpoint", font_size=24,
                      color=OK).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The Jaina's own example is a jar. <bookmark mark='a'/>Considered as a jar, in its own substance, it "
            "exists. Considered as cloth, it does not: a jar is not a piece of cloth. <bookmark mark='b'/>Here, in "
            "this room, it exists. And considered both ways at once, as existing and not existing together, it "
            "cannot be expressed in a single word. <bookmark mark='c'/>So the full predication is the seventh: "
            "in some respect it is, in some respect it is not, and in some respect it is inexpressible. "
            "<bookmark mark='d'/>There is no contradiction, because each value is relative to a standpoint. It is "
            "Part 4's idea of truth at a world, with standpoints in place of worlds."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]))
            vo.wait_until("c")
            self.play(FadeIn(res))
            vo.wait_until("d")
            self.play(FadeIn(moral))
        self.clear_scene()
