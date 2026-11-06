from __future__ import annotations

from videos.philosophy.philosophy9.common import *  # noqa: F403


class Field(VoiceoverScene):
    def construct(self):
        card = chapter_card(11, r"Science without numbers", r"Could physics do without mathematics?", lit=(1899, 1980),
                            part=PART)
        with self.voiceover("Chapter eleven. Science without numbers."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.program()
        self.represent()
        self.fiction()

    def program(self):
        hc = history_card(1980, r"Hartry Field", r"\textit{Science without Numbers}", width=5.0, color=HIST).to_corner(
            UL, buff=0.35)
        left = VGroup(label(r"Newtonian gravity, \ as usually stated", font_size=24, color=NUM),
                      MathTex(r"\nabla^2 \phi = 4\pi G \rho", font_size=40, color=NUM),
                      label(r"a field: \ a function from points to real numbers", font_size=20, color=GREY_A)).arrange(
            DOWN, buff=0.2)
        right = VGroup(label(r"Field's version", font_size=24, color=CONCRETE),
                       label(r"points and regions of spacetime", font_size=22, color=WHITE),
                       label(r"betweenness, \ congruence, \ and comparisons of potential", font_size=20,
                             color=GREY_A),
                       label(r"no numbers at all", font_size=20, color=CONCRETE)).arrange(DOWN, buff=0.15)
        cols = VGroup(left, right).arrange(RIGHT, buff=1.4).move_to([0, 0.6, 0])
        arr = Arrow(left.get_right(), right.get_left(), buff=0.3, color=GREY_B)
        rows = VGroup(
            label(r"model: \ Hilbert's \textit{Foundations of Geometry} \ (1899): \ points and relations, \ no "
                  r"coordinates", font_size=22, color=GREY_A),
            label(r"then add mathematics as a tool: \ it is \textit{conservative}, \ it proves no new facts about the "
                  r"physical world", font_size=24, color=OK),
            label(r"mathematics need not be true, \ only conservative: \ a quicker route between true physical claims",
                  font_size=24, color=GOAL)).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "In 1980 Hartry Field set out to answer the indispensability argument head on. <bookmark mark='a'/>"
            "Newton's theory of gravity, as usually stated, describes a field: a function from points of space to "
            "real numbers. <bookmark mark='b'/>Field rewrote it with no numbers at all. His theory quantifies over "
            "points and regions of spacetime, which a nominalist can accept, and uses only relations among them: "
            "betweenness, congruence of segments, and comparisons of gravitational potential. "
            "<bookmark mark='c'/>The model was Hilbert's geometry of 1899, which axiomatizes points and lines with "
            "no coordinates. <bookmark mark='d'/>Mathematics then comes back as a tool. Field proved it is "
            "conservative: adding it to the physics proves no new claims about the physical world. "
            "<bookmark mark='e'/>So mathematics need not be true, only conservative: a quicker route between true "
            "claims about the world, like Hilbert's ideal elements."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(GrowArrow(arr), FadeIn(right))
            for mk, r in zip("cde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def represent(self):
        d = load("represent")
        head = label(r"Numbers recovered from a structure of points", font_size=32, color=CONN).to_edge(UP, buff=0.35)
        hidden = d["hidden"]
        names = sorted(hidden)
        line = Line([-5.5, 1.3, 0], [5.5, 1.3, 0], color=GREY_C, stroke_width=2)
        scale = 2.0

        def px(v):
            return np.array([-5.0 + scale * v, 1.3, 0])
        dots = VGroup(*[Dot(px(hidden[n]), radius=0.1, color=CONCRETE) for n in names])
        nl = VGroup(*[MathTex(n, font_size=30, color=CONCRETE).next_to(dt, UP, buff=0.18) for n, dt in zip(names,
                                                                                                         dots)])
        arcs = VGroup()
        cols = [NUM, OK, ABSTRACT, PROOF, GOAL, BAD]
        for k, (s1, s2) in enumerate(d["cong"]):
            col = cols[k % len(cols)]
            for s in (s1, s2):
                a, b = px(hidden[s[0]]), px(hidden[s[1]])
                arcs.add(ArcBetweenPoints(a, b, angle=-0.9, color=col, stroke_width=2).shift(DOWN * 0.05 * (k % 3)))
        facts = label(rf"given only: \ {d['bet']} facts of betweenness \ (`$b$ lies between $a$ and $c$') \ and "
                      rf"{len(d['cong'])} of congruence \ (`$ab$ is as long as $bc$')", font_size=22,
                      color=GREY_A).move_to([0, 2.45, 0])
        reps = d["reps"]
        hd = [label(r"", font_size=20)] + [MathTex(n, font_size=26, color=CONCRETE) for n in names]
        rows = [[label(rf"coordinates {i + 1}", font_size=20)] + [MathTex(str(r[n]), font_size=26) for n in names]
                for i, r in enumerate(reps)]
        grid = ValueGrid(hd, rows, col_w=[2.2] + [1.05] * len(names), cell_h=0.45, font_size=22).move_to(
            [-2.6, -1.45, 0])
        assert len(reps) == 4
        side = VGroup(VGroup(label(r"the Reasoner tries every assignment", font_size=20, color=GREY_A),
                             label(r"of whole numbers, \ $-12$ to $12$, \ with $a$ at $0$", font_size=20,
                                   color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
                      label(r"exactly four survive: \ $x \mapsto \pm x, \ \pm 2x$", font_size=22, color=OK),
                      label(r"choose a unit and a direction, \ and the numbers are fixed", font_size=22, color=GOAL),
                      label(r"the representation theorem, \ in miniature", font_size=20, color=GREY_B)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.22).move_to([4.2, -1.4, 0])
        with self.voiceover(
            "The heart of Field's method is a representation theorem, and the Reasoner can run a small one. "
            "<bookmark mark='a'/>Here are five points on a line. The Reasoner is not told where they are. It is "
            "told only which point lies between which, and which segments are as long as which: twenty facts of "
            "betweenness and six of congruence. No numbers. <bookmark mark='b'/>Now it tries every way of giving the "
            "points whole-number coordinates from minus twelve to twelve, with a at zero, keeping only those that "
            "make exactly the given facts true. <bookmark mark='c'/>Four survive. Each is the same picture, reflected "
            "or stretched: x, minus x, two x, minus two x. <bookmark mark='d'/>Choose a unit and a direction, and "
            "the numbers are fixed. The numbers were never in the points. They are a way of describing the "
            "structure of the points, unique once we make two arbitrary choices. That is what measurement is, and "
            "for Field, all that numbers in physics ever were."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(dots), FadeIn(nl), FadeIn(facts))
            self.play(LaggedStart(*[Create(a) for a in arcs], lag_ratio=0.15), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(side[0]), FadeIn(grid.head), FadeIn(grid.rows_bg), FadeIn(grid.rule))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(VGroup(*grid.cell[r])) for r in range(len(rows))], lag_ratio=0.4),
                      FadeIn(side[1]), run_time=3)
            vo.wait_until("d")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
        self.clear_scene()

    def fiction(self):
        head = label(r"Fictionalism", font_size=34, color=CONN).to_edge(UP, buff=0.5)
        pair = VGroup(
            VGroup(label(r"`Holmes lives at 221B Baker Street'", font_size=24, color=CONCRETE),
                   label(r"false, \ but true \textit{in the stories}", font_size=21, color=GREY_A)).arrange(DOWN,
                                                                                                         buff=0.12),
            VGroup(label(r"`there are infinitely many primes'", font_size=24, color=NUM),
                   label(r"false, \ but true \textit{in the story of mathematics}", font_size=21,
                         color=GREY_A)).arrange(DOWN, buff=0.12)).arrange(RIGHT, buff=1.0).move_to([0, 1.5, 0])
        who = label(r"Field; \ Balaguer (1998); \ Leng, \textit{Mathematics and Reality} (2010)", font_size=22,
                    color=GREY_B).next_to(pair, DOWN, buff=0.35)
        rows = VGroup(
            label(r"objections: \ quantum mechanics resists Field's treatment \ (Malament 1982)", font_size=22,
                  color=BAD),
            label(r"conservativeness needs a strong logic, \ or a semantic notion: \ more mathematics \ "
                  r"(Shapiro 1983)", font_size=22, color=BAD),
            label(r"the `easy road': \ no rewriting at all, \ mathematics as figurative speech \ (Azzouni 2004; "
                  r"Yablo 2005)", font_size=22, color=OK),
            label(r"what we know, \ on this view: \ which theorems follow from which axioms", font_size=24,
                  color=GOAL)).arrange(DOWN, buff=0.28).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Field's view is called fictionalism. <bookmark mark='a'/>'Holmes lives at 221B Baker Street' is false, "
            "since there was no Holmes, but true in the stories. 'There are infinitely many primes' is, for the "
            "fictionalist, false, since there are no numbers, but true in the story of mathematics; and the story is "
            "useful the way a good map is. <bookmark mark='b'/>Mark Balaguer and Mary Leng developed the view. "
            "<bookmark mark='c'/>It faces objections. David Malament argued in 1982 that quantum mechanics, built on "
            "spaces of functions, resists Field's treatment. <bookmark mark='d'/>Stewart Shapiro showed that the "
            "conservativeness Field needs requires either a strong logic or a semantic notion of consequence, which "
            "brings mathematics back in. <bookmark mark='e'/>So some fictionalists take an easy road: no rewriting of "
            "physics at all, only the claim that mathematical talk, like figurative speech, need not be taken "
            "literally. <bookmark mark='f'/>Either way, what we know, on this view, is which theorems follow from "
            "which axioms, and that is knowledge of logic, not of objects."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(pair))
            vo.wait_until("b")
            self.play(FadeIn(who))
            for mk, r in zip("cdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
