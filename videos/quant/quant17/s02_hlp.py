from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant17.common import BAD, GOOD, NET, OPT, PART, REF, illustration, load


class HLP(VoiceoverScene):
    def construct(self):
        h = load("hlp")
        self.card()
        self.idea(h)
        self.curve(h)
        self.hedge(h)

    def card(self):
        c = chapter_card(1, r"Learning a pricing formula", r"Can a network learn Black--Scholes from prices alone?",
                         part=PART)
        with self.voiceover("Chapter one. Learning a pricing formula."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def idea(self, h):
        rows = [cmath(r"\frac{C}{K}", r"=", r"f_\theta\!\left(\frac{S}{K},\ T - t\right)", font_size=42,
                      colors={r"\frac{C}{K}": OPT}),
                cmath(r"\Delta", r"=", r"\frac{\partial f_\theta}{\partial (S/K)}", font_size=42, colors={r"\Delta": NET})]
        whys = [why(r"Hutchinson, Lo and Poggio (1994): no model, only prices; a call's price per unit of strike depends on "
                    r"moneyness and time (Merton's homogeneity), so a network with two inputs can learn it"),
                why(r"the hedge comes free: differentiate the network. The test of a pricing formula is not its fit but "
                    r"its hedge")]
        step = ladder(self, rows, whys, keep=2, top=2.4, x=-0.6, buff=1.1, edge=6.9)
        n = h["n_train"]
        foot = wrapped_label(rf"trained on {n:,} prices: ten simulated two-year histories, with calls listed every month "
                             r"at five strikes around the price and three months to expiry, as an exchange would list them; "
                             r"HLP used the same design, then S\&P 500 futures options from 1987 to 1991".replace(",", "{,}", 1),
                             11.6, 20, GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "In 1994 James Hutchinson, Andrew Lo and Tomaso Poggio asked a question that sounds modern: could a "
            "learning network discover an option pricing formula from prices alone, with no model at all? A call's "
            "price per unit of strike depends only on moneyness and time to expiry, so the network needs just two "
            "inputs. <bookmark mark='a'/> And the hedge comes free: differentiate the network with respect to the "
            "price. <bookmark mark='b'/> They trained on simulated histories with options listed as an exchange lists "
            "them, then on S&P 500 futures options from 1987 to 1991. We repeat the simulated experiment, with a small "
            "modern network."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def curve(self, h):
        c = h["curve"]
        x, yn, yb = np.asarray(c["x"]), np.asarray(c["net"]), np.asarray(c["bs"])
        g = axes([0.8, 1.2], [0, 0.22], x_length=7.2, y_length=4.4, xlabel=r"moneyness $S/K$",
                 ylabel=r"call price per unit of strike, $C/K$", xticks=[0.8, 0.9, 1.0, 1.1, 1.2],
                 yticks=[0, 0.1, 0.2], font_size=15).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        ax = g.ax
        ref = DashedVMobject(curve(ax, x, yb, REF, stroke_width=2.5), num_dashes=40)
        net = curve(ax, x, yn, NET, stroke_width=4)
        leg = legend([(REF, r"Black--Scholes (never shown to the network)"), (NET, r"the network")], font_size=17)
        leg.next_to(g, UP, buff=0.1).align_to(g, LEFT)
        err = np.abs(yn - yb).max() * 100
        side = wrapped_label(rf"six weeks to expiry: the learned curve sits within {err:.2f}\% of the strike of the formula "
                             r"that generated the data, everywhere in the range it was trained on", 4.2, 19,
                             GREY_A).to_edge(RIGHT, buff=0.5)
        src = illustration(r"20\% volatility, zero rates; a three-layer network of 64 units")
        with self.voiceover(
            "Here is what the network learned, six weeks before expiry, against the Black–Scholes formula it never saw. "
            f"<bookmark mark='a'/> The two curves lie within {err:.2f} percent of the strike everywhere in the range it "
            "was trained on."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(ref), FadeIn(leg[0]))
            vo.wait_until("a")
            self.play(Create(net), FadeIn(leg[1]), FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def hedge(self, h):
        te = h["tracking_mean_abs"]
        bars = VGroup()
        mx = max(te.values()) * 1.25
        for i, (k, name, col) in enumerate((("bs", r"Black--Scholes delta", REF), ("net", r"the network's delta", NET))):
            hgt = te[k] / mx * 4.0
            r_ = Rectangle(width=1.6, height=hgt, fill_color=col, fill_opacity=0.85, stroke_width=0)
            r_.move_to([-3.5 + 3.2 * i, -2.2 + hgt / 2, 0])
            bars.add(VGroup(r_, MathTex(f"{te[k]:.2f}", font_size=34, color=col).next_to(r_, UP, buff=0.15),
                            label(name, font_size=22, color=col).next_to(r_, DOWN, buff=0.2)))
        head = label(r"average hedging error per option, held to expiry", font_size=26).to_edge(UP, buff=0.8)
        ratio = te["net"] / te["bs"]
        pct = 100 * (ratio - 1)
        side = wrapped_label(rf"rebalanced daily on 200 fresh at-the-money options: the network's tracking error is "
                             rf"within {pct:.0f}\% of the true formula's, learned from prices alone. HLP found the same in "
                             r"simulation, sometimes better, since rebalancing daily is itself an error; on S\&P 500 futures "
                             r"options, 1987--1991, their networks beat Black--Scholes in many cases", 4.6, 20,
                             GREY_A).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "The real test is the hedge. Two hundred fresh options, held to expiry and rebalanced daily, once with the "
            "true Black–Scholes delta and once with the network's own derivative. <bookmark mark='a'/> The network "
            f"hedges almost exactly as well as the formula that generated its data: its tracking error is within "
            f"{pct:.0f} percent, learned from prices alone. Hutchinson, Lo and Poggio's networks did the same in "
            "simulation, sometimes "
            "better, because rebalancing once a day is itself an error; and on S&P 500 futures options from 1987 to "
            "1991, where Black–Scholes is itself wrong, they beat it in many cases. Thirty years later, this part asks "
            "what networks can do that formulas cannot."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bars[0]))
            vo.wait_until("a")
            self.play(FadeIn(bars[1]), FadeIn(side))
        self.wait(0.5)
        self.clear_scene()
