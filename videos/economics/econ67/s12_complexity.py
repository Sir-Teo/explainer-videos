from __future__ import annotations

from videos.economics.econ67.common import *  # noqa: F403

PATH_COL = {"1.0": TRUE, "4.0": PUB, "9.0": FAIL}


class Complexity(VoiceoverScene):
    def construct(self):
        card(self, 10, r"What the models leave out", r"What happens when traders are not all alike, \ and switch "
             r"between rules of thumb?", "Chapter ten. What the models leave out.",
             lit={1997: "Brock and Hommes", 2009: "Farmer and Foley", 2021: "Arthur"}, scale=("market", "world"),
             horizon=("a year",))
        self.case()
        self.market()
        self.bifurcation()
        self.verdict()

    def case(self):
        cards = point_cards([
            (r"the complaint", r"equilibrium models assume the economy has settled; \ agents are alike or average "
             r"out; \ expectations are right on average", FAIL),
            (r"the alternative", r"agent-based models: \ many different agents with rules, \ interacting; \ the "
             r"aggregate is whatever emerges \ (Arthur; \ Farmer and Foley)", FIRST),
            (r"its best case", r"booms, \ crashes and fat tails can come from inside the economy, \ without a shock "
             r"from outside \ (Parts 33 and 52)", PUB),
            (r"its problem", r"many free parameters; \ many models fit the same facts; \ hard to estimate and "
             r"to refute", STATE),
        ], width=12.6, cols=2, font_size=19).move_to(DOWN * 0.2)
        head = label(r"complexity economics", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(r"Farmer and Foley, \ \emph{Nature} 460 (2009); \ Arthur, \ \emph{Nature Reviews "
                            r"Physics} 3 (2021)", corner=DL, font_size=12)
        with self.voiceover(
            "Most of this series has used equilibrium models. Their critics have a case. <bookmark mark='a'/> The "
            "complaint: equilibrium models assume the economy has already settled, that people are alike or average "
            "out, and that expectations are right on average. <bookmark mark='b'/> The alternative, argued by Brian "
            "Arthur and by Doyne Farmer and Duncan Foley after the crisis of 2008, is to simulate many different "
            "agents following rules, and let the aggregate be whatever emerges. <bookmark mark='c'/> Its best case: "
            "booms, crashes and fat-tailed swings can come from inside the economy, with no shock from outside, as "
            "in the credit cycles of Part thirty-three. <bookmark mark='d'/> Its problem is the mirror image of its "
            "freedom: many parameters, many models that fit the same facts, and few ways to estimate or refute them. "
            "One model shows both sides."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def market(self):
        B = load("abm")
        eqs = VGroup(
            MathTex(r"-B\,x_t", r"=", r"b\,\big[n_t\,x_t + (1 - n_t)\,x_{t-1}\big]", font_size=36),
            MathTex(r"n_t = \frac{1}{1 + e^{-\beta\,\left[\frac{b}{2}(x_{t-1} - x_{t-2})^2 - C\right]}}",
                    font_size=36),
        ).arrange(DOWN, buff=0.5).move_to(UP * 1.2)
        eqs[0][2].set_color(PUB)
        rows = VGroup(
            label(r"$x$: \ the price's distance from its steady state; \ demand $-Bx$, \ supply from forecasts",
                  font_size=19, color=GREY_A),
            label(r"a share $n$ pays $C$ for the correct forecast; \ the rest expect last period's price, \ free",
                  font_size=19, color=PUB),
            label(r"each period, \ traders switch towards whichever rule did better, \ net of its cost; \ $\beta$: "
                  r"how fast", font_size=19, color=FIRST),
            label(rf"here $b/B = {B['b_over_B']:.2f}$: \ naive traders alone would make the market explode",
                  font_size=19, color=FAIL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(eqs, DOWN, buff=0.55)
        tag = published_tag(r"Brock and Hommes, \ \emph{Econometrica} 65(5) (1997)", corner=DL, font_size=12)
        with self.voiceover(
            "William Brock and Cars Hommes built it in 1997, on the oldest model of a farm market, the cobweb. "
            "<bookmark mark='a'/> "
            "Farmers decide how much to plant before they know the price, so supply depends on what they expect. "
            "<bookmark mark='b'/> Some pay a cost for the correct forecast; the rest simply expect last period's "
            "price, for free. <bookmark mark='c'/> Each period, farmers switch towards whichever rule earned more "
            "last time, net of its cost. Beta measures how quickly they switch. <bookmark mark='d'/> And the supply "
            "curve is steeper than demand, so a market of naive farmers alone would swing ever wider. Near the "
            "steady state the naive rule is good enough and costs nothing; far from it, the correct forecast pays."
        ) as vo:
            self.play(FadeIn(tag), Write(eqs[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Write(eqs[1]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def bifurcation(self):
        B = load("abm")
        ax = plane([0, 10], [-1.0, 1.0], center=LEFT * 2.6 + DOWN * 0.35, x_length=7.0, y_length=5.0,
                   xticks=[0, 2, 4, 6, 8, 10], yticks=[-1, -0.5, 0, 0.5, 1],
                   xlabel=r"$\beta$, \ how fast traders switch", ylabel=r"prices visited, \ $x$",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}".replace("-", "{-}"), font_size=14)
        seen, per, pts_ = set(), {}, []
        for b_, x_ in zip(B["beta"], B["x"]):
            key_ = (round(b_, 3), round(x_, 2))
            if -1 <= x_ <= 1 and key_ not in seen and per.get(key_[0], 0) < 30:
                seen.add(key_)
                per[key_[0]] = per.get(key_[0], 0) + 1
                pts_.append((b_, x_))
        cloud = VGroup(*[Dot(ax.ax.c2p(b_, x_), radius=0.014, color=PUB, fill_opacity=0.8) for b_, x_ in pts_])
        cb = [b_ for b_, _ in pts_]
        flip = vline(ax, B["beta_flip"], -1, 1, GREY_B, 1.6)
        fl = label(rf"$\beta = {B['beta_flip']:.2f}$", font_size=14, color=GREY_B).next_to(ax.ax.c2p(
            B["beta_flip"], 0.85), RIGHT, buff=0.08)
        # three paths on the right
        small = VGroup()
        for k, (bk, col) in enumerate(PATH_COL.items()):
            pa = plane([0, 70], [-1, 1], x_length=4.6, y_length=1.25, xticks=[], yticks=[], font_size=10)
            xs = B["paths"][bk]["x"]
            ln = path(pa, list(range(len(xs))), xs, col, 2.0, smooth=False)
            t = label(rf"$\beta = {float(bk):.0f}$: \ " + (r"a steady state" if k == 0 else
                                                          (r"a two-cycle" if k == 1 else r"chaos")),
                      font_size=15, color=col).next_to(pa.ax, UP, buff=0.04).align_to(pa.ax, LEFT)
            small.add(VGroup(pa, ln, t))
        small.arrange(DOWN, buff=0.35).next_to(ax.ax, RIGHT, buff=0.7)
        if small.get_right()[0] > 6.9:
            small.scale_to_fit_width(6.9 - small.get_left()[0])
        tag = island_tag(r"computed: \ agora.field.brock\_hommes \ ($b/B = 1.35$, \ $C = 1$)", corner=DL,
                         font_size=12)
        with self.voiceover(
            "Now vary one number, how fast traders switch, and record the prices the market keeps visiting. "
            "<bookmark mark='a'/> When they switch slowly, enough of them pay for the correct forecast and the "
            "price settles at its steady state. <bookmark mark='b'/> Beyond a beta of "
            f"{B['beta_flip']:.1f}, the steady state loses its stability: the market alternates between a high price "
            "and a low one, as traders flood into the free rule when prices are calm and pay for the good one when "
            "they swing. <bookmark mark='c'/> Faster still, the cycle splits, and splits again, and the prices "
            "become chaotic: never repeating, though nothing outside the market has changed. <bookmark mark='d'/> "
            "Fluctuations from nowhere, with every trader acting sensibly. That is the agent-based case in one "
            "picture."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(small[0][0]), Create(small[0][1]), FadeIn(small[0][2]))
            self.play(FadeIn(VGroup(*[d for d, b_ in zip(cloud, cb) if b_ < B["beta_flip"]])))
            vo.wait_until("b")
            self.play(Create(flip), FadeIn(fl), FadeIn(small[1][0]), Create(small[1][1]), FadeIn(small[1][2]))
            self.play(FadeIn(VGroup(*[d for d, b_ in zip(cloud, cb) if B["beta_flip"] <= b_ < 6.5])))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*[d for d, b_ in zip(cloud, cb) if b_ >= 6.5])), FadeIn(small[2][0]),
                      Create(small[2][1]), FadeIn(small[2][2]), run_time=2.0)
        self.clear_scene()

    def verdict(self):
        rows = VGroup(
            label(r"the same price data fit many values of $\beta$ \ and many other models", font_size=22,
                  color=STATE),
            label(r"Brock and Hommes's model can be estimated; \ many agent-based models cannot", font_size=22,
                  color=PUB),
            label(r"in laboratories, \ people do switch between simple forecasting rules", font_size=22,
                  color=TRUE),
            label(r"the series' view: \ a tool for mechanisms, \ disciplined by data like any other", font_size=22,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(UP * 0.2)
        with self.voiceover(
            "And the other side. <bookmark mark='a'/> Chaotic prices can look like random shocks, so the same data "
            "fit many values of beta and many other models. <bookmark mark='b'/> This model is small enough to "
            "estimate; many agent-based models, with hundreds of rules and parameters, are not. <bookmark mark='c'/> "
            "Where the idea has been tested, in laboratory markets, people do switch between simple forecasting "
            "rules much as the model says. <bookmark mark='d'/> So the view of this series: agent-based models are "
            "a way to explore mechanisms that equilibrium models assume away, like the networks of Part sixty-three "
            "and the many agents of Part fifty-two. They earn trust the same way as everything else, by meeting "
            "data."
        ) as vo:
            for mk, r_ in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()
