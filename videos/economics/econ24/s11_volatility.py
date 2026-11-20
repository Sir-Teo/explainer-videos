from __future__ import annotations

from videos.economics.econ24.common import *  # noqa: F403


class Volatility(VoiceoverScene):
    def construct(self):
        card(self, 9, r"The volatility puzzle", r"Why does unemployment swing so much more than the model says?",
             "Chapter nine. The volatility puzzle.", lit={2005: r"Shimer; \ Hall", 2008: r"Hagedorn and Manovskii",
                                                         2017: r"Ljungqvist and Sargent"},
             scale=("market",), horizon=("years",))
        self.data_()
        self.model()
        self.called()
        self.repairs()
        self.surplus()

    def data_(self):
        v = load("volatility")
        ax = plane([2001, 2020], [-1.0, 0.7], center=LEFT * 1.8 + DOWN * 0.3, x_length=8.6, y_length=5.0,
                   xticks=[2002, 2006, 2010, 2014, 2018], yticks=[-1.0, -0.5, 0, 0.5],
                   ylabel=r"log deviation from trend", xfmt=lambda x: f"{x:.0f}", yfmt=lambda x: f"{x:g}",
                   font_size=16)
        zero = seg(ax, 2001, 0, 2020, 0, color=GREY_D, width=2)
        vu = path(ax, v["t"], v["c_vu"], color=TIGHT, width=3, smooth=False)
        pr = path(ax, v["t"], v["c_p"], color=MATCH, width=4, smooth=False)
        side = VGroup(
            label(rf"openings per unemployed worker: \\ s.d.\ {v['sd_vu']:.2f}", font_size=21, color=TIGHT),
            label(rf"output per hour: \\ s.d.\ {v['sd_p']:.3f}", font_size=21, color=MATCH),
            label(rf"ratio: \ about {v['ratio']:.0f}", font_size=26, color=E.ACCENT),
            label(rf"Shimer, \ 1951--2003: \\ {v['shimer_paper']['sd_vu']:.3f} against "
                  rf"{v['shimer_paper']['sd_p']:.3f}, \ almost 20", font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).to_edge(RIGHT, buff=0.35)
        tag = data_tag(r"JOLTS and the CPS; \ BLS output per hour, \ nonfarm business; \ quarterly, \ logs, \ "
                       r"HP filter ($\lambda = 10^5$), \ via FRED", corner=DR, font_size=12)
        with self.voiceover(
            "Chapter six ended with a warning. Here is the data that makes it a puzzle. Take each quarter from 2001 "
            "to 2019 and strip out the slow trends, leaving the business cycle. <bookmark mark='a'/> Openings per "
            "unemployed worker swing enormously: in the Great Recession they fell to well under half their trend. "
            f"Their standard deviation is about {v['sd_vu']:.2f}. <bookmark mark='b'/> Output per hour, the "
            "productivity that drives the model, barely moves: a standard deviation of about "
            f"{100 * v['sd_p']:.1f} percent. <bookmark mark='c'/> Tightness is about {v['ratio']:.0f} times as "
            "volatile as productivity. <bookmark mark='d'/> Robert Shimer made the same comparison in 2005, for "
            "1951 to 2003, with older data on help-wanted advertising: almost twenty times."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(tag), Create(vu), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(side[0]), Indicate(vu, color=WHITE))
            vo.wait_until("b")
            self.play(Create(pr), FadeIn(side[1]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def model(self):
        v = load("volatility")
        sh, hm = v["shimer"], v["hm"]
        ax = plane([-0.6, 2.6], [0, 36], center=LEFT * 2.0 + DOWN * 0.3, x_length=7.0, y_length=4.8, xticks=[],
                   yticks=[0, 10, 20, 30], ylabel=r"\% change in $V/U$ per 1\% change in productivity",
                   yfmt=lambda x: f"{x:.0f}", font_size=16)
        vals = ((v["ratio"], r"the data, \\ 2001--2019", TIGHT), (sh["elasticity"], r"the model, \\ Shimer's numbers",
                                                                  JOB),
                (hm["elasticity"], r"the model, \\ small surplus", HOLD))
        bars, tops, names = VGroup(), VGroup(), VGroup()
        for k, (val, name, c) in enumerate(vals):
            lo, hi = ax.ax.c2p(k, 0), ax.ax.c2p(k, val)
            bars.add(Rectangle(width=0.9, height=max(hi[1] - lo[1], 0.04), fill_color=c, fill_opacity=0.8,
                               stroke_width=0).move_to((lo + hi) / 2))
            tops.add(label(f"{val:.1f}", font_size=22, color=c).next_to(bars[-1], UP, buff=0.08))
            names.add(label(name, font_size=16, color=c).next_to(lo, DOWN, buff=0.15))
        side = VGroup(
            label(rf"Shimer's calibration: \ $b = {sh['b']:g}$, \\ $\beta = \eta = {sh['beta']:g}$, \ quarterly",
                  font_size=20, color=JOB),
            label(r"a productivity rise goes \\ mostly into the wage, \\ so vacancies barely respond", font_size=20,
                  color=WAGE),
            label(rf"Hagedorn and Manovskii: \\ $b = {hm['b']:g}$, \ $\beta = {hm['beta']:g}$", font_size=20,
                  color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Now ask the model the same question: when productivity rises one percent, by how much does tightness "
            f"rise? <bookmark mark='a'/> The data say about {v['ratio']:.0f}. <bookmark mark='b'/> Shimer "
            "calibrated the model to American averages: benefits worth four-tenths of output, a worker's share and a "
            f"matching elasticity of 0.72. It answers {sh['elasticity']:.1f}. <bookmark mark='c'/> The reason is the "
            "wage. When productivity rises, Nash bargaining hands most of the gain to the worker, through both p "
            "and the tighter market, so the profit from a new hire hardly changes, and firms open hardly any more "
            "vacancies. <bookmark mark='d'/> In 2008 Marcus Hagedorn and Iourii Manovskii proposed different "
            "numbers: a fallback worth ninety-five percent of output, and a worker's share of five percent. Then "
            f"the model answers {hm['elasticity']:.0f}: more than enough."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=0.8)
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[0], DOWN), FadeIn(tops[0]), FadeIn(names[0]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[1], DOWN), FadeIn(tops[1]), FadeIn(names[1]), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(GrowFromEdge(bars[2], DOWN), FadeIn(tops[2]), FadeIn(names[2]), FadeIn(side[2]))
        self.clear_scene()

    def called(self):
        c = calls.CALLS["dmp_volatility"]
        cc = call_card(tex_safe(c.who), c.when, tex_safe(c.said), tex_safe(c.outcome), c.verdict, width=12.4,
                       font_size=20).move_to(UP * 0.1)
        tag = published_tag(r"Mortensen and Pissarides, RES 61(3) (1994); \ Shimer, AER 95(1) (2005); \ Hall, AER "
                            r"95(1) (2005)", corner=DR, font_size=12)
        with self.voiceover(
            "Called it? <bookmark mark='a'/> In 1994 Dale Mortensen and Christopher Pissarides simulated their "
            "model, driven by aggregate shocks alone, and reported that it reproduced reasonably well the cyclical "
            "behaviour of job creation and job destruction in the United States. <bookmark mark='b'/> The pattern "
            "held up: in recessions job destruction jumps and job creation falls, as their model says. The size did "
            "not. Shimer showed that with productivity shocks of the size actually observed, the model's "
            "vacancies and unemployment barely move. Robert Hall put it the same way: the model explains the "
            "direction of the labour market's response to shocks, but needs implausibly large shocks to explain "
            "the magnitude. <bookmark mark='c'/> Partly right."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1]), FadeIn(tag))
            vo.wait_until("b")
            self.play(FadeIn(cc[2]))
            vo.wait_until("c")
            self.play(FadeIn(cc.stamp, scale=1.3))
        self.clear_scene()

    def repairs(self):
        rows = VGroup(
            label(r"twenty years of repairs", font_size=30, color=E.ACCENT),
            label(r"sticky wages \ (Hall, \ 2005): \ if the wage does not move, \ the whole productivity gain "
                  r"is profit", font_size=22, color=WAGE),
            label(r"but wages of \emph{new} hires move with the cycle \ (Pissarides, \ 2009), \ and those are the "
                  r"ones that matter for hiring", font_size=21, color=GREY_A),
            label(r"alternating-offer bargaining \ (Hall and Milgrom, \ 2008): \ walking away is not the threat",
                  font_size=22, color=WAGE),
            label(r"a small surplus \ (Hagedorn and Manovskii, \ 2008): \ then workers barely prefer working",
                  font_size=22, color=HOLD),
            label(r"shocks other than productivity: \ discount rates, \ financial conditions, \ demand",
                  font_size=22, color=JOB),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Hall, AER 95(1) (2005); \ Hall and Milgrom, AER 98(4) (2008); \ Pissarides, "
                            r"Econometrica 77(5) (2009)", corner=DR, font_size=12)
        with self.voiceover(
            "Twenty years of repairs followed. <bookmark mark='a'/> Robert Hall's answer was sticky wages: if the "
            "wage does not rise with productivity, the whole gain is profit, and firms rush to hire. "
            "<bookmark mark='b'/> But Christopher Pissarides pointed out in 2009 that what matters for opening a "
            "vacancy is the wage of the person hired, and the wages of new hires move strongly with the cycle in "
            "the studies he reviewed, even when the wages of long-standing employees do not. "
            "<bookmark mark='c'/> Hall and Paul Milgrom replaced Nash's threat of walking away with Rubinstein's "
            "alternating offers, so that the outside market matters less to the wage. "
            "<bookmark mark='d'/> Hagedorn and Manovskii's small surplus works, but it says that the unemployed "
            "are almost as well off as the employed. <bookmark mark='e'/> And other work looks for shocks other "
            "than productivity: to the rate at which firms discount the future, to credit, to demand."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def surplus(self):
        v = load("volatility")
        sh, hm = v["shimer"], v["hm"]
        rows = VGroup(
            MathTex(r"\frac{d\ln\theta}{d\ln p} \;=\; \underbrace{\frac{r + s + \beta f}{\eta\,(r+s) + \beta f}}"
                    r"_{\text{between 1 and } 1/\eta} \;\times\; \underbrace{\frac{p}{p - b}}_{\text{one over the "
                    r"fundamental surplus}}", font_size=40, color=WHITE),
            label(r"Ljungqvist and Sargent, \ 2017: \ every repair works by shrinking the second factor", font_size=23,
                  color=E.ACCENT),
            label(rf"Shimer: \ $p/(p - b) = 1/(1 - {sh['b']:g}) \approx {1 / (1 - sh['b']):.1f}$ \ $\Rightarrow$ \ "
                  rf"{sh['elasticity']:.1f}", font_size=25, color=JOB),
            label(rf"Hagedorn and Manovskii: \ $1/(1 - {hm['b']:g}) \approx {1 / (1 - hm['b']):.0f}$ \ $\Rightarrow$ "
                  rf"\ {hm['elasticity']:.0f}", font_size=25, color=HOLD),
            label(r"the question becomes: \ how much of a job's output is really left over \ after paying what "
                  r"the worker could get elsewhere?", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"Ljungqvist and Sargent, AER 107(9) (2017): \ 2630--2665", corner=DR, font_size=12)
        with self.voiceover(
            "In 2017 Lars Ljungqvist and Thomas Sargent showed what all these repairs have in common. "
            "<bookmark mark='a'/> The elasticity of tightness with respect to productivity factors into two "
            "pieces. The first is always between one and one over eta: it cannot do much. The second is output "
            "divided by output minus the worker's fallback: one over what they call the fundamental surplus. "
            "<bookmark mark='b'/> Every repair that works shrinks the fundamental surplus. "
            f"<bookmark mark='c'/> With Shimer's numbers, one over one minus 0.4 is about "
            f"{1 / (1 - sh['b']):.1f}, and the elasticity is {sh['elasticity']:.1f}. "
            f"<bookmark mark='d'/> With Hagedorn and Manovskii's, it is about {1 / (1 - hm['b']):.0f}, and the "
            f"elasticity is {hm['elasticity']:.0f}. <bookmark mark='e'/> So the puzzle becomes a question of "
            "measurement: how much of a job's output is left over after paying what the worker could get elsewhere? "
            "If little, small shocks move unemployment a lot."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
