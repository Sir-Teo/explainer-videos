from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant43.common import (ACT_C, BAD, COST_C, GOOD, HURDLE, LUCK_C, MKT_C, PART, REC_C, SKILL_C, comma,
                                         fit_right, load)

SHORT = {"classic_bab_part24": r"betting against beta", "classic_cma_part24": r"investment (CMA)",
         "classic_hml_part24": r"value (HML)", "classic_mkt_part24": r"the market", "classic_qmj_part24": r"quality",
         "classic_rmw_part24": r"profitability (RMW)", "classic_smb_part24": r"size (SMB)",
         "classic_tsmom_part24": r"time-series momentum", "classic_umd_part24": r"momentum (UMD)",
         "classic_valmom_part24": r"value and momentum", "kns_sdf_part25": r"the shrinkage SDF",
         "zoo_equal_weight_part25": r"the zoo, equal weight", "kmz_timer_part27": r"a market timer",
         "nn3_coin_ls_part27": r"a network on coins", "sestm_fomc_drift_part28": r"FOMC text",
         "mined_combination_part29": r"mined alphas", "equal_weight_part30": r"1/N", "hrp_part30": r"HRP",
         "lw_gmv_part30": r"shrunk min-variance", "gp_calm_reversal_part31": r"the GP trader",
         "riskparity_part32": r"risk parity", "trend_part32": r"trend", "residual_sscore_part33": r"stat arb",
         "carry_basis_part39": r"crypto carry", "house_ensemble_part43": r"the House's ensemble"}


