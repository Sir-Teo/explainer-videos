from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant24.common import BAD, FCOL, GOOD, HML, MKT, PART, SMB, UMD, ask, fit_right, illustration, load

ORDER = ["MKT", "SMB", "HML", "UMD", "RMW", "CMA", "BAB", "QMJ", "TSMOM", "VALMOM"]


class Track(VoiceoverScene):
    def construct(self):
        e = load("envelope")
        self.card()
        self.rules(e)
        self.register(e)
        self.table(e)
        self.bars(e)
        self.years(e)
        self.reading(e)
        self.counter(e)

    def card(self):
        c = chapter_card(13, r"The Track Record opens", r"What did the factors do on data no one had used?", lit=(2021,),
                         part=PART)
        with self.voiceover("Chapter thirteen. Since Part one, five years of data have been sealed. For the first time, "
                            "strategies are opened onto them."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def rules(self, e):
        cards = VGroup(
            desk_question(r"the sealed envelope", r"January 2021 to December 2025, hashed in Part 1; no chapter of this "
                          r"part has read it", width=12.0, font_size=20),
            desk_question(r"registration first", r"each factor registered before opening: its code's hash, its definition "
                          r"(as published, no parameters chosen here), its cost model, and one trial each", width=12.0,
                          font_size=20),
            desk_question(r"one look", r"the envelope opens once per strategy; a second opening with different code is "
                          r"refused, and the result is shown whatever it is", width=12.0, font_size=20),
        ).arrange(DOWN, buff=0.3)
        with self.voiceover(
            "The rules, set in Part one. <bookmark mark='a'/> Every month from January 2021 to December 2025 is "
            "sealed; its fingerprint was recorded, and nothing in this part has looked at it. <bookmark mark='b'/> A "
            "strategy must be registered before the envelope opens: the hash of its code, its definition, its cost "
            "model, and how many versions were tried. <bookmark mark='c'/> It opens once. A second opening with "
            "different code is refused, and the result is shown whatever it is."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                if i:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def register(self, e):
        lines = [r"pit.register(f\"classic_{k}_part24\", code,",
                 r"             dict(RULE, factor=k, cost_per_year=COSTS[k]), trials=1)",
                 r"hd, hx = pit.open_envelope(strat, f\"factors/{k}_monthly\", stamp, x)",
                 r"track.record(strat, 24, x[d <= END], hx, COSTS[k])"]
        card = lab_card(r"Opening the envelope", [ln.replace("\\\"", '"') for ln in lines],
                        source="videos/quant/quant24/compute.py: compute_envelope", width=10.0)
        card.to_edge(UP, buff=0.8)
        foot = wrapped_label(r"ten rows: the market, the five Fama--French factors and momentum (Ken French), and betting "
                             r"against beta, quality minus junk, time-series momentum and the 50/50 value--momentum mix "
                             r"(AQR), each exactly as its authors publish it. Placeholder costs until Part 26: 0.05\% a year "
                             r"for the market, 1\% for most, 1.5\% for BAB and the mix, 3\% for momentum", 12.0, 16,
                             GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Ten rows enter the Track Record: the market, the five Fama-French factors and momentum, and AQR's betting "
            "against beta, quality minus junk, time-series momentum and the value-momentum mix. Each is registered "
            "exactly as its authors publish it, so no parameter was chosen here, and each counts as one trial. "
            "<bookmark mark='a'/> Then the envelope opens, and each row is scored with the same placeholder cost "
            "model, from a twentieth of a percent a year for the market to three percent for momentum, until Part "
            "twenty-six replaces it."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def table(self, e):
        rows = e["rows"]
        hx = [-5.4, -3.4, -1.3, 0.9, 3.0, 5.3]
        heads = [r"factor", r"research, Sharpe", r"2021--25, return", r"2021--25, Sharpe", r"worst drawdown", r"net Sharpe"]
        tab = VGroup(VGroup(*[label(h_, font_size=15, color=GREY_A).move_to([x, 2.95, 0]) for h_, x in zip(heads, hx)]))
        for i, k in enumerate(ORDER):
            r_, h = rows[k]["research"], rows[k]["holdout"]
            y = 2.45 - 0.49 * i
            col = GOOD if h["sharpe"] > 0.3 else (BAD if h["sharpe"] < 0 else WHITE)
            tab.add(VGroup(label(k, font_size=17, color=FCOL[k]).move_to([hx[0], y, 0]),
                           MathTex(rf"{r_['sharpe']:.2f} \pm {r_['sharpe_se']:.2f}", font_size=20).move_to([hx[1], y, 0]),
                           MathTex(rf"{100 * h['mean']:+.1f}\%", font_size=20).move_to([hx[2], y, 0]),
                           MathTex(rf"{h['sharpe']:.2f} \pm {h['sharpe_se']:.2f}", font_size=20, color=col).move_to(
                               [hx[3], y, 0]),
                           MathTex(rf"{100 * h['maxdd']:.0f}\%", font_size=20).move_to([hx[4], y, 0]),
                           MathTex(f"{h['sharpe_net']:.2f}", font_size=20, color=GREY_B).move_to([hx[5], y, 0])))
        with self.voiceover(
            "Here is the Track Record's first page. <bookmark mark='a'/> On the left, each factor's Sharpe ratio in "
            "the research window, with its standard error. <bookmark mark='b'/> On the right, what it did in the five "
            "sealed years: its annual return, its Sharpe ratio, its worst drawdown, and its Sharpe ratio after the "
            "placeholder costs. Notice the standard errors: about a seventh in the long research samples, almost half "
            "in five years. Five years cannot tell a Sharpe ratio of a half from zero."
        ) as vo:
            self.play(FadeIn(tab[0]), LaggedStart(*[FadeIn(r_[0]) for r_ in tab[1:]], lag_ratio=0.1))
            vo.wait_until("a")
            self.play(*[FadeIn(r_[1]) for r_ in tab[1:]])
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(*r_[2:])) for r_ in tab[1:]], lag_ratio=0.2))
        self.wait(1.0)
        self.clear_scene()

    def bars(self, e):
        rows = e["rows"]
        g = axes([-0.6, len(ORDER) - 0.4], [-0.6, 1.3], x_length=10.4, y_length=4.4, xlabel=r"", ylabel=r"Sharpe ratio",
                 xticks=[], yticks=[-0.5, 0, 0.5, 1.0], font_size=13).to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)
        ax = g.ax
        b1, b2, err, labs = VGroup(), VGroup(), VGroup(), VGroup()
        for i, k in enumerate(ORDER):
            for off, s, grp, op in ((-0.2, rows[k]["research"], b1, 0.45), (0.2, rows[k]["holdout"], b2, 0.9)):
                v = s["sharpe"]
                y0, y1 = ax.c2p(0, 0)[1], ax.c2p(0, v)[1]
                grp.add(Rectangle(width=0.34, height=max(abs(y1 - y0), 0.01), stroke_width=0, fill_color=FCOL[k],
                                  fill_opacity=op).move_to([ax.c2p(i + off, 0)[0], (y0 + y1) / 2, 0]))
                if grp is b2:
                    lo, hi = v - s["sharpe_se"], v + s["sharpe_se"]
                    err.add(Line(ax.c2p(i + off, max(lo, -0.6)), ax.c2p(i + off, min(hi, 1.3)), color=GREY_A,
                                 stroke_width=1.5))
            labs.add(label(k, font_size=14, color=FCOL[k]).next_to(ax.c2p(i, -0.6), DOWN, buff=0.1))
        avg_r = np.mean([rows[k]["research"]["sharpe"] for k in ORDER])
        avg_h = np.mean([rows[k]["holdout"]["sharpe"] for k in ORDER])
        side = MathTex(rf"\text{{average}}:\ {avg_r:.2f}\ \to\ {avg_h:.2f}", font_size=24).to_corner(UR, buff=0.5)
        foot = label(r"pale: research window; solid: 2021--2025, with one standard error", font_size=15,
                     color=GREY_A).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "As a picture: pale bars for the research window, solid bars for the sealed years, with one standard "
            "error. <bookmark mark='a'/> The market did better than its history, and so did value and profitability, "
            "value rebounding by more than forty percent over the five years. <bookmark mark='b'/> Size lost money "
            "every year. Momentum, investment, betting against beta and quality earned little, and time-series momentum "
            "far less than its history. <bookmark mark='c'/> The value-momentum mix did almost exactly what it had "
            "always done. On average, the Sharpe ratios fell from about six tenths to a third."
        ) as vo:
            self.play(FadeIn(g), FadeIn(labs), FadeIn(b1), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN if b_.get_center()[1] >= ax.c2p(0, 0)[1] else UP)
                                    for b_ in b2], lag_ratio=0.1), FadeIn(err), run_time=2.5)
            vo.wait_until("b")
            self.play(Indicate(labs[1], color=BAD), Indicate(labs[3]), Indicate(labs[6]), Indicate(labs[8]))
            vo.wait_until("c")
            self.play(Indicate(labs[9], color=GOOD), FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def years(self, e):
        rows = e["rows"]
        sel = ["MKT", "SMB", "HML", "UMD", "TSMOM", "VALMOM"]
        hx = [-4.6, -2.6, -0.8, 1.0, 2.8, 4.6]
        heads = [r"", r"2021", r"2022", r"2023", r"2024", r"2025"]
        tab = VGroup(VGroup(*[label(h_, font_size=17, color=GREY_A).move_to([x, 2.3, 0]) for h_, x in zip(heads, hx)]))
        for i, k in enumerate(sel):
            d = np.asarray(rows[k]["holdout_dates"])
            w = np.asarray(rows[k]["holdout_cum"])
            prev, cells = 1.0, []
            for y in range(2021, 2026):
                m = (d // 100) == y
                end = w[m][-1]
                cells.append(end / prev - 1)
                prev = end
            yy = 1.65 - 0.6 * i
            tab.add(VGroup(label(k, font_size=18, color=FCOL[k]).move_to([hx[0], yy, 0]),
                           *[MathTex(rf"{100 * c:+.0f}\%", font_size=22, color=GOOD if c > 0 else BAD).move_to([hx[j + 1], yy, 0])
                             for j, c in enumerate(cells)]))
        foot = wrapped_label(r"calendar-year returns in the sealed years. 2022, a bear market with rising rates, was the "
                             r"year of value and trend; 2023, of the market and of growth", 12.0, 17, GREY_A).to_edge(
            DOWN, buff=0.5)
        with self.voiceover(
            "Year by year, a few rows. <bookmark mark='a'/> 2022 was the decisive year: the market fell twenty-one "
            "percent as interest rates rose, and value gained thirty-two percent, momentum twenty, and time-series "
            "momentum twenty-five, short the bonds whose prices were falling. <bookmark mark='b'/> In 2023 the market "
            "rose by a fifth and value, momentum and trend all lost. Size lost in every one of the five years. A "
            "factor's five years are a handful of draws, each dominated by the year's one big theme."
        ) as vo:
            self.play(FadeIn(tab[0]), *[FadeIn(r_[0]) for r_ in tab[1:]])
            vo.wait_until("a")
            self.play(*[FadeIn(r_[1:3]) for r_ in tab[1:]])
            vo.wait_until("b")
            self.play(*[FadeIn(r_[3:]) for r_ in tab[1:]], FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def reading(self, e):
        cards = VGroup(
            desk_question(r"decay, as predicted", r"published factors earn less after publication (chapter 2): an average "
                          r"Sharpe ratio falling from 0.57 to 0.35 is in line with McLean and Pontiff", width=12.0,
                          font_size=20),
            desk_question(r"but not significance", r"with standard errors near 0.45, no single row's hold-out differs "
                          r"significantly from its history, and only the mix's is two standard errors above zero", width=12.0,
                          font_size=20),
            desk_question(r"diversification held", r"the mix of value and momentum, negatively correlated by design, "
                          r"delivered its Sharpe ratio again; the single factors scattered around it", width=12.0,
                          font_size=20),
        ).arrange(DOWN, buff=0.3)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        with self.voiceover(
            "How to read it honestly. <bookmark mark='a'/> The factors decayed, roughly as the research on "
            "publication predicts: an average Sharpe ratio from about six tenths to a third. <bookmark mark='b'/> But "
            "with standard errors near a half, no single row is significantly different from its history, and only "
            "one is clearly above zero. Five years are not enough to judge a factor. <bookmark mark='c'/> What did hold up was "
            "diversification: the negatively correlated mix of value and momentum delivered its Sharpe ratio again, "
            "while the single factors scattered around it. That is the result worth remembering."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                if i:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def counter(self, e):
        num = MathTex(r"315", font_size=96, color=QC.HOUSE)
        num2 = MathTex(rf"{e['trials']}", font_size=96, color=QC.HOUSE)
        cap = label(r"the trial counter: configurations tried across the series so far", font_size=22,
                    color=GREY_A).next_to(num, DOWN, buff=0.5)
        foot = wrapped_label(r"ten registrations, one trial each: the definitions came from their authors. Part 25 asks how "
                             r"many trials the authors themselves ran before publishing", 11.0, 18, GREY_A).to_edge(
            DOWN, buff=0.8)
        with self.voiceover(
            "And the trial counter, which records every configuration the series has tried. <bookmark mark='a'/> Ten "
            "registrations, one trial each, take it from three hundred and fifteen to three hundred and twenty-five. "
            "One trial each, because no choice was made here: the definitions came from their authors. "
            "<bookmark mark='b'/> But how many versions did the authors try before publishing? That question, the "
            "factor zoo, is Part twenty-five."
        ) as vo:
            self.play(FadeIn(num), FadeIn(cap))
            vo.wait_until("a")
            self.play(TransformMatchingTex(num, num2))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.5)
        self.clear_scene()
