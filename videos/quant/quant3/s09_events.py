from __future__ import annotations

from datetime import date

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant3.common import GAIN, LOSS, PART, PRICE, VALUE, load, real_data


def _yr(n: int) -> float:
    d = date(n // 10000, n // 100 % 100, n % 100)
    return d.year + (d.timetuple().tm_yday - 1) / 365.25


class Events(VoiceoverScene):
    def construct(self):
        m = load("merger")
        self.card()
        self.derive()
        self.capri(m)
        self.kink(m)
        self.shire()

    def card(self):
        c = chapter_card(15, r"Merger arbitrage", r"What is a takeover spread paying you for?", part=PART)
        with self.voiceover("Chapter fifteen. Merger arbitrage."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def derive(self):
        rows = [
            cmath(r"P_t", r"=", r"e^{-r\tau}\big[\,p\,O + (1 - p)\,B\,\big]", font_size=42, colors={r"P_t": PRICE}),
            cmath(r"p", r"=", r"\frac{P_t e^{r\tau} - B}{O - B}", font_size=44, colors={r"p": QC.Q}),
            cmath(r"P = 47,\ O = 50,\ B = 35,\ r\tau = 2\%", r":", r"\ p = 86\%\ \ (80\%\ \text{ignoring interest})",
                  font_size=34),
        ]
        whys = [why(r"under the risk-neutral measure the price is the discounted expected payoff: the offer $O$ if the "
                    r"deal closes, the fallback price $B$ if it breaks"),
                why(r"solve for $p$: the market's implied chance of closing"),
                why(r"a risk-neutral probability, not a forecast: it includes a premium for bearing deal risk")]
        step = ladder(self, rows, whys, keep=3, top=2.4, x=-0.4, buff=0.9, edge=6.9)
        with self.voiceover(
            "When one company bids cash for another, the target's shares jump towards the offer, but not all the way, and a "
            "merger arbitrageur buys and waits. Price it like Part one's fair game: the price is the discounted expected payoff, "
            "the offer if the deal closes, the fallback if it breaks. <bookmark mark='a'/> Solve for p: the market's implied "
            "chance of closing. <bookmark mark='b'/> A target at forty-seven, an offer of fifty, a fallback of thirty-five, six "
            "months at four percent: eighty-six percent. It is risk-neutral, so it includes a premium for bearing deal risk."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def capri(self, m):
        d, px, pp = np.asarray(m["cpri_date"]), np.asarray(m["cpri"]), np.asarray(m["cpri_p"])
        X = np.array([_yr(int(x)) for x in d])
        O, B = m["cpri_O"], m["cpri_B"]
        g = axes([2023.0, 2025.0], [15, 65], x_length=8.0, y_length=3.0, ylabel=r"Capri Holdings (CPRI), weekly close",
                 xticks=[2023, 2024, 2025], xfmt=lambda v: f"{int(v)}", yticks=[20, 35, 50], font_size=17)
        g.to_edge(LEFT, buff=0.5).to_edge(UP, buff=0.55)
        ax = g.ax
        h = axes([2023.0, 2025.0], [-0.2, 1.1], x_length=8.0, y_length=1.9, ylabel=r"implied chance of closing",
                 xticks=[], yticks=[0, 0.5, 1], yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=17)
        h.next_to(g, DOWN, buff=0.45).align_to(g, LEFT)
        hx = h.ax
        k = ValueTracker(0)
        line = tracing(ax, X, px, k, PRICE)
        post = X >= _yr(20230801)
        # after the ruling the price fell below the old close, so the implied p goes negative: drawn at the floor
        Xp, Pp = X[post], np.clip(pp[post], -0.2, 1.1)
        k2 = ValueTracker(0)
        pline = tracing(hx, Xp, Pp, k2, QC.Q)
        offer = DashedLine(ax.c2p(_yr(20230810), O), ax.c2p(2025, O), color=GAIN, stroke_width=2)
        fall = DashedLine(ax.c2p(2023, B), ax.c2p(2025, B), color=LOSS, stroke_width=2)
        ol = label(rf"offer \${O:.0f} cash", font_size=17, color=GAIN).next_to(ax.c2p(2025, O), LEFT, buff=0.1).shift(UP * 0.18)
        fl = label(rf"last close before the deal \${B:.2f}", font_size=17, color=LOSS).next_to(ax.c2p(2023.0, B), RIGHT,
                                                                                           buff=0.1).shift(DOWN * 0.2)
        events = [(20230810, r"10 Aug 2023: Tapestry bids \$57, about \$8.5bn with debt"),
                  (20240422, r"22 Apr 2024: the FTC sues to block"),
                  (20241024, r"24 Oct 2024: injunction granted"),
                  (20241114, r"14 Nov 2024: deal terminated")]
        notes = VGroup()
        for i, (dt, txt) in enumerate(events):
            x = _yr(dt)
            notes.add(VGroup(DashedLine(ax.c2p(x, 15), ax.c2p(x, 65), color=GREY_C, stroke_width=1.2),
                             label(txt, font_size=16, color=GREY_A)))
        side = VGroup(*[n[1] for n in notes]).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.3)
        side.shift(UP * 1.4)
        lows = label(rf"the week of the ruling: \${px[np.searchsorted(d, 20241019)]:.2f}, below where it started",
                     font_size=18, color=LOSS).next_to(side, DOWN, buff=0.4).align_to(side, LEFT)
        caveat = label(r"a case file (2023--24), not a backtest; ignoring interest", font_size=16, color=GREY_B)
        caveat.next_to(lows, DOWN, buff=0.25).align_to(side, LEFT)
        src = real_data(r"Yahoo Finance weekly closes; Tapestry and Capri releases; FTC; S.D.N.Y.")
        with self.voiceover(
            "A real deal, as it happened. In August 2023 Tapestry, the owner of Coach, agreed to buy Capri, the owner of Michael "
            f"Kors and Versace, for fifty-seven dollars a share in cash; Capri had closed the week before at {B:.2f}. "
            "<bookmark mark='a'/> The price jumped, but stopped short. Below, the implied chance of closing, recomputed every week. "
            "<bookmark mark='b'/> In April 2024 the Federal Trade Commission sued to block the deal, alleging it would reduce "
            "competition in accessible luxury handbags, and the probability fell. <bookmark mark='c'/> In October a federal judge "
            "granted a preliminary injunction; Capri fell to about twenty-one dollars, below where it started, and the companies "
            "terminated the agreement. A few dollars if it closes, half the price if it breaks."
        ) as vo:
            self.play(FadeIn(g), FadeIn(h), Create(fall), FadeIn(fl), FadeIn(src))
            self.add(line)
            self.play(k.animate.set_value(int(np.searchsorted(d, 20230801))), run_time=2, rate_func=linear)
            vo.wait_until("a")
            self.play(Create(notes[0][0]), FadeIn(notes[0][1]), Create(offer), FadeIn(ol))
            self.add(pline)
            i_apr = int(np.searchsorted(d, 20240420))
            self.play(k.animate.set_value(i_apr), k2.animate.set_value(int(np.searchsorted(d[post], 20240420))),
                      run_time=4, rate_func=linear)
            vo.wait_until("b")
            self.play(Create(notes[1][0]), FadeIn(notes[1][1]))
            i_oct = int(np.searchsorted(d, 20241019))
            self.play(k.animate.set_value(i_oct - 1), k2.animate.set_value(int(np.searchsorted(d[post], 20241019)) - 1),
                      run_time=3, rate_func=linear)
            vo.wait_until("c")
            self.play(Create(notes[2][0]), FadeIn(notes[2][1]), k.animate.set_value(len(d) - 1),
                      k2.animate.set_value(int(post.sum()) - 1), run_time=2)
            self.play(Create(notes[3][0]), FadeIn(notes[3][1]), FadeIn(lows), FadeIn(caveat))
        line.clear_updaters()
        pline.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def kink(self, m):
        rm, rs = np.asarray(m["rm"]), np.asarray(m["rs"])
        g = axes([-0.2, 0.15], [-0.09, 0.07], x_length=6.4, y_length=4.6, xlabel=r"S\&P 500 return in the month",
                 ylabel=r"The Merger Fund's return", xticks=[-0.15, -0.1, -0.05, 0, 0.05, 0.1],
                 yticks=[-0.08, -0.04, 0, 0.04], xfmt=lambda u: f"{100 * u:.0f}\\%", yfmt=lambda u: f"{100 * u:.0f}\\%",
                 font_size=17).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(x, y), radius=0.035, color=QC.SPOT, fill_opacity=0.7)
                        for x, y in zip(np.clip(rs, -0.2, 0.15), np.clip(rm, -0.09, 0.07))])
        a, bu, be = m["alpha"], m["beta_up"], m["beta_extra"]
        xs = np.linspace(-0.2, 0.15, 71)
        kx = ValueTracker(0.0)

        def fit():
            e = kx.get_value()
            ys = a + bu * xs + e * be * np.minimum(xs + 0.04, 0)
            return curve(ax, xs, ys, VALUE, stroke_width=4)

        fl = always_redraw(fit)
        sure = m["boot_lo"] > 0
        side = VGroup(
            label(rf"{m['n']} months, 1989--2020; mean {100 * m['mean']:.1f}\% a year, volatility "
                  rf"{100 * m['vol']:.1f}\%", font_size=20, color=GREY_A),
            MathTex(rf"\beta = {bu:.2f}\ \text{{above a }}{-4}\%\ \text{{month}},\ {m['beta_down']:.2f}\ \text{{below}}",
                    font_size=28, color=VALUE),
            MathTex(rf"\text{{extra slope }}{be:.2f},\ 95\%\ \text{{bootstrap}}\ [{m['boot_lo']:.2f}, {m['boot_hi']:.2f}]",
                    font_size=26, color=GAIN if sure else GREY_A),
            wrapped_label((r"the kink is clear of zero" if sure else
                           r"the kink has Mitchell and Pulvino's sign, but one fund's thirty years cannot pin it down"),
                          4.8, 21, GAIN if sure else GREY_A),
            wrapped_label(r"Mitchell and Pulvino (2001), 4{,}750 mergers, 1963--1998: returns shaped like a short "
                          r"index put; about 4\% a year in excess returns after costs", 4.8, 20, QC.IDEA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4)
        src = real_data(r"Yahoo Finance monthly total returns: MERFX; S\&P 500 price index")
        kink_line = ("The bootstrap band of the extra slope is clear of zero. " if sure else
                     "The extra slope has their sign, but its bootstrap band includes zero: one fund and a handful of "
                     "crash months cannot pin it down. ")
        with self.voiceover(
            "Add up many deals and you get a strategy. Mitchell and Pulvino measured it in 2001 on four thousand seven hundred "
            "and fifty mergers: in calm markets the returns barely depend on the market, but in severe falls they do, because "
            "deals break together. <bookmark mark='a'/> Test that on public data: The Merger Fund, one of the oldest "
            "merger-arbitrage mutual funds, month by month since 1989 against the S&P 500. Its worst month was "
            f"{100 * m['worst']:.1f} percent. <bookmark mark='b'/> Fit a line with a hinge at a four percent market fall: slope "
            f"{bu:.2f} above, {m['beta_down']:.2f} below. {kink_line}<bookmark mark='c'/> A small steady gain with a kink "
            "into losses in a crash is the payoff of selling a put. They found about four percent a year after costs: payment for "
            "insurance."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.005, run_time=2.5))
            vo.wait_until("b")
            self.add(fl)
            self.play(kx.animate.set_value(1.0), run_time=2.5)
            self.play(FadeIn(side[1]), FadeIn(side[2]), FadeIn(side[3]))
            vo.wait_until("c")
            self.play(FadeIn(side[4]))
        fl.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def shire(self):
        card = firm_card(r"AbbVie and Shire, 2014",
                         r"AbbVie agreed in July 2014 to buy Shire for about \$54 billion, partly to move its tax "
                         r"domicile abroad. On 22 September the US Treasury announced rules against such tax "
                         r"inversions; on 15 October AbbVie's board withdrew its recommendation, and the deal ended.",
                         numbers=[(r"\$1.6\text{bn}", r"break fee AbbVie paid Shire"),
                                  (r"\text{Oct.\ 2014}", r"spreads widened across the merger-arbitrage book")],
                         source=r"AbbVie, Form 8-K, October 2014; Gabelli funds' letters", width=8.4)
        card.move_to(UP * 0.4)
        pp = desk_question(r"A target trades at 47 under a cash offer of 50; if the deal breaks it falls to 35. It "
                           r"closes in six months and cash earns 4\% a year. What chance of closing is priced in?",
                           width=8.4, font_size=21).next_to(card, DOWN, buff=0.3)
        with self.voiceover(
            "And the put is exercised on the whole book at once. In 2014 AbbVie agreed to buy Shire for about fifty-four billion "
            "dollars, partly to move its tax home out of the United States. In September the Treasury announced rules against such "
            "inversions, and in October AbbVie walked away, paying a break fee of about one point six billion. Funds holding the "
            "spread lost heavily, and spreads on other deals widened at the same time. <bookmark mark='a'/> The desk question from "
            "the start of the chapter is in the notes, with its solution."
            " Every model in this part trusts the statements. Next: what happens when they lie."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(pp))
        self.wait(0.6)
        self.clear_scene()
