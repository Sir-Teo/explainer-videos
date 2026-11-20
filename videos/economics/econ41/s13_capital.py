from __future__ import annotations

from videos.economics.econ41.common import *  # noqa: F403


class Capital(VoiceoverScene):
    def construct(self):
        card(self, 11, r"Taxing capital", r"Should saving be taxed at all?",
             "Chapter eleven. Taxing capital.", lit={1976: r"Atkinson and Stiglitz", 1985: r"Judd",
                                                     1986: r"Chamley", 2020: r"Straub and Werning"},
             scale=("household", "nation"), horizon=("a decade", "a century"))
        self.compound()
        self.debate()

    def compound(self):
        years = np.arange(0, 41)
        r = 0.05
        rows = []
        for tau, col in ((0.0, GAIN), (0.25, REVENUE), (0.5, LOSS)):
            rows.append((tau, col, (1 + r * (1 - tau)) ** years))
        ax = plane([0, 40], [1, 7.5], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.4, y_length=4.6,
                   xticks=[0, 10, 20, 30, 40], yticks=[1, 2, 3, 4, 5, 6, 7], xlabel=r"years saved",
                   ylabel=r"what \$1 saved becomes \ (5\% return)", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        lines = VGroup(*[path(ax, years, v, c, 3.2) for _, c, v in rows])
        side = VGroup(*[label(rf"tax on the return {100 * tau:.0f}\%: \\ \${v[-1]:.2f} after 40 years", font_size=18,
                              color=c) for tau, c, v in rows])
        cut = 100 * (1 - rows[2][2][-1] / rows[0][2][-1])
        side.add(label(rf"a {100 * rows[2][0]:.0f}\% tax on the return \\ is a {cut:.0f}\% "
                       r"tax on \\ consumption 40 years on", font_size=18, color=WHITE))
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "A tax on the return to saving compounds. <bookmark mark='a'/> A dollar saved at five percent becomes "
            f"{rows[0][2][-1]:.2f} dollars in forty years without tax; <bookmark mark='b'/> with a quarter of the "
            f"return taxed, {rows[1][2][-1]:.2f}; <bookmark mark='c'/> with half, {rows[2][2][-1]:.2f}. "
            "<bookmark mark='d'/> So a tax of half the return is, in effect, a tax of "
            f"{100 * (1 - rows[2][2][-1] / rows[0][2][-1]):.0f} percent on consumption forty years away, and the "
            "further away, the heavier. That is the root of the case against taxing capital."
        ) as vo:
            self.play(FadeIn(ax), run_time=1.0)
            for mk, k in zip("abc", range(3)):
                vo.wait_until(mk)
                self.play(Create(lines[k]), FadeIn(side[k]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def debate(self):
        cards = point_cards([
            (r"Atkinson and Stiglitz", r"with a good income \\ tax and separable \\ tastes, \ do not tax \\ saving "
                                       r"either", TOP),
            (r"Chamley and Judd", r"in an infinite-horizon \\ economy, \ the optimal \\ long-run tax on \\ capital is "
                                  r"zero", RATE),
            (r"Straub and Werning", r"in Judd's own model \\ the long-run tax is \\ positive when the \\ elasticity of "
                                    r"\\ substitution is below one", GAIN),
            (r"what remains", r"returns differ across \\ people; \ inheritances; \\ rents: \ reasons to \\ tax capital "
                              r"after all", WORKER),
        ], width=12.8, cols=4, font_size=18).move_to(DOWN * 0.1)
        head = label(r"the case against taxing capital, \ and its unravelling", font_size=28,
                     color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.CAPITAL_TAX.tag, corner=DR, font_size=10)
        with self.voiceover(
            "Two famous results said: do not tax capital. <bookmark mark='a'/> Atkinson and Stiglitz: if the income "
            "tax is well designed and tastes are separable, taxing saving, which is taxing future consumption, adds "
            "nothing. <bookmark mark='b'/> Christophe Chamley and Kenneth Judd, in the mid-1980s: in an economy of "
            "infinitely lived dynasties, the optimal tax on capital income is zero in the long run, even for a "
            "government that cares only about workers. <bookmark mark='c'/> In 2020 Ludwig Straub and Ivan Werning "
            "re-examined the models, and found that in Judd's main model the long-run tax is positive and large "
            "whenever the elasticity of intertemporal substitution is below one, as many estimates suggest. "
            "<bookmark mark='d'/> Add what the simple models leave out, that returns differ across people, that "
            "wealth is inherited, that some capital income is rent, and the case for some tax on capital returns."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
