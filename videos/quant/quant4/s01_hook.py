from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant4.common import MART, P_C, PART, load, real_data


class Hook(VoiceoverScene):
    def construct(self):
        e = load("eprocess")
        self.title_card()
        self.betting(e)
        self.points()
        self.era()
        self.objectives()
        self.house()

    def title_card(self):
        card = part_title(PART, r"Can you beat a fair game?")
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part four. Martingales and measure. The first act asked whether prices are a fair game. This act builds "
            "the mathematics that makes the question precise, and its first tool is the oldest idea in gambling: a "
            "fair bet."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(disc))
        self.play(FadeOut(card), FadeOut(disc))

    def betting(self, e):
        old, new = e["19260701"], e["20000101"]
        g = axes([1926, 2021], [-2, 105], x_length=6.4, y_length=4.4, ylabel=r"historical diagnostic score, 1926 start",
                 xticks=[1930, 1960, 1990, 2020], xfmt=lambda x: f"{int(x)}", yticks=[0, 25, 50, 75, 100],
                 yfmt=lambda u: rf"10^{{{int(u)}}}" if u else "1", font_size=18).to_edge(LEFT, buff=0.6).shift(DOWN * 0.4)
        ax = g.ax
        t0, l0 = np.asarray(old["t"]), np.asarray(old["loge"])
        line0 = curve(ax, t0, l0, P_C, stroke_width=2.5)
        g2 = axes([2000, 2021], [-1, 2], x_length=4.6, y_length=2.4, ylabel=r"betting since 2000",
                  xticks=[2000, 2010, 2020], xfmt=lambda x: f"{int(x)}", yticks=[-1, 0, 1, 2],
                  yfmt=lambda u: {-1: "0.1", 0: "1", 1: "10", 2: "100"}[int(u)], font_size=16)
        g2.to_corner(DR, buff=0.6).shift(UP * 0.2)
        ax2 = g2.ax
        t1, l1 = np.asarray(new["t"]), np.asarray(new["loge"])
        line1 = curve(ax2, t1, l1, MART, stroke_width=2.5)
        bar = DashedLine(ax2.c2p(2000, np.log10(20)), ax2.c2p(2021, np.log10(20)), color=QC.LOSS, stroke_width=2)
        barl = label(r"20", font_size=18, color=QC.LOSS).next_to(ax2.c2p(2021, np.log10(20)), RIGHT, buff=0.08)
        bar0 = DashedLine(ax.c2p(1926, np.log10(20)), ax.c2p(2021, np.log10(20)), color=QC.LOSS, stroke_width=2)
        i29 = int(np.argmax(l0 >= np.log10(20)))
        dot29 = Dot(ax.c2p(t0[i29], l0[i29]), radius=0.07, color=YELLOW)
        side = VGroup(
            wrapped_label(r"yesterday's sign times centred, scaled, clipped returns; a mixture of both betting directions",
                          5.2, 21, GREY_A),
            MathTex(rf"\text{{from 1926: }} 10^{{{int(np.log10(old['max']))}}}\text{{; past 20 in Feb.\ 1929}}",
                    font_size=28, color=P_C),
            MathTex(rf"\text{{from 2000: at most }} {new['max']:.1f}", font_size=28, color=MART),
            wrapped_label(r"Theorem: a calibrated nonnegative test martingale reaches 20 with probability at most 5\%. "
                          r"These retrospective scores need additional modeling checks (chapter 15).", 5.2, 20, QC.LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        for m_ in side:
            if m_.width > 5.4:
                m_.scale_to_fit_width(5.4)
        side.to_corner(UR, buff=0.4)
        src = real_data(r"Kenneth French's daily US market, 1926--2020; bets sized by the House's e-process (chapter 15)",
                        corner=DL)
        tk = ValueTracker(0.0)
        live0 = tracing(ax, t0, l0, tk, P_C, stroke_width=2.5)
        year = always_redraw(lambda: MathTex(rf"{int(at_index(t0, tk))}", font_size=40, color=P_C).next_to(
            ax.c2p(1926, 100), RIGHT, buff=0.2))
        head = always_redraw(lambda: glow_dot(ax.c2p(at_index(t0, tk), at_index(l0, tk)), color=P_C, radius=0.05))
        with self.voiceover(
            "Here is a historical betting score using yesterday's sign and transformed American market returns. "
            "<bookmark mark='a'/> A calibrated nonnegative test martingale has at most a five-percent chance of "
            "ever reaching twenty. This score uses estimated centering, clipping and a retrospective scale "
            "initialization; chapter fifteen checks why those choices matter. It crossed twenty in February "
            "1929 and eventually reached roughly ten to the hundredth. "
            "<bookmark mark='b'/> Start the same gambler in 2000, and the wealth wanders and never reaches twenty. "
            "<bookmark mark='c'/> The contrast motivates testing by betting. By the end you will know when its "
            "anytime guarantee applies, and when a historical score alone does not supply it."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(side[0]), Create(bar0))
            self.add(live0, year, head)
            self.play(tk.animate.set_value(float(i29)), run_time=3, rate_func=linear)
            self.play(FadeIn(dot29), Flash(dot29.get_center(), color=YELLOW))
            vo.wait_until("a")
            self.play(FadeIn(side[3]))
            self.play(tk.animate.set_value(float(len(t0) - 1)), run_time=4, rate_func=linear)
            live0.clear_updaters()
            year.clear_updaters()
            head.clear_updaters()
            self.play(FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(g2), Create(bar), FadeIn(barl))
            self.play(Create(line1), FadeIn(side[2]), run_time=2)
            vo.wait_until("c")
        self.wait(0.4)
        self.clear_scene()

    def points(self):
        # the problem of points: first to 3 wins 64 pistoles; A leads 2-1 (Pascal to Fermat, 29 July 1654)
        def node(txt, pos, col=GREY_B, r=0.42):
            c = Circle(radius=r, stroke_color=col, stroke_width=2.5, fill_color=BACKGROUND, fill_opacity=1).move_to(pos)
            return VGroup(c, MathTex(txt, font_size=26, color=col).move_to(pos))

        root = node(r"2{:}1", LEFT * 4.6 + UP * 0.3)
        a_win = node(r"3{:}1", LEFT * 1.6 + UP * 1.7, MART)
        tie = node(r"2{:}2", LEFT * 1.6 + DOWN * 1.1)
        a2 = node(r"3{:}2", RIGHT * 1.4 + UP * 0.1, MART)
        b2 = node(r"2{:}3", RIGHT * 1.4 + DOWN * 2.3, QC.LOSS)
        edges = VGroup(*[Line(a[0].get_center(), b[0].get_center(), buff=0.44, color=GREY_D, stroke_width=2)
                         for a, b in ((root, a_win), (root, tie), (tie, a2), (tie, b2))])
        half = VGroup(*[MathTex(r"\tfrac12", font_size=24, color=GREY_B).move_to(e.get_center() + UP * 0.25)
                        for e in edges])
        vals = {"aw": MathTex(r"64", font_size=34, color=MART).next_to(a_win, RIGHT, buff=0.2),
                "a2": MathTex(r"64", font_size=34, color=MART).next_to(a2, RIGHT, buff=0.2),
                "b2": MathTex(r"0", font_size=34, color=QC.LOSS).next_to(b2, RIGHT, buff=0.2),
                "tie": MathTex(r"\tfrac12 \cdot 64 + \tfrac12 \cdot 0 = 32", font_size=30, color=P_C).next_to(tie, DOWN, buff=0.2),
                "root": MathTex(r"\tfrac12 \cdot 64 + \tfrac12 \cdot 32 = 48", font_size=32, color=QC.IDEA).next_to(root, DOWN, buff=0.25)}
        tree = VGroup(edges, half, root, a_win, tie, a2, b2).shift(LEFT * 0.6 + DOWN * 0.2)
        for k in ("aw", "a2", "b2"):
            vals[k].shift(LEFT * 0.6 + DOWN * 0.2)
        vals["tie"].next_to(tie, DOWN, buff=0.2)
        vals["root"].next_to(root, DOWN, buff=0.25)
        head = label(r"The problem of points: first to 3 wins 64 pistoles; the game stops at 2--1", font_size=26,
                     color=GREY_A).to_edge(UP, buff=0.4)
        side = VGroup(
            label(r"A's fair share = the expected payout", font_size=22, color=GREY_A),
            MathTex(r"2{:}1 \;\to\; 48 : 16", font_size=34, color=QC.IDEA),
            MathTex(r"2{:}0 \;\to\; 64\,(1 - \tfrac18) = 56 : 8", font_size=34, color=QC.IDEA),
            wrapped_label(r"the value of an interrupted fair game is its conditional expectation; the sequence of values "
                          r"is a martingale (chapter 3)", 4.0, 20, MART),
            note(r"Pascal to Fermat, 29 July 1654", font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "The question is older than the stock market. In 1654 Blaise Pascal was asked how to split the stakes of "
            "a game stopped early: first to three points wins sixty-four pistoles, and A leads two to one. "
            "<bookmark mark='a'/> Reason backwards. If A wins the next point, A takes sixty-four. If B wins it, the "
            "next point decides, so that position is worth thirty-two. <bookmark mark='b'/> Averaging, A's fair share "
            "is forty-eight; from two to nothing, it is fifty-six. <bookmark mark='c'/> The fair value of an "
            "unfinished game is its expected payout given what has happened: a conditional expectation. Point by "
            "point, those values form a martingale."
        ) as vo:
            self.play(FadeIn(head), FadeIn(root), FadeIn(side[4]))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(e) for e in edges], lag_ratio=0.2), FadeIn(half),
                      FadeIn(VGroup(a_win, tie, a2, b2)))
            self.play(FadeIn(vals["aw"]), FadeIn(vals["a2"]), FadeIn(vals["b2"]))
            self.play(Write(vals["tie"]))
            vo.wait_until("b")
            self.play(Write(vals["root"]), FadeIn(side[:2]))
            self.play(FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]), Indicate(vals["root"], color=QC.IDEA))
        self.wait(0.4)
        self.clear_scene()

    def era(self):
        events = [(1654, r"Pascal and Fermat: the problem of points", QC.IDEA),
                  (1718, r"de Moivre: the gambler's ruin", QC.IDEA),
                  (1900, r"Bachelier: prices as a fair game", QC.IDEA),
                  (1933, r"Kolmogorov: the axioms", QC.IDEA),
                  (1939, r"Ville: martingales and betting", QC.IDEA),
                  (1945, r"Wald: sequential tests", QC.IDEA),
                  (1953, r"Doob: \textit{Stochastic Processes}", QC.IDEA),
                  (1965, r"Samuelson; Dubins--Savage", QC.IDEA),
                  (1981, r"Harrison--Pliska: pricing as a martingale", QC.IDEA),
                  (1995, r"Barings", QC.CRISIS),
                  (2001, r"Shafer--Vovk: probability as a game", QC.IDEA),
                  (2023, r"anytime-valid inference (Ramdas et al.)", QC.IDEA)]
        y0, y1 = 1640, 2030
        W = 12.4

        def X(y):
            return -W / 2 + W * (y - y0) / (y1 - y0)

        line = Line([X(y0), 0, 0], [X(y1), 0, 0], color=GREY_D, stroke_width=2).shift(DOWN * 0.2)
        ticks = VGroup(*[VGroup(Line([X(y), -0.26, 0], [X(y), -0.14, 0], color=GREY_D),
                                Text(str(y), font_size=14, color=GREY_D).move_to([X(y), -0.48, 0]))
                         for y in (1650, 1700, 1750, 1800, 1850, 1900, 1950, 2000)])
        dots, labs, leads = VGroup(), VGroup(), VGroup()
        tiers = [0.55, -0.95, 1.05, -1.45, 1.55, -1.95, 2.05, -2.45, 2.55, 3.0]  # the last two keep the 2000s apart
        used = {k: [] for k in range(len(tiers))}
        for i, (yr, name, col) in enumerate(events):
            d = Dot([X(yr), -0.2, 0], radius=0.07, color=col)
            dots.add(d)
            t = label(rf"{yr}\; {name}", font_size=17, color=col)
            for k, y in enumerate(tiers):
                t.move_to([X(yr), y - 0.2, 0])
                keep_in_frame(t, margin=0.3)
                a, b = t.get_left()[0], t.get_right()[0]
                if all(b + 0.2 < u or a - 0.2 > v for u, v in used[k]):
                    used[k].append((a, b))
                    break
            labs.add(t)
            up = t.get_y() > d.get_y()
            leads.add(Line(d.get_center(), [X(yr), t.get_bottom()[1] if up else t.get_top()[1], 0], color=col,
                           stroke_width=1, stroke_opacity=0.5))
        title = label(r"How we got here", font_size=36).to_edge(UP, buff=0.5)
        cap = wrapped_label(r"three centuries of one idea: a fair game, its value as information arrives, and what no "
                            r"strategy can do to it", 11.0, 22, GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "From Pascal the idea runs through de Moivre's gambler's ruin and Bachelier's fair prices. "
            "<bookmark mark='a'/> Kolmogorov gave probability its axioms in 1933, Ville named the martingale in "
            "1939, Wald tested sequentially, and Doob wrote the theory. <bookmark mark='b'/> Samuelson, Harrison and "
            "Pliska made prices martingales. <bookmark mark='c'/> Barings showed what doubling does to a bank, and "
            "Shafer, Vovk and Ramdas turned Ville's betting into tests valid at any time."
        ) as vo:
            self.play(FadeIn(title), Create(line), FadeIn(ticks), FadeIn(cap))
            groups = [(0, 3, "a"), (3, 7, "b"), (7, 9, "c"), (9, 12, None)]
            for a, b, mark in groups:
                self.play(LaggedStart(*[AnimationGroup(GrowFromCenter(dots[i]), Create(leads[i]),
                                                       FadeIn(labs[i], shift=UP * 0.1))
                                        for i in range(a, b)], lag_ratio=0.5), run_time=2.4)
                if mark:
                    vo.wait_until(mark)
        self.wait(0.4)
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Information: $\sigma$-algebras, filtrations; conditional expectation as a projection (ch.\ 1--2)",
            r"Martingales; the martingale transform: no system beats a fair game (ch.\ 3--4)",
            r"Stopping times, optional stopping proved, pattern waits; doubling, admissibility, Barings (ch.\ 5--8)",
            r"Gambler's ruin and bold play; martingale convergence: upcrossings, P\'olya, L\'evy (ch.\ 9--10)",
            r"Doob's decomposition; change of measure, Esscher, Radon--Nikodym, Kakutani (ch.\ 11--13)",
            r"Heavy tails as stable laws: the characteristic function, a fit replayed (ch.\ 14)",
            r"Ville's inequality, testing by betting, learning the bet, confidence sequences (ch.\ 15--16)",
            r"Casinos, bookmakers, prediction markets; the 2023--2026 frontier, e-BH (ch.\ 17--18)",
        ], color=QC.IDEA, font_size=23)
        with self.voiceover(
            "The plan, in eighteen chapters: information and projection; martingales and why no system beats them; "
            "stopping, doubling and Barings; ruin and convergence; Doob, the change of measure and Radon-Nikodym; "
            "stable laws; testing and learning to bet; and the industry and the frontier."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows],
                                                     lag_ratio=0.5, run_time=10))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("data",))
        with self.voiceover(
            "In the House, this part adds a monitor to the data desk: an e-process for "
            "a specified bounded-outcome model over time, with a false-alarm guarantee when its null is correctly "
            "calibrated. <bookmark mark='a'/> The "
            "research desk will inherit it, when it starts testing hundreds of ideas at once."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["data"], color=QC.HOUSE, scale_factor=1.05))
            vo.wait_until("a")
            self.play(Indicate(chart.desk["research"], color=QC.HOUSE, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()
