from __future__ import annotations

from videos.economics.econ53.common import *  # noqa: F403


class Relational(VoiceoverScene):
    def construct(self):
        card(self, 13, r"Relational contracts", r"Why keep a promise no court will enforce?",
             "Chapter thirteen. Relational contracts.", lit={2003: r"Levin", 1987: r"Bull"},
             scale=("person", "firm"), horizon=("a decade",))
        self.setup_()
        self.curve()

    def setup_(self):
        R = load("relational")
        rows = VGroup(
            label(r"a firm promises a bonus for good work; \ effort cannot be written into a contract", font_size=22,
                  color=WHITE),
            label(r"after the work is done, \ the firm could keep the bonus", font_size=22, color=ERR),
            label(r"but then the relationship ends, \ and with it all future surplus", font_size=22, color=SENDER),
            label(r"so the promise is kept if the bonus is no more than the future is worth:", font_size=22,
                  color=WHITE),
            MathTex(r"b \;\le\; \frac{\delta}{1 - \delta}\,\big(\text{surplus per period}\big)", font_size=38,
                    color=THEORY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.36).move_to(UP * 0.2)
        rows[4].shift(RIGHT * 1.5)
        tag = published_tag(r"Bull, \ QJE (1987); \ Levin, \ AER 93(3) (2003)", corner=DR, font_size=12)
        with self.voiceover(
            "The last idea is the oldest kind of incentive: a promise kept because the future matters. <bookmark "
            "mark='a'/> A firm promises a bonus for good work, but the quality of the work cannot be written into "
            "a contract a court would enforce. <bookmark mark='b'/> Once the work is done, the firm could simply "
            "keep the bonus. <bookmark mark='c'/> But then the worker leaves, or works badly from then on, and the "
            "firm loses the surplus of the relationship for ever. <bookmark mark='d'/> So the promise is credible "
            "if the bonus is no larger than the discounted value of the future: <bookmark mark='e'/> delta over one "
            "minus delta times the surplus each period. Clive Bull stated it in 1987; Jonathan Levin worked out "
            "the best such contracts in 2003."
        ) as vo:
            self.play(FadeIn(tag))
            for mk, r_ in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        del R
        self.clear_scene()

    def curve(self):
        R = load("relational")
        d = np.array(R["delta"])
        ax = plane([0, 1], [0, 1.2], center=LEFT * 1.8 + DOWN * 0.3, x_length=7.4, y_length=4.6,
                   xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=[0, 0.25, 0.5, 0.75, 1.0],
                   xlabel=r"how much the future matters, \ $\delta$", ylabel=r"effort the promise can sustain",
                   xfmt=lambda v: f"{v:.2f}", yfmt=lambda v: f"{v:.2f}", font_size=14)
        e = path(ax, d, R["effort"], SENDER, 3.0)
        fb = seg(ax, 0, R["first_best"], 1, R["first_best"], GAIN, 1.8, dashed=True)
        ds = vline(ax, R["delta_star"], 0, 1.15, E.ACCENT, 2.0)
        side = VGroup(
            label(r"gold: \ the most effort \\ a self-enforcing bonus buys", font_size=19, color=SENDER),
            label(r"green: \ what a court-enforced \\ contract would buy", font_size=19, color=GAIN),
            label(rf"from $\delta = {R['delta_star']:.2f}$, \\ the promise is as good as a contract", font_size=20,
                  color=E.ACCENT),
            label(r"impatient partners, \ uncertain futures, \\ and the promise shrinks", font_size=19, color=ERR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = island_tag(r"effort $e$ worth $e$, \ costing $e^2/2$; \ computed", corner=DL, font_size=12)
        with self.voiceover(
            "In a simple version, effort produces output worth its amount and costs the worker half its square. "
            "<bookmark mark='a'/> The gold curve is the most effort a self-enforcing bonus can buy, against how "
            "much the future matters. <bookmark mark='b'/> The green line is what a contract a court would "
            "enforce could buy. <bookmark mark='c'/> Once the discount factor reaches "
            f"{R['delta_star']:.2f}, the promise is as good as a contract. <bookmark mark='d'/> Below that, the "
            "bonus that would be needed is larger than the future is worth, and effort falls in proportion. This is "
            "why "
            "long-term relationships, between firms and suppliers and between employers and staff, can do what "
            "contracts cannot, and why a shock that shortens horizons can unravel them. It is the repeated-game "
            "logic of Part eleven, put to work inside the firm."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(e), FadeIn(side[0]), run_time=1.6)
            vo.wait_until("b")
            self.play(Create(fb), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(ds), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
