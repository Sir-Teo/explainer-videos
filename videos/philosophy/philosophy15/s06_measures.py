from __future__ import annotations

from videos.philosophy.philosophy15.common import *  # noqa: F403

MEAS = [("difference", r"d", r"P(H\mid E) - P(H)", "E2"),
        ("log ratio", r"r", r"\log \frac{P(H\mid E)}{P(H)}", "E1"),
        ("log likelihood ratio", r"l", r"\log \frac{P(E\mid H)}{P(E\mid \lnot H)}", "E1"),
        ("Kemeny-Oppenheim", r"k", r"\frac{P(E\mid H) - P(E\mid\lnot H)}{P(E\mid H) + P(E\mid\lnot H)}", "E1"),
        ("Carnap", r"c", r"P(H \wedge E) - P(H)P(E)", "E2"),
        ("Christensen", r"s", r"P(H\mid E) - P(H\mid \lnot E)", "E2")]


class Measures(VoiceoverScene):
    def construct(self):
        card = chapter_card(5, r"Measuring confirmation", r"How much does evidence support a hypothesis?",
                            lit=(1950,), part=PART)
        with self.voiceover("Chapter five. Measuring confirmation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.incremental()
        self.table()
        self.symmetries()
        self.oldev()

    def incremental(self):
        head = label(r"Two senses of `confirms'", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        a = VGroup(label(r"firmness", font_size=25, color=PAST),
                   MathTex(r"P(H \mid E) > t", font_size=36, color=PAST),
                   label(r"$H$ is probable, \ given $E$", font_size=21, color=GREY_A)).arrange(DOWN, buff=0.2)
        b = VGroup(label(r"increase", font_size=25, color=FUT),
                   MathTex(r"P(H \mid E) > P(H)", font_size=36, color=FUT),
                   label(r"$E$ raises the probability of $H$", font_size=21, color=GREY_A)).arrange(DOWN, buff=0.2)
        ab = VGroup(a, b).arrange(RIGHT, buff=2.0).next_to(head, DOWN, buff=0.5)
        # a bar picture: prior and posterior for two cases
        ax_y = -1.6

        def bars(x, pr, po, col):
            base = Line([x - 0.9, ax_y, 0], [x + 0.9, ax_y, 0], color=GREY_C, stroke_width=2)
            r1 = Rectangle(width=0.6, height=pr * 2.4, stroke_width=0, fill_color=GREY_B, fill_opacity=0.7)
            r2 = Rectangle(width=0.6, height=po * 2.4, stroke_width=0, fill_color=col, fill_opacity=0.85)
            r1.move_to([x - 0.4, ax_y + r1.height / 2, 0])
            r2.move_to([x + 0.4, ax_y + r2.height / 2, 0])
            t1 = label(r"before", font_size=16, color=GREY_B).next_to(r1, DOWN, buff=0.1)
            t2 = label(r"after", font_size=16, color=col).next_to(r2, DOWN, buff=0.1)
            return VGroup(base, r1, r2, t1, t2)
        case1 = bars(-3.2, 0.85, 0.80, BAD)
        case2 = bars(3.2, 0.05, 0.4, OK)
        c1 = label(r"probable, \ but $E$ lowered it", font_size=20, color=BAD).next_to(case1, DOWN, buff=0.1)
        c2 = label(r"improbable, \ but $E$ raised it eightfold", font_size=20, color=OK).next_to(case2, DOWN,
                                                                                                 buff=0.1)
        foot = label(r"Carnap \ (1950, \ 2nd ed.\ 1962) \ drew the distinction; \ the ravens are about increase",
                     font_size=21, color=GREY_A).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Before measuring confirmation, we should say what it is. Carnap, in the preface to the second edition "
            "of his Logical Foundations of Probability, separated two senses. <bookmark mark='a'/>Firmness: given E, "
            "H is probable. <bookmark mark='b'/>Increase: E raises the probability of H. <bookmark mark='c'/>They "
            "come apart. A hypothesis can be probable after the evidence even though the evidence lowered it. "
            "<bookmark mark='d'/>And a hypothesis can stay improbable even though the evidence raised it eightfold. "
            "<bookmark mark='e'/>The ravens, and almost all of modern confirmation theory, concern increase."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(a))
            vo.wait_until("b")
            self.play(FadeIn(b))
            vo.wait_until("c")
            self.play(FadeIn(case1), FadeIn(c1))
            vo.wait_until("d")
            self.play(FadeIn(case2), FadeIn(c2))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def table(self):
        d = load("measures")
        head = label(r"Six measures, \ two pieces of evidence", font_size=30, color=CONN).to_edge(UP, buff=0.25)
        ev = stack([(r"$E_1$: \ a long shot \ ($P(H) = 0.01$) \ made 9 times likelier \ by the likelihoods", A_C),
                    (r"$E_2$: \ an even bet \ ($P(H) = 0.5$) \ with likelihoods 0.9 vs 0.5", B_C)], font_size=21,
                   aligned_edge=LEFT).next_to(head, DOWN, buff=0.25)
        hd = [r"", r"\text{measure}", r"E_1", r"E_2", r"\text{prefers}"]
        rows = []
        for name, sym, formula, pref in MEAS:
            rows.append([MathTex(sym, font_size=26, color=FUT), MathTex(formula, font_size=24),
                         MathTex(f"{d['E1'][name]:.3f}", font_size=24, color=A_C),
                         MathTex(f"{d['E2'][name]:.3f}", font_size=24, color=B_C),
                         MathTex(r"E_1" if pref == "E1" else r"E_2", font_size=26, color=A_C if pref == "E1" else B_C)])
        grid = ValueGrid(hd, rows, col_w=[0.6, 5.4, 1.4, 1.4, 1.5], cell_h=0.66, font_size=24).next_to(ev, DOWN,
                                                                                                      buff=0.25)
        names = VGroup(*[label(n, font_size=18, color=GREY_B).next_to(grid.cell[i][0], LEFT, buff=0.15)
                         for i, (n, _, _, _) in enumerate(MEAS)])
        foot = label(r"three measures rank $E_1$ higher, \ three rank $E_2$: \ `how much' has no single answer",
                     font_size=22, color=GOAL).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "Increase can be measured in many ways, and they disagree. <bookmark mark='a'/>Take two pieces of "
            "evidence. E one makes a long shot, with prior one in a hundred, nine times likelier by the "
            "likelihoods. E two bears on an even bet, with likelihoods point nine against point five. "
            "<bookmark mark='b'/>Here are six measures from the literature: the difference, the log of the "
            "probability ratio, the log likelihood ratio, Kemeny and Oppenheim's normalized version of it, Carnap's "
            "relevance measure, and Christensen's. <bookmark mark='c'/>The Reasoner computes each. "
            "<bookmark mark='d'/>The difference measure says E two confirms more; so do Carnap's and Christensen's. "
            "The ratio and likelihood measures say E one does. <bookmark mark='e'/>Branden Fitelson showed that "
            "many arguments in confirmation theory, including some answers to the ravens, hold on one measure and "
            "fail on another. How much evidence confirms has no single answer."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ev))
            vo.wait_until("b")
            self.play(FadeIn(grid.head), Create(grid.rule))
            self.play(LaggedStart(*[FadeIn(VGroup(grid.cell[r][0], grid.cell[r][1], names[r])) for r in
                                    range(len(MEAS))], lag_ratio=0.25))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(VGroup(grid.cell[r][2], grid.cell[r][3])) for r in range(len(MEAS))],
                                  lag_ratio=0.2))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(grid.cell[r][4], scale=1.3) for r in range(len(MEAS))], lag_ratio=0.2))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def symmetries(self):
        d = load("measures")["desiderata"]
        tab = d["table"]
        head = label(r"Which measures behave? \ Three symmetries", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        syms = [("hypothesis symmetry", r"c(H, E) = -c(\lnot H, E)", True),
                ("evidence symmetry", r"c(H, E) = -c(H, \lnot E)", False),
                ("commutativity", r"c(H, E) = c(E, H)", False)]
        hd = [r"\text{measure}"] + [MathTex(f, font_size=22, color=OK if want else BAD) for _, f, want in syms]
        rows = []
        for name, sym, _, _ in MEAS:
            r = [MathTex(sym, font_size=26, color=FUT)]
            for key, _, want in syms:
                r.append(bool(tab[name][key]))
            rows.append(r)
        grid = ValueGrid(hd, rows, col_w=[1.6, 3.4, 3.4, 3.0], cell_h=0.52, font_size=24).next_to(head, DOWN, buff=0.4)
        wants = VGroup(*[label(r"wanted" if want else r"unwanted", font_size=18, color=OK if want else BAD).next_to(
            grid.head[i + 1], UP, buff=0.1) for i, (_, _, want) in enumerate(syms)])
        names = VGroup(*[label(n, font_size=18, color=GREY_B).next_to(grid.cell[i][0], LEFT, buff=0.15)
                         for i, (n, _, _, _) in enumerate(MEAS)])
        keep = [i for i, (n, _, _, _) in enumerate(MEAS) if tab[n]["hypothesis symmetry"] and
                not tab[n]["evidence symmetry"] and not tab[n]["commutativity"]]
        boxes = VGroup(*[grid.row_box(i, color=GOAL) for i in keep]) if hasattr(grid, "row_box") else VGroup()
        foot = label(r"Eells and Fitelson \ (2002): \ only $d$, \ $l$ \ and $k$ pass; \ checked on " +
                     f"{d['samples']:,}".replace(",", "{,}") + r" random distributions", font_size=21,
                     color=GOAL).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "If the measures disagree, which should we use? Ellery Eells and Branden Fitelson proposed testing them "
            "against symmetries. <bookmark mark='a'/>Hypothesis symmetry: evidence that confirms H should "
            "disconfirm not-H by the same amount. That seems right. <bookmark mark='b'/>Evidence symmetry: if E "
            "confirms H, then not-E should disconfirm H by the same amount. That seems wrong: finding a black "
            "raven confirms a little, but failing to find one need not disconfirm equally. "
            "<bookmark mark='c'/>And commutativity: E confirms H exactly as much as H confirms E. Also wrong. "
            "<bookmark mark='d'/>The Reasoner checks each measure on two thousand random probability "
            "distributions. <bookmark mark='e'/>Only the difference, the log likelihood ratio, and Kemeny and "
            "Oppenheim's measure have the wanted symmetry and lack the unwanted ones."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(grid.head[0]), FadeIn(grid.head[1]), FadeIn(wants[0]), Create(grid.rule))
            vo.wait_until("b")
            self.play(FadeIn(grid.head[2]), FadeIn(wants[1]))
            vo.wait_until("c")
            self.play(FadeIn(grid.head[3]), FadeIn(wants[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(VGroup(*grid.cell[r], names[r])) for r in range(len(MEAS))],
                                  lag_ratio=0.2))
            vo.wait_until("e")
            self.play(*[Create(b) for b in boxes], FadeIn(foot))
        self.clear_scene()

    def oldev(self):
        hc = history_card(1980, r"Clark Glymour", r"\textit{Theory and Evidence}: \ the problem of old evidence",
                          width=6.6, color=HIST).to_corner(UL, buff=0.35)
        story = stack([(r"1859: \ Le Verrier: \ Mercury's perihelion advances faster than Newton allows \ (about 43'' a century)", PAST),
                       (r"1915: \ Einstein derives exactly 43'' from general relativity", FUT),
                       (r"the strongest early evidence for the theory", OK)], font_size=22,
                      aligned_edge=LEFT).next_to(hc, DOWN, buff=0.35).set_x(-1.6)
        eq = MathTex(r"P(E) = 1 \ \Rightarrow\ P(H\mid E) = \frac{P(H)\,P(E\mid H)}{P(E)} = P(H)", font_size=34,
                     color=BAD).next_to(story, DOWN, buff=0.4).set_x(0)
        resp = stack([
            (r"counterfactual: \ judge with the credence you \textit{would} have had without $E$ \ (Howson)", GREY_A),
            (r"logical learning: \ what was learned in 1915 was $H \vdash E$ \ (Garber, \ Jeffrey, \ Niiniluoto)",
             GREY_A),
        ], font_size=21, aligned_edge=LEFT).next_to(eq, DOWN, buff=0.35).set_x(0)
        with self.voiceover(
            "One more problem for the Bayesian account, Clark Glymour's problem of old evidence. "
            "<bookmark mark='a'/>Since Le Verrier in 1859, astronomers had known that Mercury's perihelion "
            "advances faster than Newton allows, by about forty-three arc seconds a century. <bookmark mark='b'/>In 1915 Einstein derived exactly that "
            "from general relativity, <bookmark mark='c'/>and it became the strongest early evidence for the theory. "
            "<bookmark mark='d'/>But the evidence was already known, with probability one. And when the probability "
            "of E is one, conditioning on it changes nothing: the posterior equals the prior. Old evidence cannot "
            "confirm. <bookmark mark='e'/>Two answers. Colin Howson: measure confirmation against the credence you "
            "would have had without E. <bookmark mark='f'/>Daniel Garber, Richard Jeffrey and Ilkka Niiniluoto: what "
            "Einstein learned in 1915 was not E but a logical fact, that the theory entails E, and for an agent who "
            "is not logically omniscient that is real news."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abc", story):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("d")
            self.play(Write(eq))
            for mk, r in zip("ef", resp):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
