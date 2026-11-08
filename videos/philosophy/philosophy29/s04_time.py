from __future__ import annotations

from videos.philosophy.philosophy29.common import *  # noqa: F403

NOTES = ["C", "D", "E", "F", "G"]
NOTE_COL = [ACT, WORLD, SIGN, OBJ, BODY]


class Time(VoiceoverScene):
    def construct(self):
        card = chapter_card(3, r"The living present", r"How can we hear a melody?", lit=(1890, 1905), part=PART)
        with self.voiceover("Chapter three. The living present."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.puzzle()
        self.diagram()
        self.computed()
        self.models()

    def puzzle(self):
        head = label(r"A melody, \ one note at a time", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        staff = VGroup(*[Line([-5.5, 1.6 - 0.3 * i, 0], [5.5, 1.6 - 0.3 * i, 0], color=GREY_D, stroke_width=1.5)
                         for i in range(5)])
        dots = VGroup(*[Dot([-4.2 + 2.0 * k, 0.4 + 0.3 * k, 0], radius=0.16, color=NOTE_COL[k]) for k in range(5)])
        names = VGroup(*[label(n, font_size=20, color=c).next_to(d, DOWN, buff=0.15) for n, c, d in
                         zip(NOTES, NOTE_COL, dots)])
        knife = Rectangle(width=0.5, height=2.4, color=BAD, stroke_width=3).move_to([dots[3].get_x(), 0.9, 0])
        rows = stack([(r"a knife-edge present holds one note: \ a rising D-E-F and a falling A-G-F end alike, \ but "
                       r"sound different", BAD),
                      (r"James \ (1890): \ `the practically cognized present is no knife-edge, \ but a saddle-back'",
                       HIST),
                      (r"yet hearing the melody is not remembering it: \ the past notes are still \textit{heard}", TIME)],
                     font_size=20, aligned_edge=LEFT, width=12.0, buff=0.22).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Listen to a melody: C, D, E, F, G. <bookmark mark='a'/>At each instant only one note is sounding. If "
            "consciousness were a series of instants, each holding only what is present at it, we would hear a "
            "sequence of separate notes, never a melody. <bookmark mark='b'/>Take the instant when F sounds. Up to "
            "then the melody might have been D, E, F, rising, or A, G, F, falling; on a knife-edge present they "
            "end the same, but they sound different. <bookmark mark='c'/>William James, in 1890, "
            "borrowed a name for the alternative: the specious present. The practically cognized present, he wrote, "
            "is no knife-edge, but a saddle-back, with a certain breadth of its own. <bookmark mark='d'/>But what is "
            "that breadth? It is not memory: when I hear the melody I am not remembering D and E, as I might "
            "remember yesterday's concert. They are still heard, as just past."
        ) as vo:
            self.play(FadeIn(head), Create(staff))
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.3), FadeIn(names))
            vo.wait_until("a")
            self.play(Create(knife), *[d.animate.set_opacity(0.15) for i, d in enumerate(dots) if i != 3])
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]), *[d.animate.set_opacity(1) for d in dots], FadeOut(knife))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def diagram(self):
        d = load("diagram")
        head = label(r"Husserl's diagram \ (1905)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        ox, oy, sx = -4.8, 1.8, 2.0

        def P(p):
            return np.array([ox + sx * p[0], oy + sx * p[1], 0])

        now_line = Arrow(P([-0.1, 0]), P([4.7, 0]), buff=0, color=GREY_B, stroke_width=3)
        nows = VGroup(*[Dot(P(p), radius=0.09, color=NOTE_COL[i]) for i, p in enumerate(d["nows"])])
        nl = VGroup(*[label(n, font_size=20, color=c).next_to(nows[i], UP, buff=0.12) for i, (n, c) in
                      enumerate(zip(NOTES, NOTE_COL))])
        diags = VGroup()
        for k in range(5):
            pts = d["diagonals"][str(k)]
            if len(pts) > 1:
                diags.add(Line(P(pts[0]), P(pts[-1]), color=NOTE_COL[k], stroke_width=2.5))
        sect = d["section"]
        vert = Line(P([4, 0.15]), P([4, -0.55 * 4 - 0.2]), color=TIME, stroke_width=4)
        sdots = VGroup(*[Dot(P(p), radius=0.08, color=NOTE_COL[k]).set_opacity(1 - 0.18 * (4 - k))
                         for k, p in enumerate(sect)])
        prot = DashedLine(P([4, 0]), P([4.6, 0.45]), color=GOAL, stroke_width=3)
        tags = VGroup(label(r"now-points", font_size=18, color=GREY_A).next_to(P([2, 0]), UP, buff=0.55),
                      label(r"sinking into retention", font_size=18, color=GREY_A).move_to(P([1.6, -1.25])),
                      label(r"the living present", font_size=18, color=TIME).next_to(vert, RIGHT, buff=0.15).shift(
                          DOWN * 0.6),
                      label(r"protention", font_size=18, color=GOAL).next_to(prot.get_end(), RIGHT, buff=0.1))
        rows = stack([(r"primal impression: \ the note now sounding", ACT),
                      (r"retention: \ the just-past, \ still held, \ ever fainter", TIME),
                      (r"protention: \ the about-to-come, \ anticipated", GOAL)], font_size=20, aligned_edge=LEFT,
                     width=5.4, buff=0.22).move_to([-3.1, -2.5, 0])
        assert d["slope"] == 0.55 and len(d["nows"]) == 5
        with self.voiceover(
            "In lectures given in 1905, and published in 1928, Husserl drew a diagram of it. "
            "<bookmark mark='a'/>The horizontal line is the series of now-points: C, then D, E, F and G. "
            "<bookmark mark='b'/>From each now-point a diagonal runs down: the same note, sinking into the past as "
            "new nows arrive. <bookmark mark='c'/>Now stand at G and look down the vertical. It cuts every diagonal: "
            "G as it sounds, F just past, E further, D and C further still, each fainter. That vertical is the "
            "living present. <bookmark mark='d'/>Husserl named its parts. The primal impression is the note now "
            "sounding. Retention holds the just-past, not as an image or a memory, but as the tail of the present "
            "itself. <bookmark mark='e'/>And protention reaches forward: the note we expect next, which is why a "
            "wrong note is heard as wrong."
        ) as vo:
            self.play(FadeIn(head), GrowArrow(now_line))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in nows], lag_ratio=0.3), FadeIn(nl), FadeIn(tags[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(x) for x in diags], lag_ratio=0.3), FadeIn(tags[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(vert), LaggedStart(*[FadeIn(x) for x in sdots], lag_ratio=0.2), FadeIn(tags[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("e")
            self.play(Create(prot), FadeIn(tags[3]), FadeIn(rows[2]))
        self.clear_scene()

    def computed(self):
        d = load("retention")
        head = label(r"Three presents, \ on every five-note melody", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["melodies"] == 120 and d["distinct"] == {"knife": 5, "window": 20, "retention": 120}
        assert d["decoded"] == 120 and d["decay"] == 0.5
        eq = MathTex(r"\text{present}(t) \;=\; \sum_{k \le t} \lambda^{\,t-k}\, e_{\text{note}(k)}", r",\quad",
                     r"\lambda = \tfrac12", font_size=32, color=TIME).move_to([0, 1.9, 0])
        hd = [r"\text{the present holds}", r"\text{melodies told apart, of 120}"]
        cells = [[label(r"only the note now sounding", font_size=19, color=BAD), MathTex("5", font_size=24, color=BAD)],
                 [label(r"the last two notes", font_size=19, color=OBJ), MathTex("20", font_size=24, color=OBJ)],
                 [label(r"every past note, \ fading by half each step", font_size=19, color=OK),
                  MathTex("120", font_size=24, color=OK)]]
        grid = ValueGrid(hd, cells, col_w=[5.0, 3.6], cell_h=0.55, font_size=20).move_to([0, 0.2, 0])
        foot = stack([(r"and from the fading weights alone the Reasoner reads back the order of all 120", OK),
                      (r"an analogy: \ the recurrent state of a network \ (\textit{AI, Built}) \ is such a present",
                       HIST)], font_size=20, aligned_edge=LEFT, width=12.0, buff=0.22).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "The Reasoner tests the idea on every ordering of five notes: a hundred and twenty melodies. At the "
            "last note, what can each kind of present tell apart? <bookmark mark='a'/>A knife-edge present, holding "
            "only the note now sounding, sorts them into just five groups, by their last note. "
            "<bookmark mark='b'/>A present that holds the last two notes tells apart twenty. "
            "<bookmark mark='c'/>A retentional present holds every past note, fainter by half with each step it "
            "sinks. It tells apart all one hundred and twenty. <bookmark mark='d'/>And from the fading weights "
            "alone the whole order can be read back: the faintest note came first. "
            "<bookmark mark='e'/>This is a model, not Husserl's analysis, but the shape is the same: a present with "
            "a tail. The recurrent networks of the AI series carry exactly such a state."
        ) as vo:
            self.play(FadeIn(head), Write(eq))
            vo.wait_until("a")
            self.play(FadeIn(grid.head), Create(grid.rule), *[FadeIn(c) for c in grid.cell[0]])
            vo.wait_until("b")
            self.play(*[FadeIn(c) for c in grid.cell[1]])
            vo.wait_until("c")
            self.play(*[FadeIn(c) for c in grid.cell[2]])
            vo.wait_until("d")
            self.play(FadeIn(foot[0]))
            vo.wait_until("e")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def models(self):
        head = label(r"Models of the experienced present", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"cinematic", r"experience is a series of momentary snapshots; \ succession is judged, \ not seen", BAD),
            (r"retentional", r"each momentary experience contains retentions of the past and protentions of the "
                             r"future \ (Husserl)", TIME),
            (r"extensional", r"experiences themselves last a short while, \ and the succession is in them \ "
                             r"(Dainton, \ \textit{Stream of Consciousness}, \ 2000)", ACT),
            (r"Grush \ (2006)", r"retention and protention as a trajectory estimate: \ the brain smooths the recent past "
                                r"and predicts the next moment", GOAL),
            (r"Varela \ (1999)", r"the present's width tied to the integration of neural assemblies, \ over half a second "
                                r"to a few seconds", WORLD),
        ]
        g = rows_table(rows, top=1.6, gap=0.45)
        with self.voiceover(
            "Philosophers of time now sort the options into three models, in Barry Dainton's terms. "
            "<bookmark mark='a'/>On the cinematic model, experience is a series of momentary snapshots, and "
            "succession is judged rather than seen. <bookmark mark='b'/>On the retentional model, Husserl's, each "
            "momentary experience contains retentions of the past and protentions of the future. "
            "<bookmark mark='c'/>On the extensional model, experiences themselves are extended in time, lasting a "
            "short while, and the succession is in them. <bookmark mark='d'/>Rick Grush gave the retentional model "
            "a computational form in 2006: the brain keeps an estimate of a short trajectory, smoothing the recent "
            "past and predicting the next moment, as an engineer's filter does. <bookmark mark='e'/>And Francisco "
            "Varela tied the width of the present to the time neural assemblies take to integrate, from half a second "
            "to a few seconds. A century after "
            "the lectures, Husserl's diagram had become a hypothesis about brains."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
