from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant28.common import BAD, GOOD, HURDLE, PART, WORD, fit_right, illustration, load

KINDS = [(r"satellite images", r"cars in retailers' car parks; oil tanks' floating roofs; crops", QC.SPOT),
         (r"card and receipt panels", r"anonymised spending by merchant, weeks before a company reports", QC.CASH),
         (r"web and app data", r"traffic, downloads, prices scraped from online shops", QC.OPTION),
         (r"job postings", r"who is hiring, for what, where", QC.VEGA),
         (r"shipping and flights", r"ship positions, cargo, corporate jets", QC.DELTA),
         (r"text", r"news, filings, calls, social media: this part", WORD)]


class AltData(VoiceoverScene):
    def construct(self):
        a = load("altdata")
        self.card()
        self.kinds()
        self.space()
        self.kyle(a)
        self.decay(a)
        self.question()

    def card(self):
        c = chapter_card(14, r"Alternative data", r"What is a data set worth once everyone has bought it?", part=PART)
        with self.voiceover("Chapter fourteen. Text is one kind of alternative data: information that is not a price, a "
                            "volume or a filed number. What is a new data set worth, and what is it worth once everyone "
                            "has bought it?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def kinds(self):
        rows = VGroup()
        for name, what, col in KINDS:
            r_ = VGroup(label(name, font_size=24, color=col), label(what, font_size=19, color=GREY_A)).arrange(RIGHT, buff=0.4)
            rows.add(r_)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.33).move_to(DOWN * 0.1)
        head = label(r"what the industry buys", font_size=30).to_edge(UP, buff=0.5)
        with self.voiceover(
            "The menu is long. <bookmark mark='a'/> Satellite images of car parks, oil tanks and fields; panels of "
            "anonymised card spending that show a retailer's sales weeks before it reports; web traffic and app "
            "downloads and scraped prices; job postings; ships and planes. <bookmark mark='b'/> And text, the subject "
            "of this part. What they share: each measures something about a company's business before the company "
            "says it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[:5]], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(FadeIn(rows[5]))
        self.wait(0.4)
        self.clear_scene()

    def space(self):
        card = firm_card(r"Katona, Painter, Patatoukas and Zeng (2025)", r"`On the capital market consequences of big "
                         r"data: evidence from outer space': RS Metrics' daily counts of cars in the car parks of major "
                         r"U.S. retailers, 2011--2017, sold to investors",
                         numbers=((r"+", r"buyers could trade profitably ahead of retailers' quarterly reports, above "
                                         r"all bad-news quarters"),
                                  (r"\uparrow", r"more informed short selling; less informed buying by individuals"),
                                  (r"\downarrow", r"lower liquidity around the reports of covered retailers")),
                         source=r"\textit{Journal of Financial and Quantitative Analysis} 60 (2025)", kind=r"Paper file",
                         width=10.6, font_size=22).move_to(ORIGIN)
        with self.voiceover(
            "The cleanest evidence comes from space. <bookmark mark='a'/> Katona, Painter, Patatoukas and Zeng "
            "studied the satellite counts of cars in American retailers' car parks that were sold to "
            "investors over 2011 to 2017. Those who bought them could trade profitably ahead of quarterly reports, especially "
            "the bad ones. <bookmark mark='b'/> But the market as a whole did not become better informed in the way "
            "you might hope: short sellers with the data traded more, individual buyers without it lost out, and "
            "liquidity around the covered retailers' reports fell. Unequal access to data can widen the gap between "
            "investors without improving prices."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(Indicate(card.submobjects[-1], color=QC.FIRM, scale_factor=1.02))
        self.wait(0.4)
        self.clear_scene()

    def kyle(self, a):
        rows = [cmath(r"v \sim N(0, \sigma_v^2)", r",", r"u \sim N(0, \sigma_u^2),\quad x_n = \beta v,\quad p = \lambda\big(\textstyle"
                      r"\sum_n x_n + u\big)", font_size=30),
                cmath(r"\lambda", r"=", r"\frac{\sigma_v\sqrt N}{(N + 1)\,\sigma_u},\qquad \beta = \frac{\sigma_u}{\sigma_v\sqrt N}",
                      font_size=32, colors={r"\lambda": HURDLE}),
                cmath(r"\mathbb E[\pi_n]", r"=", r"\frac{\sigma_u\sigma_v}{(N + 1)\sqrt N},\qquad \frac{\operatorname{Var}(v) - "
                      r"\operatorname{Var}(v \mid p)}{\operatorname{Var}(v)} = \frac{N}{N + 1}", font_size=30,
                      colors={r"\mathbb E[\pi_n]": GOOD})]
        whys = [why(r"Kyle (1985) with $N$ funds that bought the same data: each sees the value $v$, noise traders "
                    r"bring $u$, a market maker sets the price from total order flow"),
                why(r"the symmetric equilibrium (Admati and Pfleiderer 1988's case of a common signal)"),
                why(r"each buyer's profit falls like $N^{-3/2}$, and the price reveals $N/(N + 1)$ of the signal")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The arithmetic of a shared data set is Kyle's model of an informed trader, which Part thirty-five derives, "
            "with more than one insider. "
            "<bookmark mark='a'/> N funds buy the same data, so each knows the same value; noise traders add their "
            "orders; a market maker prices the total. <bookmark mark='b'/> In equilibrium each fund trades less "
            "aggressively as N grows, because the others are trading on the same thing. <bookmark mark='c'/> Each "
            "fund's expected profit falls like N to the minus three halves, and the price reveals N over N plus one of "
            "the information. One buyer keeps half of it secret; ten buyers, about one eleventh."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def decay(self, a):
        Ns = np.asarray(a["Ns"], float)
        each = np.asarray(a["each"], float)
        g = axes([0, 40], [0, 0.55], x_length=6.0, y_length=4.0, xlabel=r"funds that bought the data, $N$",
                 ylabel=r"each fund's expected profit ($\sigma_u\sigma_v = 1$)", xticks=[1, 10, 20, 30, 40],
                 yticks=[0, 0.25, 0.5], font_size=14).move_to(LEFT * 3.3 + DOWN * 0.2)
        ax = g.ax
        c1 = curve(ax, Ns, each, GOOD, stroke_width=3)
        sims = VGroup(*[Dot(ax.c2p(s_["N"], s_["each"]), radius=0.07, color=HURDLE) for s_ in a["sim"]])
        p = a["path"]
        yrs = np.asarray(p["years"], float)
        g2 = axes([yrs[0], yrs[-1]], [0, 0.55], x_length=5.4, y_length=4.0, xlabel=r"year (a stylised adoption curve)",
                  ylabel=r"each buyer's profit", xticks=[2010, 2015, 2020, 2025], yticks=[0, 0.25, 0.5],
                  font_size=14).move_to(RIGHT * 3.5 + DOWN * 0.2)
        ax2 = g2.ax
        c2 = curve(ax2, yrs, p["each"], BAD, stroke_width=3)
        nlab = VGroup(*[label(rf"{int(n)}", font_size=13, color=GREY_B).move_to(ax2.c2p(y, e) + UP * 0.25)
                        for y, n, e in zip(yrs[::3], np.asarray(p["N"])[::3], np.asarray(p["each"])[::3])])
        sim_txt = ", ".join(f"{s_['each']:.3f}" for s_ in a["sim"][:3])
        with self.voiceover(
            "Draw it. <bookmark mark='a'/> Each fund's profit against the number of funds with the data: half the "
            "maximum is gone by the second buyer. The dots are a simulation of the market, two hundred "
            f"thousand draws each, landing on the formula: {sim_txt} for one, two and five buyers. "
            "<bookmark mark='b'/> Now let a vendor sell the data to more funds each year, along an S-shaped adoption "
            "curve. The profit of being a buyer collapses within a few years of the data's launch, long before most "
            "of the market has heard of it. The edge in alternative data is in being early, and it does not last."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Create(c1), FadeIn(sims))
            vo.wait_until("b")
            self.play(FadeIn(g2), Create(c2), FadeIn(nlab), run_time=2)
        self.add(illustration(r"a model: Kyle with $N$ informed traders; the adoption curve is stylised"))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a data set's buyers go from 4 to 9. By what factor does each buyer's expected profit fall? "
                       r"And the buyers' total?")
        with self.voiceover(
            "Pause and predict. A data set's buyers go from four to nine. By what factor does each buyer's profit fall, "
            "and what happens to the buyers' total?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
