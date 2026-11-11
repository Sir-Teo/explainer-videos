from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant35.common import BAD, FLOW_C, GOOD, HURDLE, INF_C, PART, PRICE_C, fit_right, load


class VPIN(VoiceoverScene):
    def construct(self):
        v = load("vpin")
        self.card()
        self.pin()
        self.vpin_def()
        self.pin_trouble()
        self.series(v)
        self.events(v)
        self.critique(v)
        self.markouts()
        self.lessons()
        self.question()

    def card(self):
        c = chapter_card(6, r"Toxic flow: PIN and VPIN", r"Can the share of informed trading be measured, live?", part=PART)
        self.add(c)
        with self.voiceover("Chapter six. Glosten and Milgrom's mu, the share of informed traders, sets the spread. If it "
                            "could be measured, a market maker would know when to widen its quotes. Two famous attempts, "
                            "and a test of the second."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def pin(self):
        rows = [cmath(r"\text{day}", r":", r"\text{news with probability } \alpha;\ \text{good or bad}", font_size=32),
                cmath(r"\text{arrivals}", r":", r"\text{noise } \varepsilon_b, \varepsilon_s;\ \text{informed } \mu "
                      r"\text{ on the news side}", font_size=30),
                cmath(r"\text{PIN}", r"=", r"\frac{\alpha\mu}{\alpha\mu + \varepsilon_b + \varepsilon_s}", font_size=38,
                      colors={r"\text{PIN}": INF_C})]
        whys = [why(r"Easley, Kiefer, O'Hara and Paperman (1996): each day there is private news or not"),
                why(r"buys and sells arrive as Poisson processes; informed traders add to one side on news days"),
                why(r"the probability that a trade is informed, estimated by maximum likelihood from daily counts of buys and "
                    r"sells")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover(
            "PIN. <bookmark mark='a'/> David Easley, Nicholas Kiefer, Maureen O'Hara and Joseph Paperman: each day there "
            "is private news, or not. <bookmark mark='b'/> Buys and sells arrive at random, and on news days informed "
            "traders add to one side. <bookmark mark='c'/> The probability that a trade is informed is estimated from "
            "daily counts of buys and sells, by maximum likelihood. It became a standard variable in asset pricing, "
            "and a slow one: it needs many days of data."
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

    def vpin_def(self):
        rows = [cmath(r"V_\tau^B", r"=", r"\textstyle\sum_{i \in \tau} V_i\,\Phi\big(\Delta p_i/\sigma_{\Delta p}\big)",
                      font_size=34, colors={r"V_\tau^B": GOOD}),
                cmath(r"\text{VPIN}", r"=", r"\frac{1}{n}\textstyle\sum_{\tau} \frac{|V_\tau^B - V_\tau^S|}{V}",
                      font_size=36, colors={r"\text{VPIN}": INF_C}),
                cmath(r"V", r"=", r"\tfrac{1}{50}\ \text{of a day's volume};\ n = 50", font_size=32)]
        whys = [why(r"bulk volume classification: each bar's volume is split into buys and sells by how far its price "
                    r"moved, with no trade-by-trade signs needed"),
                why("Easley, Lopez de Prado and O'Hara (2012): the mean absolute imbalance over equal-volume buckets; the probability-of-information interpretation needs additional assumptions"),
                why(r"buckets of equal volume, not equal time, so a busy hour counts more")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover(
            "VPIN uses an estimated classification. <bookmark mark='a'/> Split each bar's volume using the Normal cumulative probability of its standardized price change; split a bar across equal-volume buckets when necessary. <bookmark mark='b'/> Average each bucket's absolute buy-sell imbalance over fifty buckets. This is a statistic, not automatically the probability of informed trading. <bookmark mark='c'/> Our unchanged original estimates return standard deviation and mean daily volume from the full four-year sample. Bucket size is that average divided by fifty. Those full-sample choices use future observations relative to early dates, so this is an ex-post research construction, not an implemented live signal."
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

    def pin_trouble(self):
        cards = VGroup(
            desk_question(r"hard to estimate", r"PIN's likelihood has many local maxima and overflows for active stocks; "
                          r"estimates depend on the optimiser's starting point", width=12.4, font_size=25),
            desk_question(r"why is it priced?", r"Duarte and Young (2009) found that the part of PIN that predicts returns "
                          r"is the part related to illiquidity, not to asymmetric information", width=12.4, font_size=25),
            desk_question(r"order flow without signs", r"both need buys and sells: PIN from a trade classifier, VPIN from "
                          r"price moves; the classifier is the weak link", width=12.4, font_size=25),
        ).arrange(DOWN, buff=0.25)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        self.add(cards[0])
        with self.voiceover(
            "PIN has its own troubles. <bookmark mark='a'/> Its likelihood has many local maxima, and estimates depend on "
            "where the optimiser starts. <bookmark mark='b'/> Jefferson Duarte and Lance Young found that the part of PIN "
            "that predicts stock returns is the part related to illiquidity, not to private information. "
            "<bookmark mark='c'/> And both measures need to know which trades were buys: PIN from a trade classifier, VPIN "
            "from price moves. The classifier is the weak link, which is the test that follows."
        ) as vo:
            for k_, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def series(self, v):
        t = np.asarray(v["t"], float)
        y = np.asarray(v["vpin"], float)
        ok = np.isfinite(y)
        yr = 2021 + (t - 1609459200) / (365.25 * 86400)
        top = max(0.6, float(np.ceil(np.nanmax(y) * 10) / 10))
        g = axes([2021, 2025], [0, top], x_length=8.0, y_length=4.2, xlabel=r"BTCUSDT, 2021--2024",
                 ylabel=r"VPIN", xticks=[2021, 2022, 2023, 2024, 2025], yticks=[0, top / 2, top], xfmt=lambda u: f"{u:.0f}",
                 font_size=15).move_to(LEFT * 0.8 + DOWN * 0.2)
        ax = g.ax
        c1 = curve(ax, yr[ok], y[ok], INF_C, stroke_width=1.5)
        self.add(g, c1)
        with self.voiceover(
            "VPIN on four years of Bitcoin, one-minute bars. <bookmark mark='a'/> It averages about "
            f"{v['mean']:.2f}, with spikes. The question is what the spikes mean."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Create(c1), run_time=2.5)
        self.wait(0.4)
        self.clear_scene()

    def events(self, v):
        ev = v["events"]
        panels = VGroup()
        top = max(0.6, float(np.ceil(max(np.nanmax(e["vpin"]) for e in ev.values()) * 10) / 10))
        for k, (name, e) in enumerate(ev.items()):
            g = axes([-7, 7], [0, top], x_length=5.6, y_length=3.0, xlabel=rf"days from {name}", ylabel=r"VPIN",
                     xticks=[-7, 0, 7], yticks=[0, top], font_size=13)
            ax = g.ax
            vt = np.asarray(e["t"], float)
            vy = np.asarray(e["vpin"], float)
            ok = np.isfinite(vy)
            c1 = curve(ax, vt[ok], vy[ok], INF_C, stroke_width=2)
            pt = np.asarray(e["pt"], float)
            pp = np.asarray(e["price"], float)
            pn = top * (pp - pp.min()) / (pp.max() - pp.min())
            c2 = curve(ax, pt, pn, PRICE_C, stroke_width=1.5)
            zero = DashedLine(ax.c2p(0, 0), ax.c2p(0, top), color=BAD, stroke_width=1.5)
            panels.add(VGroup(g, c1, c2, zero))
        panels.arrange(RIGHT, buff=0.6).move_to(DOWN * 0.2)
        leg = legend([(INF_C, r"VPIN"), (PRICE_C, r"price, rescaled")], font_size=16).to_edge(UP, buff=0.4)
        self.add(leg, panels[0])
        with self.voiceover(
            "Two selected event windows. <bookmark mark='a'/> May nineteenth, 2021, surrounds a large Bitcoin selloff. <bookmark mark='b'/> November eighth, 2022, surrounds the FTX crisis. Price is separately rescaled to each panel, while VPIN retains its own scale. These ex-post selected plots do not establish predictive lead, calibrated false-alarm rates or causality. A defensible warning study would require a predeclared rule and genuinely available inputs, not full-sample bucket and volatility estimates."
        ) as vo:
            self.play(FadeIn(leg))
            vo.wait_until("a")
            self.play(FadeIn(panels[0]))
            vo.wait_until("b")
            self.play(FadeIn(panels[1]))
        self.wait(0.4)
        self.clear_scene()

    def critique(self, v):
        rows = [cmath(r"\operatorname{corr}(\text{VPIN}, \text{volatility})", r"=", rf"{v['corr_rv']:.2f}", font_size=34,
                      colors={r"\operatorname{corr}(\text{VPIN}, \text{volatility})": BAD}),
                cmath('\\operatorname{corr}(\\text{VPIN}, \\text{aggregate taker imbalance})', r"=", rf"{v['corr_true']:.2f}",
                      font_size=34, colors={'\\operatorname{corr}(\\text{VPIN}, \\text{aggregate taker imbalance})': BAD}),
                cmath(r"\Phi(\Delta p/\sigma)", r":", r"\text{large moves} \Rightarrow \text{large measured imbalance}",
                      font_size=32)]
        whys = [why(r"over the same windows: VPIN moves with realised volatility"),
                why('comparison uses the absolute net taker imbalance aggregated across approximate whole-bar windows; it is not the same mean-absolute-bucket statistic'),
                why(r"bulk classification assigns a big price move to one side by construction; Andersen and Bondarenko "
                    r"(2014) made this critique of VPIN and the flash crash")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover(
            f"""Two descriptive correlations, with an essential mismatch. <bookmark mark='a'/> VPIN correlates {v['corr_rv']:.2f} with realized volatility in the selected overlapping windows. <bookmark mark='b'/> Its correlation with absolute aggregate taker imbalance is {v['corr_true']:.2f}. But that comparator takes the absolute value after summing a roughly fifty-bucket whole-bar window. VPIN averages absolute imbalances within equal-volume buckets. Opposite bucket imbalances can cancel in the first statistic but not the second, and boundary bars differ. <bookmark mark='c'/> Bulk classification mechanically uses price moves. The results illustrate sensitivity, not validation against true VPIN or proof about informed trading. Overlap, full-sample calibration and lack of inference further limit the comparison."""
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

    def markouts(self):
        rows = [cmath(r"\text{markout}(\Delta)", r"=", r"q\,(m_{t+\Delta} - p_t)", font_size=36, colors={r"\text{markout}(\Delta)": FLOW_C}),
                cmath(r"\Delta", r"\in", r"\{1\,\text{s},\ 10\,\text{s},\ 1\,\text{min},\ 5\,\text{min}\}", font_size=34),
                cmath(r"\text{toxic flow}", r":", r"\text{markouts that keep falling after the fill}", font_size=32,
                      colors={r"\text{toxic flow}": BAD})]
        whys = [why('dealer-side convention: $q=+1$ when the dealer buys, $q=-1$ when it sells; positive markout is favorable to that dealer'),
                why(r"measured at several horizons, by counterparty, venue and time of day"),
                why('adverse dealer-side markouts can reflect selection and price dynamics; they do not uniquely identify informed counterparties')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        self.add(rows[0], whys[0])
        with self.voiceover(
            "Define whose markout is measured. <bookmark mark='a'/> Let q be the dealer's execution side: plus one for a dealer buy, minus one for a dealer sell. The displayed signed future-midpoint minus fill-price difference is favorable when positive. <bookmark mark='b'/> Use several stated horizons and consistent timestamps, grouped by venue or counterparty when lawfully known. <bookmark mark='c'/> More negative markouts are adverse to the dealer. They can reflect selection and price dynamics; they do not uniquely reveal private information or abusive intent. If one instead signs by the counterparty's side, every sign reverses. Spread income and fees also matter."
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

    def lessons(self):
        cards = VGroup(
            desk_question(r"a measure inherits its classifier", r"a toxicity measure built on price moves will rise when "
                          r"prices move, whatever the flow", width=12.4, font_size=25),
            desk_question(r"use signed flow where it exists", 'taker flags identify aggressive base-asset side on this venue, not private information; compare identical bucket statistics before judging a classifier', width=12.4, font_size=25),
            desk_question(r"volatility is still useful", 'higher volatility can change inventory risk; an optimal quote response depends on the objective, costs and fill model', width=12.4, font_size=25),
        ).arrange(DOWN, buff=0.25)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        self.add(cards[0])
        with self.voiceover(
            "Interpretation follows construction. <bookmark mark='a'/> A statistic built from standardized price moves can inherit volatility effects; correlation alone does not quantify classifier accuracy. <bookmark mark='b'/> Use recorded taker signs where available, but align the bucket definition and boundary allocation before comparing with bulk classification. Neither identifies informed intent. <bookmark mark='c'/> A real quote policy needs a specified objective, costs and available information. This ex-post VPIN illustration does not validate a live toxicity signal or an optimal response."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        eq = MathTex('V=1000\\ \\mathrm{BTC},\\quad\\Delta p/\\sigma=2,\\quad V_B=V\\Phi(2),\\ V_S=V-V_B', font_size=32)
        if eq.width > 12.1:
            eq.scale_to_fit_width(12.1)
        conditions = wrapped_label('This is bulk classification from price change. Compare its assigned split with a possible recorded taker split of 500/500; neither gives informed probability.', 12.0, 22, GREY_A)
        setup = VGroup(eq, conditions).arrange(DOWN, buff=0.6).move_to(UP * 0.2)
        q = pause_card(r"Use the stated assumptions; derive the result and check its units and interpretation.")
        self.add(setup, q)
        with self.voiceover('Pause and predict. A thousand-bitcoin bar rises by two standardized return units. Compute the bulk-classified buy and sell volumes. Could the recorded taker split still be five hundred each? Explain what is classified and what remains unidentified.'):
            self.wait(0.4)
        self.wait(0.5)
        self.clear_scene()