class Record(VoiceoverScene):
    def construct(self):
        r = load("record")
        e = load("ensemble")
        self.card(r)
        self.rules()
        self.table(r, 0)
        self.table(r, 13)
        self.scatter(r)
        self.families(r)
        self.research_dsr(r)
        self.deflate(r)
        self.luck_bar(r)
        self.surprises(r)
        self.zoo_note()
        self.ensemble(e)
        self.path(e)
        self.verdict(r)
        self.question()

    def card(self, r):
        c = chapter_card(5, r"The Track Record, opened in full", r"What did the House's strategies deliver out of "
                         r"sample?", part=PART)
        sl, sll, mr, mh = r["slope"], r["slope_long"], r["mean_res"], r["mean_hold"]
        with self.voiceover(
            f"Chapter five, and the answer to the pause: the average Sharpe ratio went from {mr:.2f} in research to "
            f"{mh:.2f} in the hold-out, and a regression of one on the other has a slope of {sl:.2f}: about half of each "
            f"strategy's research Sharpe, above the average, survived. On the {r['n_long']} strategies with long "
            f"research windows, the slope is {sll:.2f}. Close to McLean and Pontiff, and this time with no possibility "
            "of choosing which results to show."
        ):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def rules(self):
        rows = [cmath(r"\text{registered}", r":", r"\text{code hash, parameters, cost model, trial count}", font_size=36,
                      colors={r"\text{registered}": REC_C}),
                cmath(r"\text{research}", r":", r"\text{data to 31 December 2020 only}", font_size=38),
                cmath(r"\text{hold-out}", r":", r"\text{2021 to 2025, opened once, shown whatever it said}", font_size=36,
                      colors={r"\text{hold-out}": HURDLE}),
                cmath(r"\text{the counter}", r":", r"\text{every configuration tried, summed}", font_size=38)]
        whys = [why(r"Part 1's sealed envelope: the rule is fixed and hashed before the data are seen"),
                why(r"every choice, from parameters to the strategy itself, was made on this window"),
                why(r"a second opening with different code is refused by the House's own code (Part 26)"),
                why(r"Part 26's deflation needs the number of trials; the House kept it from Part 3 on")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "First, what the record is. <bookmark mark='a'/> Every strategy was registered with a hash of its code, "
            "its parameters, its cost model and the number of configurations tried. <bookmark mark='b'/> Every choice "
            "was made on data to the end of twenty twenty. <bookmark mark='c'/> The sealed hold-out, twenty twenty-one "
            "to twenty twenty-five, was opened once per strategy and shown whatever it said; the House's code refuses "
            "a second look. <bookmark mark='d'/> And the trial counter summed every configuration tried."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def table(self, r, start):
        rows = r["rows"][start:start + 13]
        head = VGroup(*[label(h_, font_size=16, color=QC.IDEA) for h_ in
                        (r"strategy", r"part", r"research SR", r"hold-out SR", r"net", r"trials")])
        tab = VGroup(head)
        for o in rows:
            col = GOOD if o["hold_net"] > 0 else BAD
            tab.add(VGroup(label(SHORT.get(o["name"], o["name"].replace("_", r"\_")), font_size=16, color=GREY_A),
                           label(rf"{o['part']}", font_size=16),
                           label(rf"{o['res_sr']:.2f}", font_size=16, color=MKT_C),
                           label(rf"{o['hold_sr']:.2f} $\pm$ {o['hold_se']:.2f}", font_size=16, color=col),
                           label(rf"{o['hold_net']:.2f}", font_size=16, color=col),
                           label(comma(o["trials"]), font_size=16, color=GREY_B)))
        xs = [-5.0, -1.6, -0.3, 1.9, 4.0, 5.5]
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([xs[i], 3.2 - 0.47 * j, 0])
            row[0].align_to([-6.6, 0, 0], LEFT)
        first = start == 0
        with self.voiceover(
            ("The rows, in the order they were opened. <bookmark mark='a'/> Part twenty-four's ten classic factors, "
             "published long before the hold-out began: the market, value and profitability did well; size lost; "
             "momentum, net of its costs, roughly broke even. <bookmark mark='b'/> Then the factor zoo's shrinkage "
             "portfolios, which did well, and Part twenty-seven's models.") if first else
            ("<bookmark mark='a'/> The rest: text, mined alphas, portfolio construction, the risk-model trader, trend "
             "and risk parity, statistical arbitrage, crypto carry, and the House's own ensemble. <bookmark mark='b'/> "
             "Green is positive net of the House's cost model, red negative. Most are green; few are far from their "
             "standard errors.")
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x_) for x_ in tab[1:8]], lag_ratio=0.15), run_time=2)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x_) for x_ in tab[8:]], lag_ratio=0.15), run_time=2)
        self.wait(0.5)
        self.clear_scene()

    def scatter(self, r):
        rows = r["rows"]
        x = np.array([o["res_sr"] for o in rows])
        y = np.array([o["hold_sr"] for o in rows])
        g = axes([-1, 5], [-1, 3.5], x_length=6.4, y_length=4.6, xlabel=r"research-window Sharpe ratio",
                 ylabel=r"hold-out Sharpe ratio, 2021--2025", xticks=[-1, 0, 1, 2, 3, 4, 5], yticks=[-1, 0, 1, 2, 3],
                 font_size=15).move_to(LEFT * 2.2 + DOWN * 0.2)
        ax = g.ax
        diag = DashedLine(ax.c2p(-1, -1), ax.c2p(3.5, 3.5), color=GREY_C, stroke_width=1.5)
        xx = np.linspace(-1, 5, 50)
        fit = curve(ax, xx, r["intercept"] + r["slope"] * xx, HURDLE, stroke_width=3)
        dots = VGroup(*[Dot(ax.c2p(a_, b_), radius=0.07, color=REC_C if o["name"] != "house_ensemble_part43" else SKILL_C)
                        for a_, b_, o in zip(x, y, rows)])
        side = VGroup(label(r"dashed: no decay", font_size=16, color=GREY_B),
                      label(rf"fit: slope {r['slope']:.2f}, intercept {r['intercept']:.2f}", font_size=17, color=HURDLE),
                      label(rf"long research windows only: slope {r['slope_long']:.2f}", font_size=16, color=GREY_A),
                      label(r"green: the House's ensemble", font_size=16, color=SKILL_C)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(g, RIGHT, buff=0.5)
        fit_right(side)
        sl, ic = r["slope"], r["intercept"]
        with self.voiceover(
            "All twenty-five at once. <bookmark mark='a'/> If nothing decayed, every point would sit on the dashed "
            "line. <bookmark mark='b'/> They sit below it, along a line with slope "
            f"{sl:.2f} and intercept {ic:.2f}: a research Sharpe ratio one point higher bought about half a point more "
            "out of sample. <bookmark mark='c'/> The points far above it, a coin network and the mined alphas, had research "
            "windows of two and three years, so their research Sharpes were themselves barely measured."
        ) as vo:
            self.play(FadeIn(g), FadeIn(diag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_, scale=1.4) for d_ in dots], lag_ratio=0.05), run_time=2)
            vo.wait_until("b")
            self.play(Create(fit), FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    def families(self, r):
        fam = r["families"]
        tab = VGroup(VGroup(*[label(h_, font_size=18, color=QC.IDEA) for h_ in
                              (r"family", r"rows", r"research SR", r"hold-out SR", r"net")]))
        for f in fam:
            col = GOOD if f["net"] > 0 else BAD
            tab.add(VGroup(label(f["family"], font_size=18, color=GREY_A), label(rf"{f['n']}", font_size=18),
                           label(rf"{f['res']:.2f}", font_size=18, color=MKT_C), label(rf"{f['hold']:.2f}", font_size=18, color=col),
                           label(rf"{f['net']:.2f}", font_size=18, color=col)))
        xs = [-4.4, -1.2, 0.6, 2.8, 4.8]
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([xs[i], 2.7 - 0.6 * j, 0])
            row[0].align_to([-6.4, 0, 0], LEFT)
        cl = fam[0]
        with self.voiceover(
            "By family. <bookmark mark='a'/> The classic factors, the most trustworthy because others chose them "
            f"decades ago, went from {cl['res']:.2f} to {cl['hold']:.2f}, and {cl['net']:.2f} after costs. "
            "<bookmark mark='b'/> The factor zoo's shrinkage portfolios and crypto carry kept high Sharpe ratios. Machine "
            "learning and text did better out of sample than in, on short research windows. Portfolio construction "
            "and systematic macro kept modest, positive ones."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[2:]], lag_ratio=0.2), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def research_dsr(self, r):
        rows = sorted([o for o in r["rows"] if o["trials"] > 1], key=lambda o: -o["trials"])
        tab = VGroup(VGroup(*[label(h_, font_size=17, color=QC.IDEA) for h_ in
                              (r"strategy", r"trials", r"research SR", r"deflated", r"hold-out SR")]))
        for o in rows:
            col = GOOD if o["dsr_research"] > 0.95 else (HURDLE if o["dsr_research"] > 0.5 else BAD)
            tab.add(VGroup(label(SHORT.get(o["name"], o["name"]), font_size=17, color=GREY_A), label(comma(o["trials"]), font_size=17),
                           label(rf"{o['res_sr']:.2f}", font_size=17, color=MKT_C),
                           label(rf"{o['dsr_research']:.2f}", font_size=17, color=col),
                           label(rf"{o['hold_sr']:.2f}", font_size=17)))
        xs = [-4.6, -1.4, 0.6, 2.6, 4.6]
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([xs[i], 3.0 - 0.5 * j, 0])
            row[0].align_to([-6.5, 0, 0], LEFT)
        with self.voiceover(
            "Before the hold-out, what did the counter say about the searched strategies? <bookmark mark='a'/> The "
            "deflated Sharpe ratio: the probability that the research Sharpe beats the best of that many trials of "
            "noise. Crypto carry and the portfolio methods passed. <bookmark mark='b'/> The market timer, the text "
            "signal, the coin network and the mined alphas did not: their research could not separate them from luck. "
            "Then two of those four did well anyway, and two did not. The counter measures what research can claim, "
            "not what the future holds."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x_) for x_ in tab[1:6]], lag_ratio=0.15), run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x_) for x_ in tab[6:]], lag_ratio=0.15), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    def deflate(self, r):
        rows = [cmath(r"\text{the counter}", r":", rf"{comma(r['trials'])}\ \text{{configurations, {r['n_registered']} registrations}}",
                      font_size=36, colors={r"\text{the counter}": REC_C}),
                cmath(r"\text{mined alphas}", r":", r"13{,}010\ \text{trials: research SR } 1.73 \to \text{DSR } 0.19", font_size=36,
                      colors={r"\text{mined alphas}": BAD}),
                cmath(r"\text{the classics}", r":", r"1\ \text{trial each: DSR} \approx 1", font_size=38, colors={r"\text{the classics}": GOOD}),
                cmath(r"\text{lesson}", r":", r"\text{deflation is about selection, not about the strategy}", font_size=34)]
        whys = [why(r"every configuration tried across the series, from Part 3's accounting signals to this part's one"),
                why(r"deflated by its own 13,010 trials, three years of research could not distinguish it from the best "
                    r"of noise; it then earned 2.78 in the hold-out, 1.64 net"),
                why(r"factors chosen by others, decades before, carry no selection of the House's own"),
                why(r"a low deflated Sharpe says the research could not tell; only the hold-out can")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        tr = r["trials"]
        with self.voiceover(
            f"The trial counter, final: <bookmark mark='a'/> {tr:,.0f} configurations across the series. "
            "<bookmark mark='b'/> The most searched strategy, Part twenty-nine's mined alphas, tried thirteen thousand "
            "and ten configurations; deflated by them, its research record was indistinguishable from the best of "
            "noise. It then did well in the hold-out. <bookmark mark='c'/> The classic factors, chosen by others "
            "decades earlier, carry no selection of the House's own. <bookmark mark='d'/> The lesson: a low deflated "
            "Sharpe ratio means the research could not tell. It does not mean the strategy fails."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def luck_bar(self, r):
        rows = [cmath(r"\text{se}(\widehat{SR})", r"\approx", rf"{r['median_se']:.2f}\ \ \text{{(five years)}}", font_size=40,
                      colors={r"\text{se}(\widehat{SR})": LUCK_C}),
                cmath(r"\mathbb E\max_{25}", r"\approx", rf"{r['best_null']:.2f}", font_size=42, colors={r"\mathbb E\max_{25}": HURDLE}),
                cmath(r"\text{above it}", r":", rf"{len(r['above'])}\ \text{{of 25 rows}}", font_size=40, colors={r"\text{above it}": SKILL_C})]
        whys = [why(r"the median standard error of a hold-out Sharpe ratio across the rows"),
                why(r"Part 26's expected maximum of 25 zero-skill Sharpe ratios with that error: the luck bar for the "
                    r"best row"),
                why(r"the zoo's two portfolios, value and momentum, crypto carry, the mined alphas and the coin network")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        se, bn, na = r["median_se"], r["best_null"], len(r["above"])
        with self.voiceover(
            "And the hold-out has its own multiple-testing problem: twenty-five rows were opened. "
            f"<bookmark mark='a'/> A five-year Sharpe ratio has a standard error of about {se:.2f}. "
            f"<bookmark mark='b'/> So the best of twenty-five strategies with no edge at all would show about "
            f"{bn:.2f}. <bookmark mark='c'/> {na} rows clear that bar: the zoo's two portfolios, value and momentum, "
            "crypto carry, the mined alphas and the coin network."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def surprises(self, r):
        cards = VGroup(
            desk_question(r"what held", r"the shrinkage SDF and the zoo's equal weight, value and momentum combined, "
                          r"crypto carry, and the market itself", width=12.4, font_size=19),
            desk_question(r"what did not", r"size, a market timer, the GP trader, whose crypto universe was dominated "
                          r"by near-riskless stablecoins (Part 31)", width=12.4, font_size=19),
            desk_question(r"what to make of it", r"five years is short: a hold-out Sharpe ratio has a standard error "
                          r"near 0.45, so most rows cannot be told from their research values or from zero", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "What held, and what did not. <bookmark mark='a'/> The shrinkage portfolios of the factor zoo, value and "
            "momentum together, crypto carry, and the market itself all did well. <bookmark mark='b'/> Size lost, the "
            "market timer lost, and the risk-model trader was undone by stablecoins in its universe. "
            "<bookmark mark='c'/> And the honest caveat: five years is short. A hold-out Sharpe ratio has a standard "
            "error near nought point four five, so most rows cannot be told apart from their research values, or from "
            "zero."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def zoo_note(self):
        cards = VGroup(
            desk_question(r"why the zoo's rows did so well", r"their hold-out covers 2021--23 only, the data the "
                          r"open-source library had, and the shrinkage portfolio spreads across hundreds of published "
                          r"long-short anomalies", width=12.4, font_size=19),
            desk_question(r"what it does not mean", r"the returns are of paper portfolios, before the costs of trading "
                          r"small and illiquid legs; Part 25 charged a cost model, which cannot be exact", width=12.4,
                          font_size=19),
            desk_question(r"what it does mean", r"published anomalies, combined and shrunk, kept much of their "
                          r"premium in three years they had never seen", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "A word on the brightest rows. <bookmark mark='a'/> The factor zoo's portfolios were scored on twenty "
            "twenty-one to twenty-three, the years their open-source library covered, and they spread across hundreds "
            "of published anomalies. <bookmark mark='b'/> They are paper portfolios, and the costs of trading their "
            "small and illiquid legs can only be estimated. <bookmark mark='c'/> But combined and shrunk, published "
            "anomalies kept much of their premium in three years they had never seen."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def ensemble(self, e):
        row = e["row"]
        res, hold = row["research"], row["holdout"]
        keys, w = e["keys"], e["weights"]
        bars = VGroup()
        for i, (k, w_) in enumerate(zip(keys, w)):
            b = Rectangle(width=0.55, height=6.0 * w_, stroke_width=0, fill_color=REC_C, fill_opacity=0.85)
            b.move_to([-5.7 + 0.72 * i, -2.0 + 3.0 * w_, 0])
            t = label(k, font_size=12, color=GREY_A).rotate(PI / 4).next_to(b, DOWN, buff=0.12)
            bars.add(VGroup(b, t))
        info = VGroup(label(r"the House's ensemble: equal risk across ten classic factors", font_size=19, color=REC_C),
                      label(rf"research 1993--2020: Sharpe {res['sharpe']:.2f}, net {res['sharpe_net']:.2f}", font_size=18, color=MKT_C),
                      label(rf"hold-out 2021--2025: Sharpe {hold['sharpe']:.2f} $\pm$ {hold['sharpe_se']:.2f}, net "
                            rf"{hold['sharpe_net']:.2f}", font_size=18, color=SKILL_C),
                      label(rf"worst drawdown {100 * hold['maxdd']:.1f}\%; one trial", font_size=17, color=GREY_A)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.5).shift(UP * 0.4)
        rs, rn, hs, hn = res["sharpe"], res["sharpe_net"], hold["sharpe"], hold["sharpe_net"]
        with self.voiceover(
            "And the House's own row, registered in this part with one trial. <bookmark mark='a'/> Equal risk across "
            "the ten classic factors, weights fixed from their volatilities in the decade to twenty twenty. "
            f"<bookmark mark='b'/> In research, a Sharpe ratio of {rs:.2f}, {rn:.2f} after costs. "
            f"<bookmark mark='c'/> In the hold-out, {hs:.2f}, and {hn:.2f} after costs. Diversification across "
            "published premia, the dullest strategy in the series, kept most of its promise."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_, shift=UP * 0.2) for b_ in bars], lag_ratio=0.1), FadeIn(info[0]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(info[1]))
            vo.wait_until("c")
            self.play(FadeIn(info[2]), FadeIn(info[3]))
        self.wait(0.4)
        self.clear_scene()

    def path(self, e):
        c = np.asarray(e["holdout_cum"], float)
        t = 2021 + np.arange(len(c)) / 12
        g = axes([2021, 2026], [0.85, float(c.max()) * 1.05], x_length=7.6, y_length=4.2, xlabel=r"the hold-out, monthly",
                 ylabel=r"the House's ensemble, growth of 1", xticks=[2021, 2022, 2023, 2024, 2025, 2026],
                 yticks=[0.9, 1.0, 1.1, 1.2], font_size=15).move_to(LEFT * 1.0 + DOWN * 0.2)
        ln = curve(g.ax, t, c, REC_C, stroke_width=3)
        end = c[-1]
        with self.voiceover(
            "The House's ensemble through the hold-out, month by month. <bookmark mark='a'/> Through the inflation "
            "shock of twenty twenty-two, when stocks and bonds fell together, the diversified premia held up. "
            f"<bookmark mark='b'/> One unit at the start of twenty twenty-one became {end:.2f} by the end of twenty "
            "twenty-five, before costs: steady, unspectacular, and as registered."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Create(ln), run_time=3)
            vo.wait_until("b")
            self.play(Indicate(ln, color=SKILL_C))
        self.wait(0.4)
        self.clear_scene()

    def verdict(self, r):
        sp, ss, pi0 = 100 * r["share_positive"], 100 * r["share_sig"], r["pi0"]
        rows = VGroup(
            label(rf"positive hold-out Sharpe: {sp:.0f}\% of rows", font_size=24, color=GOOD),
            label(rf"significant at 5\% on their own: {ss:.0f}\%", font_size=24, color=HURDLE),
            label(rf"Storey's estimate of rows with no edge: {pi0:.2f}, on 25 rows, very roughly", font_size=22, color=LUCK_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(UP * 0.2)
        with self.voiceover(
            f"The verdict on the record. <bookmark mark='a'/> {sp:.0f} percent of the rows had a positive hold-out "
            f"Sharpe ratio. <bookmark mark='b'/> But only {ss:.0f} percent were significant on their own, in five years. "
            "<bookmark mark='c'/> And Storey's estimator, from Chapter two, puts the share with no edge at about "
            f"{pi0:.2f}, an estimate from twenty-five rows that the research chapter will put in its place. Most of what "
            "the House found was real, smaller than it looked, and mostly published premia."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"nine pricing models were fitted to the same options surface across Parts 10 to 14. Which fitted "
                       r"best, and was it the most complex?")
        with self.voiceover(
            "Pause and predict. Nine pricing models were fitted to the same options surface across Parts ten to "
            "fourteen. Which fitted best, and was it the most complex?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
