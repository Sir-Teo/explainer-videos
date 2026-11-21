from __future__ import annotations

from videos.economics.econ63.common import *  # noqa: F403

THETAS = (("theta_0.15", 0.15, SHOCK), ("theta_0.5", 0.5, SEED), ("theta_1", 1.0, GREY_B), ("theta_1.5", 1.5, LINK))


class Nonlinear(VoiceoverScene):
    def construct(self):
        card(self, 5, r"Beyond Hulten: \ large shocks", r"When does a sector matter more than its sales?",
             "Chapter five. Beyond Hulten: large shocks.", lit={1973: r"the oil embargo", 2019: r"Baqaee and Farhi"},
             scale=("market", "nation"), horizon=("a year",))
        self.curves()
        self.weight()
        self.oil()

    def curves(self):
        R = load("response")
        x = 100 * np.array(R["shocks"])
        ax = plane([-72, 32], [-30, 10], center=LEFT * 2.3 + DOWN * 0.3, x_length=7.2, y_length=5.0,
                   xticks=[-60, -40, -20, 0, 20], yticks=[-30, -20, -10, 0, 10],
                   xlabel=r"change in energy's productivity, \ log points",
                   ylabel=r"change in GDP, \ log points", xfmt=lambda v: f"{v:+.0f}".replace("-", "{-}") if v else "0",
                   yfmt=lambda v: f"{v:+.0f}".replace("-", "{-}") if v else "0", font_size=14)
        hl = path(ax, x, 100 * np.array(R["hulten"]), WHITE, 2.4, smooth=False)
        hl = DashedVMobject(hl, num_dashes=40)
        curves = {k: path(ax, x, 100 * np.array(R[k]), c, 3.4) for k, _, c in THETAS}
        side = VGroup(
            label(r"dashed: \ Hulten's straight line, \ slope 0.25", font_size=19, color=WHITE),
            label(r"grey: \ inputs substitute at elasticity 1: \ exactly Hulten", font_size=19, color=GREY_B),
            label(r"red: \ hard to substitute \ (0.15): \ losses bend down", font_size=19, color=SHOCK),
            label(r"blue: \ easy to substitute \ (1.5): \ losses soften", font_size=19, color=LINK),
            label(r"with complements, \ busts are deeper than booms are high", font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        if side.width > 5.6:
            side.width = 5.6
            side.to_edge(RIGHT, buff=0.3)
        lo = R["theta_0.15"][0]
        tag = island_tag(r"the Island: \ CES production network; \ agora.network.gdp\_response", corner=DL,
                         font_size=12)
        with self.voiceover(
            "Hulten's theorem is a statement about small shocks. David Baqaee and Emmanuel Farhi asked what happens "
            "with large ones. On the Island, change energy's productivity by every amount from a severe loss to a "
            "healthy gain. <bookmark mark='a'/> Hulten's rule is a straight line through the origin, with slope "
            "equal to energy's sales share, a quarter. <bookmark mark='b'/> If firms can swap between inputs with "
            "an elasticity of one, the computed response lies exactly on it. <bookmark mark='c'/> If inputs are "
            "hard to substitute, as they are within a year, the curve bends down: a loss of seventy log points in "
            f"energy costs {-100 * lo:.0f} log points of GDP, not seventeen and a half. <bookmark mark='d'/> If "
            "inputs are easy to substitute, it bends the other way. <bookmark mark='e'/> And with complements the "
            "curve is not symmetric: a bad shock costs more than a good shock of the same size gains."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(hl), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(curves["theta_1"]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(curves["theta_0.15"]), Create(curves["theta_0.5"]), FadeIn(side[2]), run_time=1.6)
            vo.wait_until("d")
            self.play(Create(curves["theta_1.5"]), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def weight(self):
        R = load("response")
        xs = np.array(R["shocks"])
        x = 100 * xs
        ax = plane([-72, 32], [0, 0.65], center=LEFT * 2.3 + DOWN * 0.3, x_length=7.2, y_length=4.8,
                   xticks=[-60, -40, -20, 0, 20], yticks=[0, 0.2, 0.4, 0.6],
                   xlabel=r"change in energy's productivity, \ log points", ylabel=r"energy's sales over GDP",
                   xfmt=lambda v: f"{v:+.0f}".replace("-", "{-}") if v else "0", yfmt=lambda v: f"{v:.1f}",
                   font_size=14)
        lines = VGroup(*[path(ax, x, np.gradient(np.array(R[k]), xs), c, 3.2) for k, _, c in THETAS])
        sl = np.gradient(np.array(R["theta_0.15"]), xs)
        eq = label(r"$\dfrac{d^2 \log Y}{d \log A_i^2} = \dfrac{d \lambda_i}{d \log A_i}$", font_size=32)
        side = VGroup(
            eq,
            label(r"Hulten holds at every point: \\ the slope is always the sales share", font_size=19, color=WHITE),
            label(rf"but with complements the share moves: \\ energy grows dearer and its share rises, \\ "
                  rf"0.25 to {sl[0]:.2f}", font_size=19, color=SHOCK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.35)
        tag = island_tag(r"the Island: \ slopes of the curves before", corner=DL, font_size=12)
        with self.voiceover(
            "Why does the curve bend? <bookmark mark='a'/> Hulten's rule still holds at every point on it: the "
            "slope is always energy's current sales share. The second derivative is the change in that share. "
            "<bookmark mark='b'/> Plot the share. When inputs substitute at an elasticity of one, it never moves. "
            "<bookmark mark='c'/> When they are complements, energy grows scarce and dear, everyone still needs it, "
            f"so spending on it rises: its share climbs from a quarter towards {sl[0]:.2f}, and each further loss "
            "costs more than the last. The network matters again, through prices: a sector that everyone needs "
            "and nobody can replace becomes a bigger share of the economy exactly when it fails."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(Create(lines[2]), run_time=1.2)
            vo.wait_until("c")
            self.play(Create(lines[0]), Create(lines[1]), Create(lines[3]), FadeIn(side[2]), run_time=1.6)
        self.clear_scene()

    def oil(self):
        cards = VGroup(
            history_card(1973, r"the oil embargo", r"the price of crude roughly quadruples in a few months; \ oil is a "
                         r"small share of rich countries' spending, \ yet recessions follow", color=SEED, width=11.2,
                         font_size=21),
            history_card(2019, r"Baqaee and Farhi", r"the macroeconomic impact of microeconomic shocks: \ second-order "
                         r"terms, \ set by elasticities and by the network, \ can dominate for large shocks to "
                         r"inputs that are hard to replace", color=SHOCK, width=11.2, font_size=21),
            history_card(r"the lesson", r"sales first, \ then substitution", r"a small sector can matter a great deal, "
                         r"\ if it is essential and the shock is large", color=GDP, width=11.2, font_size=21),
        ).arrange(DOWN, buff=0.35).move_to(UP * 0.2)
        tag = published_tag(r"Baqaee and Farhi, \ Econometrica 87(4) (2019)", corner=DL, font_size=12)
        with self.voiceover(
            "This is an old puzzle with a new answer. <bookmark mark='a'/> In 1973 the price of crude oil roughly "
            "quadrupled within a few months. Oil was a small share of rich countries' spending, and Hulten's "
            "arithmetic says a small sector cannot cost much. Yet recessions followed. <bookmark mark='b'/> Baqaee "
            "and Farhi showed that the second-order terms, which depend on elasticities of substitution and on the "
            "shape of the network, can dominate when the shock is large and the input is hard to replace. "
            "<bookmark mark='c'/> So the rule is: sales first, then substitution. A small sector can matter a "
            "great deal if nobody can do without it, and the shock is big. Which brings us back to Japan."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.1), FadeIn(tag))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(cards[2], shift=UP * 0.1))
        self.clear_scene()
