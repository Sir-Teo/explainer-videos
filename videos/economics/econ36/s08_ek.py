from __future__ import annotations

from videos.economics.econ36.common import *  # noqa: F403


class EK(VoiceoverScene):
    def construct(self):
        card(self, 7, r"Eaton and Kortum: \ Ricardo with a distribution",
             r"Can comparative advantage produce gravity?", "Chapter seven. Eaton and Kortum: Ricardo with a "
             "distribution.", lit={2002: r"Eaton and Kortum"}, scale=("nation", "world"), horizon=("a decade",))
        self.shares()
        self.prices()

    def shares(self):
        K = load("ek")
        A, S = np.array(K["analytic"]), np.array(K["simulated"])
        names = (r"the Island", r"the Archipelago", r"the Far Isle")
        eq = MathTex(r"\pi_{ni} = \frac{T_i (w_i d_{ni})^{-\theta}}{\sum_k T_k (w_k d_{nk})^{-\theta}}", font_size=40,
                     color=WHITE).to_edge(UP, buff=0.4)
        grid, sim = VGroup(), VGroup()
        for n in range(3):
            for i in range(3):
                w_ = label(f"{100 * A[n, i]:.1f}\\%", font_size=22, color=WHITE)
                g_ = label(f"{100 * S[n, i]:.1f}\\%", font_size=17, color=ARCH)
                VGroup(w_, g_).arrange(DOWN, buff=0.06).move_to(np.array([-1.6 + 2.4 * i, 0.9 - 1.0 * n, 0]))
                grid.add(w_)
                sim.add(g_)
        rows = VGroup(*[label(nm, font_size=18, color=GREY_A).move_to(np.array([-4.6, 0.9 - 1.0 * n, 0]))
                        for n, nm in enumerate(names)])
        cols = VGroup(*[label(nm, font_size=18, color=GREY_A).move_to(np.array([-1.6 + 2.4 * i, 1.7, 0]))
                        for i, nm in enumerate(names)])
        foot = VGroup(
            label(r"each row: \ where a buyer's spending goes; \ white by formula, \ gold from 20,000 simulated goods",
                  font_size=18, color=GREY_A),
            label(r"the formula is gravity: \ size ($T$), \ costs ($w$), \ distance ($d$)", font_size=20,
                  color=GAIN),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.5)
        tag = published_tag(r"Eaton and Kortum, \ \emph{Econometrica} 70(5) (2002); \ the Island", corner=DR,
                            font_size=12)
        with self.voiceover(
            "In 2002 Jonathan Eaton and Samuel Kortum turned Ricardo into a model of many countries. "
            "<bookmark mark='a'/> Each country draws its productivity in each of a continuum of goods at random, "
            "from a distribution whose average level is its technology, T, and whose spread is governed by theta. "
            "Every buyer buys each good from whichever country sells it cheapest, delivered. "
            "<bookmark mark='b'/> The result is a formula for the share of a country's spending that goes to each "
            "supplier. <bookmark mark='c'/> Here it is for three islands, white by the formula, gold from a "
            "simulation of twenty thousand goods with random productivities. The two agree. <bookmark mark='d'/> "
            "And the formula has the shape of gravity: more trade with suppliers that are large and efficient, less "
            "with those that are far away. Comparative advantage, with enough goods, produces gravity, and theta is "
            "the trade elasticity of Part thirty-five's formula."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(rows), FadeIn(cols), LaggedStart(*[FadeIn(g) for g in grid],
                                                                            lag_ratio=0.1), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(eq))
            vo.wait_until("b")
            self.play(Indicate(eq, color=WHITE, scale_factor=1.03))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(g) for g in sim], lag_ratio=0.1), FadeIn(foot[0]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def prices(self):
        P = load("ek_prices")
        names = (r"the Island", r"the Archipelago", r"the Far Isle")
        cols = (ISLAND, ARCH, CHINA)
        first, win = np.array(P["first"]), P["first_win"]
        ax = plane([0.5, 12.5], [-1.5, 1.5], center=LEFT * 3.0 + DOWN * 0.3, x_length=6.4, y_length=4.4,
                   xticks=[1, 4, 8, 12], yticks=[-1, 0, 1], xlabel=r"goods", ylabel=r"log price, \ delivered",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:+.0f}", font_size=13)
        dots_ = VGroup()
        for g in range(12):
            for i in range(3):
                y = float(np.clip(first[g, i], -1.5, 1.5))
                dots_.add(Dot(ax.ax.c2p(g + 1 + 0.18 * (i - 1), y), radius=0.06, color=cols[i],
                              fill_opacity=1.0 if win[g] == i else 0.25))
        rows = VGroup()
        for i in range(3):
            rows.add(VGroup(label(names[i], font_size=18, color=cols[i]),
                            label(rf"wins {100 * P['share'][i]:.0f}\% of goods", font_size=17, color=WHITE),
                            label(rf"mean log price paid: \ {P['mean_log'][i]:+.3f}", font_size=17,
                                  color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.08))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(RIGHT * 3.6 + DOWN * 0.1)
        theory = label(rf"theory, \ the same for every source: \ {P['theory_mean_log']:+.3f}", font_size=18,
                       color=GAIN).next_to(rows, DOWN, buff=0.35)
        head = label(r"what the Island pays, \ good by good \ (bright: \ the cheapest source wins)", font_size=20,
                     color=E.ACCENT).to_edge(UP, buff=0.45)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "The model has a property that surprises everyone who meets it. <bookmark mark='a'/> For each good, "
            "every island offers the Island a delivered price, and the cheapest wins: the bright dots. "
            f"<bookmark mark='b'/> The Archipelago, with the best technology, wins {100 * P['share'][1]:.0f} percent "
            f"of the goods; the Island itself {100 * P['share'][0]:.0f}; the distant Far Isle only "
            f"{100 * P['share'][2]:.0f}. <bookmark mark='c'/> Now ask what the Island pays for the goods it buys from "
            "each source. You might expect the strong supplier's goods to be cheaper. They are not: the average log "
            "price is the same whichever island sold the good. <bookmark mark='d'/> A strong supplier wins more "
            "goods, including ones where it is only barely the cheapest, and those marginal wins exactly offset its "
            "advantage. That is why a country's share of a buyer's spending equals its share of the goods it wins, "
            "and why the formula is so simple."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(head), FadeIn(dots_, lag_ratio=0.01), run_time=2.0)
            vo.wait_until("a")
            self.play(Indicate(VGroup(*[d for d in dots_ if d.get_fill_opacity() > 0.9]), color=WHITE))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r[:2]) for r in rows], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r[2]) for r in rows], lag_ratio=0.3))
            vo.wait_until("d")
            self.play(FadeIn(theory))
        self.clear_scene()
