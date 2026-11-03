from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant8.common import ALT, KELLY, OVER, PART, UNDER, VALUE, illustration, load, real_data


class LTCM(VoiceoverScene):
    def construct(self):
        self.card()
        self.fractional(load("fractional"))
        self.fuzzy(load("kelly_us"), load("edge_error"))
        self.file()
        self.leverage(load("ltcm"))

    def card(self):
        c = chapter_card(9, r"Fractional Kelly, estimation risk, and LTCM", r"What if your edge is smaller than you "
                         r"think?", lit=(1998,), part=PART)
        with self.voiceover("Chapter nine. Fractional Kelly, estimation risk, and Long-Term Capital Management."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def fractional(self, fr):
        rows = [cmath(r"g(cf^*) - r", r"=", r"c f^*(\mu - r) - \tfrac12 c^2 f^{*2}\sigma^2", font_size=32),
                cmath(r"g(cf^*) - r", r"=", r"(2c - c^2)\,\big(g(f^*) - r\big)", font_size=32,
                      colors={r"(2c - c^2)": KELLY}),
                cmath(r"\hat\mu - r = k(\mu - r)", r"\ \Rightarrow\ ", r"\hat f = c\,k\,f^*,\qquad g - r = (2ck - c^2k^2)"
                      r"\,\big(g(f^*) - r\big)", font_size=30)]
        whys = [why(r"bet $c$ times Kelly: substitute $f = c f^*$ into the growth parabola", font_size=21),
                why(r"use $f^*\sigma^2 = \mu - r$: the same curve for every asset. $c = \frac12$ keeps 75\% of the growth "
                    r"at half the volatility; $c = 2$ earns nothing", font_size=21),
                why(r"overestimate the edge $k$-fold: you bet $ck$ times true Kelly. Full Kelly earns nothing at $k = 2$, "
                    r"half Kelly at $k = 4$", font_size=21)]
        step = ladder(self, rows, whys, keep=3, top=3.1, x=-0.4, buff=0.85, edge=6.9)
        m = fr["by_mult"]
        quote = VGroup(
            label(r"``If one overestimates the advantage by more than a factor of two, Kelly betting will cause a "
                  r"negative rate of capital growth.''", font_size=21, color=VALUE),
            label(r"--- William Benter (1994), on the Hong Kong racing syndicate he ran", font_size=18, color=GREY_B),
        ).arrange(DOWN, aligned_edge=RIGHT, buff=0.1).to_edge(DOWN, buff=0.5)
        if quote.width > 13.0:
            quote.scale_to_fit_width(13.0)
        with self.voiceover(
            "Practitioners rarely bet full Kelly. Bet c times Kelly and substitute: <bookmark mark='a'/> the excess growth "
            "is two c minus c squared times Kelly's, for every asset. Half Kelly keeps three quarters of the growth at half "
            f"the volatility, and halves wealth from a peak within ten years {100 * m['0.5']['p_dd50']:.0f} percent of the "
            f"time, against {100 * m['1.0']['p_dd50']:.0f} for full Kelly. <bookmark mark='b'/> The deeper reason: overestimate "
            "the edge k-fold and full Kelly on the estimate is k times Kelly on the truth; at two, it earns nothing. "
            "<bookmark mark='c'/> William Benter, who ran a Hong Kong racing syndicate, wrote exactly that in 1994, and bet a "
            "half or a third of Kelly."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            self.play(FadeIn(quote))
        self.wait(0.4)
        self.clear_scene()

    def fuzzy(self, k, e):
        f, gr = np.asarray(k["f"]), np.asarray(k["growth"])
        ok = np.isfinite(gr) & (gr > -0.06)
        g = axes([0, 4], [-0.06, 0.14], x_length=6.2, y_length=3.6, xlabel=r"fraction in US stocks",
                 ylabel=r"realized growth, 1926--2020", xticks=[0, 1, 2, 3, 4], xfmt=lambda u: f"{100 * u:.0f}\\%",
                 yticks=[0, 0.05, 0.1], yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=16).to_corner(UL, buff=0.5)
        ax = g.ax
        line = curve(ax, f[ok], gr[ok], KELLY, stroke_width=4)
        bs = np.asarray(k["best_bs"])
        rng = np.random.default_rng(2)
        cloud = VGroup(*[Dot(ax.c2p(b, -0.045 + 0.02 * rng.random()), radius=0.03, color=ALT).set_opacity(0.5)
                         for b in bs])
        gat = lambda x: float(np.interp(x, f, gr))  # noqa: E731
        fullm = VGroup(*[Dot(ax.c2p(min(b, 4), gat(min(b, 4))), radius=0.035,
                             color=OVER if gat(b) < k["growth_at_best"] - 0.01 else KELLY).set_opacity(0.6)
                         for b in bs[::4]])
        halfm = VGroup(*[Dot(ax.c2p(b / 2, gat(b / 2)), radius=0.035,
                             color=OVER if gat(b / 2) < k["growth_at_best"] - 0.01 else UNDER).set_opacity(0.6)
                         for b in bs[::4]])
        ks = np.asarray(e["ks"])
        g2 = axes([0.5, 4.5], [-1.5, 1.1], x_length=5.6, y_length=3.4, xlabel=r"overestimate of the edge, $k$",
                  ylabel=r"excess growth, share of true Kelly's", xticks=[1, 2, 3, 4], yticks=[-1, 0, 1],
                  yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=16).to_corner(UR, buff=0.5)
        a2 = g2.ax
        zero = DashedLine(a2.c2p(0.5, 0), a2.c2p(4.5, 0), color=GREY_C, stroke_width=1.5)
        fl = curve(a2, ks, np.clip(np.asarray(e["full"]), -1.5, 1.1), OVER, stroke_width=4)
        hl = curve(a2, ks, np.clip(np.asarray(e["half"]), -1.5, 1.1), UNDER, stroke_width=4)
        mc = VGroup(*[VGroup(Dot(a2.c2p(r_["k"], max(r_["c1"], -1.5)), color=WHITE, radius=0.05),
                             Dot(a2.c2p(r_["k"], max(r_["c0.5"], -1.5)), color=WHITE, radius=0.05)) for r_ in e["mc"]])
        leg = legend([(OVER, r"full Kelly on the estimate"), (UNDER, r"half Kelly on the estimate"),
                      (WHITE, r"2{,}000 simulated 30-year paths")], font_size=16).next_to(g2, DOWN, buff=0.3).align_to(
            g2, LEFT)
        split = VGroup(
            label(r"the House's registered test: choose on 1926--1972, invest 1973--2020", font_size=20, color=GREY_A),
            MathTex(rf"\text{{chosen }}{100 * k['split_f1']:.0f}\%\to {100 * k['split_g2_at_f1']:.1f}\%,\ \ "
                    rf"\text{{half of it}}\to {100 * k['split_g2_at_half']:.1f}\%", font_size=24),
            MathTex(rf"\text{{hindsight best }}{100 * k['split_f2']:.0f}\%\to{100 * k['split_g2_best']:.1f}\%",
                    font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(g, DOWN, buff=0.5).align_to(g, LEFT)
        q = pause_card(r"You estimate a Sharpe ratio of 1; the truth is 0.5. Full or half Kelly on your estimate?",
                       width=5.6, font_size=20).next_to(leg, DOWN, buff=0.3).align_to(g2, LEFT)
        src = real_data(r"Kenneth French, monthly 1926--2020; 400 block-bootstrap histories", corner=DL)
        with self.voiceover(
            "On real data: resample US history in one-year blocks four hundred times and find each best fraction. Ninety "
            f"percent lie between {100 * k['bs_p05']:.0f} and {100 * k['bs_p95']:.0f} percent. <bookmark mark='a'/> Bet full "
            "Kelly on each estimate and score it on actual history: many land on the steep side, in red. Half of each "
            "estimate stays on the flat top. <bookmark mark='b'/> In general, full Kelly's excess growth hits zero at k "
            "equals two, half Kelly's at four, and simulated paths agree. Pause and predict: you estimate a Sharpe ratio of "
            "one; the truth is a half. Which grows faster? <bookmark mark='c'/> Half Kelly, which is exactly Kelly on the "
            "truth. <bookmark mark='d'/> History can be kind: the House's registered test chose "
            f"{100 * k['split_f1']:.0f} percent on 1926 to 1972, and it grew at {100 * k['split_g2_at_f1']:.1f} percent a "
            "year afterwards."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(line))
            self.play(LaggedStart(*[FadeIn(d_) for d_ in cloud], lag_ratio=0.005, run_time=2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in fullm], lag_ratio=0.01, run_time=1.5))
            self.play(FadeOut(fullm), LaggedStart(*[FadeIn(d_) for d_ in halfm], lag_ratio=0.01, run_time=1.5))
            vo.wait_until("b")
            self.play(FadeIn(g2), Create(zero), Create(fl), Create(hl), FadeIn(leg), run_time=2)
            self.play(FadeIn(mc), FadeIn(q))
            vo.wait_until("c")
            self.play(Indicate(hl, color=UNDER))
            vo.wait_until("d")
            self.play(FadeIn(split))
        self.wait(0.4)
        self.clear_scene()

    def file(self):
        card = crisis_card(
            r"17 August -- 23 September 1998", r"Long-Term Capital Management",
            r"A hedge fund founded in February 1994 by John Meriwether, with Robert Merton and Myron Scholes among its "
            r"partners, ran convergence trades: long the cheap bond, short the dear one, levered many times. At the end "
            r"of 1997 it had balance-sheet assets of \$129 billion on \$4.7 billion of capital, and derivatives with a "
            r"notional value of \$1.3 trillion. After Russia defaulted in August 1998, spreads widened instead of "
            r"converging, and the fund lost 44\% of its value that month. On 23 September fourteen banks and brokerage "
            r"firms, brought together by the New York Fed, put in \$3.6 billion for 90\% of the fund.",
            stats=[(r"28 : 1", r"assets to equity, end of 1997"), (r"\$1.3\text{tn}", r"derivatives, notional"),
                   (r"-44\%", r"August 1998")],
            width=11.0, font_size=25)
        card.move_to(ORIGIN)
        src = note(r"U.S. Treasury testimony (Gensler, 6 May 1999), presenting the President's Working Group's figures; "
                   r"Federal Reserve History, ``Near Failure of Long-Term Capital Management''", font_size=18,
                   color=GREY_B).to_corner(DR, buff=0.25)
        with self.voiceover(
            "The crisis file. Long-Term Capital Management was founded in February 1994 by the bond trader John "
            "Meriwether; Robert Merton and Myron Scholes, who shared the Nobel prize in 1997, were among its partners. It "
            "bought cheap bonds and sold similar dear ones, betting that the spread between them would close: small, steady "
            "profits, levered many times. At the end of 1997 it had balance-sheet assets of a hundred and twenty-nine billion "
            "dollars on four point seven billion of capital, twenty-eight to one, and derivatives with a notional value of "
            "one point three trillion. In August 1998 Russia defaulted, investors fled to safety, and the spreads widened "
            "instead of closing: the fund lost forty-four percent of its value in that month alone. On September the "
            "twenty-third, fourteen banks and brokerage firms, brought together by the Federal Reserve Bank of New York, put "
            "in three point six billion dollars and took ninety percent of the fund."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(src))
        self.wait(0.5)
        self.clear_scene()

    def leverage(self, l_):
        g = axes([1, 3], [0, 110], x_length=6.4, y_length=4.4, xlabel=r"volatility, as a multiple of the calm level",
                 ylabel=r"Kelly leverage $= (\mu - r)/\sigma^2$", xticks=[1, 1.5, 2, 2.5, 3], yticks=[0, 28, 50, 100],
                 font_size=17).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        m = np.linspace(1, 3, 101)
        kel = l_["kelly_before"] / m ** 2
        kl = curve(ax, m, kel, KELLY, stroke_width=4)
        lt = DashedLine(ax.c2p(1, 28), ax.c2p(3, 28), color=OVER, stroke_width=2.5)
        ltl = label(r"28 : 1", font_size=20, color=OVER).next_to(ax.c2p(3, 28), UP, buff=0.08)
        m2 = 2 * kel <= 110  # twice Kelly only where it is inside the axes
        two = curve(ax, m[m2], 2 * kel[m2], OVER, stroke_width=1.5).set_stroke(opacity=0.5)
        tk = ValueTracker(1.0)
        dot = always_redraw(lambda: Dot(ax.c2p(tk.get_value(), l_["kelly_before"] / tk.get_value() ** 2), color=KELLY,
                                        radius=0.09))
        cross = float(np.sqrt(l_["kelly_before"] / 28))
        side = VGroup(
            wrapped_label(r"an illustrative convergence trade: 1\% a year over funding, 1\% volatility, unlevered", 4.4,
                          20, GREY_A),
            MathTex(rf"\text{{calm: Kelly}} = {l_['kelly_before']:.0f};\ \ 28 = {28 / l_['kelly_before']:.2f}\times"
                    r"\text{Kelly}", font_size=28, color=UNDER),
            MathTex(rf"\sigma\times 3:\ \text{{Kelly}} = {l_['kelly_after']:.0f};\ \ 28 = {28 / l_['kelly_after']:.1f}"
                    r"\times\text{Kelly}", font_size=28, color=OVER),
            MathTex(rf"\text{{growth at 28: }}{100 * l_['g28_before']:+.0f}\% \to {100 * l_['g28_after']:+.0f}\%",
                    font_size=28),
            wrapped_label(r"faint line: twice Kelly, where growth is zero. Leverage sized in calm markets is far "
                          r"beyond it in a storm. The full story, with funding and fire sales: Part 41.", 4.4, 19,
                          GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4)
        src = illustration(r"illustration: an assumed trade, not LTCM's books")
        with self.voiceover(
            "Why so dangerous? An illustration, not the fund's books: a trade earning one percent a year with one percent "
            f"volatility has a Kelly leverage of {l_['kelly_before']:.0f}, so twenty-eight to one looks cautious. "
            "<bookmark mark='a'/> But Kelly leverage falls with the square of volatility. At "
            f"{cross:.1f} times the calm volatility, twenty-eight is full Kelly; at three times, it is "
            f"{28 / l_['kelly_after']:.1f} times Kelly, past the line where growth is zero. <bookmark mark='b'/> Sizing is "
            "only as good as the volatility forecast."
            " Kelly has a famous critic. Next: Samuelson's objection."
        ) as vo:
            self.play(FadeIn(g), Create(lt), FadeIn(ltl), FadeIn(side[0]), FadeIn(side[1]), FadeIn(src))
            self.add(dot)
            self.play(Create(kl))
            vo.wait_until("a")
            self.play(tk.animate.set_value(3.0), Create(two), run_time=4)
            self.play(FadeIn(side[2]), FadeIn(side[3]))
            vo.wait_until("b")
            self.play(FadeIn(side[4]))
        dot.clear_updaters()
        self.wait(0.4)
        self.clear_scene()
