from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant43.common import (ACT_C, BAD, COST_C, GOOD, HURDLE, LUCK_C, MKT_C, PART, SKILL_C, fit_right,
                                         load)


class Scale(VoiceoverScene):
    def construct(self):
        s = load("scale")
        self.card()
        self.model()
        self.assets(s)
        self.net(s)
        self.revenue(s)
        self.value_added()
        self.pst()
        self.hedge_funds()
        self.choosing()
        self.question()

    def card(self):
        c = chapter_card(3, r"Skill, scale and money", r"Where does a skilled manager's skill end up?", part=PART)
        with self.voiceover(
            "Chapter three, and the answer to the pause: the investors earn about the market, and the manager is "
            "paid for the skill. Jonathan Berk and Richard Green's argument: money flows to a manager who has shown "
            "skill, and because skill does not scale, the flows continue until the fund's alpha to its investors is "
            "zero. The skill is real; it shows up in the fund's size and the manager's fees, not in investors' returns."
        ):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def model(self):
        rows = [cmath(r"\alpha_{\text{gross}}(A)", r"=", r"a - bA", font_size=42, colors={r"\alpha_{\text{gross}}(A)": SKILL_C}),
                cmath(r"\mathbb E_t[a] - bA_t - f", r"=", r"0", font_size=42),
                cmath(r"\mathbb E_t[a]", r"\leftarrow", r"\text{Bayes, from realised returns}", font_size=40),
                cmath(r"\Rightarrow", r"", r"A_t = \frac{\mathbb E_t[a] - f}{b}", font_size=42, colors={r"\Rightarrow": HURDLE})]
        whys = [why(r"decreasing returns to scale: each extra dollar lowers the gross alpha on every dollar"),
                why(r"competitive investors move money in or out until the expected net alpha is zero; $f$ is the fee"),
                why(r"no one knows a manager's skill: investors learn it from returns, with a prior across managers"),
                why(r"so the fund's size tracks estimated skill, and investors' expected alpha is zero at every date")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The model, in the House's skill module. <bookmark mark='a'/> A manager earns a gross alpha a on the first "
            "dollar, and each extra dollar lowers it. <bookmark mark='b'/> Investors move money until the expected net "
            "alpha, after the fee, is zero. <bookmark mark='c'/> They do not know a, so they learn it from returns, by "
            "Bayes' rule. <bookmark mark='d'/> So the fund's size follows its estimated skill, and its investors' "
            "expected alpha is zero at every date."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def assets(self, s):
        y = np.asarray(s["years"], float)
        at = np.asarray(s["assets_top"], float)
        aa = np.asarray(s["assets_all"], float)
        g = axes([0, 20], [0, float(at.max()) * 1.15], x_length=7.4, y_length=4.2, xlabel=r"year",
                 ylabel=r"average assets, units", xticks=[0, 5, 10, 15, 20], yticks=[], font_size=15
                 ).move_to(LEFT * 1.3 + DOWN * 0.2)
        ax = g.ax
        l1 = curve(ax, y, at, SKILL_C, stroke_width=3)
        l2 = curve(ax, y, aa, ACT_C, stroke_width=3)
        leg = legend([(SKILL_C, r"the 40 most skilled of 400"), (ACT_C, r"all 400")], font_size=17)
        side = VGroup(leg, label(rf"skill against final size: correlation {s['corr_skill_assets']:.2f}", font_size=16,
                                 color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(g, RIGHT, buff=0.4)
        fit_right(side)
        ca, sa = s["corr_skill_assets"], 100 * s["share_active"]
        with self.voiceover(
            "Four hundred managers, twenty years, in simulation. <bookmark mark='a'/> The most skilled forty attract "
            "money as their records accumulate; <bookmark mark='b'/> most managers attract little or none: only "
            f"{sa:.0f} percent are running any money at the end. Among those, a manager's final size has a correlation "
            f"of {ca:.2f} with true skill. The market for money finds the skill."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side))
            vo.wait_until("a")
            self.play(Create(l1), run_time=2)
            vo.wait_until("b")
            self.play(Create(l2), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def net(self, s):
        y = np.asarray(s["years"], float)[1:]
        n = np.asarray(s["aw_net"], float)[1:]
        g = axes([0, 20], [-0.03, 0.03], x_length=7.4, y_length=4.2, xlabel=r"year",
                 ylabel=r"net alpha to investors, asset-weighted", xticks=[0, 5, 10, 15, 20], yticks=[-0.02, 0, 0.02],
                 yfmt=lambda u: rf"{100 * u:+.0f}\%", font_size=15).move_to(LEFT * 1.3 + DOWN * 0.2)
        ax = g.ax
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(20, 0), color=GREY_C, stroke_width=1.5)
        dots = VGroup(*[Dot(ax.c2p(a_, b_), radius=0.06, color=ACT_C) for a_, b_ in zip(y, n)])
        side = VGroup(label(rf"average after year 5: {100 * s['aw_net_mean']:+.1f}\%", font_size=17, color=ACT_C),
                      label(rf"skill against net alpha: correlation {s['corr_skill_netalpha']:.2f}", font_size=17, color=GREY_A),
                      label(rf"top 40: skill {100 * s['skill_top']:.1f}\% on the first dollar, gross alpha "
                            rf"{100 * s['gross_top']:.1f}\% at their size", font_size=15, color=SKILL_C)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(g, RIGHT, buff=0.4)
        fit_right(side)
        an, cn, st, gt = 100 * s["aw_net_mean"], s["corr_skill_netalpha"], 100 * s["skill_top"], 100 * s["gross_top"]
        with self.voiceover(
            "And what investors earned. <bookmark mark='a'/> Weighted by the money actually invested, the net alpha "
            f"scatters around zero: {an:+.1f} percent a year on average. <bookmark mark='b'/> Its correlation with true "
            f"skill is {cn:.2f}: nothing. <bookmark mark='c'/> The most skilled managers would earn {st:.1f} percent on "
            f"their first dollar; at the size they reach, their gross alpha is {gt:.1f} percent, just about their fee. "
            "Their skill went into their size."
        ) as vo:
            self.play(FadeIn(g), FadeIn(zero))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.1), FadeIn(side[0]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def revenue(self, s):
        rows = [cmath(r"\text{manager's revenue}", r"=", r"f \times A", font_size=42, colors={r"\text{manager's revenue}": SKILL_C}),
                cmath(r"\text{value added}", r"=", r"(a - bA)\,A", font_size=42),
                cmath(r"\text{investors' alpha}", r"=", r"a - bA - f \approx 0", font_size=42, colors={r"\text{investors' alpha}": ACT_C})]
        whys = [why(rf"in the simulation, managers collect about {s['revenue']:.0f} units a year in fees across the "
                    r"industry"),
                why(rf"value added, gross alpha times assets: about {s['va_total']:.1f} units a year"),
                why(r"and investors, who supplied the capital, earn the market: competition for skill is won by "
                    r"the scarce side")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        rv, va = s["revenue"], s["va_total"]
        with self.voiceover(
            "So who gets what. <bookmark mark='a'/> The manager's revenue is the fee times the assets: in the "
            f"simulation, about {rv:.0f} units a year across the industry. <bookmark mark='b'/> The value added, gross "
            f"alpha times assets, about {va:.1f}. <bookmark mark='c'/> And investors, who supply the money, earn about "
            "the market. Skill is the scarce input, so its owner keeps the rent."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def value_added(self):
        cards = VGroup(
            desk_question(r"Berk and van Binsbergen (2015)", r"measure skill as value added, alpha before fees times "
                          r"assets, against the investable alternatives; the average fund adds about \$3 million a year, "
                          r"as they report", width=12.4, font_size=19),
            desk_question(r"and it persists", r"funds that added value keep adding it, while their net alphas to "
                          r"investors do not stand out: Berk and Green's prediction", width=12.4, font_size=19),
            desk_question(r"the lesson for investors", r"skill and investor returns are different questions; the "
                          r"second is answered by Sharpe's arithmetic", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "In real data. <bookmark mark='a'/> Jonathan Berk and Jules van Binsbergen measured skill as value added: "
            "alpha before fees, times the assets managed. The average fund adds about three million dollars a year, as "
            "they report. <bookmark mark='b'/> And funds that added value keep adding it, while their investors' net "
            "alphas do not stand out. <bookmark mark='c'/> Skill and investors' returns are different questions, and "
            "the second is answered by Sharpe's arithmetic."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def pst(self):
        cards = VGroup(
            desk_question(r"Pástor, Stambaugh and Taylor (2015)", r"decreasing returns at the industry level: when the "
                          r"active fund industry is larger, each fund's performance is worse, as they report", width=12.4,
                          font_size=19),
            desk_question(r"skill rising, alpha flat", r"they also find managers becoming more skilled over time, while "
                          r"performance does not improve: more skill competing for the same mispricings", width=12.4,
                          font_size=19),
            desk_question(r"which is Grossman and Stiglitz", r"the reward to being informed falls as more become "
                          r"informed", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Scale at the level of the industry. <bookmark mark='a'/> Luboš Pástor, Robert Stambaugh and Lucian Taylor "
            "found that when the active industry is larger, each fund does worse, as they report. "
            "<bookmark mark='b'/> And managers have become more skilled over time while performance has not improved: "
            "more skill, competing for the same mispricings. <bookmark mark='c'/> That is Grossman and Stiglitz: the "
            "reward to being informed falls as more people become informed."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def hedge_funds(self):
        cards = VGroup(
            desk_question(r"capacity", r"every strategy has a size beyond which its impact eats its alpha: Part 37's "
                          r"square root, in Berk and Green's language", width=12.4, font_size=19),
            desk_question(r"closed funds", r"some of the best-known quant funds return outside money and run only "
                          r"their own: the opposite of growing assets, and consistent with the model, as reported",
                          width=12.4, font_size=19),
            desk_question(r"the House", r"Part 34's platform caps each pod's capital: the House sizes to capacity, "
                          r"not to demand", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "And why some managers refuse money. <bookmark mark='a'/> Every strategy has a capacity, a size beyond "
            "which its impact eats its alpha: Part thirty-seven's square root, in Berk and Green's language. "
            "<bookmark mark='b'/> So some of the best-known quantitative funds have returned outside money and run "
            "only their own, as reported. <bookmark mark='c'/> And the House, since Part thirty-four, sizes each pod to "
            "its capacity rather than to demand."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def choosing(self):
        cards = VGroup(
            desk_question(r"for an investor choosing a fund", r"past returns say little about future net returns; "
                          r"fees and costs say a lot, and they are known in advance", width=12.4, font_size=19),
            desk_question(r"for a manager choosing a size", r"capacity is part of the strategy: every unit of assets "
                          r"beyond it is paid for by existing investors", width=12.4, font_size=19),
            desk_question(r"for an economist", r"no persistence in investors' returns is not evidence of no skill: Berk "
                          r"and Green's market hides skill exactly where Chapter 2 looked for it", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "What follows for each of the three parties. <bookmark mark='a'/> For an investor choosing a fund: past "
            "returns say little about future net returns, while fees say a lot, and are known in advance. "
            "<bookmark mark='b'/> For a manager: capacity is part of the strategy, and every dollar beyond it is paid "
            "for by the investors already in. <bookmark mark='c'/> And for an economist: no persistence in what "
            "investors earn is not evidence of no skill. This market hides skill exactly where Chapter two looked for "
            "it."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"has the US stock market become harder to predict from its own past? Guess the autocorrelation "
                       r"of daily returns in the 1970s, and in the 2010s.")
        with self.voiceover(
            "Pause and predict. Has the American stock market become harder to predict from its own past? Guess the "
            "autocorrelation of daily returns in the nineteen seventies, and in the twenty tens."
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
