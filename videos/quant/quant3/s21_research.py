from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant3.common import EQUITY, GAIN, LOSS, PART, PRICE, VALUE, load


def comma(n) -> str:
    return f"{int(n):,}".replace(",", "{,}")


class Research(VoiceoverScene):
    def construct(self):
        t = load("ohlson_theory")
        self.card()
        self.dynamics()
        self.derive()
        self.check(t)
        self.sensitivity(t)
        self.estimate(t)
        self.open_problems()
        self.question()

    def card(self):
        c = research_card(r"Ohlson's information dynamics", r"How long do abnormal earnings last, and what is that "
                          r"worth?", part=PART)
        with self.voiceover("For the researcher: Chapter 8's residual-income value needs a forecast of every future "
                            "abnormal earning. James Ohlson's model of how they evolve turns it into a formula, and the "
                            "data say how long excess profits last."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c), run_time=0.4)

    def dynamics(self):
        rows = [cmath(r"b_t", r"=", r"b_{t-1} + x_t - d_t", font_size=34, colors={r"b_t": EQUITY}),
                cmath(r"x^a_t", r"=", r"x_t - r\,b_{t-1}", font_size=34, colors={r"x^a_t": VALUE}),
                cmath(r"x^a_{t+1}", r"=", r"\omega\,x^a_t + \nu_t + \varepsilon_{1,t+1}", font_size=34,
                      colors={r"x^a_{t+1}": VALUE}),
                cmath(r"\nu_{t+1}", r"=", r"\gamma\,\nu_t + \varepsilon_{2,t+1}", font_size=34, colors={r"\nu_{t+1}": PRICE})]
        whys = [why(r"clean surplus (Chapter 8): book equity changes only by earnings and by dividends paid"),
                why(r"abnormal earnings: what the firm earns beyond the required return on its book"),
                why(r"Ohlson (1995): they decay at rate $\omega$, as competition erodes excess profits, and are pushed by "
                    r"'other information' $\nu$ that is not yet in the accounts (an order book, a patent, an analyst's "
                    r"forecast)"),
                why(r"$0 \le \omega,\gamma < 1$, $r>0$; shocks have conditional mean zero; discounted future book "
                    r"vanishes in expectation")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.3, buff=0.42, edge=6.9)
        with self.voiceover(
            "Four equations. <bookmark mark='a'/> Clean surplus: book equity changes only by earnings, less dividends. "
            "<bookmark mark='b'/> Abnormal earnings: earnings beyond the required return on last year's book. "
            "<bookmark mark='c'/> Ohlson's assumption, in 1995: abnormal earnings decay at a rate omega, as "
            "competition erodes excess profits, and are pushed by other information, news that is not yet in the "
            "accounts. <bookmark mark='d'/> And that information decays too, at a rate gamma. Two numbers describe "
            "how long an advantage lasts."
        ) as vo:
            step(0, run_time=0.5)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.wait(0.5)
        self.clear_scene()

    def derive(self):
        rows = [cmath(r"P_t", r"=", r"b_t + \textstyle\sum_{\tau \ge 1} R^{-\tau}\,\mathbb E_t[x^a_{t+\tau}]", font_size=32,
                      colors={r"P_t": PRICE}),
                cmath(r"\mathbb E_t[x^a_{t+\tau}]", r"=", r"\omega^\tau x^a_t + \frac{\omega^\tau - \gamma^\tau}{\omega - \gamma}"
                      r"\,\nu_t", font_size=32, colors={r"\mathbb E_t[x^a_{t+\tau}]": VALUE}),
                cmath(r"P_t", r"=", r"b_t + \alpha_1 x^a_t + \alpha_2 \nu_t", font_size=32, colors={r"P_t": PRICE}),
                cmath(r"\alpha_1 = \frac{\omega}{R - \omega}", r",", r"\alpha_2 = \frac{R}{(R - \omega)(R - \gamma)},\quad "
                      r"R = 1 + r", font_size=32, colors={r"\alpha_1 = \frac{\omega}{R - \omega}": GAIN})]
        whys = [why(r"Chapter 8's residual-income identity: dividends discounted are book plus discounted abnormal earnings, "
                    r"given clean surplus and a transversality condition"),
                why(r"iterate for $\omega\ne\gamma$; when $\omega=\gamma$, the push is "
                    r"$\tau\omega^{\tau-1}\nu_t$ (its continuous limit)"),
                why(r"sum the geometric series: the value is linear in the state, book plus two multiples"),
                why(r"the first sum is $\sum(\omega/R)^\tau$; the second, after partial fractions, collapses to "
                    r"$R/((R - \omega)(R - \gamma))$")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.3, buff=0.42, edge=6.9)
        with self.voiceover(
            "The derivation. <bookmark mark='a'/> Start from Chapter 8's identity: the value is book plus every future "
            "abnormal earning, expected and discounted. <bookmark mark='b'/> Iterate the dynamics forward: each year "
            "multiplies today's abnormal earnings by omega, and the other information adds a push that itself "
            "decays. <bookmark mark='c'/> Sum the geometric series, and the value is linear in what is known today: "
            "book, plus a multiple of abnormal earnings, plus a multiple of the other information. <bookmark "
            "mark='d'/> The first multiple is omega over R minus omega. As persistence approaches one, it tends to "
            "one over r, a finite perpetuity multiple when r is positive. At eight percent, that limit is twelve "
            "and a half. The apparent singularity when omega equals gamma also has a finite limit."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.wait(0.5)
        self.clear_scene()

    def check(self, t):
        hx = [-3.6, -1.6, 0.6, 2.8, 5.0]
        head = VGroup(label(r"$\omega$", font_size=20), label(r"$\gamma$", font_size=20), label(r"formula", font_size=20,
                      color=VALUE), label(r"Monte Carlo", font_size=20, color=PRICE), label(r"$\alpha_1$", font_size=20))
        tab = VGroup()
        for j, row in enumerate([head] + [VGroup(MathTex(rf"{c['omega']:g}", font_size=26), MathTex(rf"{c['gamma']:g}", font_size=26),
                                                 MathTex(rf"{c['formula']:.2f}", font_size=26), MathTex(rf"{c['mc']:.2f}", font_size=26),
                                                 MathTex(rf"{c['a1']:.2f}", font_size=26)) for c in t["checks"]]):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.6 - 0.65 * j, 0])
            tab.add(row)
        foot = wrapped_label(r"book 100, abnormal earnings 5, other information 2, $r$ = 8\%; Monte Carlo: 20{,}000 paths "
                             r"of 400 years, discounted residual income averaged (the House's \texttt{valuation.ohlson\_"
                             r"monte\_carlo})", 11.6, 16, GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Check it against brute force. <bookmark mark='a'/> Simulate twenty thousand futures of four hundred "
            "years each, discount every abnormal earning, and average. For each pair of persistence rates the "
            "formula and the simulation are close. Monte Carlo noise and finite-horizon truncation remain; "
            "agreement here is a numerical check, not a proof."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(tab[1]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[2:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def sensitivity(self, t):
        r = t["r"]
        ws = np.linspace(0, 1, 201)
        pb = 1 + ws / (1 + r - ws) * 0.05
        g = axes([0, 1], [0.95, 1.7], x_length=7.6, y_length=4.0, xlabel=r"persistence $\omega$",
                 ylabel=r"price-to-book, abnormal ROE 5\%, $r$ = 8\%", xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[1, 1.25, 1.5],
                 font_size=13).move_to(LEFT * 1.6 + DOWN * 0.3)
        ax = g.ax
        line = curve(ax, ws, pb, VALUE, stroke_width=3)
        marks = VGroup()
        for w, txt, col in ((0.62, r"DHS 1999", GREY_A), (t["omega"], r"EDGAR, 2010--20", PRICE)):
            y = 1 + w / (1 + r - w) * 0.05
            marks.add(VGroup(Dot(ax.c2p(w, y), radius=0.07, color=col),
                             label(txt, font_size=15, color=col).next_to(ax.c2p(w, y), UL, buff=0.08)))
        rw = Dot(ax.c2p(1.0, 1 + 1 / r * 0.05), radius=0.07, color=LOSS)
        side = VGroup(
            MathTex(r"\omega = 0:\ P/B = 1", font_size=24),
            MathTex(rf"\omega = 0.62:\ {t['pb_at_5pct']['0.62']:.3f}", font_size=24),
            MathTex(rf"\omega = {t['omega']:.2f}:\ {1 + t['omega'] / (1 + r - t['omega']) * 0.05:.3f}", font_size=24, color=PRICE),
            MathTex(rf"\omega = 1:\ {t['pb_at_5pct']['1.0']:.3f}", font_size=24, color=LOSS),
            wrapped_label(r"a 5\% abnormal return on book adds nothing beyond book if it vanishes at once, "
                          r"and 62.5 cents per dollar of book if it is permanent", 3.2, 15, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "What persistence is worth. <bookmark mark='a'/> A firm earning five percent a year above its cost of "
            "equity, on each dollar of book. If the advantage vanishes at once, it is worth book. If it decays at "
            "Dechow, Hutton and Sloan's estimate of point six two, about seven percent more. <bookmark mark='b'/> And "
            "if it never fades, sixty-two percent more: the curve bends up steeply as omega approaches one. Here "
            "only persistence changes; real firms also differ "
            "in book value, earnings, discount rates and other information."
        ) as vo:
            self.play(FadeIn(g), Create(line), run_time=1)
            vo.wait_until("a")
            self.play(FadeIn(marks[0]), FadeIn(side[:2]))
            vo.wait_until("b")
            self.play(FadeIn(marks[1]), FadeIn(side[2:]), FadeIn(rw))
        self.wait(0.4)
        self.clear_scene()

    def estimate(self, t):
        sc = np.asarray(t["scatter"])
        lo, hi = -0.6, 0.6
        g = axes([lo, hi], [lo, hi], x_length=5.4, y_length=4.4, xlabel=r"$x^a_t / b_{t-1}$",
                 ylabel=r"$x^a_{t+1} / b_{t-1}$", xticks=[-0.4, 0, 0.4], yticks=[-0.4, 0, 0.4], font_size=13).to_edge(
            LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        m = (sc[:, 0] > lo) & (sc[:, 0] < hi) & (sc[:, 1] > lo) & (sc[:, 1] < hi)
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.018, color=LOSS if a < 0 else GAIN, fill_opacity=0.45)
                        for a, b in sc[m]])
        b0 = t["intercept"]
        fit = Line(ax.c2p(lo, b0 + t["omega"] * lo), ax.c2p(hi, b0 + t["omega"] * hi), color=WHITE, stroke_width=2.5)
        bs = t["by_sign"]
        side = VGroup(
            MathTex(rf"\hat\omega = {t['omega']:.2f}\ (\pm {t['omega_se']:.2f})", font_size=28, color=PRICE),
            MathTex(rf"x^a > 0:\ \hat\omega = {bs['profit']['omega']:.2f}", font_size=26, color=GAIN),
            MathTex(rf"x^a < 0:\ \hat\omega = {bs['loss']['omega']:.2f}", font_size=26, color=LOSS),
            wrapped_label(rf"{comma(t['n_obs'])} firm-years of {comma(t['n_firms'])} EDGAR filers with book equity above "
                          r"\$10 million, fiscal 2010--2020: net income and stockholders' equity from the XBRL frames; "
                          r"$r$ = 8\%; winsorised at 1\%; standard errors clustered by firm. Dechow, Hutton and Sloan "
                          r"(1999), Compustat 1976--95: 0.62", 4.6, 15, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.35)
        fit_right(side)
        with self.voiceover(
            "Now the data. <bookmark mark='a'/> Eligible American filers with matched XBRL frame observations and "
            "book equity above ten million dollars, fiscal 2010 to 2020: this year's abnormal earnings against next year's, both "
            "per dollar of last year's book. <bookmark mark='b'/> Pooled, omega is point eight three, more persistent "
            "than Dechow, Hutton and Sloan found for 1976 to 1995. <bookmark mark='c'/> But split by sign, and the "
            "picture is lopsided. Profits above the cost of equity have a slope of point five four; shortfalls have "
            "a slope of point nine two. These are descriptive pooled regressions, not causal estimates of competition "
            "or a clean estimate of structural omega: the other-information state is omitted."
        ) as vo:
            self.play(FadeIn(g), FadeIn(dots), run_time=0.6)
            vo.wait_until("a")
            self.play(Indicate(dots, scale_factor=1.02, color=GREY_A))
            vo.wait_until("b")
            self.play(Create(fit), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[1:]))
        self.wait(0.4)
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"open: what is $\nu$?", r"the 'other information' is unobserved; Dechow, Hutton and Sloan "
                          r"proxied it with analysts' forecasts. How to measure it from text or prices (Part 28) is open",
                          width=12.4, font_size=18),
            desk_question(r"open: conservatism and nonlinearity", r"accounting conservatism makes book understate value "
                          r"(Feltham and Ohlson 1995). Which nonlinear dynamics capture persistence without losing "
                          r"tractable valuation?", width=12.4, font_size=18),
            desk_question(r"open: does it price?", r"LID values with estimated $\omega$ underestimate market prices on "
                          r"average and forecast returns weakly; whether the gap is mispricing, risk or missing $\nu$ is debated",
                          width=12.4, font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Three open questions. <bookmark mark='a'/> The other information is not observed. Dechow, Hutton and "
            "Sloan used analysts' forecasts; how to measure it from text or prices is the subject of Part 28, and "
            "open. <bookmark mark='b'/> Conservative accounting can make book understate value. Which nonlinear "
            "dynamics best capture the persistence patterns while keeping valuation tractable? <bookmark mark='c'/> "
            "And values built this way can sit below market prices and forecast "
            "returns only weakly: mispricing, risk, or the missing other information, nobody has settled."
        ) as vo:
            self.play(FadeIn(cards[0]))
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"$b = 50$, $x^a = 4$, $\nu = 1$, $\omega = 0.7$, $\gamma = 0.5$, $r = 10\%$. Find $\alpha_1$, $\alpha_2$ "
                       r"and the value. How much of it is the other information?").move_to(ORIGIN)
        with self.voiceover(
            "Pause and predict. Book of fifty, abnormal earnings of four, other information of one, omega point seven, "
            "gamma point five, and a ten percent cost of equity. Find the two multiples and the value. How much of it "
            "comes from the other information?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
        self.answer()

    def answer(self):
        title = label(r"From information to value", font_size=36, color=VALUE).to_edge(UP, buff=0.5)
        rows = VGroup(
            MathTex(r"R=1.1,\quad\alpha_1=\frac{0.7}{1.1-0.7}=1.75", font_size=36, color=VALUE),
            MathTex(r"\alpha_2=\frac{1.1}{(1.1-0.7)(1.1-0.5)}=4.5833", font_size=36, color=PRICE),
            MathTex(r"P=\underbrace{50}_{\text{book}}+\underbrace{7}_{\alpha_1 x^a}"
                    r"+\underbrace{4.5833}_{\alpha_2\nu}=61.5833", font_size=38),
            MathTex(r"\text{other information}:\quad\frac{4.5833}{61.5833}=7.44\%", font_size=32, color=PRICE),
        ).arrange(DOWN, buff=0.45).move_to(DOWN * 0.1)
        amounts = (50, 7, 4.583333333333333)
        pieces = VGroup(*[
            Rectangle(width=10.5 * amount / sum(amounts), height=0.35, stroke_width=0,
                      fill_color=color, fill_opacity=0.85)
            for amount, color in zip(amounts, (EQUITY, VALUE, PRICE))
        ]).arrange(RIGHT, buff=0).move_to(DOWN * 3)
        nums = VGroup(*[MathTex(text, font_size=20, color=color).next_to(piece, UP, buff=0.08)
                        for text, piece, color in zip(("50", "7", "4.58"), pieces, (EQUITY, VALUE, PRICE))])
        with self.voiceover(
            "Reveal the answer. The gross discount factor is one point one, so the abnormal-earnings multiple is "
            "one point seven five. <bookmark mark='a'/> The other-information multiple is about four point five "
            "eight three. <bookmark mark='b'/> Book contributes fifty, abnormal earnings seven, and other information "
            "four point five eight three: total value, sixty-one point five eight three. <bookmark mark='c'/> Other "
            "information supplies about seven point four four percent. A small state can matter because it feeds "
            "earnings for more than one year."
        ) as vo:
            self.play(FadeIn(title), FadeIn(rows[0]))
            for i, mark in enumerate(("a", "b", "c"), 1):
                vo.wait_until(mark)
                self.play(FadeIn(rows[i], shift=UP * 0.15))
                if i == 2:
                    self.play(LaggedStart(*[GrowFromEdge(piece, LEFT) for piece in pieces], lag_ratio=0.2), FadeIn(nums))
                elif i == 3:
                    self.play(Indicate(pieces[2], color=PRICE, scale_factor=1.1))
        self.wait(0.4)
        self.clear_scene()
