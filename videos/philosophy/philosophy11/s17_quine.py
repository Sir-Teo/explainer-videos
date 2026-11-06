from __future__ import annotations

from videos.philosophy.philosophy11.common import *  # noqa: F403


class Quine(VoiceoverScene):
    def construct(self):
        card = chapter_card(16, r"Two dogmas", r"Is any belief immune to revision?", lit=(1951,), part=PART)
        with self.voiceover("Chapter sixteen. Two dogmas."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.circle()
        self.web()
        self.revisions()

    def circle(self):
        hc = history_card(1951, r"W.\ V.\ O.\ Quine", r"`Two Dogmas of Empiricism', \ \textit{Philosophical "
                          r"Review}", width=6.2, color=HIST).to_corner(UL, buff=0.35)
        dogmas = VGroup(label(r"dogma 1: \ a sharp line between analytic and synthetic truths", font_size=23),
                        label(r"dogma 2: \ each statement has its own experiences that would confirm it",
                              font_size=23)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([0.6, 1.45, 0])
        names = [r"analytic", r"synonymous", r"interchangeable, \ truth kept", r"`necessarily'"]
        c = np.array([-1.9, -1.4, 0])
        R = 1.6
        pos = [c + R * np.array([np.cos(a), np.sin(a), 0]) for a in (PI / 2, 0, -PI / 2, PI)]
        nodes = VGroup(*[label(n, font_size=23, color=GOAL).move_to(p) for n, p in zip(names, pos)])
        arcs = VGroup()
        for i in range(4):
            a0 = PI / 2 - i * PI / 2 - 0.35
            arc = Arc(radius=R, start_angle=a0, angle=-PI / 2 + 0.7, arc_center=c, color=GREY_B, stroke_width=3)
            arc.add_tip(tip_length=0.18)
            arcs.add(arc)
        gl = VGroup(label(r"analytic: \ true by synonymy, \ like `bachelors are unmarried'", font_size=19,
                          color=GREY_A),
                    label(r"synonymy: \ interchangeable without changing truth", font_size=19, color=GREY_A),
                    label(r"but only in a language with `necessarily',", font_size=19, color=GREY_A),
                    label(r"which must be explained by analyticity", font_size=19, color=GREY_A))
        for m in gl:
            if m.width > 4.6:
                m.width = 4.6
        gl.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([4.3, -1.4, 0])
        with self.voiceover(
            "In 1951 W. V. O. Quine published the most influential paper of postwar philosophy. "
            "<bookmark mark='a'/>He attacked two dogmas of empiricism. The first: that there is a sharp line between "
            "analytic truths, true by meaning alone, and synthetic truths, true by the facts. The second: that each "
            "statement, taken by itself, has its own range of experiences that would confirm or refute it. "
            "<bookmark mark='b'/>Against the first, Quine tried every way of explaining analyticity, and found a "
            "circle. A statement is analytic if it comes from a logical truth by putting synonyms for synonyms. "
            "<bookmark mark='c'/>Two expressions are synonymous if they are interchangeable in every sentence without "
            "changing its truth. <bookmark mark='d'/>But that works only in a language that contains an adverb like "
            "necessarily, <bookmark mark='e'/>and necessarily, in the sense required, is explained by analyticity. "
            "We are back where we started."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(dogmas))
            vo.wait_until("b")
            self.play(FadeIn(nodes[0]), FadeIn(gl[0]))
            vo.wait_until("c")
            self.play(Create(arcs[0]), FadeIn(nodes[1]), FadeIn(gl[1]))
            vo.wait_until("d")
            self.play(Create(arcs[1]), FadeIn(nodes[2]), FadeIn(gl[2]))
            self.play(Create(arcs[2]), FadeIn(nodes[3]))
            vo.wait_until("e")
            self.play(Create(arcs[3]), FadeIn(gl[3]))
        self.clear_scene()

    def web(self):
        head = label(r"The web of belief", font_size=32, color=CONN).to_edge(UP, buff=0.3)
        c = np.array([-2.8, -0.5, 0])
        rings = VGroup(*[Circle(radius=r, stroke_color=col, stroke_width=2.5).move_to(c) for r, col in
                         ((2.8, SKEP), (2.1, BEL), (1.35, JUST), (0.6, KNOW))])
        names = VGroup(label(r"experience", font_size=19, color=SKEP).move_to(c + UP * 2.45),
                       label(r"observation reports", font_size=19, color=BEL).move_to(c + UP * 1.75),
                       label(r"physics", font_size=19, color=JUST).move_to(c + UP * 1.0),
                       label(r"logic, \ maths", font_size=19, color=KNOW).move_to(c))
        kick = Arrow(c + np.array([3.6, 2.2, 0]), c + np.array([2.0, 1.95, 0]), color=BAD, buff=0, stroke_width=4)
        kl = label(r"a recalcitrant experience", font_size=20, color=BAD).next_to(kick.get_start(), RIGHT, buff=0.1)
        q = quote_card(r"The totality of our so-called knowledge or beliefs \dots\ is a man-made fabric which "
                       r"impinges on experience only along the edges.", r"Quine", r"`Two Dogmas', \ \S 6",
                       width=6.0, font_size=21).move_to([3.4, 0.4, 0])
        rows = VGroup(label(r"`no statement is immune to revision'", font_size=24, color=GOAL),
                      label(r"not even logic: \ quantum logic drops distributivity \ (Putnam 1968)", font_size=21,
                            color=GREY_A)).arrange(DOWN, buff=0.15).move_to([3.4, -2.3, 0])
        with self.voiceover(
            "Against the second dogma, Quine offered a picture. <bookmark mark='a'/>Our beliefs form a single web. At "
            "its edge, experience; then observation reports; then the sciences; and at the centre, mathematics and "
            "logic. <bookmark mark='b'/>The totality of our so-called knowledge, he wrote, is a man-made fabric "
            "which impinges on experience only along the edges. <bookmark mark='c'/>When an experience conflicts "
            "with the web, the conflict does not single out one belief to blame. We have a choice about where to "
            "revise, and we choose to disturb the system as little as possible, which is why logic and mathematics, "
            "at the centre, are hardly ever touched. <bookmark mark='d'/>But hardly ever is not never. No statement "
            "is immune to revision. Quine noted that revising even the law of excluded middle had been proposed, to "
            "simplify quantum mechanics; and in 1968 Hilary Putnam argued that quantum mechanics is a reason to give "
            "up the distributive law of logic."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=0.3), FadeIn(names), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(q))
            vo.wait_until("c")
            self.play(GrowArrow(kick), FadeIn(kl))
            self.play(Indicate(rings[0], color=BAD), Indicate(rings[1], color=BAD))
            vo.wait_until("d")
            self.play(FadeIn(rows))
        self.clear_scene()

    def revisions(self):
        d = load("web")
        head = label(r"Duhem and Quine: \ which belief goes?", font_size=32, color=CONN).to_edge(UP, buff=0.3)
        keys = list(d["beliefs"])
        sym = {"N": r"$N$", "K": r"$K$", "T": r"$T$", "L": r"$N \land K \land T \rightarrow O$", "notO": r"$\lnot O$"}
        text = {"N": r"Newton's laws of motion and gravitation", "K": r"the known planets are all the planets",
                "T": r"the telescopes and the tables are right",
                "L": r"the mathematics of the prediction", "notO": r"the orbit observed is not the orbit predicted"}
        cards = VGroup()
        for k in keys:
            box = RoundedRectangle(width=6.4, height=0.62, corner_radius=0.1, stroke_color=P.CLAIM, stroke_width=2)
            t = VGroup(label(sym[k], font_size=22, color=GOAL), label(text[k], font_size=20, color=WHITE)).arrange(
                RIGHT, buff=0.3)
            if t.width > 6.1:
                t.width = 6.1
            cards.add(VGroup(box, t.move_to(box)))
        cards.arrange(DOWN, buff=0.14).move_to([-3.1, -0.1, 0])
        incon = label(r"the five together: \ unsatisfiable", font_size=21, color=BAD).next_to(cards, DOWN, buff=0.2)
        assert d["revisions"] == [[k] for k in keys]
        hist = {"N": r"Mercury, \ 1859--1915: \ drop Newton \ (general relativity)",
                "K": r"Uranus, \ 1846: \ drop $K$ \ (Le Verrier finds Neptune)",
                "T": r"blame the instruments \ (the usual first suspect)",
                "L": r"revise the logic \ (Quine's extreme case)",
                "notO": r"reject the observation \ (a bad night, \ a bad plate)"}
        notes = VGroup(*[label(hist[k], font_size=20, color=GREY_A) for k in keys])
        for n, cd in zip(notes, cards):
            n.move_to([0.6 + n.width / 2, cd.get_y(), 0])
        for n in notes:
            if n.get_right()[0] > 6.9:
                n.width = 6.9 - 0.6
                n.move_to([0.6 + n.width / 2, n.get_y(), 0])
        rlab = label(r"the Reasoner: \ every minimal revision \ =\ drop any one", font_size=22, color=OK).move_to(
            [3.5, cards.get_top()[1] + 0.35, 0])
        vul = label(r"and Vulcan, \ the planet proposed inside Mercury's orbit, \ was never found", font_size=21,
                    color=LUCK).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The Reasoner can make Quine's point exact, with a story from astronomy. <bookmark mark='a'/>Five "
            "beliefs: Newton's laws; that the known planets are all the planets; that the telescopes and tables are "
            "right; the mathematics that derives the predicted orbit from those three; and the observation that the "
            "orbit is not as predicted. <bookmark mark='b'/>Together they are inconsistent. The Reasoner searches "
            "for every minimal revision, every smallest set of beliefs whose removal restores consistency, and finds "
            "exactly five: drop any one. Logic alone does not say which. <bookmark mark='c'/>History chose "
            "differently each time. When Uranus strayed, in the 1840s, Urbain Le Verrier dropped the belief that the "
            "known planets were all of them, computed where another must be, and in 1846 Neptune was found there. "
            "<bookmark mark='d'/>When Mercury strayed, Le Verrier tried the same move and proposed a planet, Vulcan, "
            "inside Mercury's orbit. <bookmark mark='e'/>It was never found. In 1915 the belief that went was Newton's "
            "law itself, replaced by general relativity. Same logical structure, different revisions: that is the "
            "Duhem-Quine thesis. <bookmark mark='f'/>And the other revisions are always there to be chosen: blame the "
            "instruments, reject the observation, or, in Quine's extreme case, revise the logic."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(cd) for cd in cards], lag_ratio=0.3), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(incon))
            self.play(FadeIn(rlab))
            for i in range(5):
                self.play(Indicate(cards[i], color=OK, scale_factor=1.04), run_time=0.7)
            vo.wait_until("c")
            self.play(FadeIn(notes[1]), Indicate(cards[1], color=OK))
            vo.wait_until("d")
            self.play(FadeIn(vul))
            vo.wait_until("e")
            self.play(FadeIn(notes[0]), Indicate(cards[0], color=OK))
            vo.wait_until("f")
            self.play(FadeIn(notes[2]), FadeIn(notes[4]), FadeIn(notes[3]))
        self.clear_scene()
