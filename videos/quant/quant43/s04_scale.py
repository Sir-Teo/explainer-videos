from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant43.common import ladder
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
            "Chapter three. In the idealised competitive Bayesian model, positive allocations have zero conditional expected net alpha, while a manager is "
            "paid fees proportional to allocated assets. This is a model-specific mechanism, not a universal result for investors. Jonathan Berk and Richard Green's argument: money flows to a manager who has shown "
            "skill, and because skill does not scale, the flows continue until the fund's alpha to its investors is "
            "zero. The skill is real; it shows up in the fund's size and the manager's fees, not in investors' returns."
        ):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def model(self):
        rows = [cmath(r"\alpha_{\text{gross}}(A)", r"=", r"a - bA", font_size=42, colors={r"\alpha_{\text{gross}}(A)": SKILL_C}),
                cmath(r"\mathbb E_t[a] - bA_t - f", r"=", r"0\quad(A_t>0)", font_size=42),
                cmath(r"\mathbb E_t[a]", r"\leftarrow", r"\text{Bayes, from realised returns}", font_size=40),
                cmath(r"\Rightarrow", r"", r"A_t = \max\{0,(\mathbb E_t[a]-f)/b\}", font_size=42, colors={r"\Rightarrow": HURDLE})]
        whys = [why(r"decreasing returns to scale: each extra dollar lowers the gross alpha on every dollar"),
                why(r"interior positive allocations have zero conditional expected net alpha; the boundary is zero assets"),
                why(r"no one knows a manager's skill: investors learn it from returns, with a prior across managers"),
                why(r"size follows posterior mean skill; expected invested-dollar alpha is zero including the boundary")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The model, in the House's skill module. <bookmark mark='a'/> A manager earns a gross alpha a on the first "
            "dollar, and each extra dollar lowers it. <bookmark mark='b'/> Investors move money until the expected net "
            "alpha, after the fee, is zero. <bookmark mark='c'/> They do not know a, so they learn it from returns, by "
            "Bayes' rule. <bookmark mark='d'/> So the fund's size follows its estimated skill, and its investors' "
            "conditional expected invested-dollar alpha is zero under the stated Bayesian and noise assumptions, including a zero-asset boundary."
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
        side = VGroup(leg, label(rf"among final active funds: skill-size correlation {s['corr_skill_assets']:.2f}", font_size=16,
                                 color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(g, RIGHT, buff=0.4)
        fit_right(side)
        ca, sa = s["corr_skill_assets"], 100 * s["share_active"]
        with self.voiceover(
            "Four hundred managers, twenty years, in simulation. <bookmark mark='a'/> The most skilled forty attract "
            "money as their records accumulate; <bookmark mark='b'/> most managers attract little or none: only "
            f"{sa:.0f} percent are running any money at the end. Among those, a manager's final size has a correlation "
            f"of {ca:.2f} with true skill. This finite model associates final size with true skill among active funds; it is not an empirical manager-selection guarantee."
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
                      label(rf"skill vs last-five-year net alpha, final active funds: {s['corr_skill_netalpha']:.2f}", font_size=17, color=GREY_A),
                      label(rf"top 40: skill {100 * s['skill_top']:.1f}\% on the first dollar, gross alpha "
                            rf"{100 * s['gross_top']:.1f}\% at their size", font_size=15, color=SKILL_C)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(g, RIGHT, buff=0.4)
        fit_right(side)
        an, cn, st, gt = 100 * s["aw_net_mean"], s["corr_skill_netalpha"], 100 * s["skill_top"], 100 * s["gross_top"]
        with self.voiceover(
            "And what investors earned. <bookmark mark='a'/> Weighted by the money actually invested, the net alpha "
            f"scatters around zero: {an:+.1f} percent a year on average. <bookmark mark='b'/> Its correlation with true "
            f"skill is {cn:.2f} in this selected finite run; this is not proof of zero dependence. <bookmark mark='c'/> The most skilled managers would earn {st:.1f} percent on "
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
                cmath(r"\text{investors' alpha}", r"=", r"\mathbb E_t[a]-bA-f=0\quad(A>0)", font_size=42, colors={r"\text{investors' alpha}": ACT_C})]
        whys = [why(rf"in the simulation, managers collect about {s['revenue']:.0f} units a year in fees across the "
                    r"industry"),
                why(rf"value added, gross alpha times assets: about {s['va_total']:.1f} units a year"),
                why(r"positive allocations have zero conditional expected net alpha under the model; realised returns need not equal "
                    r"that expectation")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        rv, va = s["revenue"], s["va_total"]
        with self.voiceover(
            "So who gets what. <bookmark mark='a'/> The manager's revenue is the fee times the assets: in the "
            f"simulation, about {rv:.0f} units a year across the industry. <bookmark mark='b'/> The value added, gross "
            f"alpha times assets, about {va:.1f}. <bookmark mark='c'/> For positive allocations, conditional expected net alpha is zero under the model. Finite realised investor returns need not equal "
            "that expectation. Value added uses true gross alpha times arbitrary asset units; fees are revenue, not profit after operating expenses."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def value_added(self):
        cards=VGroup(
            desk_question('Berk and van Binsbergen (2015)','study dollar value added relative to investable alternatives, distinguishing scale from net percentage alpha',width=12.4,font_size=19),
            desk_question('the measurement problem','benchmark choice, costs, timing and the asset base affect measured value added',width=12.4,font_size=19),
            desk_question('the lesson',"manager skill, fee revenue, operating profit and investors' net returns are different quantities",width=12.4,font_size=19)
        ).arrange(DOWN,buff=.25)
        with self.voiceover("A different empirical measurement. <bookmark mark='a'/> Berk and van Binsbergen study dollar value added relative to investable alternatives, separating scale from net percentage alpha. <bookmark mark='b'/> That measurement depends on benchmark, costs, timing and the asset base. <bookmark mark='c'/> Manager skill, fee revenue, operating profit and investor net returns are distinct quantities. Sharpe's aggregate holdings identity does not determine the expected performance of an individual fund.") as vo:
            self.play(FadeIn(cards[0]))
            for k,mark in enumerate(('a','b','c')):
                vo.wait_until(mark)
                if k:self.play(FadeIn(cards[k],shift=UP*.2))
        self.clear_scene()

    def pst(self):
        cards=VGroup(
            desk_question('Pástor, Stambaugh and Taylor (2015)','study scale and skill in active management, including industry-level decreasing returns',width=12.4,font_size=19),
            desk_question('empirical interpretation','fund and industry size, changing skill and opportunity sets need an identified empirical design',width=12.4,font_size=19),
            desk_question('the connection','competition and congestion can affect rewards; this is related intuition, not the same theorem as costly-information equilibrium',width=12.4,font_size=19)
        ).arrange(DOWN,buff=.25)
        with self.voiceover("Scale is also studied empirically. <bookmark mark='a'/> Pástor, Stambaugh and Taylor examine scale and skill in active management, including industry-level decreasing returns. <bookmark mark='b'/> Separating fund size, industry size, changing skill and opportunities requires their empirical design; a size-performance correlation alone is not a causal estimate. <bookmark mark='c'/> Competition and congestion can affect rewards. This intuition is related to costly-information equilibrium, but it is not the same theorem and does not establish a universal response to every inflow.") as vo:
            self.play(FadeIn(cards[0]))
            for k,mark in enumerate(('a','b','c')):
                vo.wait_until(mark)
                if k:self.play(FadeIn(cards[k],shift=UP*.2))
        self.clear_scene()

    def hedge_funds(self):
        cards=VGroup(
            desk_question('capacity','impact, funding, borrow or limited opportunities can make returns depend on scale',width=12.4,font_size=19),
            desk_question('the inference limit','a fund closing to outside capital does not by itself identify skill or a specific scale-cost model',width=12.4,font_size=19),
            desk_question('proposed governance','evaluate capacity and liquidity before assigning a risk budget',width=12.4,font_size=19)
        ).arrange(DOWN,buff=.25)
        with self.voiceover("Capacity is an economic question. <bookmark mark='a'/> Impact, funding, borrow or limited opportunities can make returns depend on scale. A square-root impact approximation is one model, not a universal law for every strategy. <bookmark mark='b'/> Refusing outside capital does not by itself identify skill or the form of scale costs. <bookmark mark='c'/> The teaching House therefore proposes capacity and liquidity review before assigning a risk budget, rather than claiming a particular fund's capacity has been established.") as vo:
            self.play(FadeIn(cards[0]))
            for k,mark in enumerate(('a','b','c')):
                vo.wait_until(mark)
                if k:self.play(FadeIn(cards[k],shift=UP*.2))
        self.clear_scene()

    def choosing(self):
        cards=VGroup(
            desk_question('for an investor','ask how benchmark, costs, capacity and selection affect the prospective net claim',width=12.4,font_size=19),
            desk_question('for a manager','justify the scale-cost and implementation assumptions, rather than treating all inflows as costless',width=12.4,font_size=19),
            desk_question('for an economist','weak net-return persistence alone neither proves nor rules out skill',width=12.4,font_size=19)
        ).arrange(DOWN,buff=.25)
        with self.voiceover("Three questions follow. <bookmark mark='a'/> For an investor, what benchmark, costs, capacity and selection assumptions support the prospective net-return claim? A fee schedule may be known while future dollar fees and market impact remain uncertain. <bookmark mark='b'/> For a manager, how are scale costs and implementation justified? <bookmark mark='c'/> For an economist, weak net-return persistence alone neither proves nor rules out skill. The competitive Bayesian allocation model supplies one possible mechanism, under its assumptions.") as vo:
            self.play(FadeIn(cards[0]))
            for k,mark in enumerate(('a','b','c')):
                vo.wait_until(mark)
                if k:self.play(FadeIn(cards[k],shift=UP*.2))
        self.clear_scene()

    def question(self):
        q = pause_card(r"has the US stock market become harder to predict from its own past? Guess the autocorrelation "
                       r"of daily returns in the 1970s, and in the 2010s.")
        with self.voiceover(
            "Pause and predict. Has the American stock market become harder to predict from its own past? Guess the "
            "autocorrelation of daily returns in the nineteen seventies, and in the twenty tens."
        ):
            self.play(FadeIn(q))
        self.wait(6.0)
        self.clear_scene()
