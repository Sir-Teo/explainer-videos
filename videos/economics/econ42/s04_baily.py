from __future__ import annotations

from videos.economics.econ42.common import *  # noqa: F403


class Baily(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Optimal unemployment insurance, \ derived", r"What two numbers set the best benefit?",
             "Chapter three. Optimal unemployment insurance, derived.", lit={1978: r"Baily", 2006: r"Chetty"},
             scale=("person", "nation"), horizon=("a year",))
        self.derive()
        self.sides()
        self.measurable()

    def derive(self):
        lines = VGroup(
            MathTex(r"W = e\,u(c_e) + (1 - e)\,u(c_u) - \psi(e), \qquad (1 - e)\,b = e\,\tau", font_size=36),
            MathTex(r"dW = (1 - e)\,u'(c_u)\,db \;-\; e\,u'(c_e)\,d\tau", font_size=36),
            MathTex(r"d\tau = \frac{1 - e}{e}\,db \;+\; \frac{b}{e^{2}}\,(-de)", font_size=36),
            MathTex(r"\frac{u'(c_u) - u'(c_e)}{u'(c_e)} \;=\; \frac{\varepsilon_{1-e,\,b}}{e}", font_size=46,
                    color=E.ACCENT),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.5)
        notes = VGroup(
            label(r"welfare: \ found work, \ or not, \ less the cost of searching; \ the budget balances",
                  font_size=18, color=GREY_A),
            label(r"raise $b$: \ the unemployed gain; \ the employed pay more tax \ (the worker's own search "
                  r"change nets out)", font_size=18, color=GREY_A),
            label(r"the tax rises for two reasons: \ the benefit itself, \ and fewer finding work", font_size=18,
                  color=GREY_A),
            label(r"left: \ the value of moving a dollar to the unemployed; \ right: \ the cost through longer "
                  r"unemployment", font_size=18, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(DOWN, buff=0.35)
        tag = published_tag(tables.UI_THEORY.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Martin Baily in 1978, and Raj Chetty in 2006, reduced the question to a formula. Take one worker who "
            "has lost a job. <bookmark mark='a'/> Welfare is the chance e of finding work times the utility of "
            "consumption when employed, plus the chance of not finding it times the utility when unemployed, minus "
            "the cost of searching. The benefits are paid by a tax on those who find work, so the budget balances. "
            "<bookmark mark='b'/> Raise the benefit a little. The unemployed gain the marginal utility of their "
            "consumption on each extra dollar; the employed lose it on the extra tax. The worker's own change in "
            "search does not count, because it was already chosen to make the worker best off. "
            "<bookmark mark='c'/> The tax must rise for two reasons: to pay the higher benefit, and because fewer "
            "people now find work and pay in. <bookmark mark='d'/> Set the change in welfare to zero, and out "
            "comes Baily's formula. On the left, how much more a dollar is worth to the unemployed than to the "
            "employed. On the right, the elasticity of the chance of staying unemployed with respect to the "
            "benefit, divided by the chance of finding work: the cost of the extra unemployment benefits cause."
        ) as vo:
            self.play(Write(lines[0]), FadeIn(notes[0]), FadeIn(tag), run_time=2.0)
            for mk, k in zip("bcd", range(1, 4)):
                vo.wait_until(mk)
                self.play(Write(lines[k]), FadeIn(notes[k]), run_time=1.5)
        self.clear_scene()

    def sides(self):
        B = load("baily")
        b = np.array(B["b"])
        ax = plane([0, 0.6], [0, 1.2], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.6,
                   xticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6], yticks=[0, 0.4, 0.8, 1.2],
                   xlabel=r"benefit, \ share of the wage", ylabel=r"each side of the formula",
                   xfmt=lambda v: f"{100 * v:.0f}\\%", yfmt=lambda v: f"{v:.1f}", font_size=14)
        g = path(ax, b, B["gain"], SMOOTH, 3.4, yr=(0, 1.2))
        c = path(ax, b, B["cost"], COST, 3.4, yr=(0, 1.2))
        at = B["at"]
        cross = VGroup(vline(ax, B["bstar"], 0, 1.2, GAIN), dot(ax, B["bstar"], at["gain"], GAIN, 0.09))
        side = VGroup(
            label(r"blue: \ the gain from \\ smoothing consumption \\ falls as benefits rise", font_size=18,
                  color=SMOOTH),
            label(r"red: \ the cost of longer \\ unemployment rises", font_size=18, color=COST),
            label(rf"they cross at {100 * B['bstar']:.0f}\%: \\ both equal {at['gain']:.2f}", font_size=19,
                  color=GAIN),
            label(r"the same benefit \\ that maximized welfare \\ in chapter 2", font_size=18, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "On the Island, both sides can be computed at every benefit. <bookmark mark='a'/> The gain from "
            "smoothing consumption is large when benefits are small, because losing a job then means a deep fall in "
            "consumption, and it shrinks as benefits rise. <bookmark mark='b'/> The cost rises with the benefit, "
            "as more people search less and the tax to pay for them climbs. <bookmark mark='c'/> They cross at "
            f"{say_pct(B['bstar'], 0)} of the wage, where both equal {at['gain']:.2f}. <bookmark mark='d'/> That is "
            "exactly the benefit that maximized welfare in the game. The formula is not an approximation in this "
            "model; it is the condition for the best benefit, written in quantities that can be measured."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(g), FadeIn(side[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(c), FadeIn(side[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(cross), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def measurable(self):
        lines = VGroup(
            MathTex(r"\frac{u'(c_u) - u'(c_e)}{u'(c_e)} \;\approx\; \gamma\,\frac{\Delta c}{c}", font_size=42),
            MathTex(r"\gamma\,\frac{\Delta c}{c} \;\approx\; \varepsilon", font_size=52, color=E.ACCENT),
        ).arrange(DOWN, buff=0.6).move_to(UP * 0.9)
        cards = point_cards([
            (r"$\gamma$", r"risk aversion: \\ how much a fall \\ in consumption hurts", RISK),
            (r"$\Delta c / c$", r"the fall in consumption \\ on losing a job: \\ measured in surveys", SMOOTH),
            (r"$\varepsilon$", r"how much benefits \\ lengthen unemployment: \\ measured from reforms", COST),
        ], width=11.6, cols=3, font_size=20).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "To use the formula on real data, one more step. <bookmark mark='a'/> For moderate falls in "
            "consumption, the left side is approximately risk aversion, gamma, times the percentage fall in "
            "consumption on losing a job. <bookmark mark='b'/> So the rule becomes: benefits are about right when "
            "risk aversion times the consumption drop equals the elasticity of unemployment with respect to "
            "benefits. <bookmark mark='c'/> Risk aversion is the subject of Part seven. <bookmark mark='d'/> The "
            "consumption drop can be measured in household surveys. <bookmark mark='e'/> And the elasticity can be "
            "measured from changes in benefits. The next chapter measures the last two."
        ) as vo:
            self.play(Write(lines[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Write(lines[1]))
            for mk, c in zip("cde", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
