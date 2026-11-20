from __future__ import annotations

from videos.economics.econ33.common import *  # noqa: F403


class Collateral(VoiceoverScene):
    def construct(self):
        card(self, 5, r"Collateral cycles", r"What happens when land is both an input and the security for loans?",
             "Chapter five. Collateral cycles.", lit={1997: r"Kiyotaki and Moore"}, scale=("household", "nation"),
             horizon=("a year", "a decade"))
        self.model()
        self.paths()

    def model(self):
        K = load("km")
        eqs = VGroup(
            label(r"farmers: \ productive, \ but can borrow only against their land", font_size=24, color=HOUSE),
            MathTex(r"b_t \le \frac{q_{t+1}\, k_t}{R}", font_size=40, color=CREDIT),
            label(r"so they invest all their net worth in the down payment:", font_size=22, color=GREY_A),
            MathTex(r"k_t \,\underbrace{\left(q_t - \tfrac{q_{t+1}}{R}\right)}_{\text{user cost } u_t} \;=\; "
                    r"(a + q_t)\,k_{t-1} - R\, b_{t-1}", font_size=38, color=WHITE),
            label(r"gatherers: \ hold the rest of the land, \ where its marginal product is lower", font_size=22,
                  color=CALM),
            MathTex(r"u_t = a\,(k_t / k^*)^{1/\eta}, \qquad q_t = \sum_{s \ge 0} R^{-s}\, u_{t+s}", font_size=36,
                    color=CALM),
        ).arrange(DOWN, buff=0.3).move_to(UP * 0.1)
        foot = label(rf"the Island: \ $R = {K['R']:.1f}$, \ $\eta = {K['eta']:.0f}$; \ land is worth "
                     rf"{K['leverage']:.0f} years of its rent, \ so farmers are leveraged {K['leverage']:.0f} to 1",
                     font_size=21, color=GREY_B).to_edge(DOWN, buff=0.75)
        tag = published_tag(r"Kiyotaki and Moore, \ ``Credit Cycles'', \ \emph{JPE} 105(2) (1997)", corner=DR,
                            font_size=12)
        with self.voiceover(
            "In 1997 Nobuhiro Kiyotaki and John Moore found a mechanism that needs no information problem at all, "
            "only the fact that lenders want security. <bookmark mark='a'/> Farmers are the productive users of "
            "land, but they can borrow only against it: no more than what their land will be worth next period. "
            "<bookmark mark='b'/> So they put all their net worth into the down payment on land. The land they can "
            "hold equals their net worth, divided by the part of the price they must pay themselves, the user cost. "
            "<bookmark mark='c'/> The rest of the land is held by gatherers, who use it less well; the user cost is "
            "their marginal product, and the price of land is the discounted sum of future user costs. "
            "<bookmark mark='d'/> Land is a factor of production and the collateral for the loans that pay for it. "
            "That double role is the whole story."
        ) as vo:
            self.play(FadeIn(eqs[0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(eqs[1]))
            vo.wait_until("b")
            self.play(FadeIn(eqs[2]), FadeIn(eqs[3]))
            vo.wait_until("c")
            self.play(FadeIn(eqs[4]), FadeIn(eqs[5]))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def paths(self):
        K = load("km")
        t = np.array(K["t"])
        ax = plane([0, 15], [-6, 0.5], center=LEFT * 3.3 + DOWN * 0.3, x_length=5.6, y_length=4.4,
                   xticks=[0, 5, 10, 15], yticks=[-6, -4, -2, 0], xlabel=r"periods after the shock",
                   ylabel=r"farmers' land, \ \% from normal", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}",
                   font_size=14)
        ax2 = plane([0, 15], [-0.8, 0.1], center=RIGHT * 3.3 + DOWN * 0.3, x_length=5.6, y_length=4.4,
                    xticks=[0, 5, 10, 15], yticks=[-0.8, -0.6, -0.4, -0.2, 0], xlabel=r"periods after the shock",
                    ylabel=r"\% from normal", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}", font_size=14)
        zero = seg(ax, 0, 0, 15, 0, GREY_C, 1.2)
        zero2 = seg(ax2, 0, 0, 15, 0, GREY_C, 1.2)
        ks = path(ax, t, K["k_static"], GREY_B, 3.0, xr=(0, 15), smooth=False)
        kd = path(ax, t, K["k"], HOUSE, 3.5, xr=(0, 15), smooth=False)
        qd = path(ax2, t, K["q"], CREDIT, 3.2, xr=(0, 15), smooth=False)
        yd = path(ax2, t, K["Y"], OUTPUT, 3.2, xr=(0, 15), smooth=False)
        direct = seg(ax2, 0, -K["direct"], 1.0, -K["direct"], CRISIS, 3.0, dashed=True)
        k1 = VGroup(label(rf"grey: \ price held fixed: \ {K['static']:.2f} $\times$ the shock", font_size=16,
                          color=GREY_B),
                    label(rf"gold: \ with the price's feedback: \ {K['dynamic']:.1f} $\times$", font_size=16,
                          color=HOUSE)).arrange(DOWN, aligned_edge=LEFT, buff=0.06).next_to(ax, UP, buff=0.1)
        k2 = VGroup(label(rf"purple: \ the land price, \ {K['q0']:.2f}\%", font_size=16, color=CREDIT),
                    label(rf"green: \ output, \ {K['Y0']:.2f}\% \ (the shock alone: \ "
                          rf"$-{K['direct']:.2f}\%$, \ red)", font_size=16, color=OUTPUT)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.06).next_to(ax2, UP, buff=0.1)
        foot = label(r"a 1\% loss for the farmers; \ at 2\%, \ this calibration has no equilibrium at all",
                     font_size=21, color=GREY_A).to_edge(DOWN, buff=0.3)
        tag = island_tag(corner=DR, font_size=13)
        with self.voiceover(
            "Now an unexpected bad harvest: the farmers' saleable output falls one percent for one period. "
            "<bookmark mark='a'/> If the price of land stayed put, farmers would have one percent less to put down, "
            f"and their landholding would fall {K['static']:.2f} percent. That is the static effect, and it is "
            "small. <bookmark mark='b'/> But the price does not stay put. With less land in farmers' hands, more "
            "goes to gatherers, the user cost falls, and so, now and for years ahead, does the price of land. "
            "Farmers hold land bought on credit, so a lower price is a capital loss on their whole holding, which "
            "cuts their net worth again. Solving for the price and the path together, the fall in the farmers' "
            f"land is {K['dynamic']:.1f} times the shock. <bookmark mark='c'/> And it lasts: with less net worth "
            "this period, farmers hold less land next period, earn less, and rebuild slowly. "
            "<bookmark mark='d'/> The price of land falls by less than one percent, but on a balance sheet "
            f"leveraged {K['leverage']:.0f} to one that is enough. <bookmark mark='e'/> Output falls "
            f"{abs(K['Y0']):.2f} percent, more than twice the direct loss, and stays low for years as land "
            "sits in the wrong hands. <bookmark mark='f'/> Make the shock two percent and, in this calibration, "
            "there is no price at which the farmers can keep any land on credit: the model breaks, as balance "
            "sheets do in a crisis."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(ax2), FadeIn(zero), FadeIn(zero2), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(ks), FadeIn(k1[0]), run_time=1.4)
            vo.wait_until("b")
            self.play(Create(kd), FadeIn(k1[1]), run_time=1.8)
            vo.wait_until("c")
            self.play(Indicate(kd, color=WHITE, scale_factor=1.0))
            vo.wait_until("d")
            self.play(Create(qd), FadeIn(k2[0]), run_time=1.5)
            vo.wait_until("e")
            self.play(Create(yd), Create(direct), FadeIn(k2[1]), run_time=1.5)
            vo.wait_until("f")
            self.play(FadeIn(foot))
        self.clear_scene()
