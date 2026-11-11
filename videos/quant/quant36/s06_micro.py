from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant36.common import (ASK_C, BAD, BID_C, GOOD, HURDLE, MICRO_C, MID_C, PART, fit_right, load)


class Micro(VoiceoverScene):
    def construct(self):
        m = load("micro")
        self.answer()
        self.card()
        self.candidates()
        self.weighted_fails()
        self.chain()
        self.curve_g(m)
        self.test(m)
        self.drift_btc()
        self.small_tick(m)
        self.interview(m)
        self.uses()
        self.question()

    def answer(self):
        move = 0.1 / (2 * 8) * 12
        rows = [cmath(r"\Delta p", r"\approx", r"\frac{0.10}{2 \times 8} \times 12", font_size=40),
                cmath(r"", r"=", rf"\${move:.3f}", font_size=40, colors={rf"\${move:.3f}": HURDLE}),
                cmath(r"", r"\approx", r"\tfrac34\ \text{of a tick}", font_size=40)]
        whys = [why(r"the stylised impact: a tick over twice the depth, per unit of imbalance"),
                why(r"twelve bitcoin of net buying against queues of eight"),
                why(r"the regressions put the real slope a little steeper than one over depth, so in thin books slightly "
                    r"more")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The answer to the pause. <bookmark mark='a'/> Ten cents over twice eight, times twelve: <bookmark mark='b'/> "
            f"about {100 * move:.1f} cents, <bookmark mark='c'/> three-quarters of a tick. Twelve bitcoin of net buying is "
            "one and a half queues' worth, and the stylised model moves the mid half a tick per queue."
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

    def card(self):
        c = chapter_card(5, r"The microprice", r"What is the fair price, given the whole state of the top of the book?",
                         part=PART)
        with self.voiceover("Chapter five. Back to the interview question: fair value, given the two best queues. In "
                            "twenty eighteen Sasha Stoikov gave an answer with a definition, a theorem and an estimator. "
                            "We fit it on two days of Bitcoin's book and test it on two others."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def candidates(self):
        rows = [cmath(r"M", r"=", r"\tfrac12 (p^b + p^a)", font_size=38, colors={r"M": MID_C}),
                cmath(r"W", r"=", r"I\,p^a + (1 - I)\,p^b,\qquad I = \frac{q^b}{q^b + q^a}", font_size=34),
                cmath(r"P^{\text{micro}}", r"=", r"\lim_{n\to\infty} \mathbb E[M_{\tau_n} \mid I_t, S_t]", font_size=36,
                      colors={r"P^{\text{micro}}": MICRO_C})]
        whys = [why(r"the mid ignores the queues entirely"),
                why(r"the weighted mid leans toward the side with the smaller queue, the side likely to be eaten first"),
                why(r"Stoikov (2018): the expected mid after many future mid changes $\tau_1 < \tau_2 < \cdots$, given "
                    r"the imbalance $I$ and spread $S$ now")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Three candidates. <bookmark mark='a'/> The mid ignores the queues. <bookmark mark='b'/> The weighted mid "
            "leans toward the side with the smaller queue, the side likely to be eaten first: with the offer nearly "
            "gone it sits almost on the offer. <bookmark mark='c'/> Stoikov's microprice is the expected mid, not at "
            "the next move, but after many future mid changes, given the imbalance and the spread now."
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

    def weighted_fails(self):
        def book(qb, qa, y, title):
            hb = Rectangle(width=2.6 * qb / 10, height=0.5, fill_color=BID_C, fill_opacity=0.75, stroke_width=0)
            ha = Rectangle(width=max(0.08, 2.6 * qa / 10), height=0.5, fill_color=ASK_C, fill_opacity=0.75,
                           stroke_width=0)
            hb.next_to(ORIGIN + UP * y, LEFT, buff=0.05)
            ha.next_to(ORIGIN + UP * y, RIGHT, buff=0.05)
            t = label(title, font_size=18, color=GREY_A).next_to(hb, LEFT, buff=0.35)
            return VGroup(hb, ha, t)
        b1 = book(10, 0.3, 1.6, r"before: the offer nearly gone")
        b2 = book(4, 10, 0.2, r"after the tick up: a fresh offer")
        notes = VGroup(label(r"weighted mid: almost the old offer", font_size=18, color=GREY_A).next_to(b1, RIGHT, buff=0.4),
                       label(r"weighted mid: back below the new mid", font_size=18, color=GREY_A).next_to(b2, RIGHT,
                                                                                                         buff=0.4))
        for n_ in notes:
            fit_right(n_)
        foot = wrapped_label('one stipulated path does not determine conditional expectation; the weighted formula must be checked against the model-specific martingale equation', 11.5, 19,
                             GREY_A).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "The weighted midpoint is not automatically a martingale. <bookmark mark='a'/> In this stipulated sequence it first leans toward a thin offer. <bookmark mark='b'/> After a price move and queue refill it can move back relative to the new midpoint. <bookmark mark='c'/> A drawn path alone does not prove a nonzero conditional expectation; the model's transition law is needed. The weighted formula generally fails the state-adjusted martingale equation. Nor does predictability of a constructed mid estimate establish an executable arbitrage once spreads, fees and risk are included."
        ) as vo:
            self.wait(0.1)
            self.play(FadeIn(b1), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(b2), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def chain(self):
        rows = [cmath(r"x", r"=", r"(I, S)\ \text{bucketed}", font_size=36),
                cmath(r"Q,\ T,\ R", r":", r"\text{no mid move};\ \text{a mid move to state } y;\ \text{its size}",
                      font_size=30),
                cmath(r"G^1", r"=", r"(\mathbb 1 - Q)^{-1} R,\qquad B = (\mathbb 1 - Q)^{-1} T", font_size=34),
                cmath(r"g(x)", r"=", r"\textstyle\sum_{k \ge 0} B^k G^1 \qquad P^{\text{micro}} = M + g(I, S)",
                      font_size=34, colors={r"g(x)": MICRO_C})]
        whys = [why(r"the state: ten imbalance buckets and a spread of one or two ticks"),
                why(r"count, from the 100-ms grid, how often each state goes where, with and without a mid move"),
                why(r"sum over the steps until the next mid move: the expected first change, and the state just after it"),
                why('the estimator sums 401 terms; mirroring centers rewards under valid support and symmetry, while convergence still requires the stated mixing conditions')]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "A fitted finite-state estimator. <bookmark mark='a'/> Ten imbalance buckets and one- or two-tick spreads define twenty nominal states. <bookmark mark='b'/> Count transitions between adjacent retained snapshots, separating zero and nonzero mid changes. Concatenating days can put endpoints next to each other, so a grid lag need not equal elapsed time at a boundary. <bookmark mark='c'/> The first-step inverse gives a first-move reward and post-move operator. Empty count rows are normalized to zero, so stochasticity and support must be checked rather than assumed. <bookmark mark='d'/> Mirroring enforces antisymmetry. It does not prove irreducibility, mixing or Markov sufficiency of the real state. The theorem and the fitted estimator are separate claims."
        ) as vo:
            step(0)
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def curve_g(self, m):
        n = len(m["centers"])
        I = np.asarray(m["centers"], float)
        tick = m["tick"]
        g1 = np.asarray(m["g"][:n], float) / tick
        e1 = np.asarray(m["emp"]["1 s"][:n], float) / tick
        e60 = np.asarray(m["emp"]["60 s"][:n], float) / tick
        top = float(np.ceil(np.abs(g1).max() / 10) * 10)
        g = axes([0, 1], [-top, top], x_length=6.4, y_length=4.6, xlabel=r"imbalance $I$",
                 ylabel=r"adjustment to the mid, ticks", xticks=[0, 0.5, 1], yticks=[-top, 0, top],
                 yfmt=lambda v: f"{v:.0f}", font_size=15).move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        wm = DashedLine(ax.c2p(0, -0.5), ax.c2p(1, 0.5), color=GREY_B, stroke_width=1.8)
        d1 = VGroup(*[Dot(ax.c2p(a, b), radius=0.08, color=MICRO_C) for a, b in zip(I, g1)])
        da = VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=HURDLE) for a, b in zip(I, e1)])
        db = VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=GOOD) for a, b in zip(I, e60)])
        leg = legend([(GREY_B, r"weighted mid"), (MICRO_C, r"Stoikov's microprice"), (HURDLE, r"mean move, next second"),
                      (GOOD, r"mean move, next minute")], font_size=16).to_edge(RIGHT, buff=0.3).shift(UP * 1.6)
        fit_right(leg)
        with self.voiceover(
            f"""Adjustments fitted on the two training-day arrays, displaying the one-tick-spread states. <bookmark mark='a'/> Opposite-size weighting is bounded by half a tick. <bookmark mark='b'/> The many-move fitted adjustment reaches about {abs(g1[-1]):.0f} ticks in the extreme bucket. <bookmark mark='c'/> The one-second fitted mean adjustment there has magnitude {abs(e1[-1]):.0f} ticks. <bookmark mark='d'/> The one-minute table has magnitude {abs(e60[-1]):.0f} ticks there, with a different shape across middle buckets. These are in-sample conditional-mean summaries, not bounds on possible market moves. Day boundaries can enter the concatenated horizon targets."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(wm))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x) for x in d1], lag_ratio=0.08))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(x) for x in da], lag_ratio=0.08))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(x) for x in db], lag_ratio=0.08))
        self.wait(0.4)
        self.clear_scene()

    def test(self, m):
        rows_ = m["rows"]
        hx = [-5.2, -3.4, -1.5, 0.6, 2.9, 5.2]
        head = VGroup(*[label(t, font_size=15, color=GREY_B) for t in (r"test day", r"horizon", r"mid", r"weighted mid",
                                                                         r"Stoikov", r"fitted per horizon")])
        tab = VGroup(head)
        for r in rows_:
            tab.add(VGroup(label(r["day"][5:], font_size=18), label(r["h"], font_size=18),
                           MathTex(r"100", font_size=24, color=MID_C),
                           MathTex(f"{100 * r['wmid'] / r['mid']:.1f}", font_size=24),
                           MathTex(f"{100 * r['micro'] / r['mid']:.0f}", font_size=24, color=MICRO_C),
                           MathTex(f"{100 * r['emp'] / r['mid']:.1f}", font_size=24, color=GOOD)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.4 - 0.62 * j, 0])
        foot = wrapped_label(r"mean squared error of each forecast of the future mid, as a percentage of the mid's; fitted "
                             r"on 16--17 May 2023, tested on 20--21 May", 11.5, 16, GREY_A).to_edge(DOWN, buff=0.5)
        one = [r for r in rows_ if r["h"] == "1 s"]
        worst = max(100 * r["micro"] / r["mid"] - 100 for r in one)
        ten = [r for r in rows_ if r["h"] == "10 s"]
        e_lo = min(100 * (1 - r["emp"] / r["mid"]) for r in ten)
        e_hi = max(100 * (1 - r["emp"] / r["mid"]) for r in ten)
        with self.voiceover(
            f"""Held-out forecast errors on the two weekend days. <bookmark mark='a'/> Each column reports mean squared error as a percentage of the no-adjustment midpoint forecast, normalized to one hundred on the same eligible observations. The weighted midpoint offers a small improvement. The many-move estimator is up to {worst:.0f} percent worse at one second, and remains worse at one minute. <bookmark mark='b'/> A separate conditional-mean table is fitted for each horizon. It reduces ten-second error by {e_lo:.0f} to {e_hi:.0f} percent on these two days, while its one-second result differs by day. No uncertainty interval or net execution test is supplied, and two days do not establish general superiority."""
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:4]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[4:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def drift_btc(self):
        r = load("research")["drift"]["1 s"]
        I = (np.arange(10) + 0.5) / 10
        cols = {"mid": MID_C, "micro": MICRO_C}
        top = float(np.ceil(max(abs(v) for k in cols for v in r[k]["mean"])))
        g = axes([0, 1], [-top, top], x_length=6.4, y_length=4.4, xlabel=r"imbalance $I$",
                 ylabel=r"mean change over the next second, ticks", xticks=[0, 0.5, 1], yticks=[-top, 0, top],
                 yfmt=lambda v: f"{v:.0f}", font_size=15).move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        curves = {k: VGroup(curve(ax, I, r[k]["mean"], cols[k], stroke_width=3),
                            *[Dot(ax.c2p(a, b), radius=0.06, color=cols[k]) for a, b in zip(I, r[k]["mean"])])
                  for k in cols}
        leg = legend([(MID_C, r"mid"), (MICRO_C, r"Stoikov's microprice")], font_size=16)
        leg.to_edge(RIGHT, buff=0.3).shift(UP * 1.6)
        fit_right(leg)
        md = abs(r["mid"]["mean"][-1])
        with self.voiceover(
            f"""A conditional-mean diagnostic, not a complete martingale certification. <bookmark mark='a'/> In the extreme displayed bucket the mid's next nominal second averages {md:.0f} ticks in the direction of imbalance. <bookmark mark='b'/> The fitted microprice changes in the opposite direction, consistent with overshooting. A martingale relative to the full information set must have zero conditional increments for every suitable event; selected bucket means with no robust uncertainty establish neither a universal rejection nor acceptance. The day concatenation can compress boundary time, and overlapping increments are dependent."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(curves["mid"]))
            vo.wait_until("b")
            self.play(Create(curves["micro"]))
        self.wait(0.4)
        self.clear_scene()

    def small_tick(self, m):
        mv = m["move_med"]
        rows = [cmath(r"\text{tick}", r"=", r"\$0.10 \approx 0.04\ \text{bp}", font_size=38),
                cmath(r"|\Delta M|_{100\,\text{ms}}", r"\approx", rf"{mv:.0f}\ \text{{ticks (median move)}}", font_size=34),
                cmath(r"(I, S)", '\\ \\text{may omit}\\ ', '\\text{relevant history}', font_size=38,
                      colors={'\\text{relevant history}': BAD})]
        whys = [why(r"Bitcoin's perpetual is a small-tick market: the tick is tiny against the price and its moves"),
                why(r"between two snapshots a tenth of a second apart, the book typically jumps several ticks at once; "
                    r"the best queues are a thin slice of the book"),
                why(r"after a move the state does not reset: depth beyond the best, recent order flow and Chapter 3's "
                    r"memory all matter, so the chain carries the lean forward too far")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            f"""A practical model boundary. <bookmark mark='a'/> Ten cents near twenty-seven thousand dollars is about four hundredths of a basis point, and a one-tick spread alone does not imply a large-tick regime. <bookmark mark='b'/> Conditional on a nonzero adjacent change in the concatenated training arrays, median absolute midpoint movement is {mv:.0f} ticks. Most unchanged observations are excluded from that median. <bookmark mark='c'/> Depth, past flow and aggregation may make imbalance and spread insufficient. The later conditional-history diagnostic supports that concern without an uncertainty-calibrated universal Markov test or an identified causal explanation of overshoot."""
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

    def interview(self, m):
        n = len(m["centers"])
        I = 500 / 600
        k = min(int(I * n), n - 1)
        adj = m["g_sim"][k] / m["tick"]
        fair = 100.005 + adj * 0.01
        wm = 100 + 0.01 * I
        rows = [cmath(r"I", r"=", r"\frac{500}{500 + 100} = 0.83", font_size=38),
                cmath(r"g", r"\approx", rf"{adj:.2f}\ \text{{tick}}", font_size=38, colors={r"g": MICRO_C}),
                cmath(r"P^{\text{micro}}", r"\approx", rf"\${fair:.4f}", font_size=40,
                      colors={r"P^{\text{micro}}": MICRO_C})]
        whys = [why(r"the bid holds five-sixths of the shares at the best quotes"),
                why(r"the microprice fitted in a large-tick book, the House's queue simulator of Chapter 7, for that "
                    r"bucket, in ticks"),
                why(rf"above the mid of \$100.005, a little below the weighted mid of \${wm:.4f}: lean toward the "
                    r"offer, but not all the way, because after the tick a new offer arrives")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            f"""Return to a conditional model example. <bookmark mark='a'/> In the hundred-dollar interview book, bid size is five-sixths of displayed size. <bookmark mark='b'/> Mapping that bucket to our fitted large-tick simulator gives an adjustment of {adj:.2f} of a tick. The simulator was calibrated to Bitcoin queue rates; transferring its dimensionless adjustment to a one-cent stock is an illustrative rescaling, not a stock valuation. <bookmark mark='c'/> It gives roughly a hundred dollars and eight-tenths of a cent. The weighted midpoint and first-depletion Brownian expectation are different constructions. Real quotes require venue, horizon and cost validation."""
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

    def uses(self):
        cards = VGroup(
            desk_question(r"market making", 'a candidate quote-center signal; test adverse selection, latency and net value: Part 38', width=12.4, font_size=19),
            desk_question(r"execution", 'compare horizon forecasts with spread, fees, fill probability and latency: Part 37', width=12.4, font_size=19),
            desk_question(r"measurement", 'a quote mid already removes mechanical transaction-price bounce; a microprice need not improve error or slippage noise', width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Possible research uses. <bookmark mark='a'/> A validated state signal can inform a maker's quote center, but reduced adverse selection must be tested rather than assumed. <bookmark mark='b'/> An executor can compare a horizon-specific forecast with spread, fees, fill risk and latency. <bookmark mark='c'/> A quote midpoint already removes mechanical transaction-price bid-ask alternation. Replacing it with a microprice need not reduce forecast error or slippage noise. This sample's overshoot is precisely why the benchmark matters."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                if k:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        head = label('A many-move adjustment must still beat the horizon baseline', font_size=29, color=QC.IDEA).to_edge(UP, buff=0.45)
        formula = MathTex('\\mathrm{MSE}_{\\rm mid}=0.60,\\quad\\mathrm{MSE}_{\\rm micro}=3.00,\\quad\\mathrm{MSE}_{h}=0.57\\quad[\\$^2]', font_size=33).move_to(UP * 1.2)
        if formula.width > 12.4:
            formula.scale_to_fit_width(12.4)
        assumptions = wrapped_label('Chosen error summaries on identical held-out observations, not an additional historical fit.', 12.2, 20, GREY_A).move_to(DOWN * 0.1)
        question = wrapped_label('Normalize the errors to mid=100. Report percent worse and percent reduction separately.', 12.2, 25, QC.IDEA).move_to(DOWN * 1.75)
        banner = label(r"Pause: derive the answer and check its assumptions and units.", font_size=19, color=QC.IDEA).to_edge(DOWN, buff=0.35)
        with self.voiceover('On the same stipulated held-out observations, midpoint mean squared error is point six zero squared dollars, a many-move estimate scores three, and a horizon-specific table scores point five seven. Normalize midpoint error to one hundred. Calculate the percentage increase for the many-move estimator and percentage reduction for the table. Does either establish net trading profit?'):
            self.play(FadeIn(head), FadeIn(formula), FadeIn(assumptions), FadeIn(question), FadeIn(banner))
        self.wait(6)
        self.clear_scene()


