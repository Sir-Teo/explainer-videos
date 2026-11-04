from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant24.common import BAD, GOOD, HML, MKT, PART, SMB, ask, fit_right, illustration, load


class SizeValue(VoiceoverScene):
    def construct(self):
        sv = load("sizevalue")
        self.card()
        self.anomalies()
        self.construct_sort(load("construct"))
        self.history(sv)
        self.discovery(sv)
        self.decades(sv)
        self.why()

    def card(self):
        c = chapter_card(2, r"Size, value, and three factors", r"Why should small, cheap stocks earn more?",
                         lit=(1981, 1992), part=PART)
        with self.voiceover("Chapter two. The first two factors: size and value, and the three-factor model built from "
                            "them."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def anomalies(self):
        cards = VGroup(
            desk_question(r"Basu (1977): price to earnings", r"stocks with low prices relative to earnings beat the CAPM's "
                          r"prediction; high-P/E stocks lagged it", width=12.0, font_size=20),
            desk_question(r"Banz (1981): size", r"small companies earned more than their betas justified, most of it in "
                          r"the very smallest", width=12.0, font_size=20),
            desk_question(r"Rosenberg, Reid and Lanstein (1985): book to market", r"stocks cheap relative to their "
                          r"accounting book value beat expensive ones: 'persuasive evidence of market inefficiency'",
                          width=12.0, font_size=20),
            desk_question(r"Fama and French (1992, 1993)", r"in one cross-sectional regression, size and book-to-market "
                          r"absorb earnings yield, leverage and beta itself; then two portfolios, SMB and HML, become "
                          r"factors", width=12.0, font_size=20),
        ).arrange(DOWN, buff=0.22)
        if cards.height > 6.8:
            cards.scale_to_fit_height(6.8)
        with self.voiceover(
            "Size and value began as anomalies, failures of the CAPM. <bookmark mark='a'/> Sanjoy Basu found in 1977 "
            "that stocks cheap relative to their earnings beat their betas. <bookmark mark='b'/> Rolf Banz found in "
            "1981 that small companies did, most of all the very smallest. <bookmark mark='c'/> Barr Rosenberg and "
            "colleagues found in 1985 that stocks cheap relative to their book value beat expensive ones, and titled "
            "the paper persuasive evidence of market inefficiency. <bookmark mark='d'/> Then Eugene Fama and Kenneth "
            "French showed in 1992 that size and book-to-market together absorb the others, and beta too, and in 1993 "
            "turned them into two portfolios to stand beside the market as factors."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def construct_sort(self, k):
        size, bm, nyse = np.log10(np.asarray(k["size"])), np.log10(np.asarray(k["bm"])), np.asarray(k["nyse"], bool)
        med, lo, hi = (np.log10(v) for v in k["breaks"])
        g = axes([-1.6, 1.6], [-1.4, 0.7], x_length=6.4, y_length=4.4, xlabel=r"size, $\log_{10}$ market value",
                 ylabel=r"$\log_{10}$ book-to-market", xticks=[-1, 0, 1], yticks=[-1, -0.5, 0, 0.5],
                 font_size=13).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(x, y), radius=0.06 if n else 0.045, color=WHITE if n else GREY_B,
                            fill_opacity=1 if n else 0.6) for x, y, n in zip(size, bm, nyse)])
        vline = DashedLine(ax.c2p(med, -1.4), ax.c2p(med, 0.7), color=SMB, stroke_width=2)
        h1 = DashedLine(ax.c2p(-1.6, lo), ax.c2p(1.6, lo), color=HML, stroke_width=2)
        h2 = DashedLine(ax.c2p(-1.6, hi), ax.c2p(1.6, hi), color=HML, stroke_width=2)
        P = np.asarray(k["P"])
        names = [["SL", "SM", "SH"], ["BL", "BM", "BH"]]
        cells = VGroup()
        for i in range(2):
            for j in range(3):
                cells.add(MathTex(rf"\text{{{names[i][j]}}}\ {100 * P[i, j]:+.1f}\%", font_size=20))
        side = VGroup(
            legend([(WHITE, r"NYSE stocks: set the breakpoints"), (GREY_B, r"all others")], font_size=15),
            cells.arrange_in_grid(rows=2, cols=3, buff=(0.25, 0.2)),
            MathTex(r"SMB = \tfrac13(SL + SM + SH) - \tfrac13(BL + BM + BH)", font_size=22, color=SMB),
            MathTex(r"HML = \tfrac12(SH + BH) - \tfrac12(SL + BL)", font_size=22, color=HML),
            MathTex(rf"SMB = {100 * k['smb']:+.1f}\%,\quad HML = {100 * k['hml']:+.1f}\%", font_size=24),
            wrapped_label(r"forty made-up stocks, one month's returns; each portfolio value-weighted. Rebalanced each June",
                          3.8, 15, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "How the factors are built, on forty made-up stocks. Each June, plot every stock's size against its "
            "book-to-market. <bookmark mark='a'/> Split by size at the median of the New York Stock Exchange's stocks "
            "only, so that thousands of tiny Nasdaq firms do not set the line. <bookmark mark='b'/> Split by "
            "book-to-market at the exchange's thirtieth and seventieth percentiles. Six portfolios, each "
            "value-weighted. <bookmark mark='c'/> Size is the average of the three small portfolios less the average of "
            "the three big ones. Value is the average of the two cheap portfolios less the two expensive ones. Each "
            "factor is balanced on the other characteristic, so size is not secretly value, and value not secretly "
            "size."
        ) as vo:
            self.play(FadeIn(g), LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.02), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(vline))
            vo.wait_until("b")
            self.play(Create(h1), Create(h2), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), FadeIn(side[3]), FadeIn(side[4]), FadeIn(side[5]))
        self.add(illustration(r"the House's \texttt{factors.two\_by\_three} on toy data"))
        self.wait(0.4)
        self.clear_scene()

    def history(self, sv):
        d = np.asarray(sv["date"])
        t = d // 100 + (d % 100 - 0.5) / 12
        g = axes([1926, 2021], [-0.3, 1.8], x_length=8.2, y_length=4.4, xlabel=r"year", ylabel=r"\$1 in 1926, $\log_{10}$",
                 xticks=[1930, 1950, 1970, 1990, 2010], yticks=[0, 0.5, 1.0, 1.5], font_size=14).to_edge(
            LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        ls = curve(ax, t, np.log10(np.asarray(sv["smb_cum"])), SMB, stroke_width=2.4)
        lh = curve(ax, t, np.log10(np.asarray(sv["hml_cum"])), HML, stroke_width=2.4)
        f = sv["full"]
        side = VGroup(
            legend([(SMB, r"SMB, small minus big"), (HML, r"HML, value minus growth")], font_size=17),
            MathTex(rf"SMB:\ {100 * f['SMB']['mean']:.1f}\%\ \text{{a year}},\ t = {f['SMB']['t']:.1f}", font_size=22,
                    color=SMB),
            MathTex(rf"HML:\ {100 * f['HML']['mean']:.1f}\%\ \text{{a year}},\ t = {f['HML']['t']:.1f}", font_size=22,
                    color=HML),
            wrapped_label(r"July 1926 to December 2020. Both are long--short, so a dollar in each means a dollar long and "
                          r"a dollar short, collateral in bills. Both have long flat stretches", 3.6, 16, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Here is each factor since 1926. <bookmark mark='a'/> Size earned about two and a half percent a year, with "
            "a t-statistic just above two. Value earned four, with a t of three. <bookmark mark='b'/> Look at the "
            "shapes, though: long climbs and long flat stretches. Size did most of its work before 1980, and value "
            "gave back a large part of its gains after 2007. A factor's average is a summary of a very uneven path."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(ls), Create(lh), FadeIn(side[1]), FadeIn(side[2]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(side[3]))
        self.add(illustration(r"Kenneth French's data library: the three factors since 1926"))
        self.wait(0.4)
        self.clear_scene()

    def discovery(self, sv):
        hx = [-4.0, -1.2, 1.6, 4.4]
        heads = [r"", r"1926--1980", r"1981--2020", r"January vs other months"]
        tab = VGroup(VGroup(*[label(h_, font_size=18, color=GREY_A).move_to([x, 2.2, 0]) for h_, x in zip(heads, hx)]))
        pre, post = sv["pre1981"], sv["post1981"]
        tab.add(VGroup(label(r"SMB", font_size=20, color=SMB).move_to([hx[0], 1.5, 0]),
                       MathTex(rf"{100 * pre['SMB']['mean']:.1f}\%\ (t={pre['SMB']['t']:.1f})", font_size=24).move_to([hx[1], 1.5, 0]),
                       MathTex(rf"{100 * post['SMB']['mean']:.1f}\%\ (t={post['SMB']['t']:.1f})", font_size=24, color=BAD).move_to([hx[2], 1.5, 0]),
                       MathTex(rf"{100 * sv['smb_jan']:.1f}\%\ \text{{vs}}\ {100 * sv['smb_rest']:.2f}\%\ \text{{a month}}",
                               font_size=22).move_to([hx[3], 1.5, 0])))
        tab.add(VGroup(label(r"HML", font_size=20, color=HML).move_to([hx[0], 0.8, 0]),
                       MathTex(rf"{100 * pre['HML']['mean']:.1f}\%\ (t={pre['HML']['t']:.1f})", font_size=24).move_to([hx[1], 0.8, 0]),
                       MathTex(rf"{100 * post['HML']['mean']:.1f}\%\ (t={post['HML']['t']:.1f})", font_size=24).move_to([hx[2], 0.8, 0]),
                       label(r"", font_size=20).move_to([hx[3], 0.8, 0])))
        foot = VGroup(
            wrapped_label(r"Banz published in 1981. In the forty years since, the size premium has averaged about 1\% a "
                          r"year and is statistically indistinguishable from zero; much of it, before and after, came in "
                          r"January. McLean and Pontiff (2016), 97 anomalies: returns 26\\% lower out of sample, 58\\% lower "
                          r"after publication",
                          12.0, 17, GREY_A),
        ).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Now split the history at the year size was published. <bookmark mark='a'/> Before 1981, small stocks beat "
            "big ones by about three and a half percent a year. In the forty years since, by one percent, with a "
            "t-statistic of about six tenths: nothing distinguishable from zero. Value halved too, to two and a half "
            "percent, though it stayed positive. <bookmark mark='b'/> And size has a calendar. In January, small stocks "
            "beat large ones by two percent a month on average; in the other eleven months, by almost nothing. "
            "<bookmark mark='c'/> David McLean and Jeffrey Pontiff found the same pattern across nearly a hundred "
            "anomalies: their returns were about a quarter lower out of sample, and more than half lower after publication. Some of what looked like a premium was "
            "a mispricing that publication corrected, and some was never there."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(FadeIn(tab[1][:3]), FadeIn(tab[2]))
            vo.wait_until("b")
            self.play(FadeIn(tab[1][3]))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def decades(self, sv):
        dec = sv["decades"]
        ys = sorted(dec, key=int)
        g = axes([-0.6, len(ys) - 0.4], [-0.04, 0.12], x_length=8.6, y_length=4.2, xlabel=r"", ylabel=r"\% a year",
                 xticks=[], yticks=[-0.04, 0, 0.04, 0.08, 0.12], font_size=13).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        bars = VGroup()
        for i, y in enumerate(ys):
            for off, k, col in ((-0.18, "SMB", SMB), (0.18, "HML", HML)):
                v = dec[y][k]
                y0, y1 = ax.c2p(0, 0)[1], ax.c2p(0, v)[1]
                bars.add(Rectangle(width=0.3, height=max(abs(y1 - y0), 0.01), stroke_width=0, fill_color=col,
                                   fill_opacity=0.85).move_to([ax.c2p(i + off, 0)[0], (y0 + y1) / 2, 0]))
        labs = VGroup(*[label(rf"{y}s", font_size=14, color=GREY_A).next_to(ax.c2p(i, -0.04), DOWN, buff=0.1)
                        for i, y in enumerate(ys)])
        side = VGroup(legend([(SMB, r"SMB"), (HML, r"HML")], font_size=17),
                      wrapped_label(r"average return in each decade. Size was negative in three of the last five decades; "
                                    r"value lost in the 2010s for the first time", 3.2, 16, GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Decade by decade. <bookmark mark='a'/> Size is erratic: large in the 1930s, the 1960s and 2000s, "
            "negative or flat in the 1950s, the 1980s, the 1990s and the 2010s. Value is steadier, positive in every "
            "decade until the 2010s, when it lost for a full ten years for the first time. Chapter eight measures that "
            "decade."
        ) as vo:
            self.play(FadeIn(g), FadeIn(labs), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.05), FadeIn(side[1]),
                      run_time=3)
        self.wait(0.4)
        self.clear_scene()

    def why(self):
        cards = VGroup(
            desk_question(r"risk: distress", r"Fama and French (1993, 1996): value firms are often in trouble, and HML "
                          r"loads on a distress risk the market beta misses", width=12.0, font_size=20),
            desk_question(r"error: extrapolation", r"Lakonishok, Shleifer and Vishny (1994): investors extrapolate past "
                          r"growth, overpay for glamour, and are surprised when growth reverts", width=12.0, font_size=20),
            desk_question(r"size, rescued?", r"Asness, Frazzini, Israel, Moskowitz and Pedersen (2018): controlling for "
                          r"quality ('junk'), the size premium reappears and is more stable", width=12.0, font_size=20),
        ).arrange(DOWN, buff=0.3)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        with self.voiceover(
            "Why should either pay? Part twenty-three's three reasons apply. <bookmark mark='a'/> Risk: Fama and "
            "French argued that cheap firms are often distressed, and value loads on a risk of hard times that the "
            "market beta misses. <bookmark mark='b'/> Error: Josef Lakonishok, Andrei Shleifer and Robert Vishny argued "
            "that investors extrapolate past growth, overpay for glamour stocks, and are disappointed when growth "
            "reverts. <bookmark mark='c'/> And size may have been mis-measured: Cliff Asness and colleagues found that "
            "once low-quality small firms are set aside, a size premium reappears, steadier than before."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"the size premium was about 3.4\% a year before 1981 and 1.0\% after, with $t \approx 0.6$. Is it dead, "
                r"was it never there, or is it hiding? What evidence would tell them apart?")
        with self.voiceover("The size premium fell from three and a half percent before 1981 to one percent after. Is it "
                            "dead, was it never there, or is it hiding? What evidence would tell them apart?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
