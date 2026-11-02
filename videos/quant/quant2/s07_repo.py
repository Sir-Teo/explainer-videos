from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant2.common import CASH, LOSS, PART, RATE, TRADE, lab, load, node

C_ = {r"h": RATE, r"h'": LOSS, r"g": QC.HOUSE}


def row(*parts, fs=38):
    return cmath(*parts, colors=C_, font_size=fs)


class Repo(VoiceoverScene):
    def construct(self):
        s = load("spiral")
        self.card()
        self.repo()
        self.tower(s)
        self.spiral(s)
        self.specials()

    def card(self):
        c = chapter_card(11, r"Repo, lending and specials", r"Where does the money for leverage come from?",
                         lit=(2008,), part=PART)
        with self.voiceover("Chapter eleven. Repo, securities lending, and specials."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def repo(self):
        a, b = node(r"a fund", TRADE, width=2.4), node(r"a money fund or bank", CASH, width=2.9)
        VGroup(a, b).arrange(RIGHT, buff=4.6).shift(UP * 2.1)
        top = Arrow(a.get_right() + UP * 0.2, b.get_left() + UP * 0.2, buff=0.1, color=RATE, stroke_width=3)
        bot = Arrow(b.get_left() + DOWN * 0.2, a.get_right() + DOWN * 0.2, buff=0.1, color=CASH, stroke_width=3)
        tl = label(r"today: \$102 of Treasuries", font_size=22, color=RATE).next_to(top, UP, buff=0.08)
        bl = label(r"today: \$100 of cash", font_size=22, color=CASH).next_to(bot, DOWN, buff=0.08)
        eq = MathTex(r"\text{interest} = \text{cash} \times r_{\text{repo}} \times \tfrac{\text{days}}{360}:\ "
                     r"\$100\text{m at } 5.25\%,\ 1\text{ day} = \$14{,}583", font_size=30).shift(UP * 0.4)
        kinds = VGroup(
            definition_card(r"Tri-party repo", r"a clearing bank holds the collateral, values it and applies the "
                            r"haircuts; money funds lend to dealers this way", width=4.3, color=RATE, font_size=20),
            definition_card(r"Bilateral repo", r"the two sides deal directly, often cleared (FICC); dealers lend on to "
                            r"hedge funds this way, haircut by haircut", width=4.3, color=TRADE, font_size=20),
            definition_card(r"Securities lending", r"the same trade from the other side: the lender of a stock "
                            r"receives cash and pays a rebate; chapter ten's fee", width=4.3, color=CASH, font_size=20),
        ).arrange(RIGHT, buff=0.25, aligned_edge=UP).next_to(eq, DOWN, buff=0.4)
        cmw = wrapped_label(r"Copeland, Martin and Walker (\textit{Journal of Finance}, 2014): in 2008 tri-party "
                            r"margins and funding stayed fairly stable for most dealers; Lehman's fell sharply before "
                            r"it failed. No system-wide run there; the runs were firm by firm.", 12.4, 19, GREY_A)
        cmw.to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Most leverage is funded overnight by repo: a fund hands over Treasuries and gets cash, and tomorrow repays it "
            "with interest. Legally a sale and repurchase; economically a secured loan, the collateral worth a bit more than "
            "the cash: the haircut. <bookmark mark='a'/> Interest is cash times rate times days over three sixty. "
            "<bookmark mark='b'/> Money funds lend to dealers in tri-party repo, through a clearing bank; dealers lend on to "
            "hedge funds bilaterally; securities lending is the same trade from the stock side. In 2008, Copeland, Martin and "
            "Walker found, tri-party haircuts barely moved for most dealers while Lehman's collapsed: runs on firms, not on "
            "the market."
        ) as vo:
            self.play(FadeIn(a), FadeIn(b), GrowArrow(top), FadeIn(tl), GrowArrow(bot), FadeIn(bl))
            vo.wait_until("a")
            self.play(Write(eq))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(k) for k in kinds], lag_ratio=0.4))
            self.play(FadeIn(cmw))
        self.wait(0.4)
        self.clear_scene()

    def _tower(self, h, n=40, width=3.0, total_h=5.6, base=-2.9, x=-4.0, color=RATE, scale_to=None):
        """Blocks each (1 - h) times the one below: the leverage a haircut allows, drawn as a stack."""
        vals = (1 - h) ** np.arange(n)
        S = scale_to or vals.sum()
        g = VGroup()
        y = base
        for v in vals:
            hh = total_h * v / S
            g.add(Rectangle(width=width * (0.35 + 0.65 * v), height=max(hh - 0.01, 0.005), stroke_width=0,
                            fill_color=color, fill_opacity=0.35 + 0.5 * v).move_to([x, y + hh / 2, 0]))
            y += hh
        return g

    def tower(self, s):
        tw = s["tower"]
        h0, h1 = 0.02, 0.04
        t0 = self._tower(h0, n=60, scale_to=1 / h0)
        t1 = self._tower(h1, n=60, scale_to=1 / h0)
        rows = [
            row(r"1 + (1-h) + (1-h)^2 + \dots", r"=", r"\frac{1}{h}"),
            row(r"\text{at } h \to h':\ \text{sell}", r"=", r"A\Big(1 - \frac{h}{h'}\Big)"),
            row(r"\text{total sold}", r"=", r"\frac{\text{first sale}}{1 - g}"),
        ]
        whys = [why(r"each dollar of collateral borrows $1-h$, which buys more collateral", font_size=20),
                why(r"assets must fall to equity over the new haircut, $E/h'$: half the book, from 2\% to 4\%",
                    font_size=20),
                why(r"sales move the price, cut equity and force more sales: a loop with gain $g$", font_size=20)]
        for r_ in rows:
            r_.scale(0.85)
        step = ladder(self, rows, whys, keep=3, top=3.0, x=2.3, buff=0.55, edge=6.9)
        lev = MathTex(r"h = 2\%:\ 50\times", font_size=34, color=RATE).next_to(t0, UP, buff=0.15)
        sold = np.asarray(tw["sold"], float)
        pr = np.asarray(tw["price"], float)
        bins = VGroup()
        with self.voiceover(
            "The haircut is a leverage limit, and it has a shape. At two percent, a dollar of collateral borrows ninety-eight "
            "cents, which buys more collateral, which borrows again: a tower, each block ninety-eight percent of the one "
            "below, summing to one over the haircut: fifty times. <bookmark mark='a'/> Now the lender raises the haircut to "
            "four percent. The tower may only be half as tall: half the book must be sold at once. <bookmark mark='b'/> And "
            "selling moves the price, which cuts the fund's equity, which shrinks the tower again. The House's deleverage "
            f"function plays it out: sales of {sold[0]:.0f}, then {sold[1]:.1f}, then {sold[2]:.1f} percent of the original "
            f"book, {tw['amplification']:.2f} times the first round in all: the loop's gain turned into a multiplier."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.2) for b in t0], lag_ratio=0.03, run_time=3), FadeIn(lev))
            step(0)
            vo.wait_until("a")
            step(1)
            self.play(Transform(t0, t1), lev.animate.become(MathTex(r"h = 4\%:\ 25\times", font_size=34, color=LOSS)
                                                            .next_to(t1, UP, buff=0.15)), run_time=2)
            vo.wait_until("b")
            step(2)
            q = 100.0 - np.cumsum(sold)
            for k in range(1, min(len(sold), 4)):
                self.play(t0.animate.stretch(q[k] / q[k - 1], 1, about_edge=DOWN), run_time=0.8)
        self.wait(0.4)
        self.clear_scene()

    def spiral(self, s):
        runs = s["runs"]
        hs = ["0.03", "0.04", "0.06"]
        g = axes([0.5, 3.5], [0, 8], x_length=5.0, y_length=3.6, xlabel=r"new haircut (from 2\%)",
                 ylabel=r"total sold / first round", xticks=[1, 2, 3], xfmt=lambda v: ["3\\%", "4\\%", "6\\%"][int(v) - 1],
                 yticks=[0, 2, 4, 6, 8], font_size=16).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        dots = VGroup()
        for i, hk in enumerate(hs, start=1):
            for a in runs[hk]["amp"]:
                dots.add(Dot(ax.c2p(i + np.random.default_rng(len(dots)).uniform(-0.12, 0.12), min(a, 8)),
                             radius=0.05, color=LOSS))
        means = [float(np.mean(runs[hk]["amp"])) for hk in hs]
        drops = [float(np.mean(runs[hk]["drop"])) for hk in hs]
        card = lab_card(r"deleveraging", [
            "def deleverage(E, A, h_new, impact):",
            "    q, p, D = A, 1.0, A - E",
            "    while True:",
            "        s = q - (q * p - D) / (h_new * p)   # forced sale",
            "        if s <= 1e-9 * A: break",
            "        p *= 1 - impact * s                  # sales move the price",
            "        D -= s * p; q -= s",
        ], source="explainer/quant/house/funding.py", width=6.6, font_size=17).to_edge(RIGHT, buff=0.3).shift(UP * 1.2)
        src = note(r"simulated: ten funds with 2--3\% equity on \$100 of assets each; price impact 0.004\% per unit "
                   r"sold; haircuts rise with the fall (Brunnermeier and Pedersen 2009); 8 seeds", font_size=16)
        src.to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "Now ten funds near the limit in the same asset, with haircuts that rise as prices fall: Brunnermeier and "
            f"Pedersen's spiral. <bookmark mark='a'/> To three percent, total selling is {means[0]:.1f} times the first round; "
            f"to four, {means[1]:.1f}; to six, {means[2]:.1f}. Small shocks are amplified most, and every case ends about "
            f"{100 * np.mean(drops):.0f} percent lower. <bookmark mark='b'/> The House's code is the loop itself."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.05, run_time=3))
            vo.wait_until("b")
            self.play(FadeIn(card))
            lab(self, card, [f"h 2% -> 3%: total/first = {means[0]:.2f}",
                             f"h 2% -> 4%: total/first = {means[1]:.2f}",
                             f"h 2% -> 6%: total/first = {means[2]:.2f}"])
        self.wait(0.4)
        self.clear_scene()

    def specials(self):
        rows = [
            row(r"P_{\text{special}} - P_{\text{GC}}", r"=", r"\sum_t \frac{(r_{GC} - r_s)\,P\,\Delta t}{(1+r)^t}"),
            row(r"r_{GC} = 4\%,\ r_s = -1\%,\ 3\text{ months}", r"\Rightarrow", r"\approx 5\% \times 0.25 = 1.25 \text{ per } 100"),
        ]
        whys = [why(r"a bond in demand to borrow lets its owner borrow cash cheaply in repo: that saving is priced in",
                    font_size=20),
                why(r"worked example: the owner saves the rate gap on the bond's value for as long as it stays special",
                    font_size=20)]
        step = ladder(self, rows, whys, keep=2, top=2.2, x=0.0, buff=0.8, edge=6.9)
        head = wrapped_label(r"Duffie (1996), ``Special repo rates'' (\textit{Journal of Finance}): when everyone wants "
                             r"to borrow one bond, its repo rate falls below general collateral; the newest "
                             r"(on-the-run) Treasury is often special, which is part of its premium", 12.0, 21, RATE)
        head.to_edge(UP, buff=0.4)
        q = desk_question(r"A Treasury is special at $-1\%$ for three months while GC repo pays 4\%. What does that do "
                          r"to its price?", width=8.4, font_size=22).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "When many traders short the same bond, they all need to borrow it, and its owner can borrow cash against it "
            "cheaply: the bond is special. Duffie priced it. <bookmark mark='a'/> The owner's saving is priced into the bond. "
            "<bookmark mark='b'/> Special at minus one percent for three months while general collateral pays four: about a "
            "point and a quarter of price, part of why the newest Treasury trades rich. Predict, and check the sign."
        ) as vo:
            self.play(FadeIn(head))
            step(0)
            vo.wait_until("a")
            vo.wait_until("b")
            step(1)
            self.play(FadeIn(q))
        self.wait(1.0)
        self.clear_scene()
