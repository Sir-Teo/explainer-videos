from __future__ import annotations

from videos.philosophy.philosophy40.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.title()
        self.teaser()
        self.questions()
        self.objectives()

    def title(self):
        t = part_title(PART)
        q = quote_card(r"Beauty is no quality in things themselves: \ it exists merely in the mind which contemplates "
                       r"them.", r"David Hume", r"``Of the Standard of Taste'' \ (1757)", width=8.8,
                       font_size=30).next_to(t, DOWN, buff=0.5)
        with self.voiceover(
            "Parts 35 to 39 asked about the right, the good and the just. This part asks about the beautiful, and "
            "whether judgments of beauty can be right or wrong. <bookmark mark='a'/>David Hume wrote, in 1757, that "
            "beauty is no quality in things themselves: it exists merely in the mind which contemplates them. "
            "<bookmark mark='b'/>He then spent the rest of the essay arguing that some judgments of beauty are "
            "nevertheless better than others. This part asks how both can be true, and tests every theory that says "
            "beauty is something you can measure."
        ) as vo:
            self.play(FadeIn(t, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(Indicate(q, color=TASTE, scale_factor=1.03))
        self.clear_scene()

    def questions(self):
        head = label(r"Four questions about beauty", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"measure", r"is beauty mathematical order: \ ratio, \ symmetry, \ compression?", FORM),
                (r"taste", r"if beauty is felt, \ can anyone be wrong about it?", TASTE),
                (r"art", r"what makes something a work of art, \ and does it matter who made it?", ART),
                (r"elsewhere", r"how do proofs, \ skills and other traditions see beauty?", EAST)]
        g = rows_table(rows, top=1.5, gap=0.55, width=8.4, x_text=-2.4)
        with self.voiceover(
            "Four questions run through the part. <bookmark mark='a'/>Measure: is beauty mathematical order, in "
            "ratios, symmetries or compressibility? <bookmark mark='b'/>Taste: if beauty is felt, can anyone be wrong "
            "about it? <bookmark mark='c'/>Art: what makes something a work of art, and does it matter who, or what, "
            "made it? <bookmark mark='d'/>And elsewhere: how do mathematicians, craftsmen and the Chinese tradition "
            "see beauty? The answer to the second question, Hume's paradox of taste, is this part's brick in the "
            "Wall."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Plato's ladder and his critique of art; \ Aristotle's \textit{Poetics}; \ Burke's sublime",
            r"Pythagorean ratios; \ the comma $3^{12}/2^{19}$; \ equal temperament, \ measured",
            r"the dissonance curve, \ built: \ consonances as dips; \ stretched timbres",
            r"all 17 wallpaper groups, \ generated and classified",
            r"Birkhoff's measure; \ compression and Schmidhuber's interest, \ as a toy",
            r"the golden ratio, \ and a test of finding it everywhere",
            r"Hume's true judges, \ simulated \ (the Wall); \ Kant's four moments; \ the sublime",
            r"Danto's Brillo boxes; \ forgery; \ AI art and the law; \ Hardy; \ Xie He; \ Cook Ding",
        ], font_size=22)
        with self.voiceover(
            "The plan. <bookmark mark='a'/>Plato's ladder of love and his critique of art, Aristotle's Poetics, and "
            "the sublime. <bookmark mark='b'/>The Pythagorean ratios, the comma that stops the circle of fifths from "
            "closing, and equal temperament, measured. <bookmark mark='c'/>The dissonance curve, built, with the "
            "consonances appearing as its dips. <bookmark mark='d'/>All seventeen wallpaper groups, generated and "
            "classified by the Reasoner. <bookmark mark='e'/>Birkhoff's measure of beauty, and compression as a "
            "measure of interest. <bookmark mark='f'/>The golden ratio, and a test of what finding it is worth. "
            "<bookmark mark='g'/>Hume's true judges, simulated, Kant's four moments and the sublime. <bookmark "
            "mark='h'/>And Danto's Brillo boxes, forgery, AI art before the courts, mathematical beauty, Xie He's "
            "principles of painting and Zhuangzi's Cook Ding."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefgh", range(8)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()

    def teaser(self):
        c = load("curve")
        w = load("wallpaper")
        assert w["distinct"] == 17 and len(c["minima"]) == 6
        head = label(r"Beauty, \ computed?", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[1.0, 2.3, 0.1], y_range=[0, 1.05, 0.25], x_length=6.0, y_length=2.8,
                  axis_config={"color": GREY_B, "include_tip": False}, tips=False).move_to([-3.3, 0.4, 0])
        curve = VMobject(color=HARM, stroke_width=3).set_points_as_corners([ax.c2p(x, y) for x, y in zip(c["r"], c["d"])])
        t1 = label(r"consonance as a dip in roughness", font_size=19, color=HARM).next_to(ax, DOWN, buff=0.2)
        p = load("patterns")["p6m"]
        tiles = VGroup()
        for poly, fl in zip(p["polys"], p["flip"]):
            cc = np.mean(poly, axis=0)
            if -0.2 <= cc[0] <= 1.8 and -0.2 <= cc[1] <= 1.8:
                tiles.add(Polygon(*[np.array([(x - 0.8) * 1.4 + 3.3, (y - 0.8) * 1.4 + 0.4, 0]) for x, y in poly],
                                  stroke_width=0.6, stroke_color=WHITE, fill_color=ART if fl else SYM, fill_opacity=0.7))
        t2 = label(r"symmetry as a group", font_size=19, color=SYM).move_to([3.3, -1.6, 0])
        q = label(r"and yet: \ is a Brillo box beautiful? \ who decides?", font_size=23, color=TASTE).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Two promises of this part, in preview. <bookmark mark='a'/>The consonant intervals of music will appear "
            "as the dips of a curve computed from the physics of hearing. <bookmark mark='b'/>And the possible "
            "symmetries of a patterned wall will be generated, all seventeen of them, and named by machine. <bookmark "
            "mark='c'/>And yet, by the end, the hardest questions will be ones no computation settles: why a copy of "
            "a soap-pad carton can be a work of art, and who decides what is beautiful."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(ax), Create(curve), FadeIn(t1), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(tiles), FadeIn(t2))
            vo.wait_until("c")
            self.play(FadeIn(q))
        self.clear_scene()
