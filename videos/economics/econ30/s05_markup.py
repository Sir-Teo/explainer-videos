from __future__ import annotations

from videos.economics.econ30.common import *  # noqa: F403


class Markup(VoiceoverScene):
    def construct(self):
        card(self, 4, r"Monopolistic competition: \ the desired markup", r"Why would a firm sell more at a price "
             r"it did not choose?", "Chapter four. Monopolistic competition: the desired markup.",
             lit={1977: r"Dixit and Stiglitz"}, scale=("firm", "market"), horizon=("a quarter",))
        self.markup()
        self.erosion()

    def markup(self):
        M = load("menu")
        eps = M["eps"]
        rows = VGroup(
            label(r"from Part 12: \ many firms, \ each with its own variety", font_size=25, color=E.ACCENT),
            MathTex(r"y_i = \Big(\frac{P_i}{P}\Big)^{-\varepsilon} Y", font_size=38),
            label(r"each firm sets its price; \ the best price is a fixed markup on marginal cost", font_size=23,
                  color=PRICE),
            MathTex(rf"P_i^* = \frac{{\varepsilon}}{{\varepsilon - 1}}\, MC = {eps / (eps - 1):.1f}\, MC "
                    rf"\quad (\varepsilon = {eps:.0f})", font_size=36, color=PRICE),
            label(r"price above marginal cost: \ selling one more unit at the going price is always welcome",
                  font_size=23, color=OUTPUT),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"Dixit and Stiglitz, \ \emph{AER} 67(3) (1977); \ Part 12", corner=DR, font_size=12)
        with self.voiceover(
            "Sticky prices need firms that set prices, so the model starts from Part twelve's monopolistic "
            "competition. <bookmark mark='a'/> Each firm sells its own variety, and its sales fall with its price "
            "relative to the average, with elasticity epsilon. <bookmark mark='b'/> Each firm sets its own price, "
            f"and the best price is a fixed markup on marginal cost. <bookmark mark='c'/> With epsilon at {eps:.0f}, "
            f"twenty percent. <bookmark mark='d'/> That markup does a quiet but essential job. Because price is "
            "above marginal cost, a firm is always glad to sell one more unit at its going price, so when demand "
            "rises and its price is stuck, it simply produces more."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def erosion(self):
        ax = plane([0, 10], [0, 2.0], center=LEFT * 2.2 + DOWN * 0.3, x_length=7.4, y_length=4.8,
                   xticks=[0, 5, 10], yticks=[0, 1, 2], xlabel=r"quantity", ylabel=r"price, \ cost",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=15)
        q = np.linspace(0.3, 10, 120)
        d0 = path(ax, q, np.clip(6 / q, 0, 2.0), GREY_B, 2.5, yr=(0, 2.0))
        d1 = path(ax, q, np.clip(8 / q, 0, 2.0), OUTPUT, 3, yr=(0, 2.0))
        mc = path(ax, q, 0.6 + 0.07 * q, COST, 3)
        p0 = 1.2 * (0.6 + 0.07 * 5.0)
        fixed = seg(ax, 0, p0, 10, p0, PRICE, 3, dashed=True)
        q0, q1 = 6 / p0, 8 / p0
        a0 = dot(ax, q0, p0, WHITE, 0.08)
        a1 = dot(ax, q1, p0, OUTPUT, 0.09)
        mc1 = 0.6 + 0.07 * q1
        gap = seg(ax, q1, mc1, q1, p0, E.ACCENT, 4)
        side = VGroup(
            label(r"grey: \ demand before; \ green: \ after it rises", font_size=19, color=OUTPUT),
            label(r"gold, \ dashed: \ the price, \ stuck", font_size=19, color=PRICE),
            label(r"purple: \ marginal cost, \ rising with output", font_size=19, color=COST),
            label(r"the firm sells more at the old price; \\ its markup shrinks \ (orange)", font_size=19,
                  color=E.ACCENT),
            label(r"output is set by demand, \\ not by the price", font_size=20, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.36).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Here is that firm when demand rises. <bookmark mark='a'/> Demand moves out, from grey to green. "
            "<bookmark mark='b'/> The price is stuck at its old level. <bookmark mark='c'/> Marginal cost rises as "
            "the firm produces more, because it must pay more for overtime and materials. "
            "<bookmark mark='d'/> The firm sells more at the old price, and its markup shrinks, but it remains "
            "positive. <bookmark mark='e'/> So output is set by demand, not by the price: exactly Keynes's "
            "effective demand, now derived from firms that choose. And the gap between what the firm would like to "
            "charge and what it does charge drives the next chapter."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(d0), Create(mc), GrowFromCenter(a0), run_time=1.2)
            vo.wait_until("a")
            self.play(Create(d1), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(fixed), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), Indicate(mc, color=WHITE, scale_factor=1.0))
            vo.wait_until("d")
            self.play(GrowFromCenter(a1), Create(gap), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()
