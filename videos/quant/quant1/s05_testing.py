from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant1.common import GAUSS, LARGE, PART, REAL, SMALL, load, real_data

C_ = {r"\rho_k": QC.IDEA, r"\rho_1": QC.IDEA, r"\operatorname{VR}(q)": REAL, r"\operatorname{VR}(2)": REAL}


def row(*parts, fs=40):
    return cmath(*parts, colors=C_, font_size=fs)


NAMES = {"small": r"smallest 10\%", "5": r"middle decile", "large": r"largest 10\%", "market": r"whole market"}
COLS = {"small": SMALL, "5": QC.IDEA, "large": LARGE, "market": REAL}


class Testing(VoiceoverScene):
    def construct(self):
        v = load("vr")
        self.card()
        self.define()
        self.replicate(v)
        self.after(v)
        self.decades(v)

    def card(self):
        c = chapter_card(4, r"Testing the walk", r"Do returns remember?", part=PART)
        with self.voiceover("Chapter four. Testing the walk."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def define(self):
        d1 = definition_card(r"Autocorrelation", r"$\rho_k = \operatorname{corr}(r_t,\ r_{t-k})$: how much this "
                             r"period's return is related to the one $k$ periods ago. A random walk has $\rho_k = 0$ "
                             r"for every $k \ge 1$.", width=6.0, color=QC.IDEA)
        d2 = definition_card(r"Variance ratio", r"$\operatorname{VR}(q) = \dfrac{\operatorname{Var}(r_t + \dots + "
                             r"r_{t+q-1})}{q\,\operatorname{Var}(r_t)}$: Regnault's law as a test. A random walk has "
                             r"$\operatorname{VR}(q) = 1$.", width=6.0, color=REAL)
        top = VGroup(d1, d2).arrange(RIGHT, buff=0.4, aligned_edge=UP).to_edge(UP, buff=0.35)
        rows = [
            row(r"\operatorname{VR}(2)", r"=", r"\frac{2\operatorname{Var}(r) + 2\operatorname{Cov}(r_t, r_{t+1})}"
                                               r"{2\operatorname{Var}(r)}", r"=", r"1 + \rho_1", fs=36),
            row(r"\operatorname{VR}(q)", r"=", r"1 + 2\sum_{k=1}^{q-1}\Big(1 - \frac{k}{q}\Big)", r"\rho_k", fs=36),
        ]
        for i, r_ in enumerate(rows):
            r_.shift((-1.0 - r_[1].get_center()[0]) * RIGHT)
        rows[0].next_to(top, DOWN, buff=0.55)
        rows[0].shift((-1.0 - rows[0][1].get_center()[0]) * RIGHT)
        rows[1].next_to(rows[0], DOWN, buff=0.45)
        rows[1].shift((-1.0 - rows[1][1].get_center()[0]) * RIGHT)
        w1 = why(r"the variance of a sum: two variances and a covariance").next_to(rows[0], DOWN, buff=0.08)
        rows[1].shift(DOWN * 0.2)
        w2 = why(r"in general: a weighted sum of autocorrelations").next_to(rows[1], DOWN, buff=0.08)
        signs = VGroup(
            MathTex(r"\operatorname{VR} > 1", font_size=32, color=SMALL),
            label(r"trends: returns continue", font_size=22, color=GREY_A),
            MathTex(r"\operatorname{VR} < 1", font_size=32, color=LARGE),
            label(r"reversals: returns undo themselves", font_size=22, color=GREY_A),
        ).arrange_in_grid(2, 2, buff=(0.3, 0.15), col_alignments="ll").to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "If returns have memory, it shows up as autocorrelation: the correlation between one period's return "
            "and an earlier one. For a random walk every autocorrelation is zero. <bookmark mark='a'/> In 1988 "
            "Andrew Lo and Craig MacKinlay turned Regnault's law into a test. Compare the variance of a "
            "q-week return with q times the variance of a one-week return. For a random walk the ratio is exactly "
            "one. <bookmark mark='b'/> For two weeks, the variance of a sum is two variances plus twice the "
            "covariance, so the ratio is one plus the first autocorrelation. In general it is one plus a weighted "
            "sum of autocorrelations, heaviest on the shortest lags. <bookmark mark='c'/> Above one means returns "
            "continue, trends. Below one means they undo themselves, reversals. And Lo and MacKinlay gave a version "
            "of the test that stays honest when volatility comes in bursts, which chapter six will show it does."
        ) as vo:
            self.play(FadeIn(d1, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(d2, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(Write(rows[0]), FadeIn(w1))
            self.play(Write(rows[1]), FadeIn(w2))
            vo.wait_until("c")
            self.play(FadeIn(signs))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def _vr_plot(self, v, per, dim=False):
        q = np.array(v["q"], float)
        g = axes([np.log2(1.6), np.log2(20)], [0.7, 2.8], x_length=6.2, y_length=4.4,
                 xlabel=r"horizon $q$, weeks (log scale)", ylabel=r"variance ratio $\operatorname{VR}(q)$",
                 xticks=[1, 2, 3, 4], xfmt=lambda x: f"{2 ** x:g}", yticks=[1, 1.5, 2, 2.5], font_size=18)
        return g

    def _lines(self, ax, v, per, op=1.0, sw=3.5):
        q = np.array(v["q"], float)
        out = VGroup()
        for name in ("small", "5", "market", "large"):
            ys = [x["vr"] for x in v[per][name]["vr"]]
            pts = [ax.c2p(np.log2(a), b) for a, b in zip(q, ys)]
            ln = VMobject(color=COLS[name], stroke_width=sw).set_points_as_corners(pts).set_stroke(opacity=op)
            dots = VGroup(*[Dot(p, radius=0.06, color=COLS[name]).set_fill(opacity=op) for p in pts])
            out.add(VGroup(ln, dots))
        return out

    def _table(self, v, per):
        hdr = [label(r"weekly", font_size=22, color=GREY_B)] + [MathTex(t, font_size=26, color=GREY_A) for t in
               (r"\rho_1", r"\operatorname{VR}(2)", r"\operatorname{VR}(4)", r"\operatorname{VR}(16)")]
        body = []
        for name in ("small", "5", "market", "large"):
            x = v[per][name]
            vr = {y["q"]: y for y in x["vr"]}
            cells = [label(NAMES[name], font_size=22, color=COLS[name]),
                     MathTex(rf"{x['rho1']:+.2f}", font_size=26, color=COLS[name])]
            for qq in (2, 4, 16):
                cells.append(MathTex(rf"{vr[qq]['vr']:.2f}\,({vr[qq]['z_star']:+.1f})", font_size=24,
                                     color=COLS[name]))
            body.append(cells)
        flat = VGroup(*hdr, *[c for cells in body for c in cells])
        flat.arrange_in_grid(len(body) + 1, 5, buff=(0.32, 0.24), col_alignments="lrrrr")
        rows = [VGroup(*hdr)] + [VGroup(*cells) for cells in body]
        foot = note(r"$z^*$ in brackets: Lo and MacKinlay's heteroskedasticity-robust statistic; $|z^*| > 2$ "
                    r"rejects the random walk", font_size=17)
        if foot.width > flat.width + 0.4:
            foot = wrapped_label(r"$z^*$ in brackets: Lo and MacKinlay's heteroskedasticity-robust statistic; "
                                 r"$|z^*| > 2$ rejects the random walk", flat.width + 0.4, 17, GREY_B)
        foot.next_to(flat, DOWN, buff=0.2).align_to(flat, LEFT)
        g = VGroup(flat, foot)
        g.rows, g.foot = rows, foot
        return g

    def replicate(self, v):
        g = self._vr_plot(v, "lm").to_edge(LEFT, buff=0.6).shift(DOWN * 0.35)
        ax = g.ax
        one = DashedLine(ax.c2p(np.log2(1.6), 1), ax.c2p(np.log2(20), 1), color=GAUSS, stroke_width=2)
        rw = label(r"random walk", font_size=20, color=GAUSS).next_to(ax.c2p(np.log2(20), 1), UP, buff=0.08).shift(LEFT * 0.7)
        lines = self._lines(ax, v, "lm")
        tab = self._table(v, "lm").scale(0.95).to_edge(RIGHT, buff=0.35).shift(UP * 0.4)
        title = label(r"Lo and MacKinlay's sample, replicated: 6 Sept 1962 to 26 Dec 1985, weekly", font_size=26)
        title.to_edge(UP, buff=0.3)
        src = real_data(r"Ken French's size deciles (value-weighted, NYSE breakpoints) and market; Wednesday-to-"
                        r"Wednesday log returns, $n = " + str(v["lm"]["small"]["n"]) + r"$ weeks")
        s, m, L = v["lm"]["small"], v["lm"]["market"], v["lm"]["large"]
        with self.voiceover(
            "Here is their test, replicated on Kenneth French's portfolios of stocks sorted by size, over exactly "
            f"their sample: September 1962 to December 1985, {s['n']:,} weeks. <bookmark mark='a'/> The smallest "
            f"tenth of stocks: the weekly autocorrelation is {s['rho1']:+.2f}, and the variance ratio climbs to "
            f"{s['vr'][-1]['vr']:.2f} at sixteen weeks, with a robust test statistic around "
            f"{s['vr'][1]['z_star']:.0f}. A random walk would almost never produce that. <bookmark mark='b'/> The "
            f"whole market: an autocorrelation of {m['rho1']:+.2f}, smaller but still a rejection. "
            f"<bookmark mark='c'/> The largest tenth: {L['rho1']:+.2f}, a variance ratio of one, a random walk. "
            "The rejection lives in small stocks, as Lo and MacKinlay found, and their paper's title said it "
            "plainly: stock market prices do not follow random walks."
        ) as vo:
            self.play(FadeIn(title), FadeIn(g), Create(one), FadeIn(rw), FadeIn(src))
            self.play(FadeIn(tab.rows[0]))
            vo.wait_until("a")
            self.play(Create(lines[0]), FadeIn(tab.rows[1]))
            self.play(Create(lines[1]), FadeIn(tab.rows[2]))
            vo.wait_until("b")
            self.play(Create(lines[2]), FadeIn(tab.rows[3]))
            vo.wait_until("c")
            self.play(Create(lines[3]), FadeIn(tab.rows[4]), FadeIn(tab.foot))
        self.lm_lines, self.lm_ax, self.lm_g, self.lm_tab, self.lm_title = lines, ax, g, tab, title
        self.lm_extra = VGroup(one, rw, src)

    def after(self, v):
        ax = self.lm_ax
        new_lines = self._lines(ax, v, "after")
        tab2 = self._table(v, "after").scale(0.95).move_to(self.lm_tab)
        title2 = label(r"The next 35 years: 1986 to 2020, weekly", font_size=26).move_to(self.lm_title)
        s = v["after"]["small"]
        with self.voiceover(
            "Their paper came out in 1988. What happened next? Here are the same tests on the thirty-five years "
            f"that followed, 1986 to 2020. <bookmark mark='a'/> Small stocks still trend, with an autocorrelation of "
            f"{s['rho1']:+.2f}, half what it was. The middle and the market have fallen to a random walk, and the "
            "largest stocks now lean slightly the other way, towards reversals."
        ) as vo:
            self.play(*[ln[0].animate.set_stroke(opacity=0.2) for ln in self.lm_lines],
                      *[ln[1].animate.set_fill(opacity=0.2) for ln in self.lm_lines], FadeOut(self.lm_tab),
                      Transform(self.lm_title, title2))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(ln) for ln in new_lines], lag_ratio=0.3), FadeIn(tab2))
        self.wait(0.4)
        self.clear_scene()

    def decades(self, v):
        y = np.asarray(v["roll_years"])
        s, L = np.asarray(v["roll_small"]), np.asarray(v["roll_large"])
        g = axes([1930, 2020], [-0.3, 0.5], x_length=10.4, y_length=4.4,
                 ylabel=r"weekly autocorrelation $\rho_1$, in rolling 5-year windows",
                 xticks=[1940, 1960, 1980, 2000, 2020], yticks=[-0.2, 0, 0.2, 0.4], xfmt=lambda x: f"{int(x)}",
                 font_size=18).shift(DOWN * 0.2)
        ax = g.ax
        zero = DashedLine(ax.c2p(1930, 0), ax.c2p(2020, 0), color=GAUSS, stroke_width=1.5)
        ls = curve(ax, y, s, SMALL, stroke_width=3.5)
        ll = curve(ax, y, L, LARGE, stroke_width=3.5)
        leg = legend([(SMALL, r"smallest 10\% of stocks"), (LARGE, r"largest 10\%")], font_size=22)
        leg.move_to(ax.c2p(1935, 0.47), aligned_edge=UL)
        pub = DashedLine(ax.c2p(1988, -0.3), ax.c2p(1988, 0.5), color=QC.IDEA, stroke_width=2)
        publ = label(r"published, 1988", font_size=20, color=QC.IDEA).next_to(ax.c2p(1988, 0.5), DOWN, buff=0.08)
        publ.shift(LEFT * 1.0)
        era = Rectangle(width=ax.c2p(2007, 0)[0] - ax.c2p(2001, 0)[0], height=ax.y_length, stroke_width=0,
                        fill_color=GREY_D, fill_opacity=0.35).move_to(ax.c2p(2004, 0.1))
        eral = wrapped_label(r"decimal prices (2001), Reg NMS and electronic trading (2005--07)", 2.6, 18, GREY_A)
        eral.next_to(era, RIGHT, buff=0.1).align_to(ax.c2p(0, 0.47), UP)
        expl = wrapped_label(r"the leading explanation: small stocks traded rarely, so their recorded prices were "
                             r"stale and caught up a week later (nonsynchronous trading; Lo--MacKinlay 1990)", 11.0, 21,
                             GREY_B).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Now the whole century, in five-year windows. The pink line is small stocks' weekly autocorrelation; "
            "the teal line, the largest stocks'. <bookmark mark='a'/> For seventy years small stocks carried a "
            "strong weekly echo, about plus a third, and it survived its own publication in 1988. "
            "<bookmark mark='b'/> Then, in the space of a few years in the middle of the 2000s, it collapsed to "
            "nothing, the same years that American stocks moved to prices in cents, and to electronic trading. "
            "<bookmark mark='c'/> The leading explanation is mundane: small stocks used to trade rarely, so their "
            "recorded closing prices were stale and caught up days later. An echo you cannot trade on is not a "
            "profit; it is a measurement problem. Once small stocks traded every second, the echo went away. That "
            "is the first lesson of testing a market: ask what the price in your data really was, and whether you "
            "could have traded at it."
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(leg))
            self.play(Create(ls), Create(ll), run_time=3)
            vo.wait_until("a")
            self.play(Create(pub), FadeIn(publ))
            vo.wait_until("b")
            self.play(FadeIn(era), FadeIn(eral))
            vo.wait_until("c")
            self.play(FadeIn(expl))
        self.wait(0.5)
        self.clear_scene()
