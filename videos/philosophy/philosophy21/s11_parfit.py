from __future__ import annotations

from videos.philosophy.philosophy21.common import *  # noqa: F403


class Parfit(VoiceoverScene):
    def construct(self):
        card = chapter_card(10, r"Continuity, connectedness, teleportation", r"What matters in survival?",
                            lit=(1971, 1984), part=PART)
        with self.voiceover("Chapter ten. Continuity, connectedness, teleportation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.relations()
        self.teleport()
        self.spectrum()
        self.matters()
        self.xphi()

    def relations(self):
        d = load("memory")
        head = label(r"Connectedness fades; \ continuity holds", font_size=30, color=CONN).to_edge(UP, buff=0.25)
        yrs = d["years"]
        ref = d["ref_age"]
        ax = Axes(x_range=[ref, yrs, 10], y_range=[0, 1, 0.25], x_length=7.0, y_length=3.4,
                  axis_config={"color": GREY_B, "font_size": 18}, x_axis_config={"include_numbers": True},
                  y_axis_config={"include_numbers": True}).move_to([-2.2, -0.4, 0])
        conn = [c for c in d["connectedness"][ref:]]
        curve = series_plot(ax, conn, NOM, xs=list(range(ref, yrs)), width=3.5)
        half = DashedLine(ax.c2p(ref, 0.5), ax.c2p(yrs, 0.5), color=GOAL, stroke_width=2)
        hl = label(r"half", font_size=18, color=GOAL).next_to(half, RIGHT, buff=0.05)
        mark = Dot(ax.c2p(d["half_at"], conn[d["half_at"] - ref]), radius=0.08, color=GOAL)
        cont = Line(ax.c2p(ref, 0.96), ax.c2p(yrs, 0.96), color=UNIV, stroke_width=4)
        cl = label(r"continuity: \ year-to-year overlap never below " + f"{100 * d['year_to_year_min']:.0f}" + r"\%",
                   font_size=18, color=UNIV).next_to(cont, UP, buff=0.05)
        al = VGroup(label(r"share of the " + f"{ref}" + r"-year-old's memories still held", font_size=18,
                          color=NOM).next_to(ax, DOWN, buff=0.35),
                    label(r"age", font_size=18, color=GREY_A).next_to(ax.x_axis, RIGHT, buff=0.12))
        rows = stack([(r"connectedness: \ direct links \ (memories, \ intentions, \ character) \ between two times",
                       NOM),
                      (r"continuity: \ an overlapping chain of strong connectedness", UNIV),
                      (r"here, \ half the links to age " + f"{ref}" + r" are gone by " + f"{d['half_at']}", GOAL),
                      (r"connectedness comes in degrees; \ identity does not", BAD)], font_size=19,
                     aligned_edge=LEFT, width=4.6).move_to([4.6, -0.2, 0])
        with self.voiceover(
            "Parfit separated two relations. <bookmark mark='a'/>Psychological connectedness: direct links between two "
            "times, such as a memory of an experience, an intention later carried out, a persisting trait of "
            "character. <bookmark mark='b'/>Psychological continuity: an overlapping chain of strong connectedness. "
            "<bookmark mark='c'/>The Reasoner simulates a toy life. Each year lays down memories, and each memory "
            "fades with a small chance per year. The share of the ten-year-old's memories still held falls by degrees: "
            "half are gone by twenty-four, nearly all by eighty. Yet from year to year the overlap never drops below "
            "ninety-four percent: the chain of continuity is unbroken. <bookmark mark='d'/>Connectedness comes in "
            "degrees. Identity does not. That mismatch is Parfit's lever."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(al))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(curve), Create(half), FadeIn(hl), run_time=3)
            self.play(FadeIn(mark), FadeIn(rows[2]), Create(cont), FadeIn(cl))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def teleport(self):
        hc = history_card(1984, r"Derek Parfit", r"\textit{Reasons and Persons}, \ Part III", width=6.0,
                          color=HIST).to_corner(UL, buff=0.3)
        earth = Circle(radius=0.6, color=UNIV, fill_opacity=0.3).move_to([-5.0, -0.8, 0])
        mars = Circle(radius=0.45, color=BAD, fill_opacity=0.3).move_to([-1.4, -0.8, 0])
        el = label(r"Earth", font_size=16, color=UNIV).next_to(earth, DOWN, buff=0.15)
        ml = label(r"Mars", font_size=16, color=BAD).next_to(mars, DOWN, buff=0.15)
        beam = DashedLine(earth.get_right(), mars.get_left(), buff=0.1, color=GOAL).add_tip(tip_length=0.2)
        bl = label(r"a complete record", font_size=15, color=GOAL).next_to(beam, UP, buff=0.08)
        rows = stack([(r"the scanner records every cell, \ and destroys the original", WHITE),
                      (r"a replica is built on Mars: \ same memories, \ intentions, \ character", NOM),
                      (r"psychological continuity: \ yes; \ physical continuity: \ none", UNIV),
                      (r"the branch-line case: \ the original survives, \ with a failing heart", BAD),
                      (r"Parfit: \ ordinary survival is about as good as teletransportation", GOAL)],
                     font_size=20, aligned_edge=LEFT, width=6.6).move_to([3.3, -0.4, 0])
        with self.voiceover(
            "Parfit's most famous case. <bookmark mark='a'/>You enter the teletransporter on Earth. It records the "
            "exact state of every cell of your body, and destroys it. <bookmark mark='b'/>The record is sent to Mars, "
            "where a replica is built: with your memories, your intentions and your character, believing it has just "
            "stepped out of the booth. <bookmark mark='c'/>There is full psychological continuity, and no physical "
            "continuity at all. Have you travelled, or died? <bookmark mark='d'/>Change the case: the new scanner does "
            "not destroy you, but damages your heart, and you will die in days, while your replica lives on Mars. Now "
            "it seems you are the one on Earth. <bookmark mark='e'/>Parfit's verdict was that ordinary survival is "
            "about as good as teletransportation: what matters is psychological continuity, by whatever cause."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(earth), FadeIn(mars), FadeIn(el), FadeIn(ml))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(beam), FadeIn(bl), FadeIn(rows[1]))
            for mk, r in zip("cde", rows[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def spectrum(self):
        head = label(r"The combined spectrum", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        bar = VGroup(*[Rectangle(width=0.55, height=0.6, stroke_width=0.5, stroke_color=GREY_D,
                                 fill_color=interpolate_color(ManimColor(NOM), ManimColor(PARTC), i / 19),
                                 fill_opacity=0.85).move_to([-5.2 + 0.55 * i, 0.8, 0]) for i in range(20)])
        l0 = label(r"you", font_size=17, color=NOM).next_to(bar, LEFT, buff=0.2)
        l1 = label(r"Greta Garbo", font_size=17, color=PARTC).next_to(bar, RIGHT, buff=0.2)
        sl = label(r"0\% \ \ \ cells and psychology replaced \ \ \ 100\%", font_size=15, color=GREY_A).next_to(
            bar, DOWN, buff=0.15)
        rows = stack([(r"at each step, \ a few more of your cells and traits are replaced by someone else's", WHITE),
                      (r"near one end, \ clearly you; \ near the other, \ clearly not", GREY_A),
                      (r"where is the line? \ any sharp line is arbitrary; \ a vague line means vague identity", BAD),
                      (r"Parfit: \ `is it me?' \ can be an empty question, \ with every fact known", GOAL),
                      (r"reductionism: \ a person's existence just consists in brains, \ bodies and events", UNIV)],
                     font_size=20, aligned_edge=LEFT, width=11.6).move_to([0, -1.6, 0])
        with self.voiceover(
            "Parfit's combined spectrum makes the point by degrees. <bookmark mark='a'/>Imagine a range of "
            "operations. At one end, nothing is changed. At each step, a few more of your cells, and a few more of "
            "your memories and traits, are replaced by those of someone else, say Greta Garbo. "
            "<bookmark mark='b'/>Near one end the result is clearly you; near the other, clearly not. "
            "<bookmark mark='c'/>Where is the line? Any sharp line is arbitrary, and a vague one seems to make identity "
            "vague, which Evans forbade. <bookmark mark='d'/>Parfit concluded that is it still me can be an empty "
            "question, even when we know every fact. <bookmark mark='e'/>His reductionism: a person's existence just "
            "consists in the existence of a brain and body and a series of interrelated events."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in bar], lag_ratio=0.05), FadeIn(l0), FadeIn(l1), FadeIn(sl),
                      FadeIn(rows[0]))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def matters(self):
        head = label(r"What matters", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Parfit", r"what matters is Relation R: \ psychological connectedness and/or continuity, \ with any "
                        r"cause", GOAL),
            (r"the liberation", r"`the wall of glass' around my life disappeared; \ I care less about my death", UNIV),
            (r"the extreme claim", r"if there is no further fact, \ why should I care specially about my own future at "
                                   r"all?", BAD),
            (r"Johnston \ (1992)", r"our concern does not need a metaphysical foundation: \ reductionism changes "
                                   r"nothing", NOM),
            (r"ethics", r"compensation across a life, \ desert, \ and the future generations of Part 36", ABS),
        ]
        g = rows_table(rows, top=1.6, gap=0.5, width=8.8, x_text=-2.4, label_size=21)
        with self.voiceover(
            "Parfit's conclusion was not only metaphysical. <bookmark mark='a'/>What matters, he argued, is not "
            "identity but Relation R: psychological connectedness and continuity, with any cause. "
            "<bookmark mark='b'/>He found the view liberating. My life had seemed a glass tunnel, he wrote; when I "
            "changed my view, the walls disappeared, and I cared less about my own death. <bookmark mark='c'/>Critics "
            "pressed an extreme claim: if there is no further fact about identity, why should I care specially about "
            "my own future at all? <bookmark mark='d'/>Mark Johnston replied that our concern never rested on a "
            "metaphysical foundation, so reductionism leaves it in place. <bookmark mark='e'/>The ethical stakes are "
            "real: whether we may trade a burden now for a benefit later in a life, and how we weigh future people, "
            "the subject of Part 36."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def xphi(self):
        head = label(r"What do people actually think?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Nichols and Bruno \ (2010)", r"most participants judge that you survive if your psychology does, \ "
                                           r"but answers shift with framing, \ as Williams predicted", UNIV),
            (r"Strohminger and Nichols \ (2014)", r"`the essential moral self': \ moral traits matter more for "
                                                  r"identity than memories", GOAL),
            (r"Tobia \ (2015)", r"a change for the better seems less to destroy the person than a change for the "
                                r"worse", WHOLE),
            (r"dementia", r"families report that a loved one `is not the same person': \ the moral self, \ again",
             NOM),
            (r"the lesson", r"folk judgments of identity are partly evaluative, \ as Locke's forensic person suggested",
             ABS),
        ]
        g = rows_table(rows, top=1.6, gap=0.5, width=8.6, x_text=-1.8, label_size=19)
        with self.voiceover(
            "Experimental philosophers have asked people. <bookmark mark='a'/>Shaun Nichols and Michael Bruno found "
            "that most judge you survive if your psychology does, though the answers shift with framing, as "
            "Williams predicted. <bookmark mark='b'/>Nina Strohminger and Nichols found something more surprising: "
            "moral traits matter more for identity than memories. Change someone's moral character, and people say "
            "they are a different person. <bookmark mark='c'/>Kevin Tobia found that a change for the better seems "
            "less destructive of identity than a change for the worse. <bookmark mark='d'/>Families of people with "
            "dementia say the same, when moral character changes. <bookmark mark='e'/>Ordinary judgments of identity "
            "are partly evaluative, just as Locke's forensic person suggested."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
