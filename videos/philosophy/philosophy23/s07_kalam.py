from __future__ import annotations

from videos.philosophy.philosophy23.common import *  # noqa: F403


class Kalam(VoiceoverScene):
    def construct(self):
        card = chapter_card(6, r"Did the universe begin?", r"Can there be an infinite past?", lit=(1095, 1979),
                            part=PART)
        with self.voiceover("Chapter six. Did the universe begin?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.argument()
        self.planets()
        self.hotel()
        self.physics()

    def argument(self):
        hc = history_card(1095, r"al-Ghazālī", r"\textit{The Incoherence of the Philosophers}", width=6.4,
                          color=HIST).to_corner(UL, buff=0.3)
        steps = stack([(r"1. \ whatever begins to exist has a cause", WHITE),
                       (r"2. \ the universe began to exist", ABS),
                       (r"3. \ so the universe has a cause", DIV)], font_size=26, aligned_edge=LEFT,
                      buff=0.3).move_to([0, 0.6, 0])
        rows = stack([(r"the \textit{kalām} tradition of Islamic theology; \ revived by Craig \ (1979)", HIST),
                      (r"against Avicenna and Aristotle's eternal world: \ al-Ghazālī argued that the past must be "
                       r"finite", WHITE),
                      (r"premise 2 has two defences: \ an actual infinite is impossible; \ and cosmology", GOAL)],
                     font_size=21, aligned_edge=LEFT, width=12.0).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "A different cosmological argument comes from the kalām, the dialectical theology of medieval Islam. "
            "<bookmark mark='a'/>Whatever begins to exist has a cause. <bookmark mark='b'/>The universe began to "
            "exist. <bookmark mark='c'/>So the universe has a cause. <bookmark mark='d'/>William Lane Craig revived "
            "it in 1979. <bookmark mark='e'/>Its great medieval champion was al-Ghazālī, arguing against Avicenna "
            "and the Aristotelian thesis that the world had no beginning. <bookmark mark='f'/>Everything turns on the "
            "second premise, and it has two kinds of defence: that an actually infinite past is impossible, and that "
            "physics shows a beginning."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abc", steps):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            for mk, r in zip("def", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def planets(self):
        d = load("ghazali")
        head = label(r"Al-Ghazālī's planets", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        sun = Dot([-4.2, 0.6, 0], radius=0.25, color=YELLOW)
        orbits = VGroup(*[Circle(radius=r, color=GREY_D, stroke_width=1.5).move_to(sun) for r in (1.0, 1.7, 2.4)])
        bodies = VGroup(*[Dot(sun.get_center() + r * np.array([np.cos(a), np.sin(a), 0]), radius=rad, color=c)
                          for r, a, rad, c in ((1.0, PI / 2, 0.1, ARG), (1.7, 7 * PI / 6, 0.15, WARM),
                                               (2.4, -PI / 6, 0.14, HUM))])
        names = VGroup(*[VGroup(Dot(radius=0.08, color=c), label(t, font_size=17, color=c)).arrange(RIGHT, buff=0.12)
                         for t, c in ((r"one year", ARG), (r"Jupiter: \ 12 years", WARM),
                                      (r"Saturn: \ 30 years", HUM))]).arrange(DOWN, aligned_edge=LEFT,
                                                                             buff=0.12).move_to([2.4, -1.05, 0])
        hd = [r"\text{years past}", r"\text{years}", r"\text{Jupiter}", r"\text{Saturn}"]
        rows = [[MathTex(f"{r['years']:,}".replace(",", r"\,"), font_size=21),
                 MathTex(f"{r['sun']:,}".replace(",", r"\,"), font_size=21, color=ARG),
                 MathTex(f"{r['jupiter']:,}".replace(",", r"\,"), font_size=21, color=WARM),
                 MathTex(f"{r['saturn']:,}".replace(",", r"\,"), font_size=21, color=HUM)] for r in d["rows"]]
        rows.append([MathTex(r"\infty", font_size=24), MathTex(r"\aleph_0", font_size=24, color=ARG),
                     MathTex(r"\aleph_0", font_size=24, color=WARM), MathTex(r"\aleph_0", font_size=24, color=HUM)])
        grid = ValueGrid(hd, rows, col_w=[1.9, 1.5, 1.5, 1.5], cell_h=0.45, font_size=19).move_to([3.2, 0.9, 0])
        rows2 = stack([(r"over any finite past, \ Saturn has two-fifths of Jupiter's revolutions", WHITE),
                       (r"over an infinite past both are infinite, \ and equal in number: \ is that absurd?", BAD),
                       (r"Cantor's answer \ (Part 6): \ not absurd, \ just infinite: \ a part can be as many as the "
                        r"whole", ABS)], font_size=20, aligned_edge=LEFT, width=12.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Al-Ghazālī's argument against an infinite past used the planets. <bookmark mark='a'/>Each year the sun "
            "goes round once; Jupiter, roughly, once in twelve years; Saturn once in thirty. <bookmark mark='b'/>Over "
            "any finite past the counts keep their proportions: in six thousand years, five hundred revolutions of "
            "Jupiter and two hundred of Saturn. <bookmark mark='c'/>But if the past were infinite, both would have "
            "made infinitely many revolutions, and the same number, though one turns two and a half times as fast as "
            "the other. Al-Ghazālī took that to be absurd; and he asked whether the number of revolutions is odd or "
            "even. <bookmark mark='d'/>After Cantor, and Part 6, we can say: it is not absurd, only infinite. A part "
            "of an infinite set can have as many members as the whole."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sun), Create(orbits))
            vo.wait_until("a")
            self.play(FadeIn(bodies), FadeIn(names))
            self.play(*[Rotate(b, angle=PI * k, about_point=sun.get_center()) for b, k in
                        zip(bodies, (2.0, 0.6, 0.25))], run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(grid.head), Create(grid.rule))
            for r in range(len(d["rows"])):
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.4)
            self.play(FadeIn(rows2[0]))
            vo.wait_until("c")
            self.play(*[FadeIn(c) for c in grid.cell[-1]], FadeIn(rows2[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows2[2]))
        self.clear_scene()

    def hotel(self):
        head = label(r"Can an actual infinite exist?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rooms = VGroup(*[Square(side_length=0.55, color=ARG, fill_opacity=0.25 if i % 2 else 0.5,
                                stroke_width=1.5).move_to([-5.8 + 0.62 * i, 1.4, 0]) for i in range(18)])
        dots = label(r"\ldots", font_size=30).next_to(rooms, RIGHT, buff=0.1)
        rl = label(r"Hilbert's hotel: \ every room full", font_size=19, color=ARG).next_to(rooms, UP, buff=0.15)
        rows = [
            (r"Craig", r"guests in the odd rooms leave: \ infinitely many remain; \ guests in rooms above 3 leave: \ "
                       r"three remain", BAD),
            (r"the charge", r"the same subtraction gives different answers: \ so an actual infinite is absurd", BAD),
            (r"the reply", r"transfinite subtraction is simply undefined, \ like dividing by zero; \ no contradiction",
             ABS),
            (r"traversal", r"even so, \ can an infinite series be completed by adding one year after another?", GOAL),
            (r"Tristram Shandy", r"Russell: \ he writes one day's life in a year; \ with an infinite past, \ is he done?",
             HUM),
        ]
        g = rows_table(rows, top=0.6, gap=0.42, width=8.8, x_text=-2.6, label_size=21)
        with self.voiceover(
            "The philosophical defence says that an actual infinite cannot exist. <bookmark mark='a'/>Craig's version "
            "uses Hilbert's hotel from Part 6. If the guests in the odd-numbered rooms check out, infinitely many "
            "remain; if all guests above room three check out, three remain. <bookmark mark='b'/>The same number has "
            "left in both cases, yet different numbers remain: absurd, says Craig, so no actual infinite can exist. "
            "<bookmark mark='c'/>Mathematicians reply that transfinite subtraction is simply undefined, like "
            "division by zero; set theory has no contradiction here. <bookmark mark='d'/>The second defence asks "
            "whether an infinite series can be completed by adding one member after another, as the years of an "
            "infinite past would have to be. <bookmark mark='e'/>Bertrand Russell's Tristram Shandy takes a year to "
            "write up each day of his life. Given an infinite past, is the autobiography finished? Philosophers have "
            "argued both ways."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rooms), FadeIn(dots), FadeIn(rl))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def physics(self):
        head = label(r"What cosmology says", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        ax = Axes(x_range=[0, 10, 2], y_range=[0, 5, 1], x_length=5.0, y_length=2.8,
                  axis_config={"color": GREY_B, "include_ticks": False}).move_to([-3.6, 0.6, 0])
        curve = ax.plot(lambda t: 0.08 * t ** 1.6 + 0.02, x_range=[0.0, 10], color=NAT, stroke_width=3)
        xl = label(r"time", font_size=17, color=GREY_A).next_to(ax.x_axis, RIGHT, buff=0.1)
        yl = label(r"size of the universe", font_size=17, color=GREY_A).next_to(ax.y_axis, UP, buff=0.1)
        q = label(r"?", font_size=40, color=GOAL).move_to(ax.c2p(0.2, 0.9))
        rows = stack([(r"the Big Bang: \ a hot, \ dense state some 13.8 billion years ago", NAT),
                      (r"Borde, \ Guth and Vilenkin \ (2003): \ a universe that has expanded on average cannot be "
                       r"extended forever into the past", WHITE),
                      (r"but that is a limit of classical spacetime, \ not a proof of a first moment", GOAL),
                      (r"quantum cosmologies: \ no boundary \ (Hartle and Hawking, \ 1983), \ bouncing and eternal "
                       r"models", ABS),
                      (r"and premise 1 meets a puzzle: \ a cause of time itself is not a cause \textit{in} time", BAD)],
                     font_size=19, aligned_edge=LEFT, width=6.0).move_to([3.6, -0.3, 0])
        with self.voiceover(
            "The scientific defence appeals to cosmology. <bookmark mark='a'/>The universe has expanded from a hot, "
            "dense state about thirteen point eight billion years ago. <bookmark mark='b'/>Arvind Borde, Alan Guth and "
            "Alexander Vilenkin proved in 2003 that a spacetime which has expanded on average cannot be extended "
            "indefinitely into the past. <bookmark mark='c'/>But that is a statement about classical spacetime "
            "breaking down, not a proof that there was a first moment. <bookmark mark='d'/>Quantum cosmology offers "
            "models without a boundary, like James Hartle and Stephen Hawking's, as well as bouncing and eternal "
            "models. <bookmark mark='e'/>And the first premise meets a puzzle of its own: a cause of time itself "
            "cannot be a cause that comes before its effect in time, so the familiar notion of cause is being "
            "stretched."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(curve), FadeIn(rows[0]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(q), FadeIn(rows[2]))
            for mk, r in zip("de", rows[3:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
