from __future__ import annotations

import numpy as np
from scipy.stats import norm

from explainer.quant import *  # noqa: F403
from videos.quant.quant20.common import BAD, GBMC, PART, RISKY, load

FIRMS = {"BA": "Boeing", "AAL": "American Airlines", "NCLH": "Norwegian Cruise Line"}


class House(VoiceoverScene):
    def construct(self):
        env = load("envelope")
        self.card()
        self.two_sources(load("models"), load("kmv"))
        self.module(env)

    def card(self):
        c = chapter_card(17, r"Rule 20: the credit desk", r"Where should a default probability come from?", part=PART)
        with self.voiceover("Chapter seventeen. The House's twentieth rule, for its credit desk."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def two_sources(self, m, k):
        hx = [-4.4, -1.3, 1.5, 4.3]
        heads = [r"", r"accounts: trees", r"market: Merton", r"what happened"]
        rows = VGroup(VGroup(*[label(h_, font_size=20, color=c_).move_to([x, 2.3, 0]) for h_, x, c_ in
                               zip(heads, hx, [GREY_A, GBMC, RISKY, GREY_A])]))

        def market_pd(tk, ymd):
            f = k[tk]
            d = np.asarray(f["date"])
            i = int(np.searchsorted(d, ymd, side="right") - 1)
            return float(norm.cdf(-f["dtd"][i])) if np.isfinite(f["dtd"][i]) else np.nan
        lines = []
        for tk, nm in FIRMS.items():
            for fy in (2019, 2020):
                r_ = next((x for x in m["firms"][tk] if x["fy"] == fy), None)
                if r_ is None:
                    continue
                lines.append((rf"{nm}, end of {fy}", r_["gbm"], market_pd(tk, fy * 10000 + 1231)))
        for i, (nm, a, b) in enumerate(lines):
            y = 1.55 - 0.55 * i
            rows.add(VGroup(label(nm, font_size=18).move_to([hx[0], y, 0]),
                            MathTex(rf"{100 * a:.1f}\%", font_size=26).move_to([hx[1], y, 0]),
                            MathTex(rf"{100 * b:.1f}\%", font_size=26).move_to([hx[2], y, 0]),
                            label(r"no default", font_size=17, color=GREY_B).move_to([hx[3], y, 0])))
        amr = next(x for x in m["firms"]["AAL"] if x["fy"] == 2010)
        foot = wrapped_label(
            rf"one-year probabilities from two independent sources. The same registered trees gave AMR, American's "
            rf"parent, {100 * amr['gbm']:.0f}\% from its 2010 accounts; it filed for bankruptcy in November 2011. "
            r"Accounts are slow and sharp, markets fast and noisy; where they disagree, someone has to find out why",
            12.4, 18, GREY_A).to_edge(DOWN, buff=0.4)
        title = label(r"Two default probabilities for the same companies", font_size=28).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Rule twenty is about where a default probability comes from. The same three companies, at the end of 2019 "
            "and 2020, seen two ways: from their accounts, by the registered trees, and from their share prices, by "
            "Merton. <bookmark mark='a'/> Before the pandemic, both said safe. <bookmark mark='b'/> A year later both "
            "had jumped, by different amounts: the accounts had caught up with a year without revenue, the market had "
            "already partly recovered. <bookmark mark='c'/> The same trees, given American's parent AMR's accounts for "
            f"2010, said {100 * amr['gbm']:.0f} percent; AMR filed in November 2011. Two sources, one slow and sharp, "
            "one fast and noisy; when they disagree, the desk has to find out why. The rule makes that concrete: "
            "when the two differ by more than a factor of four, the number is not used until an analyst has read "
            "the filings and the market news and written down which source is wrong, and why."
        ) as vo:
            self.play(FadeIn(title), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows[1::2]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows[2::2]], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def module(self, env):
        chart = house_chart(PART, lit=("credit",)).scale(0.62).to_edge(UP, buff=0.2)
        rows = [
            (r"\texttt{merton\_equity}, \texttt{merton\_solve}, \texttt{kmv\_iterate}", r"equity as a call; assets from "
                                                                                       r"prices; distance to default"),
            (r"\texttt{black\_cox\_pd}", r"first passage through a barrier"),
            (r"\texttt{survival}, \texttt{risky\_zero}, \texttt{cds\_legs}", r"hazards, recovery conventions, the two legs"),
            (r"\texttt{bootstrap\_hazard}, \texttt{cds\_upfront}", r"a hazard curve from quotes; the Big Bang's upfronts"),
            (r"\texttt{altman\_z}, \texttt{logit\_fit}, \texttt{GBM}, \texttt{auc}", r"default prediction, scored"),
            (r"\texttt{vasicek\_*}, \texttt{basel\_irb\_k}", r"the large pool and bank capital"),
            (r"\texttt{copula\_defaults}, \texttt{lhp\_tranche\_el}, \texttt{base\_correlation}", r"baskets and tranches"),
        ]
        tab = VGroup(*[VGroup(label(a, font_size=17, color=QC.HOUSE), label(b, font_size=17, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a, b in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 7.2)
        tab.next_to(chart, DOWN, buff=0.25)
        if tab.width > 13.0:
            tab.scale_to_fit_width(13.0)
        rule = wrapped_label(r"Rule 20: every default probability the House uses comes from two independent sources, "
                             r"the market and the accounts, and a disagreement beyond a factor of four is investigated "
                             r"before the number is used; probabilities are recalibrated to the credit cycle, not only ranked; "
                             r"every portfolio's capital is reported under a fat-tailed copula beside the Gaussian; and "
                             r"every credit hedge names the exposure it offsets, and by how much.  "
                             rf"Two models registered here: the counter reads {env['trials']}.", 12.4, 20,
                             QC.HOUSE).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "The credit desk opens with these tools. <bookmark mark='a'/> Merton, forwards and backwards, and the "
            "distance to default; first passage; hazards, survival and the swap's two legs; the bootstrap and the "
            "upfront; default prediction, scored; the large pool and bank capital; and copulas and tranches. "
            "<bookmark mark='b'/> And the twentieth rule. Every default probability comes from two independent "
            "sources, the market and the accounts, and a disagreement beyond a factor of four is investigated before "
            "the number is used. Probabilities are recalibrated to the credit cycle, not only ranked. Every portfolio's "
            "capital is reported under a fat-tailed copula beside the Gaussian one. And every credit hedge names the "
            f"exposure it offsets, and by how much. Two models were registered in this part; the counter reads "
            f"{env['trials']}."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["credit"], color=QC.HOUSE, scale_factor=1.05))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=5))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()
