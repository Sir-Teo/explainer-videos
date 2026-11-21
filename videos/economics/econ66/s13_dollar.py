from __future__ import annotations

from videos.economics.econ66.common import *  # noqa: F403


class Dollar(VoiceoverScene):
    def construct(self):
        card(self, 11, r"The dollar as a hub", r"Why do the world's reserves sit in dollars, \ and can the dollar be "
             r"replaced?", "Chapter eleven. The dollar as a hub.", lit={1965: "d'Estaing"}, scale=("world",),
             horizon=("a decade",))
        self.shares()
        self.why()

    def shares(self):
        ax = plane([-0.6, 2.6], [0, 75], center=LEFT * 3.0 + DOWN * 0.4, x_length=5.8, y_length=4.6, xticks=[],
                   yticks=[0, 20, 40, 60], ylabel=r"share of the world's foreign exchange reserves, \ \%",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        vals = [57.1, 20.0, 22.9]
        b = bars(ax, [0, 1, 2], vals, [US, ROW, GREY_B], width=0.6)
        names = VGroup(*[label(t, font_size=16, color=GREY_A).next_to(ax.ax.c2p(k, 0), DOWN, buff=0.15)
                         for k, t in enumerate((r"the dollar", r"the euro", r"everything else"))])
        nums = VGroup(*[label(rf"{v:.0f}\%", font_size=17, color=c).next_to(bb, UP, buff=0.08)
                        for bb, v, c in zip(b, vals, (US, ROW, GREY_B))])
        then = seg(ax, -0.3, 71, 0.3, 71, GREY_A, 2.4, dashed=True)
        tl = label(r"about 71\% in 2000", font_size=14, color=GREY_A).next_to(ax.ax.c2p(0.3, 71), RIGHT, buff=0.1)
        side = VGroup(
            label(r"the exorbitant privilege: \\ the world lends to America cheaply", font_size=19, color=US),
            label(r"the hub: \ payments clear through American banks, \\ and can be stopped there", font_size=19,
                  color=TARIFF),
            label(r"the slow drift: \ the dollar's share has fallen, \\ mostly to smaller currencies, \ not to one "
                  r"rival", font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(ax.ax, RIGHT, buff=0.7)
        if side.get_right()[0] > 6.9:
            side.scale_to_fit_width(6.9 - side.get_left()[0])
        tag = published_tag(r"IMF, \ COFER, \ first quarter of 2026", corner=DL, font_size=12)
        with self.voiceover(
            "The most important hub of all is a currency. <bookmark mark='a'/> In the first quarter of 2026, by "
            "the IMF's count, fifty-seven percent of the world's foreign exchange reserves were in dollars, twenty "
            "percent in euros, and the rest spread over everything else. At the start of the century the dollar's "
            "share was about seventy-one percent. <bookmark mark='b'/> In the nineteen-sixties the French finance "
            "minister, Valéry Giscard d'Estaing, called America's position an exorbitant privilege: the world "
            "wants dollar assets, so America borrows cheaply. <bookmark mark='c'/> It is also the hub of chapter "
            "six: dollar payments clear through American banks, and can be stopped there. <bookmark mark='d'/> The "
            "dollar's share has drifted down, but mostly towards a scatter of smaller currencies, not towards one "
            "rival."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(names), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(bb, DOWN) for bb in b], lag_ratio=0.3), FadeIn(nums), run_time=1.8)
            self.play(FadeIn(then), FadeIn(tl))
            for mk, r_ in zip("bcd", side):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()

    def why(self):
        cards = point_cards([
            (r"why it persists", r"network effects: \ a currency is useful because others use it \ (Part 25); "
             r"\ deep markets for safe assets; \ prices invoiced in dollars \ (Part 34)", US),
            (r"what threatens it", r"the 2022 freeze made dollar reserves a political risk; \ central banks have "
             r"bought gold at a record pace; \ new payment systems bypass the hub", TARIFF),
            (r"what replacing it needs", r"another currency with deep, \ open markets, \ convertible capital and "
             r"courts foreign creditors trust", ROW),
            (r"the likely path", r"not a new hub but fewer hubs: \ a more fragmented, \ more expensive system of "
             r"payments", GREY_B),
        ], width=12.6, cols=2, font_size=19).move_to(DOWN * 0.2)
        head = label(r"can the dollar be replaced?", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(r"Gourinchas and Rey (2007); \ Gopinath et al., \ AER 110(3) (2020); \ Parts 25 and "
                            r"34", corner=DL, font_size=12)
        with self.voiceover(
            "Can it be replaced? <bookmark mark='a'/> Its strength is a network effect, the logic of money in "
            "Part twenty-five: a currency is useful because everyone else uses it. Add the deepest market in safe "
            "assets, and the habit, documented in Part thirty-four, of invoicing trade in dollars. <bookmark "
            "mark='b'/> What threatens it is the weapon itself. The freeze of 2022 told every central bank that "
            "dollar reserves carry political risk; central banks have since bought gold at a record pace, and new "
            "payment systems route around the hub. <bookmark mark='c'/> But replacing the dollar needs another "
            "currency with deep, open markets, free movement of capital and courts that foreign creditors trust. "
            "None has all four. <bookmark mark='d'/> The likely path is not a new hub but fewer hubs: a more "
            "fragmented, more expensive system. Weapons that work by exclusion lose force each time they are used."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
