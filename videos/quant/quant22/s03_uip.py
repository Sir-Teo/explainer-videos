from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant22.common import BAD, BASIS, CARRY, FOR, GOOD, PART, USD, ask, fit_right, illustration, load


class UIP(VoiceoverScene):
    def construct(self):
        f = load("fama")
        self.card()
        self.idea()
        self.regression()
        self.table(f)
        self.scatter(f)
        self.explain()

    def card(self):
        c = chapter_card(2, r"Uncovered parity and the forward premium puzzle",
                         r"Do high interest rates predict a falling currency?", lit=(1984,), part=PART)
        with self.voiceover("Chapter two. Uncovered interest parity, and the puzzle Eugene Fama found in it."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def idea(self):
        rows = [cmath(r"\mathbb{E}_t\big[s_{t+1}\big] - s_t", r"=", r"(i_t^{\pounds} - i_t^{\$})\,\Delta t", font_size=40,
                      colors={r"\mathbb{E}_t\big[s_{t+1}\big] - s_t": FOR}),
                cmath(r"f_t - s_t", r"=", r"(i_t^{\pounds} - i_t^{\$})\,\Delta t", font_size=40, colors={r"f_t - s_t": BASIS})]
        whys = [why(r"uncovered parity, with $s$ = log pounds per dollar: if investors care only about expected "
                    r"returns, the high-rate currency must be expected to fall by exactly its extra interest, so that "
                    r"holding either currency pays the same"),
                why(r"covered parity (chapter 1) says the forward premium is the same differential. So uncovered "
                    r"parity says the forward is the market's forecast of the future spot rate")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "Covered parity was an arbitrage. Its uncovered cousin is a bet. Leave the forward out: a dollar investor "
            "who holds pounds earns the sterling rate, and takes the risk of the exchange rate. If investors cared "
            "only about expected returns, the high-rate currency would have to be expected to fall by exactly its "
            "extra interest, so that both deposits paid the same. <bookmark mark='a'/> Put that beside covered "
            "parity, and the forward premium is the market's forecast of the change in the spot rate. Uncovered "
            "parity is a statement about forecasts, and it can be tested."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def regression(self):
        rows = [cmath(r"s_{t+1} - s_t", r"=", r"\alpha + \beta\,(f_t - s_t) + \varepsilon_{t+1}", font_size=40,
                      colors={r"s_{t+1} - s_t": FOR}),
                cmath(r"\beta", r"=", r"1 + \frac{\text{cov}(p_t,\ f_t - s_t)}{\text{var}(f_t - s_t)}", font_size=40,
                      colors={r"\beta": BAD})]
        whys = [why(r"Fama (1984): regress the change in the exchange rate on the forward premium. Uncovered parity "
                    r"says $\beta = 1$. In the data of the 1970s and 80s it was negative, for every major currency"),
                why(r"write the forward premium as the expected change plus a risk premium $p_t$; then a slope below 1 "
                    r"means the premium moves against the expected change, and is more volatile than it")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "In 1984 Eugene Fama ran the test. Regress next month's change in the exchange rate on this month's "
            "forward premium. If uncovered parity holds, the slope is one: a currency with two percent more interest "
            "falls two percent, on average. <bookmark mark='a'/> He found slopes below zero. The high-rate currency "
            "did not fall; on average it rose. Splitting the forward premium into an expected change and a risk "
            "premium, a negative slope means the risk premium moves against the expected change, and is larger. "
            "Whatever investors are paid for holding currencies, it is big, and it varies."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def table(self, f):
        by = f["by"]
        hx = [-4.6, -2.2, 0.0, 2.2, 4.6]
        heads = [r"currency", r"since", r"slope $\beta$", r"std.\ error", r"average $i - i_\$$"]
        tab = VGroup(VGroup(*[label(h_, font_size=18, color=GREY_A).move_to([x, 2.85, 0]) for h_, x in zip(heads, hx)]))
        for i, (c, v) in enumerate(by.items()):
            y = 2.35 - 0.44 * i
            tab.add(VGroup(label(c, font_size=19).move_to([hx[0], y, 0]),
                           MathTex(f"{v['start'] // 100}", font_size=24).move_to([hx[1], y, 0]),
                           MathTex(f"{v['beta']:+.2f}", font_size=24, color=BAD if v["beta"] < 0 else GREY_A).move_to(
                               [hx[2], y, 0]),
                           MathTex(f"{v['se']:.2f}", font_size=24).move_to([hx[3], y, 0]),
                           MathTex(rf"{100 * v['mean_diff']:+.2f}\%", font_size=24).move_to([hx[4], y, 0])))
        p = f["pooled"]
        pooled = MathTex(rf"\text{{all nine pooled}}:\ \beta = {p['beta']:+.2f}\ ({p['se']:.2f}),\ "
                         rf"t(\beta = 1) = {(p['beta'] - 1) / p['se']:.1f}", font_size=30, color=BAD).to_edge(DOWN, buff=1.0)
        foot = wrapped_label(r"monthly, against the dollar, end-of-month spot (the Fed's noon rates) and the OECD's "
                             r"3-month interbank rates; Newey--West errors. Each currency alone is noisy; together they "
                             r"reject parity", 12.0, 17, GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Here is the test on this century's data, nine currencies against the dollar, month by month since 1999. "
            "<bookmark mark='a'/> Six of the nine slopes are negative, and none is above two thirds. Each alone is noisy: a "
            "monthly exchange rate moves so much that one currency's slope has a standard error of one or two. "
            f"<bookmark mark='b'/> Pooled, the slope is {p['beta']:.2f}, three standard errors below one. The puzzle "
            "Fama found forty years ago is still here."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.15))
            vo.wait_until("b")
            self.play(FadeIn(pooled), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def scatter(self, f):
        s = f["scatter"]
        fp, ds = 100 * np.asarray(s["fp"]), 100 * np.asarray(s["ds"])
        g = axes([-0.15, 0.45], [-10, 20], x_length=7.0, y_length=4.4, xlabel=r"forward premium, \% a month",
                 ylabel=r"next month's change in $s$, \%", xticks=[0, 0.2, 0.4], yticks=[-10, 0, 10, 20],
                 font_size=14).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.03, color=FOR, fill_opacity=0.6) for a, b in zip(fp, ds)])
        b_ = np.polyfit(fp, ds, 1)
        xx = np.array([-0.12, 0.43])
        fit = Line(ax.c2p(xx[0], np.polyval(b_, xx[0])), ax.c2p(xx[1], np.polyval(b_, xx[1])), color=BAD, stroke_width=3)
        uip = Line(ax.c2p(xx[0], xx[0]), ax.c2p(xx[1], xx[1]), color=GOOD, stroke_width=3)
        side = VGroup(
            legend([(GOOD, r"uncovered parity: slope 1"), (BAD, rf"fitted: slope {b_[0]:.2f}")], font_size=17),
            wrapped_label(r"the Australian dollar, 1999--2025, $s$ in Australian dollars per US dollar. The forward "
                          r"premium spans half a percent a month; the exchange rate moves many times that. The slope is "
                          r"a needle in that noise", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "One currency, drawn out: the Australian dollar, usually one of the highest-yielding. "
            "<bookmark mark='a'/> Each dot is a month: the forward premium on the horizontal axis, the next month's "
            "move on the vertical. <bookmark mark='b'/> Parity says the cloud should rise along the green line. The "
            "fitted line slopes the other way, and the cloud is so tall that the slope is almost invisible. That is the "
            "puzzle's second lesson: the exchange rate is mostly unpredictable noise, and the premium is a small, "
            "persistent tilt inside it."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.003, run_time=2))
            vo.wait_until("b")
            self.play(Create(uip), Create(fit), FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def explain(self):
        cards = VGroup(
            desk_question(r"a risk premium", r"high-rate currencies fall in bad times for the world economy: their "
                          r"holders are paid for bearing that crash risk (chapter 3)", width=12.0, font_size=21),
            desk_question(r"a peso problem", r"a large devaluation that the market prices but rarely sees: in a short "
                          r"sample, the forecast looks biased because the disaster has not happened yet", width=12.0,
                          font_size=21),
            desk_question(r"slow money", r"investors adjust their currency holdings slowly; at horizons of five to ten "
                          r"years, slopes are much closer to one (Chinn and Meredith, 2004)", width=12.0, font_size=21),
        ).arrange(DOWN, buff=0.3)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        with self.voiceover(
            "Three explanations, not exclusive. <bookmark mark='a'/> A risk premium: the high-yielding currencies are "
            "the ones that collapse when the world economy does, so holding them earns a reward for crash risk, the "
            "subject of the next chapter. <bookmark mark='b'/> A peso problem: markets price a devaluation that a short "
            "sample may never show. <bookmark mark='c'/> And slow-moving money: at horizons of five to ten years, "
            "Menzie Chinn and Guy Meredith found slopes much closer to one. Parity may hold in the long run, and fail "
            "every month along the way."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"if the slope is negative, a trader can borrow the low-rate currency and lend the high-rate one. What "
                r"does the trade's return distribution look like, and when does it lose?")
        with self.voiceover("If the slope is negative, a trader can borrow the low-rate currency and lend the high-rate "
                            "one. What does that trade's return distribution look like, and when does it lose?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
