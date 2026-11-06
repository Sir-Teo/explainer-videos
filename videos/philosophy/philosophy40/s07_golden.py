from __future__ import annotations

from videos.philosophy.philosophy40.common import *  # noqa: F403


class Golden(VoiceoverScene):
    def construct(self):
        card = chapter_card(6, r"The golden ratio, \ tested", r"Is there a number of beauty?", lit=(1876,), part=PART)
        with self.voiceover("Chapter six. The golden ratio, tested."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.ratio()
        self.lookelsewhere()
        self.evidence()
        self.sunflower()
        self.faces()

    def evidence(self):
        head = label(r"What survives", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Fechner \ (1876)", r"\textit{Vorschule der Ästhetik}: \ people chose the golden rectangle most often, \ the first experiment in aesthetics", HIST),
                (r"replications", r"McManus \ (1980) \ and Green's review \ (1995): \ a weak preference near 1.6, \ sensitive to method", TASTE),
                (r"the myths", r"Markowsky \ (1992): \ the Parthenon, \ the pyramids, \ Leonardo: \ measurements chosen to fit", BAD),
                (r"what is real", r"in nature, \ phyllotaxis: \ leaves and seeds at the golden angle, \ $137.5^\circ$, \ pack efficiently", SYM)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "What survives of the legend? <bookmark mark='a'/>Gustav Fechner's Vorschule der Ästhetik, of 1876, "
            "reported that people shown rectangles chose the golden one most often: the first experiment in "
            "aesthetics. <bookmark mark='b'/>Later work, from Chris McManus in 1980 to Christopher Green's review of "
            "1995, found at most a weak preference near one point six, and one sensitive to how the question is "
            "asked. <bookmark mark='c'/>George Markowsky's Misconceptions about the Golden Ratio, of 1992, showed "
            "that the famous architectural cases rest on measurements chosen to fit. <bookmark mark='d'/>What is real "
            "is in botany: many plants place successive leaves and seeds at the golden angle, a hundred and thirty "
            "seven and a half degrees, which packs them efficiently."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def ratio(self):
        g = load("golden")
        assert g["phi"] == 1.618034 and g["fibonacci"][-1]["ratio"] == 1.618033
        head = label(r"$\varphi = \tfrac{1 + \sqrt5}{2} \approx 1.618$", font_size=34, color=TASTE).to_edge(UP, buff=0.3)
        # the golden rectangle, subdivided
        sq = VGroup()
        x, y, w, h = -6.0, -2.6, 5.4, 5.4 / g["phi"]
        rect = Rectangle(width=w, height=h, color=TASTE, stroke_width=3).move_to([x + w / 2, y + h / 2, 0])
        cx, cy, cw, ch = x, y, w, h
        for k in range(7):
            if k % 4 == 0:
                s = ch
                sq.add(Square(side_length=s, color=SYM, stroke_width=2).move_to([cx + s / 2, cy + s / 2, 0]))
                cx, cw = cx + s, cw - s
            elif k % 4 == 1:
                s = cw
                sq.add(Square(side_length=s, color=SYM, stroke_width=2).move_to([cx + s / 2, cy + ch - s / 2, 0]))
                ch = ch - s
            elif k % 4 == 2:
                s = ch
                sq.add(Square(side_length=s, color=SYM, stroke_width=2).move_to([cx + cw - s / 2, cy + s / 2, 0]))
                cw = cw - s
            else:
                s = cw
                sq.add(Square(side_length=s, color=SYM, stroke_width=2).move_to([cx + s / 2, cy + s / 2, 0]))
                cy, ch = cy + s, ch - s
        f = MathTex(r"\frac{a + b}{a} = \frac{a}{b} = \varphi \quad\Longleftrightarrow\quad \varphi^2 = \varphi + 1",
                    font_size=30, color=WHITE).move_to([3.4, 1.9, 0])
        hd = [r"n", r"F_{n+1}/F_n"]
        cells = [[label(str(e["n"]), font_size=18, color=GREY_A), label(f"{e['ratio']:.6f}", font_size=18)]
                 for e in g["fibonacci"][::2]]
        grid = ValueGrid(hd, cells, col_w=[1.0, 2.2], cell_h=0.36, font_size=18).move_to([3.4, -0.7, 0])
        with self.voiceover(
            "The golden ratio is said to be the secret of beauty. <bookmark mark='a'/>Divide a line so that the whole "
            "is to the larger part as the larger part is to the smaller: the ratio is phi, one plus root five over "
            "two, about one point six one eight, the number whose square is itself plus one. <bookmark mark='b'/>A "
            "golden rectangle has these proportions; cut off a square and the rest is golden again, without end. "
            "<bookmark mark='c'/>And the ratios of successive Fibonacci numbers, two, one and a half, five thirds, "
            "and so on, close in on phi from both sides."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f))
            vo.wait_until("b")
            self.play(Create(rect))
            self.play(LaggedStart(*[Create(s) for s in sq], lag_ratio=0.4), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(grid.head), Create(grid.rule), LaggedStart(*[FadeIn(VGroup(*r)) for r in grid.cell],
                                                                         lag_ratio=0.2))
        self.clear_scene()

    def lookelsewhere(self):
        g = load("golden")
        assert (g["trials"], g["lengths"], g["pairs"], g["tol"], g["p_some_hit"]) == (20000, 8, 28, 0.03, 0.698)
        head = label(r"Finding $\varphi$ everywhere", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        lines = stack([(r"measure 8 lengths on an imaginary building, \ at random between 1 and 10", GREY_A),
                       (r"28 ratios of one length to another", GREY_A),
                       (rf"in {g['p_some_hit'] * 100:.0f}\% of 20,000 trials, \ some ratio is within 3\% of $\varphi$",
                        BAD),
                       (rf"on average {g['mean_hits']} golden ratios per building, \ by chance alone", BAD),
                       (r"so finding $\varphi$ in the Parthenon or the \textit{Mona Lisa} is no evidence it was put "
                        r"there", GOAL)],
                      font_size=23, buff=0.38).move_to([0, 0.1, 0])
        with self.voiceover(
            "Is the golden ratio really in the Parthenon, the pyramids and the Mona Lisa? The Reasoner runs a test of "
            "what such claims are worth. <bookmark mark='a'/>Measure eight lengths on an imaginary building, chosen "
            "at random between one and ten. <bookmark mark='b'/>That gives twenty eight ratios of one length to "
            "another. <bookmark mark='c'/>In seventy percent of twenty thousand trials, at least one of those ratios "
            "is within three percent of phi. <bookmark mark='d'/>On average, each random building contains one and a "
            "quarter golden ratios. <bookmark mark='e'/>So finding phi in a famous building, among many possible "
            "measurements, is no evidence that anyone put it there: the look-elsewhere effect of Part 16."
        ) as vo:
            self.play(FadeIn(head))
            for mk, i in zip("abcde", range(5)):
                vo.wait_until(mk)
                self.play(FadeIn(lines[i], shift=RIGHT * 0.2))
        self.clear_scene()

    def sunflower(self):
        d = load("sunflower")
        pats = d["patterns"]
        assert d["golden_angle"] == 137.508 and [p0["angle"] for p0 in pats] == [137.0, 137.508, 137.6]
        head = label(r"Seeds at the golden angle \ (Vogel, \ 1979)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        heads = Group()
        for p0, c in zip(pats, (GREY_A, TASTE, GREY_A)):
            dots = VGroup(*[Dot([x * 0.11, y * 0.11, 0], radius=0.035, color=c) for x, y in p0["pts"]])
            cap = label(rf"${p0['angle']:.3f}^\circ$" if p0["angle"] == d["golden_angle"] else rf"${p0['angle']:.1f}^\circ$",
                        font_size=22, color=c)
            gap = label(rf"closest seeds: \ {p0['min_gap']:.2f}", font_size=18, color=GREY_B)
            heads.add(Group(dots, cap, gap))
        for h in heads:
            h[1].next_to(h[0], UP, buff=0.2)
            h[2].next_to(h[0], DOWN, buff=0.2)
        heads.arrange(RIGHT, buff=0.8).move_to([0, -0.2, 0])
        f = MathTex(r"\theta_k = k \times 137.508^\circ, \qquad r_k = \sqrt{k}", font_size=30).next_to(head, DOWN, buff=0.2)
        with self.voiceover(
            "Here is where the golden ratio really lives. <bookmark mark='a'/>Helmut Vogel's model of a sunflower "
            "head, from 1979: put seed number k at an angle of k times the divergence angle, and at a distance from "
            "the centre proportional to the square root of k. <bookmark mark='b'/>At the golden angle, a hundred and "
            "thirty seven point five degrees, which divides the circle in the golden ratio, the seeds fill the disc "
            "evenly, in the interlocking spirals of a real sunflower. <bookmark mark='c'/>Half a degree less, or a "
            "tenth of a degree more, and the seeds line up in spokes with gaps between: the closest pair of seeds is "
            "a third nearer. Because phi is the hardest number to approximate by fractions, no two seeds ever line "
            "up. This is beauty as efficiency, found by selection rather than chosen by taste."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x) for x in heads[1][0]], lag_ratio=0.005), FadeIn(heads[1][1]),
                      run_time=3)
            self.play(FadeIn(heads[1][2]))
            vo.wait_until("c")
            self.play(FadeIn(heads[0]), FadeIn(heads[2]))
        self.clear_scene()

    def faces(self):
        head = label(r"Beauty in faces, \ and an art instinct", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"averageness", r"Langlois and Roggman \ (1990): \ faces averaged by computer were rated more attractive than most of their sources", SYM),
                (r"symmetry", r"symmetric faces are preferred, \ though less strongly than once claimed \ (Rhodes, \ 2006)", FORM),
                (r"Dutton \ (2009)", r"\textit{The Art Instinct}: \ tastes for skill, \ display and open landscapes, \ shaped by evolution", TASTE),
                (r"Komar and Melamid", r"1990s polls in many countries: \ nearly every nation's `most wanted' painting was a blue landscape", ART)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Psychology finds some regularities in what people find beautiful. <bookmark mark='a'/>Judith Langlois "
            "and Lori Roggman found in 1990 that faces averaged together by computer were rated more attractive than "
            "most of the faces they were made from. <bookmark mark='b'/>Symmetric faces are preferred, though, as "
            "Gillian Rhodes's review of 2006 found, less strongly than once claimed. <bookmark mark='c'/>Denis "
            "Dutton's The Art Instinct, of 2009, argued that tastes for skill, display and open, watered landscapes "
            "were shaped by evolution. <bookmark mark='d'/>The artists Vitaly Komar and Alexander Melamid "
            "commissioned opinion polls in many countries in the 1990s and painted each nation's most wanted picture: "
            "almost all were blue landscapes with water, trees and people."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
