from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant2.common import ro, CASH, CCP, LOSS, PART, TRADE, load

C_ = {r"E_h": TRADE, r"D": CCP, r"\sigma": LOSS, r"h": QC.IDEA}


def row(*parts, fs=38):
    return cmath(*parts, colors=C_, font_size=fs)


class Settlement(VoiceoverScene):
    def construct(self):
        s = load("settlement")
        self.card()
        self.cycle()
        self.belt(s)
        self.math(s)
        self.after()

    def card(self):
        c = chapter_card(7, r"Settlement and the deposit", r"Why must a broker whose customers only buy post "
                         r"collateral?", lit=(2024,), part=PART)
        with self.voiceover("Chapter seven. Settlement, and the deposit it costs."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def cycle(self):
        steps = [(r"before 1995", r"T+5"), (r"June 1995", r"T+3"), (r"September 2017", r"T+2"), (r"28 May 2024", r"T+1")]
        items = VGroup()
        for when, t in steps:
            items.add(VGroup(MathTex(t, font_size=50, color=CCP), label(when, font_size=22, color=GREY_A)).arrange(DOWN, buff=0.15))
        items.arrange(RIGHT, buff=1.3).shift(UP * 2.0)
        arrows = VGroup(*[Arrow(items[i].get_right(), items[i + 1].get_left(), buff=0.15, color=GREY_B, stroke_width=3)
                          for i in range(3)])
        defs = VGroup(
            definition_card(r"Delivery versus payment", r"shares move only if the cash moves, at the same moment: "
                            r"neither side can deliver and not be paid", width=4.2, color=CCP, font_size=20),
            definition_card(r"Continuous net settlement", r"NSCC nets each member's trades in each stock into one "
                            r"delivery or receipt a day, against the clearing house", width=4.2, color=TRADE,
                            font_size=20),
            definition_card(r"The clearing fund", r"each member's deposit: a 99\% parametric VaR on its unsettled "
                            r"positions, plus mark-to-market, special charges, and the excess capital premium",
                            width=4.2, color=LOSS, font_size=20),
        ).arrange(RIGHT, buff=0.3, aligned_edge=UP).next_to(items, DOWN, buff=0.6)
        src = note(r"SEC staff report on early 2021, section 2; DTCC", font_size=16).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "Settlement is when shares and cash actually move. American stocks once settled five business days "
            "after the trade, then three from 1995, two from 2017, and since the 28th of May 2024, one. "
            "<bookmark mark='a'/> Settlement is delivery versus payment: shares move only against cash, at the same "
            "moment. And it is netted: the clearing house turns each member's day of trades in a stock into one "
            "delivery or one receipt. <bookmark mark='b'/> Between trade and settlement the clearing house holds the "
            "risk, and each member pays into a clearing fund to cover it. The biggest piece is a ninety-nine percent "
            "value-at-risk on the member's unsettled positions; on top come mark-to-market calls, special charges, "
            "and the excess capital premium of January 2021."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(x) for x in items], lag_ratio=0.4),
                      LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.4), run_time=4)
            vo.wait_until("a")
            self.play(FadeIn(defs[0]), FadeIn(defs[1]))
            vo.wait_until("b")
            self.play(FadeIn(defs[2]), FadeIn(src))
        self.wait(0.4)
        self.clear_scene()

    def belt(self, s):
        sig = np.asarray(s["sig"], float)
        runs = s["runs"]
        D2 = np.asarray(runs["one_way_2"], float).mean(0)
        D1 = np.asarray(runs["one_way_1"], float).mean(0)
        days = len(sig)
        t = ValueTracker(0.0)
        hval = ValueTracker(2.0)
        belt_y = 1.6
        x0 = -5.6
        step_w = 1.6

        def belt():
            h = hval.get_value()
            L = step_w * h + 0.8
            g = VGroup(RoundedRectangle(width=L, height=0.35, corner_radius=0.17, stroke_color=GREY_B,
                                        fill_color=GREY_E, fill_opacity=1).move_to([x0 + L / 2, belt_y - 0.3, 0]))
            frac = t.get_value() % 1.0
            for k in range(int(np.ceil(h)) + 1):
                x = x0 + 0.4 + (k + frac) * step_w
                if x > x0 + L - 0.3:
                    continue
                g.add(Square(0.5, stroke_width=1.5, stroke_color=TRADE, fill_color=TRADE, fill_opacity=0.35)
                      .move_to([x, belt_y + 0.15, 0]))
            i = int(np.clip(t.get_value(), 0, days - 1))
            depth = 0.35 + 2.2 * sig[i] / sig.max()
            g.add(Rectangle(width=L, height=depth, stroke_width=0, fill_color=LOSS, fill_opacity=0.25)
                  .move_to([x0 + L / 2, belt_y - 0.48 - depth / 2, 0]))
            return g
        bl = always_redraw(belt)
        lab_b = VGroup(label(r"each day's net buying rides the belt until it settles", font_size=20, color=TRADE),
                       label(r"the shadow: the VaR deposit, proportional to volatility", font_size=20, color=LOSS))
        lab_b.arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_corner(UL, buff=0.35)
        g = axes([0, days], [0, max(D2.max(), 1e-9) * 1.1], x_length=6.0, y_length=2.6, xlabel=r"trading days",
                 ylabel=r"deposit (net buying of 1 a day)", xticks=[0, 60, 120], font_size=15)
        g.to_corner(DR, buff=0.4)
        ax = g.ax
        l2 = tracing(ax, np.arange(days), D2, t, CCP, stroke_width=2.5)
        l1 = tracing(ax, np.arange(days), D1, t, QC.IDEA, stroke_width=2.5)
        leg = legend([(CCP, r"T+2"), (QC.IDEA, r"T+1")], font_size=18).next_to(g, UP, buff=0.15).align_to(g, RIGHT)
        vol = ro(r"\sigma_{\text{annual}} =", lambda: 100 * sig[int(np.clip(t.get_value(), 0, days - 1))] * np.sqrt(252),
                      digits=0, font_size=28, color=LOSS, unit=r"\%").to_edge(LEFT, buff=0.5).shift(DOWN * 1.6)
        src = note(r"simulated: steady net buying, volatility 60\% a year with a 15-day spike to 400\%, 8 seeds",
                   font_size=16).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "Here is the deposit as a machine. Each day the member's customers buy, net, and that day's purchases "
            "ride a conveyor belt until they settle, two days at T plus two. Under the belt is the clearing house's "
            "shadow: the deposit, proportional to the volatility of what's on it. <bookmark mark='a'/> Now volatility "
            "jumps, from sixty percent a year to four hundred, as GameStop's did. The belt carries the same crates, "
            f"but the shadow balloons: the deposit rises about {s['spike']:.0f}-fold. A broker whose customers are "
            "only buying owes the cash on settlement day for shares that may have collapsed by then, and the "
            "clearing house wants that covered today. <bookmark mark='b'/> Shorten the belt to one day and the "
            "shadow shrinks with it."
        ) as vo:
            self.play(FadeIn(lab_b), FadeIn(g), FadeIn(leg), FadeIn(src), FadeIn(vol))
            self.add(bl, l2, l1)
            self.play(t.animate.set_value(55), run_time=5, rate_func=linear)
            vo.wait_until("a")
            self.play(t.animate.set_value(80), run_time=5, rate_func=linear)
            vo.wait_until("b")
            self.play(hval.animate.set_value(1.0), t.animate.set_value(days - 1), run_time=4, rate_func=linear)
        for m in (bl, l2, l1, vol):
            m.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def math(self, s):
        rows = [
            row(r"E_h", r"=", r"\Big|\sum_{k=0}^{h-1} f_{t-k}\Big|"),
            row(r"D", r"=", r"z_{0.99}\,", r"\sigma", r"\sqrt{\tau}\,", r"E_h"),
            row(r"\text{one-way: } f = \bar f", r"\Rightarrow", r"E_h = h\bar f", r"\quad \text{halve } h, \text{ halve } D"),
            row(r"\text{two-way: } \mathbb E f = 0", r"\Rightarrow", r"E_h \propto \sqrt{h}",
                r"\quad \text{halve } h,\ D \times \tfrac{1}{\sqrt 2}"),
        ]
        whys = [why(r"unsettled exposure: the last $h$ days of net buying $f$"),
                why(r"a 99\% Gaussian VaR over the close-out time $\tau$: the volatility component"),
                why(r"flow all one way adds up in a straight line"),
                why(r"flow that nets out grows like a random walk: shortening it saves only 29\%")]
        step = ladder(self, rows, whys, keep=4, top=2.7, x=-1.4, buff=0.5, edge=6.9)
        res = VGroup(
            MathTex(rf"\text{{simulated, T+2}} \to \text{{T+1: one-way}}\ -{100 * s['cut']['one_way']:.0f}\%,\ "
                    rf"\text{{two-way}}\ -{100 * s['cut']['two_way']:.0f}\%", font_size=30, color=QC.IDEA),
        ).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The arithmetic. The exposure is the last h days of net buying. <bookmark mark='a'/> The deposit is a "
            "ninety-nine percent value-at-risk on it: two point three three times the volatility, times the square "
            "root of the time to close it out, times the exposure. <bookmark mark='b'/> If the flow runs all one "
            "way, the exposure is h times the daily flow, and going from two days to one halves the deposit. "
            "<bookmark mark='c'/> But most members' flow nets out over days, and netted flow grows like a random "
            "walk, with the square root of h. Halving h then saves only about twenty-nine percent. "
            f"The simulation agrees: {100 * s['cut']['one_way']:.0f} percent less for one-way flow, "
            f"{100 * s['cut']['two_way']:.0f} percent less for two-way."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    def after(self):
        bars = VGroup()
        g = axes([-0.5, 1.5], [0, 14], x_length=3.6, y_length=3.6, ylabel=r"NSCC clearing fund, \$ bn",
                 yticks=[0, 5, 10], font_size=17).to_edge(LEFT, buff=1.0).shift(DOWN * 0.3)
        ax = g.ax
        for i, (v, col, t) in enumerate(((12.2, CCP, r"T+2, monthly average"), (9.8, QC.IDEA, r"after T+1"))):
            r_ = Rectangle(width=1.0, height=ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], stroke_width=0, fill_color=col,
                           fill_opacity=0.85).move_to(ax.c2p(i, v / 2))
            bars.add(VGroup(r_, MathTex(rf"\${v}\,\text{{bn}}", font_size=26, color=col).next_to(r_, UP, buff=0.1),
                            wrapped_label(t, 1.6, 17, GREY_A).next_to(ax.c2p(i, 0), DOWN, buff=0.12)))
        facts = VGroup(
            MathTex(r"-\$2.4\,\text{bn}\ (-20\%)", font_size=40, color=QC.IDEA),
            label(r"not the 50\% a one-way belt would save: most flow nets", font_size=21, color=GREY_A),
            label(r"trades affirmed by 9 p.m. on trade date: 73\% $\to$ about 95\%", font_size=22),
            label(r"CNS fail rate, July 2024: 2.12\%, in line with T+2", font_size=22),
            label(r"next: Europe and the UK move to T+1 on 11 October 2027", font_size=22, color=CCP),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.5).shift(UP * 0.2)
        q = desk_question(r"At T+0, does the deposit vanish?", r"the overnight piece does; the intraday exposure "
                          r"between trade and settlement does not", width=6.0, font_size=21)
        q.to_corner(DR, buff=0.3)
        src = note(r"SIFMA, ICI and DTCC, T+1 after-action report (September 2024)", font_size=16).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "What actually happened? After the move to T plus one, the average clearing fund fell by two point four "
            "billion dollars, from twelve point two billion to nine point eight: twenty percent, not fifty, just as "
            "netted flow predicts. <bookmark mark='a'/> The industry had to confirm trades on the trade date itself; "
            "affirmation by nine in the evening rose from seventy-three percent to about ninety-five. Failed "
            "settlements stayed where they had been under T plus two. Europe and Britain follow on the eleventh of "
            "October 2027. <bookmark mark='b'/> And Robinhood's morning? A buying frenzy, at four hundred percent "
            "volatility, on a two-day belt. Pause and predict: settle the same day, and does the deposit vanish?"
        ) as vo:
            self.play(FadeIn(g), LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.5), FadeIn(src))
            self.play(FadeIn(facts[0]), FadeIn(facts[1]))
            vo.wait_until("a")
            self.play(FadeIn(facts[2]), FadeIn(facts[3]), FadeIn(facts[4]))
            vo.wait_until("b")
            self.play(FadeIn(q))
        self.wait(1.0)
        self.clear_scene()
