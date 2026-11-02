from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant4.common import DRIFT, LOSS, MART, P_C, PART, Q_C, load, real_data

KINDS = [("mixture", r"fixed-stake mixture (the House's \texttt{EProcess})", P_C), ("ons", r"online Newton step", MART),
         ("agrapa", r"aGRAPA", Q_C), ("kelly", r"oracle Kelly (knows the edge)", QC.IDEA)]


def _date(d):
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
              "November", "December"]
    return f"{months[(d // 100) % 100 - 1]} {d // 10000}"


class House(VoiceoverScene):
    def construct(self):
        l = load("learner")
        e = load("eprocess")
        cs = load("confseq")
        env = load("envelope_ons")
        self.card()
        self.derive()
        self.replay(l)
        self.compare(l)
        self.real(l, e)
        self.confidence(cs)
        self.lab(l, env)

    def card(self):
        c = chapter_card(16, r"Learning to bet", r"How fast can a bettor find an edge?", part=PART)
        with self.voiceover("Chapter sixteen. Learning to bet."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def derive(self):
        rows = [cmath(r"W_t = \prod_{s \le t} (1 + \lambda_s x_s)", r",", r"\quad \lambda_s \in \mathcal{F}_{s-1},\ "
                      r"|\lambda_s| \le \tfrac12", font_size=38),
                cmath(r"g(\lambda) = \mathbb{E}\log(1 + \lambda x)", r"\approx",
                      r"\lambda\mu - \tfrac12\lambda^2(\sigma^2 + \mu^2) \;\Rightarrow\; \lambda^* \approx "
                      r"\frac{\mu}{\sigma^2 + \mu^2},\ g^* \approx \frac{\mu^2}{2\sigma^2}", font_size=34),
                cmath(r"t_{\text{reject}}", r"\approx", r"\frac{\log(1/\alpha)}{g^*} = \frac{2\log 20}{\text{SR}_d^2}",
                      font_size=38, colors={r"\frac{\log(1/\alpha)}{g^*} = \frac{2\log 20}{\text{SR}_d^2}": LOSS}),
                cmath(r"z_t = \frac{x_t}{1 + \lambda_t x_t},\ A_t = 1 + \sum z^2", r"\Rightarrow",
                      r"\lambda_{t+1} = \operatorname{clip}\Big(\lambda_t + \frac{2}{2 - \log 3}\frac{z_t}{A_t}\Big)",
                      font_size=34, colors={r"\lambda_{t+1} = \operatorname{clip}\Big(\lambda_t + \frac{2}{2 - \log 3}\frac{z_t}{A_t}\Big)": MART}),
                cmath(r"C_t", r"=", r"\{m : W_t(m) < 1/\alpha\}", font_size=40, colors={r"\{m : W_t(m) < 1/\alpha\}": Q_C})]
        whys = [why(r"a bettor's wealth; under $H_0: \mathbb{E}[x_t \mid \mathcal{F}_{t-1}] = 0$ a nonnegative martingale "
                    r"(chapter 4), so Ville applies whatever the stakes"),
                why(r"Taylor: the growth rate is a parabola in the stake; its top is Kelly's fraction (Part 8)"),
                why(r"time to reach 20 at the best stake; a daily Sharpe of 0.05, about 0.8 a year, needs about 2{,}400 "
                    r"days"),
                why(r"online Newton step (Cutkosky and Orabona 2018): learn the stake from the bettor's own gradients"),
                why(r"test every mean $m$ at once and keep the survivors: a confidence sequence, valid at all times")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.6, buff=0.7, edge=6.9)
        with self.voiceover(
            "The House's monitor bets a fixed menu of stakes. Can a bettor learn its stake instead? Its wealth "
            "multiplies by one plus stake times outcome, each stake chosen from the past, so under the null of mean "
            "zero it is a nonnegative martingale, and Ville's inequality holds for any rule at all. "
            "<bookmark mark='a'/> What the rule decides is speed. Expected log growth is a parabola in the stake, "
            "peaking at the Kelly fraction, the edge over the second moment. <bookmark mark='b'/> At the peak, "
            "reaching twenty takes two log twenty over the squared daily Sharpe ratio: a daily point zero five, about "
            "point eight a year, needs about two thousand four hundred days, nearly ten years, for a perfect bettor. "
            "<bookmark mark='c'/> A real bettor learns the stake online, here by an online Newton step on its own log "
            "wealth. <bookmark mark='d'/> And betting against every candidate mean at once, the means no bettor has "
            "beaten form a confidence sequence, valid at every moment simultaneously."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            step(4)
        self.wait(0.4)
        self.clear_scene()

    def replay(self, l):
        steps = np.asarray(l["steps"], float)
        lam, lw = np.asarray(l["lam"]), np.asarray(l["logw"])
        kelly = l["kelly"]
        ck = [0, 25, 50, 100, 200, 350, len(steps) - 1]

        def frame(i):
            j = ck[i]
            dial = Arc(radius=1.8, start_angle=PI, angle=-PI, color=GREY_C, stroke_width=3)
            ticks = VGroup()
            for v in (-0.5, -0.25, 0, 0.25, 0.5):
                a = PI / 2 - v * PI
                p = dial.get_arc_center() + 1.8 * np.array([np.cos(a), np.sin(a), 0])
                ticks.add(MathTex(f"{v:g}", font_size=20, color=GREY_B).move_to(p * 1.0 + 0.3 * np.array(
                    [np.cos(a), np.sin(a), 0])))
            ak = PI / 2 - kelly * PI
            gold = Line(dial.get_arc_center() + 1.55 * np.array([np.cos(ak), np.sin(ak), 0]),
                        dial.get_arc_center() + 2.0 * np.array([np.cos(ak), np.sin(ak), 0]), color=QC.IDEA, stroke_width=6)
            av = PI / 2 - lam[j] * PI
            needle = Arrow(dial.get_arc_center(), dial.get_arc_center() + 1.6 * np.array([np.cos(av), np.sin(av), 0]),
                           buff=0, color=MART, stroke_width=5)
            txt = MathTex(rf"\lambda_t = {lam[j]:.3f}", font_size=30, color=MART).next_to(dial, DOWN, buff=0.3)
            kt = label(rf"gold: Kelly $= {kelly:.3f}$", font_size=18, color=QC.IDEA).next_to(txt, DOWN, buff=0.1)
            return VGroup(dial, ticks, gold, needle, txt, kt)

        rp = TrainingReplay(steps, lw, frame, ck, ylabel=r"$\log_{10}$ wealth of the ONS bettor", xlabel=r"days",
                            color=MART)
        line20 = DashedLine(rp.ax.c2p(0, np.log10(20)), rp.ax.c2p(steps[-1], np.log10(20)), color=LOSS, stroke_width=2)
        head = label(r"10{,}000 days of a strategy with a daily Sharpe of 0.05 (simulated); the stake learns",
                     font_size=22, color=GREY_A).to_edge(UP, buff=0.3)
        cross = l["cross_day"]
        with self.voiceover(
            "Watch one learner. A strategy with a true daily Sharpe ratio of point zero five, simulated for ten "
            "thousand days. On the left, the bettor's stake as a needle on a dial, with Kelly's fraction marked in "
            "gold; on the right, its wealth on a log scale, with the line at twenty. <bookmark mark='a'/> At first "
            "the needle swings wildly: the bettor knows nothing. Then it settles near the gold mark, and the wealth "
            "begins to climb. " + (f"It crosses twenty on day {cross:,}, against about "
                                    f"{l['theory_days']:,.0f} for a bettor who knew the edge from the start."
                                    if cross else "It has not reached twenty within ten thousand days.")
        ) as vo:
            self.play(FadeIn(head), FadeIn(rp), Create(line20))
            vo.wait_until("a")
            rp.play(self, run_time=9)
        self.wait(0.4)
        self.clear_scene()

    def compare(self, l):
        G = l["grid"]
        edges = l["edges"]
        g1 = axes([-0.5, 3.5], [0, 1.05], x_length=5.6, y_length=3.4, xlabel=r"daily Sharpe of the strategy",
                  ylabel=r"share flagged within 10{,}000 days", xticks=[0, 1, 2, 3],
                  xfmt=lambda v: f"{edges[int(v)]:g}", yticks=[0, 0.05, 0.5, 1], font_size=15)
        g2 = axes([-0.5, 3.5], [0, 10000], x_length=5.6, y_length=3.4, xlabel=r"daily Sharpe of the strategy",
                  ylabel=r"median days to flag (10{,}000 = never)", xticks=[0, 1, 2, 3],
                  xfmt=lambda v: f"{edges[int(v)]:g}", yticks=[0, 5000, 10000], font_size=15)
        VGroup(g1, g2).arrange(RIGHT, buff=1.0).to_edge(UP, buff=0.9)
        alpha_line = DashedLine(g1.ax.c2p(-0.5, 0.05), g1.ax.c2p(3.5, 0.05), color=LOSS, stroke_width=1.5)
        marks1, marks2 = VGroup(), VGroup()
        for j, (kind, name, col) in enumerate(KINDS):
            dx = -0.24 + 0.16 * j
            for i, e in enumerate(edges):
                runs = G[f"{kind}|{e}"]
                rates = [r_["rate"] for r_ in runs]
                meds = [r_["median"] for r_ in runs]
                for ax, vals, grp in ((g1.ax, rates, marks1), (g2.ax, meds, marks2)):
                    lo, hi = min(vals), max(vals)
                    grp.add(Line(ax.c2p(i + dx, lo), ax.c2p(i + dx, hi), color=col, stroke_width=5))
                    grp.add(Dot(ax.c2p(i + dx, float(np.mean(vals))), radius=0.045, color=WHITE))
        leg = legend([(c, n) for _, n, c in KINDS], font_size=18).next_to(VGroup(g1, g2), DOWN, buff=0.35)
        med = {k: float(np.mean([r_["median"] for r_ in G[f"{k}|0.05"]])) for k, _, _ in KINDS}
        null_ok = all(max(r_["rate"] for r_ in G[f"{k}|0.0"]) <= 0.08 for k, _, _ in KINDS if k != "kelly")
        ons_wins = med["ons"] < med["mixture"]
        verdict = ("At a Sharpe of point zero five the learner beats the House's fixed menu." if ons_wins else
                   "At a Sharpe of point zero five, the surprise: the House's fixed menu of stakes is faster than the "
                   "learners. A small edge gives the learner little signal to learn from, while the menu already "
                   "holds a stake close to the right one. Learning pays at larger edges, or when the edge drifts.")
        with self.voiceover(
            "Now a fair race. Four bettors: the House's fixed menu, the online Newton learner, a second learner "
            "called aGRAPA that plugs in running estimates of the edge, and an oracle that knows the true edge. "
            "Four strategies, from no edge at all to a daily Sharpe of point one; eight seeds of a hundred runs each, "
            "drawn as bars from the lowest seed to the highest. <bookmark mark='a'/> With no edge, every bettor flags "
            "at most about five percent of the runs: " + ("Ville's promise, kept." if null_ok else
                                                           "close to Ville's promise.") + " "
            "<bookmark mark='b'/> With an edge, the oracle is fastest, as it must be, at "
            f"{med['kelly']:,.0f} days in the median for a Sharpe of point zero five. " + verdict
        ) as vo:
            self.play(FadeIn(g1), FadeIn(g2), Create(alpha_line), FadeIn(leg))
            vo.wait_until("a")
            n_ = len(edges)
            per = 2 * n_
            self.play(LaggedStart(*[FadeIn(VGroup(marks1[j * per: j * per + 2], marks2[j * per: j * per + 2]))
                                    for j in range(len(KINDS))], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(marks1[j * per + 2:(j + 1) * per], marks2[j * per + 2:(j + 1) * per]))
                                    for j in range(len(KINDS))], lag_ratio=0.3), run_time=3)
        self.wait(0.4)
        self.clear_scene()

    def real(self, l, e):
        R = l["real"]
        rows = []
        head = [label(t, font_size=21, color=GREY_B) for t in (r"bet: today keeps yesterday's sign", r"fixed menu",
                                                                 r"ONS learner")]
        names = {"19260701": r"US from July 1926", "19750101": r"US from 1975", "20000101": r"US from 2000",
                 "btc": r"Bitcoin from 2018"}
        for k in ("19260701", "19750101", "20000101", "btc"):
            m_cross, o_cross = e[k]["cross"], R[k]["cross"]
            rows.append([label(names[k], font_size=22),
                         label(_date(m_cross) if m_cross else rf"never (max {e[k]['max']:.1f})", font_size=22,
                               color=P_C),
                         label(_date(o_cross) if o_cross else rf"never (max {R[k]['max']:.1f})", font_size=22,
                               color=MART)])
        grid = VGroup(*head, *[c for r_ in rows for c in r_]).arrange_in_grid(rows=5, cols=3, buff=(0.7, 0.25),
                                                                               col_alignments="lcc")
        grid.to_edge(UP, buff=0.8)
        note_ = wrapped_label(r"the date each bettor's wealth first reached 20; same bets, same data; the ONS tests "
                              r"are registered with the House (four more trials)", 11.0, 20, GREY_B).next_to(
            grid, DOWN, buff=0.4)
        src = real_data(r"Kenneth French's daily US market; Binance BTCUSDT daily; research window to 2020")
        same = all(bool(e[k]["cross"]) == bool(R[k]["cross"]) for k in R)

        def when(src, k):
            return _date(src[k]["cross"]) if src[k]["cross"] else "never"
        verdict = ("The learner reaches the same verdicts as the menu, in every market." if same else
                   "The two bettors disagree on at least one market, so the verdict there depends on the bettor.")
        with self.voiceover(
            "Back to the hook's question, now with the learner. The bet is the same: today keeps yesterday's sign. "
            f"<bookmark mark='a'/> From 1926, the menu crosses twenty in {when(e, '19260701')} and the learner in "
            f"{when(R, '19260701')}. From 1975, in {when(e, '19750101')} and {when(R, '19750101')}. Since 2000: "
            f"{when(e, '20000101')} and {when(R, '20000101')}; Bitcoin since 2018: {when(e, 'btc')} and "
            f"{when(R, 'btc')}. " + verdict
        ) as vo:
            self.play(FadeIn(VGroup(*head)), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*r_)) for r_ in rows], lag_ratio=0.4), FadeIn(note_))
        self.wait(0.4)
        self.clear_scene()

    def confidence(self, cs):
        t = np.asarray(cs["t"])
        lo, hi, mu = (np.asarray(cs[k], float) for k in ("lo_bp", "hi_bp", "mean_bp"))
        g = axes([2018, 2021], [-150, 150], x_length=8.2, y_length=4.4, ylabel=r"Bitcoin's mean daily log return, "
                 r"basis points", xticks=[2018, 2019, 2020, 2021], xfmt=lambda v: f"{int(v)}",
                 yticks=[-150, -50, 0, 50, 150], font_size=17).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        tk = ValueTracker(5.0)

        def bandm():
            i = int(np.clip(tk.get_value(), 5, len(t) - 1))
            return band(ax, t[5:i + 1], np.clip(lo[5:i + 1], -150, 150), np.clip(hi[5:i + 1], -150, 150), Q_C, 0.3)

        bd = always_redraw(bandm)
        lm = tracing(ax, t, np.clip(mu, -150, 150), tk, WHITE, stroke_width=2)
        zero = DashedLine(ax.c2p(2018, 0), ax.c2p(2021, 0), color=GREY_C, stroke_width=1.5)
        side = VGroup(
            label(r"95\% confidence sequence, valid at every day at once", font_size=22, color=Q_C),
            label(r"white: the running mean", font_size=20, color=GREY_A),
            MathTex(rf"\text{{end of 2020: }} [{cs['end'][0]:.0f}, {cs['end'][1]:.0f}]\ \text{{bp}}", font_size=30,
                    color=Q_C),
            wrapped_label(r"returns clipped to $\pm 20\%$ to make them bounded (Waudby-Smith and Ramdas 2024)", 4.4, 18,
                          GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4)
        verdict = ("It still covers zero: three years of Bitcoin cannot tell its mean from nothing." if cs["covers0"]
                   else "It has left zero behind.")
        with self.voiceover(
            "And the confidence sequence. Here is Bitcoin's mean daily return, estimated as the days arrive from "
            "2018. The band is the set of means that no bettor has yet beaten, at ninety-five percent, and unlike an "
            "ordinary confidence interval it is valid on every day at once, so you may watch it as long as you like. "
            f"<bookmark mark='a'/> It narrows as the evidence grows. At the end of 2020 it runs from {cs['end'][0]:.0f} "
            f"to {cs['end'][1]:.0f} basis points a day. " + verdict
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(side[:2]), FadeIn(side[3]))
            self.add(bd, lm)
            vo.wait_until("a")
            self.play(tk.animate.set_value(float(len(t) - 1)), run_time=6, rate_func=linear)
            bd.clear_updaters()
            lm.clear_updaters()
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def lab(self, l, env):
        card = lab_card(r"the House's learning bettor", [
            "class ONSBettor:",
            "    def __init__(self, shape=()):",
            "        self.lam, self.A, self.logw = zeros(shape), ones(shape), zeros(shape)",
            "    def update(self, x):                  # |x| < 1",
            "        self.logw = self.logw + np.log1p(self.lam * x)",
            "        z = x / (1 + self.lam * x)",
            "        self.A = self.A + z * z",
            "        self.lam = np.clip(self.lam + 2 / (2 - np.log(3)) * z / self.A,",
            "                           -0.5, 0.5)",
            "        return np.exp(self.logw)",
        ], source="explainer/quant/house/martingale.py", width=8.6).to_edge(UP, buff=0.35)
        rule = wrapped_label(r"Rule 5: a claim that something beats a fair game is tested with an e-process, valid "
                             r"whenever it is checked; the stake may be learned.", 12.0, 24, QC.HOUSE).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "In the House the learner is ten lines, tested to keep false alarms under five percent. "
            f"<bookmark mark='a'/> On the simulated strategy its stake settles near {l['lam_end']:.2f}. "
            f"<bookmark mark='b'/> The trial counter reads {env['trials']}, and Rule five gains a clause: the stake "
            "may be learned."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            lab_run(self, card, ["b = ONSBettor(); [b.update(x) for x in strategy_days]",
                                 f"lambda (last 1,000 days) = {l['lam_end']:.3f}   log10 W = {l['logw_end']:.2f}"])
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()
