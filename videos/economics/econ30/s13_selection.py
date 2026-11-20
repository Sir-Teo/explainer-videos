from __future__ import annotations

from videos.economics.econ30.common import *  # noqa: F403


class Selection(VoiceoverScene):
    def construct(self):
        card(self, 11, r"Menu costs and the selection effect", r"Does it matter which prices change?", "Chapter "
             "eleven. Menu costs and the selection effect.", lit={2007: r"Golosov and Lucas"}, scale=("firm",),
             horizon=("a month", "two years"))
        self.idea()
        self.race()

    def idea(self):
        rows = VGroup(
            label(r"Calvo: \ the fairy picks firms at random", font_size=25, color=CB),
            label(r"menu costs: \ a firm reprices when its price is far enough from where it should be",
                  font_size=23, color=PRICE),
            label(r"after a rise in money, \ the firms that reprice are the ones furthest below", font_size=23,
                  color=FLEX),
            label(r"so the few price changes are large, \ and do most of the adjusting", font_size=23,
                  color=E.ACCENT),
            label(r"Golosov and Lucas, \ 2007: \ the selection effect", font_size=25, color=E.ACCENT),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"Golosov and Lucas, \ \emph{JPE} 115(2) (2007); \ Caplin and Spulber, \ \emph{QJE} "
                            r"102(4) (1987)", corner=DR, font_size=12)
        with self.voiceover(
            "Calvo's fairy has a hidden cost. <bookmark mark='a'/> It picks firms at random. "
            "<bookmark mark='b'/> With a real menu cost, a firm reprices when its price has drifted far enough "
            "from where it should be. <bookmark mark='c'/> After a rise in the money supply, the firms that "
            "reprice are the ones furthest below their best price, <bookmark mark='d'/> so the price changes that "
            "happen are large ones, and they do most of the adjusting. <bookmark mark='e'/> Mikhail Golosov and "
            "Robert Lucas called this the selection effect, in 2007. It can make money far less powerful than "
            "Calvo's model says, even with the same number of price changes."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def race(self):
        S = load("setters")
        T = island.truths(30)["setters"]
        c, m = np.array(S["calvo"]["pass_through"]), np.array(S["menu"]["pass_through"])
        months = np.arange(1, len(c) + 1)
        ax = plane([0, 24], [0, 1.1], center=LEFT * 2.0 + DOWN * 0.3, x_length=8.0, y_length=4.8,
                   xticks=[0, 6, 12, 18, 24], yticks=[0, 0.25, 0.5, 0.75, 1.0], xlabel=r"months after money rises",
                   ylabel=r"share of the rise passed into prices", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=15)
        full = seg(ax, 0, 1, 24, 1, GREY_C, 1.5, dashed=True)
        cl = path(ax, np.concatenate([[0], months]), np.concatenate([[0], c]), CB, 3.5, smooth=False)
        ml = path(ax, np.concatenate([[0], months]), np.concatenate([[0], np.minimum(m, 1.05)]), PRICE, 3.5,
                  smooth=False)
        side = VGroup(
            label(rf"{T['n']:,} firms; \ {100 * T['freq']:.0f}\% reprice \\ in a normal month, \ in both"
                  .replace(",", "{,}"), font_size=19, color=GREY_A),
            label(rf"money rises {100 * T['shock']:.0f}\%", font_size=19, color=E.ACCENT),
            label(rf"green: \ Calvo: \ half passed through \\ after {S['half_calvo']} months", font_size=19,
                  color=CB),
            label(rf"gold: \ menu costs: \ after {S['half_menu']} month{'s' if S['half_menu'] != 1 else ''}",
                  font_size=19, color=PRICE),
            label(rf"output lost: \ {S['real_calvo']:.0f} against {S['real_menu']:.0f} \\ percent-months",
                  font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.36).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            f"Here is a race between the two, on the Island, with {T['n']:,} firms whose best prices drift "
            "randomly from month to month. <bookmark mark='a'/> In both economies a tenth of firms reprice in a "
            f"normal month. <bookmark mark='b'/> Then money rises by {100 * T['shock']:.0f} percent. "
            "<bookmark mark='c'/> Under Calvo, prices follow slowly: half of the rise has passed into prices after "
            f"{S['half_calvo']} months. <bookmark mark='d'/> Under menu costs, the firms that were already close to "
            "repricing jump at once, and half has passed through within the first month. "
            "<bookmark mark='e'/> Measured as output, or real money, lost along the way, Calvo gives "
            f"{S['real_calvo']:.0f} percent-months, menu costs {S['real_menu']:.0f}. The frequency of price changes "
            "is not enough to know how much money matters; which prices change matters too. Later work, with sales "
            "and multi-product firms, restores much of the effect, and the size of the selection effect is still "
            "argued."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(full), FadeIn(tag), run_time=0.6)
            for mk, r_ in zip("ab", side[:2]):
                vo.wait_until(mk)
                self.play(FadeIn(r_))
            vo.wait_until("c")
            self.play(Create(cl), FadeIn(side[2]), run_time=2)
            vo.wait_until("d")
            self.play(Create(ml), FadeIn(side[3]), run_time=2)
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()
