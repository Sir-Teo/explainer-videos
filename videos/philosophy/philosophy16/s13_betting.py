from __future__ import annotations

import math

from videos.philosophy.philosophy16.common import *  # noqa: F403


class Betting(VoiceoverScene):
    def construct(self):
        card = chapter_card(12, r"Testing by betting", r"Is evidence what you win?", lit=(1939, 2019), part=PART)
        with self.voiceover("Chapter twelve. Testing by betting."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.idea()
        self.wealth()
        self.kelly()
        self.ville()
        self.why()

    def idea(self):
        hc = history_card(2019, r"Glenn Shafer \ and Vladimir Vovk", r"\textit{Game-Theoretic Foundations for "
                          r"Probability and Finance}", width=7.6, color=HIST).to_corner(UL, buff=0.35)
        rows = stack([
            (r"the null hypothesis sets prices: \ it says which bets are fair", NULLC),
            (r"a skeptic starts with \$1 \ and bets against it, \ round by round", FISH),
            (r"if the null is right, \ the skeptic cannot expect to gain", WHITE),
            (r"so a large fortune is evidence against the null", GOAL),
        ], font_size=24, aligned_edge=LEFT, buff=0.35).next_to(hc, DOWN, buff=0.45).set_x(0)
        eq = MathTex(r"E \ge 0,\quad \mathbb{E}_{H_0}[E] \le 1 \ \ \Longrightarrow\ \ P_{H_0}(E \ge 1/\alpha) \le \alpha",
                     font_size=32, color=ALTC).next_to(rows, DOWN, buff=0.45)
        el = label(r"an \textit{e-value}: \ the payoff of a fair bet; \ Markov's inequality does the rest",
                   font_size=20, color=GREY_A).next_to(eq, DOWN, buff=0.15)
        with self.voiceover(
            "The newest idea in the field is also one of the oldest in probability. Glenn Shafer and Vladimir Vovk "
            "rebuilt probability itself as a game. <bookmark mark='a'/>A null hypothesis sets prices: it says which "
            "bets are fair. <bookmark mark='b'/>A skeptic starts with one dollar and bets against it, round by round, "
            "at those prices. <bookmark mark='c'/>If the null is right, the skeptic cannot expect to gain. "
            "<bookmark mark='d'/>So a large fortune is evidence against the null. <bookmark mark='e'/>The payoff of "
            "such a bet is called an e-value: a nonnegative number whose expectation under the null is at most one. "
            "By Markov's inequality, the chance under the null that it reaches one over alpha is at most alpha."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("e")
            self.play(Write(eq), FadeIn(el))
        self.clear_scene()

    def wealth(self):
        d = load("betting")
        head = label(r"Betting on a coin: \ stake " + f"{d['lam']:g}" + r" of your wealth on heads, \ each toss",
                     font_size=28, color=CONN).to_edge(UP, buff=0.3)
        eq = MathTex(r"W_t = \prod_{s \le t} \big(1 + \lambda (2X_s - 1)\big)", font_size=32, color=FISH).next_to(
            head, DOWN, buff=0.25)
        n = d["n"]
        xs = list(range(0, n, 2))
        ax = Axes(x_range=[0, n, 100], y_range=[-4.5, 2, 1], x_length=8.4, y_length=3.6, tips=False,
                  axis_config={"color": GREY_C, "include_numbers": False}).move_to([-1.4, -1.3, 0])
        yt = VGroup(*[label(t, font_size=15, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1) for t, v in
                      ((r"$10^{-4}$", -4), (r"0.01", -2), (r"1", 0), (r"100", 2))])
        xt = VGroup(*[label(str(v), font_size=15, color=GREY_B).next_to(ax.c2p(v, -4.5), DOWN, buff=0.1)
                      for v in (100, 200, 300, 400)])
        xl = label(r"tosses", font_size=18, color=GREY_B).next_to(xt, DOWN, buff=0.1)
        alt = series_plot(ax, [math.log10(v) for v in d["alt_path"]], ALTC, xs=xs[:len(d["alt_path"])], width=3)
        null = series_plot(ax, [math.log10(v) for v in d["null_path"]], NULLC, xs=xs[:len(d["null_path"])], width=3)
        twenty = DashedLine(ax.c2p(0, math.log10(20)), ax.c2p(n, math.log10(20)), color=GOAL, stroke_width=2)
        tl = label(r"\$20: \ reject at $\alpha = 0.05$", font_size=17, color=GOAL).next_to(twenty, UP, buff=0.05).align_to(
            twenty, RIGHT)
        side = stack([(r"fair coin: \ wealth drifts down", NULLC),
                      (r"heads 60\%: \ wealth grows", ALTC),
                      (f"{100 * d['alt_reach_20']:.0f}" + r"\% \ reach \$20 within " + str(n) + r" tosses; \ median "
                       + f"{d['median_time_to_20']:.0f}", ALTC)], font_size=20, aligned_edge=LEFT, width=3.8).move_to(
            [5.0, -0.9, 0])
        with self.voiceover(
            "Here is a test by betting. <bookmark mark='a'/>To test whether a coin is fair, stake a fifth of your "
            "current wealth on heads at even odds, every toss. Your wealth is the product of the factors. "
            "<bookmark mark='b'/>If the coin is fair, the bet is fair, and on this logarithmic scale wealth drifts "
            "downward. <bookmark mark='c'/>If the coin lands heads sixty percent of the time, wealth grows "
            "exponentially. <bookmark mark='d'/>Reaching twenty dollars is evidence at the five percent level. "
            "Ninety-six percent of biased-coin runs get there within four hundred tosses, in a median of about a "
            "hundred and ten."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(eq), FadeIn(ax), FadeIn(yt), FadeIn(xt), FadeIn(xl))
            vo.wait_until("b")
            self.play(Create(null), FadeIn(side[0]), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(alt), FadeIn(side[1]), run_time=2.5)
            vo.wait_until("d")
            self.play(Create(twenty), FadeIn(tl), FadeIn(side[2]))
        self.clear_scene()

    def kelly(self):
        head = label(r"How much to stake? \ Kelly's growth rate", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        eq = MathTex(r"g(\lambda) = p \ln(1 + \lambda) + (1 - p) \ln(1 - \lambda), \qquad \lambda^* = 2p - 1",
                     font_size=32, color=FISH).next_to(head, DOWN, buff=0.3)
        ax = Axes(x_range=[0, 0.6, 0.2], y_range=[-0.25, 0.05, 0.05], x_length=7.4, y_length=3.6, tips=False,
                  axis_config={"color": GREY_C, "include_numbers": True, "font_size": 16}).move_to([-2.0, -1.2, 0])
        xl = label(r"stake $\lambda$", font_size=18, color=GREY_B).next_to(ax.x_axis, DOWN, buff=0.3)
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(0.6, 0), color=GREY_B, stroke_width=1.5)
        curves = VGroup()
        legend = VGroup()
        for p, c in ((0.6, ALTC), (0.55, FISH), (0.5, NULLC)):
            curves.add(ax.plot(lambda l, p=p: p * math.log(1 + l) + (1 - p) * math.log(1 - l), x_range=[0, 0.6],
                               color=c, stroke_width=4))
            legend.add(VGroup(Line(ORIGIN, RIGHT * 0.35, color=c, stroke_width=4),
                              label(rf"heads {round(100 * p)}\%", font_size=18, color=c)).arrange(RIGHT, buff=0.1))
        legend.arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(ax, UP, buff=0.05).align_to(ax, RIGHT)
        star = Star(n=5, outer_radius=0.13, color=GOAL, fill_opacity=1).move_to(
            ax.c2p(0.2, 0.6 * math.log(1.2) + 0.4 * math.log(0.8)))
        side = stack([(r"our stake, \ 0.2, \ is Kelly-optimal for 60\% heads", GOAL),
                      (r"under the null, \ every stake loses growth", NULLC),
                      (r"over-betting is ruinous: \ $g < 0$ past $\lambda \approx 0.39$", BAD),
                      (r"Kelly \ (1956); \ the GROW criterion for e-values \ (Grünwald et al.)", HIST)], font_size=20,
                     aligned_edge=LEFT, width=4.6).move_to([4.6, -0.8, 0])
        with self.voiceover(
            "How much should the skeptic stake? <bookmark mark='a'/>John Kelly answered in 1956, for a gambler with "
            "inside information: maximize the expected growth rate of log wealth. For even-odds bets on heads with "
            "probability p, the best stake is two p minus one. <bookmark mark='b'/>Plot the growth rate against the "
            "stake. If heads come sixty percent of the time, growth peaks at a stake of point two, exactly the one "
            "we used. <bookmark mark='c'/>If the coin is fair, every stake loses growth, which is why the null "
            "cannot be beaten on average. <bookmark mark='d'/>And over-betting is ruinous: beyond about point three "
            "nine, even a sixty-percent coin shrinks your wealth. Choosing e-values to maximize growth under the "
            "alternative is now a design principle, called GROW by Peter Grünwald and his colleagues."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(eq))
            vo.wait_until("b")
            self.play(FadeIn(ax), FadeIn(xl), Create(zero), Create(curves[0]), FadeIn(legend[0]))
            self.play(FadeIn(star, scale=1.5), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(Create(curves[1]), FadeIn(legend[1]), Create(curves[2]), FadeIn(legend[2]), FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
        self.clear_scene()

    def ville(self):
        d = load("betting")
        hc = history_card(1939, r"Jean Ville", r"\textit{Étude critique de la notion de collectif}", width=6.6,
                          color=HIST).to_corner(UL, buff=0.3)
        thm = MathTex(r"W \text{ a nonnegative martingale under } H_0,\ W_0 = 1:\qquad P_{H_0}\Big(\sup_t W_t \ge c\Big) "
                      r"\le \frac{1}{c}", font_size=30, color=GOAL).next_to(hc, DOWN, buff=0.35).set_x(0)
        proof = stack([(r"let $\tau$ be the first time $W_t \ge c$ \ (or the horizon); \ by optional stopping, "
                        r"$\mathbb{E}[W_\tau] = 1$", WHITE),
                       (r"and $W_\tau \ge c$ whenever the sup reaches $c$: \ so $1 \ge c \cdot P(\sup_t W_t \ge c)$ \ "
                        r"$\square$", WHITE)], font_size=21).next_to(thm, DOWN, buff=0.3)
        hd = [r"c", r"\text{bound } 1/c", r"\text{simulated}"]
        rows = [[MathTex(f"{1 / float(a):g}", font_size=24), MathTex(f"{float(a):g}", font_size=24),
                 MathTex(f"{v:.3f}", font_size=24, color=OK)] for a, v in d["ville"].items()]
        grid = ValueGrid(hd, rows, col_w=[1.6, 2.4, 2.4], cell_h=0.48, font_size=22).next_to(proof, DOWN, buff=0.3)
        gl = label(f"{d['runs']:,}".replace(",", "{,}") + r" fair-coin runs: \ how often wealth \textit{ever} reached "
                   r"$c$", font_size=18, color=GREY_B).next_to(grid, DOWN, buff=0.12)
        with self.voiceover(
            "The guarantee holds at every moment at once. Jean Ville proved it in 1939, in the thesis that "
            "introduced the word martingale into probability. <bookmark mark='a'/>If wealth is a nonnegative "
            "martingale under the null, starting at one, the chance that it ever reaches c is at most one over c. "
            "<bookmark mark='b'/>The proof takes two lines. Stop the first time wealth reaches c. A fair game "
            "stopped at any such time still has expected value one. <bookmark mark='c'/>And on the event that "
            "wealth ever reached c, the stopped wealth is at least c. So one is at least c times that probability. "
            "<bookmark mark='d'/>The Reasoner checks it on four thousand fair-coin runs: wealth ever reached five "
            "in eighteen percent, under the bound of twenty; ever reached a hundred in six tenths of a percent, "
            "under the bound of one."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Write(thm))
            vo.wait_until("b")
            self.play(FadeIn(proof[0]))
            vo.wait_until("c")
            self.play(FadeIn(proof[1]))
            vo.wait_until("d")
            self.play(FadeIn(grid.head), Create(grid.rule), *[FadeIn(c) for r in grid.cell for c in r], FadeIn(gl))
        self.clear_scene()

    def why(self):
        head = label(r"Why betting is the right frame", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"anytime-valid", r"look as often as you like, \ stop when you like: \ Chapters 5 and 11, \ solved", OK),
            (r"optional continuation", r"a promising study can be extended: \ multiply the e-values", ALTC),
            (r"meta-analysis", r"independent studies' e-values multiply; \ $p$-values do not", FISH),
            (r"likelihood ratios", r"are e-values: \ Royall's bound in Chapter 5 was Ville's inequality", BAYC),
            (r"the philosophy", r"evidence is what a skeptic could have won betting against the hypothesis "
                                r"\ (Shafer, \ 2021)", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.45, width=8.6, x_text=-2.4)
        src = label(r"Grünwald, \ de Heide and Koolen \ (2024); \ Ramdas, \ Grünwald, \ Vovk and Shafer \ (2023)",
                    font_size=19, color=HIST).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Why has this idea spread so quickly? <bookmark mark='a'/>Tests by betting are anytime-valid: look as "
            "often as you like and stop when you like, and the error guarantee holds. The problems of chapters five "
            "and eleven disappear. <bookmark mark='b'/>A promising study can be continued, and its e-values simply "
            "multiply. <bookmark mark='c'/>Independent studies combine the same way, which p-values never could. "
            "<bookmark mark='d'/>Likelihood ratios are themselves e-values, so Royall's bound in chapter five was "
            "Ville's inequality in disguise, and betting reconciles part of the likelihoodist's view with error "
            "control. <bookmark mark='e'/>Shafer proposes a philosophy to go with the mathematics: the evidence "
            "against a hypothesis is what a skeptic could have won by betting against it."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            self.play(FadeIn(src))
        self.clear_scene()
