from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant15.common import BAD, BARRIER, GOOD, IV, OPT, PART, SPOT, illustration, load


class Snowball(VoiceoverScene):
    def construct(self):
        s = load("snowball")
        o = load("outcomes")
        self.card()
        self.payoff(s)
        self.lab(o)
        self.outcomes(o)
        self.linear(o)
        self.carry(load("coupon_q"))

    def card(self):
        c = chapter_card(7, r"The snowball, priced", r"What does a saver sell when she buys a 15\% coupon?", part=PART)
        with self.voiceover("Chapter seven. The snowball, priced."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def payoff(self, s):
        t = s["terms"]
        rows = VGroup(
            VGroup(label(r"every month after the third:", font_size=24, color=GREY_A),
                   label(rf"index $\ge$ {100 * t['ko']:.0f}\% of its start $\Rightarrow$ repaid, plus the coupon for the months "
                         r"held", font_size=24, color=GOOD)).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
            VGroup(label(r"every day:", font_size=24, color=GREY_A),
                   label(rf"index closes below {100 * t['ki']:.0f}\% $\Rightarrow$ knocked in", font_size=24, color=BAD))
            .arrange(DOWN, aligned_edge=LEFT, buff=0.08),
            VGroup(label(rf"after {t['months']} months, never knocked out:", font_size=24, color=GREY_A),
                   label(r"never knocked in $\Rightarrow$ the full coupon; knocked in $\Rightarrow$ the index's loss, "
                         r"one for one", font_size=24, color=WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(UP * 0.6)
        eq = MathTex(r"\text{snowball} = \text{bond} + \text{coupon, while alive} - \text{down-and-in put}",
                     font_size=34, color=OPT).to_edge(DOWN, buff=1.2)
        note_ = wrapped_label(r"the name: the coupon accrues month by month, like a snowball rolling; the risk is the "
                              r"knock-in, which turns the note into the index itself", 11.0, 20, GREY_A).next_to(eq, DOWN, buff=0.25)
        with self.voiceover(
            "The snowball, xueqiu in Chinese, was the best-selling structured product in China, linked mostly to "
            "the CSI 500 and CSI 1000 indices. Its terms fit on a card. Every month after the third, if the index "
            "is above its starting level, the note is repaid with its coupon for the months held. <bookmark mark='a'/> "
            "Every day, if the index closes below about three-quarters of its start, the note is knocked in. "
            "<bookmark mark='b'/> If it reaches maturity without being repaid, the buyer gets the full coupon if it "
            "never knocked in, and otherwise takes the index's loss, one for one. <bookmark mark='c'/> In option "
            "terms, the buyer owns a bond and a coupon, and has sold a down-and-in put. The coupon is the put's "
            "premium, paid in instalments."
        ) as vo:
            self.play(FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(eq), FadeIn(note_))
        self.wait(0.4)
        self.clear_scene()

    def lab(self, o):
        card = lab_card(r"the snowball's payoff", [
            "for m in range(lockup, months + 1):        # monthly knock-out",
            "    i = m * days_per_month",
            "    hit = alive & (paths[i] >= ko)",
            "    pv[hit] = (1 + coupon * m / 12) * np.exp(-r * i * dt)",
            "    ko_month[hit] = m",
            "    alive &= ~hit",
            "kin = paths[: months * days_per_month + 1].min(axis=0) < ki",
            "lost = alive & kin                          # the index's loss",
            "pv[lost] = (1 + np.minimum(ST[lost] - 1, 0)) * np.exp(-r * T)",
            "full = alive & ~kin                         # the full coupon",
            "pv[full] = (1 + coupon * months / 12) * np.exp(-r * T)",
        ], source="explainer/quant/house/exotics.py: snowball_payoff", width=8.6, font_size=16).to_corner(UL, buff=0.3)
        outs = [f"40,000 paths, sigma {100 * o['sigma']:.2f}%, coupon {100 * o['coupon']:.2f}%:",
                f"knocked out {100 * o['p_ko']:.1f}%   ended knocked in {100 * o['p_lost']:.1f}%   "
                f"full coupon {100 * o['p_full']:.1f}%",
                f"mean value {o['pv_mean']:.4f}   expected life {o['life']:.1f} months"]
        with self.voiceover(
            "Here is the whole product in the House's code, eleven lines. A loop over the observation months: on "
            "every path still alive, if the index is at or above the knock-out level, pay one plus the coupon for "
            "the months held, and retire the path. <bookmark mark='a'/> Then the knock-in: did the path ever close "
            "below the barrier? Paths alive and knocked in pay the index's loss; paths alive and never knocked in "
            "pay the full coupon. <bookmark mark='b'/> Run it on forty thousand paths at the CSI 500's volatility "
            f"and the fair coupon. {100 * o['p_ko']:.0f} percent knock out, {100 * o['p_lost']:.0f} percent end "
            f"knocked in, and only {100 * o['p_full']:.0f} percent run the full two years and collect every coupon."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.play(Indicate(card.code[6:], color=BAD, scale_factor=1.02))
            vo.wait_until("b")
            lab_run(self, card, outs, font_size=16)
        self.wait(0.4)
        self.clear_scene()

    def outcomes(self, o):
        sh = o["show"]
        P = np.asarray(sh["paths"])
        kom = np.asarray(sh["ko_month"])
        kid = np.asarray(sh["ki_day"])
        n = P.shape[1]
        t = np.arange(n) * 3 / 21
        g = axes([0, 24], [0.45, 1.5], x_length=7.4, y_length=4.6, xlabel=r"months", ylabel=r"index / start",
                 xticks=[0, 3, 6, 12, 18, 24], yticks=[0.5, 0.75, 1.0, 1.25, 1.5], font_size=15)
        g.to_edge(LEFT, buff=0.5).shift(DOWN * 0.2)
        ax = g.ax
        ko_l = DashedLine(ax.c2p(3, 1.03), ax.c2p(24, 1.03), stroke_color=GOOD, stroke_width=2)
        ki_l = DashedLine(ax.c2p(0, 0.75), ax.c2p(24, 0.75), stroke_color=BARRIER, stroke_width=2)
        lines = VGroup()
        for j in range(min(len(P), 150)):
            end = int(kom[j] * 21 / 3) if kom[j] > 0 else n - 1
            y = np.clip(P[j, :end + 1], 0.45, 1.5)
            if kom[j] > 0:
                col, op = QC.HOUSE, 0.5
            elif kid[j] >= 0:
                col, op = BAD, 0.6
            else:
                col, op = WHITE, 0.6
            seg = curve(ax, t[:end + 1], y, col, stroke_width=1.2).set_stroke(opacity=op)
            lines.add(seg)
        h = np.asarray(o["ko_hist"], float)
        hb = axes([0, 24], [0, 1], x_length=4.4, y_length=2.4, xlabel=r"knock-out month", ylabel=r"share",
                  xticks=[3, 6, 12, 18, 24], yticks=[], font_size=14).to_corner(UR, buff=0.5)
        bars = VGroup()
        top = h.max()
        for m in range(3, 25):
            y1 = hb.ax.c2p(m, h[m] / top)[1]
            y0 = hb.ax.c2p(m, 0)[1]
            bars.add(Rectangle(width=0.14, height=max(y1 - y0, 0.01), stroke_width=0, fill_color=QC.HOUSE,
                               fill_opacity=0.85).move_to([hb.ax.c2p(m, 0)[0], (y0 + y1) / 2, 0]))
        stats = VGroup(
            label(rf"knocked out: {100 * o['p_ko']:.1f}\%, at month {o['mean_ko_month']:.1f} on average; "
                  rf"{100 * o['p_first']:.1f}\% at the first look", font_size=19, color=QC.HOUSE),
            label(rf"ended knocked in: {100 * o['p_lost']:.1f}\%, left with {o['mean_lost']:.2f} per 1 on average",
                  font_size=19, color=BAD),
            label(rf"full coupon: {100 * o['p_full']:.1f}\%; expected life {o['life']:.1f} months", font_size=19,
                  color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(hb, DOWN, buff=0.4).align_to(hb, LEFT)
        if stats.width > 5.4:
            stats.scale_to_fit_width(5.4)
        pp = pause_card(r"What fraction of these snowballs end before maturity?", width=5.4).to_corner(UR, buff=0.4)
        src = illustration(r"150 of 40{,}000 simulated paths at the fair coupon; gold stops at its knock-out", corner=DL)
        with self.voiceover(
            "Pause and predict: what fraction of these notes end before maturity? <bookmark mark='a'/> Watch a "
            "hundred and fifty of the paths. Each runs until it knocks out, and stops there, in gold. Paths that "
            "fall through the knock-in turn red and run to the end. White paths survive both. "
            f"<bookmark mark='b'/> The answer: {100 * o['p_ko']:.0f} percent knock out, most of them early. "
            f"{100 * o['p_first']:.0f} percent at the very first look, in month three, and the average knock-out "
            f"comes in month {o['mean_ko_month']:.0f}. The expected life of a two-year note is {o['life']:.0f} "
            f"months. <bookmark mark='c'/> And the {100 * o['p_lost']:.0f} percent that end knocked in are left, on "
            f"average, with {o['mean_lost']:.2f} per unit invested. That is the shape of the bet: many small, "
            "quick wins, and a fat tail of large losses."
        ) as vo:
            self.play(FadeIn(pp))
            vo.wait_until("a")
            self.play(FadeOut(pp), FadeIn(g), Create(ko_l), Create(ki_l), FadeIn(src))
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.02, run_time=7))
            vo.wait_until("b")
            self.play(FadeIn(hb), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.05),
                      FadeIn(stats[0]))
            vo.wait_until("c")
            self.play(FadeIn(stats[1]), FadeIn(stats[2]))
        self.wait(0.4)
        self.clear_scene()

    def linear(self, o):
        A, B, c = o["A"], o["B"], o["coupon"]
        g = axes([0, 0.3], [0.9, 1.1], x_length=6.0, y_length=4.0, xlabel=r"coupon $c$, a year",
                 ylabel=r"value of the note, $V(c)$", xticks=[0, 0.1, 0.2, 0.3], xfmt=lambda u: f"{100 * u:.0f}\\%",
                 yticks=[0.9, 1.0, 1.1], font_size=15).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        one = DashedLine(ax.c2p(0, 1), ax.c2p(0.3, 1), stroke_color=GREY_C, stroke_width=1.5)
        line = Line(ax.c2p(0, A), ax.c2p(0.3, A + 0.3 * B), stroke_color=OPT, stroke_width=3.5)
        dot = Dot(ax.c2p(c, 1), radius=0.1, color=IV)
        dl = label(rf"$c^* = {100 * c:.2f}\%$", font_size=22, color=IV).next_to(dot, DR, buff=0.1)
        rows = [cmath(r"V(c)", r"=", r"A + c\,B", font_size=40, colors={r"V(c)": OPT}),
                cmath(r"c^{*}", r"=", r"\frac{1 - A}{B}", font_size=40, colors={r"c^{*}": IV})]
        side = VGroup(rows[0],
                      wrapped_label(r"$A = \sum_m \mathbb E[D_m\mathbf 1_{\tau = m}] + \mathbb E[D_T(\mathbf 1_{\text{alive, "
                                    r"no KI}} + \min(S_T, 1)\mathbf 1_{\text{alive, KI}})]$; $B = \sum_m \tfrac{m}{12}"
                                    r"\mathbb E[D_m\mathbf 1_{\tau = m}] + 2\,\mathbb E[D_T\mathbf 1_{\text{alive, no KI}}]$",
                                    5.2, 18, GREY_A),
                      rows[1],
                      wrapped_label(rf"one simulation gives both: $A = {A:.4f}$, $B = {B:.4f}$. No root search: the "
                                    r"coupon is a linear solve (a solve, not a fit)", 5.2, 19, WHITE),
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "How was that fair coupon found? Not by trial and error. On every path, the note pays either a fixed "
            "amount or a fixed amount plus the coupon times something that does not depend on the coupon. "
            "<bookmark mark='a'/> So the note's value is a straight line in the coupon: A plus c times B. A is what "
            "the note is worth with no coupon at all; B is the present value of one unit of coupon a year, which is "
            "roughly the expected time the note stays alive and paying. <bookmark mark='b'/> One simulation gives "
            f"both: A is {A:.3f}, B is {B:.3f}. The line crosses one at c star equals one minus A over B, "
            f"{100 * c:.2f} percent. It is a solve, not a search, and it is exact on the simulated paths."
        ) as vo:
            self.play(FadeIn(g), Create(one), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("a")
            self.play(Create(line), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(dot), FadeIn(dl), FadeIn(side[2]), FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    def carry(self, cq):
        bq = cq["by_q"]
        bk = cq["by_ki"]
        g1 = axes([0, 0.08], [0, 0.32], x_length=5.0, y_length=3.6, xlabel=r"carry $q$: dividend plus futures discount",
                  ylabel=r"fair coupon", xticks=[0, 0.02, 0.04, 0.06, 0.08], xfmt=lambda u: f"{100 * u:.0f}\\%",
                  yticks=[0, 0.1, 0.2, 0.3], yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=14)
        g2 = axes([0.62, 0.88], [0, 0.32], x_length=5.0, y_length=3.6, xlabel=r"knock-in level",
                  ylabel=r"fair coupon", xticks=[0.65, 0.75, 0.85], xfmt=lambda u: f"{100 * u:.0f}\\%",
                  yticks=[0, 0.1, 0.2, 0.3], yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=14)
        VGroup(g1, g2).arrange(RIGHT, buff=1.0).to_edge(UP, buff=0.9)
        b1 = VGroup(*[Rectangle(width=0.5, height=g1.ax.c2p(0, r["coupon"])[1] - g1.ax.c2p(0, 0)[1], stroke_width=0,
                                fill_color=IV, fill_opacity=0.85).move_to(
            [g1.ax.c2p(r["q"], 0)[0], (g1.ax.c2p(0, r["coupon"])[1] + g1.ax.c2p(0, 0)[1]) / 2, 0]) for r in bq])
        t1 = VGroup(*[MathTex(f"{100 * r['coupon']:.1f}", font_size=22, color=IV).next_to(b_, UP, buff=0.05)
                      for r, b_ in zip(bq, b1)])
        b2 = VGroup(*[Rectangle(width=0.5, height=g2.ax.c2p(0.7, r["coupon"])[1] - g2.ax.c2p(0.7, 0)[1], stroke_width=0,
                                fill_color=BARRIER, fill_opacity=0.85).move_to(
            [g2.ax.c2p(r["ki"], 0)[0], (g2.ax.c2p(0.7, r["coupon"])[1] + g2.ax.c2p(0.7, 0)[1]) / 2, 0]) for r in bk])
        t2 = VGroup(*[MathTex(f"{100 * r['coupon']:.1f}", font_size=22, color=BARRIER).next_to(b_, UP, buff=0.05)
                      for r, b_ in zip(bk, b2)])
        rows = VGroup(
            MathTex(r"F_t = S_t\,e^{(r - q_{\text{eff}})(T - t)}", font_size=30, color=IV),
            wrapped_label(r"the issuer hedges with index futures. When they trade at a discount to spot, the hedge earns "
                          r"the roll, and pricing with the futures' forward is pricing with a dividend yield $q_{\text{eff}}$: "
                          r"a lower forward makes a knock-in likelier, the put the buyer sells dearer, and the coupon "
                          r"higher", 11.6, 19, GREY_A),
            wrapped_label(r"as reported: Risk.net found issuers blaming a narrowing CSI 500 futures discount for shrinking "
                          r"coupons; Bloomberg (24 April 2024) reported brokers offering coupons above 40\% after the "
                          r"selloff, before regulators told them to stop growing their exposure", 11.6, 18, GREY_B),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.3)
        q0, q4 = bq[0]["coupon"], bq[2]["coupon"]
        with self.voiceover(
            "Two more levers set the coupon. The first is carry. Issuers hedge with index futures, and for years the "
            "CSI 500 futures traded at a large discount to the index. A hedger who is long futures earns that "
            "discount as the futures converge. <bookmark mark='a'/> In the pricing it acts like a dividend yield: "
            "the forward is lower, a knock-in likelier, the put dearer, and the fair coupon higher. With no carry, "
            f"{100 * q0:.1f} percent; with four percent, {100 * q4:.1f}; with eight, {100 * bq[-1]['coupon']:.1f}. "
            "<bookmark mark='b'/> The second is the knock-in level. Move it from 75 down to 70 percent of the start, "
            f"and the fair coupon falls from {100 * bk[2]['coupon']:.1f} to {100 * bk[1]['coupon']:.1f} percent; up to "
            f"80, and it rises to {100 * bk[3]['coupon']:.1f}. <bookmark mark='c'/> The market noticed both. Risk.net "
            "reported issuers blaming a narrowing futures discount for shrinking coupons, and Bloomberg reported "
            "brokers offering coupons above forty percent after the 2024 selloff, with prices that had fallen "
            "and volatility that had risen, before regulators told them to stop growing their exposure."
        ) as vo:
            self.play(FadeIn(g1), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in b1], lag_ratio=0.2), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(t1), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(g2), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in b2], lag_ratio=0.2), FadeIn(t2))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.wait(0.4)
        self.clear_scene()
