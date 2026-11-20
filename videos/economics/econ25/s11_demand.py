from __future__ import annotations

from videos.economics.econ25.common import *  # noqa: F403

PERIODS = ((1959, 1981, r"1959--1980", MONEY), (1981, 1994, r"1981--1993", PRICE), (1994, 2020, r"1994--2019", CB))


class Demand(VoiceoverScene):
    def construct(self):
        card(self, 9, r"The demand for money", r"Why hold money that pays no interest, \ and how much?",
             "Chapter nine. The demand for money.", lit={1952: r"Baumol", 1956: r"Tobin", 2015: r"Lucas and Nicolini"},
             scale=("household", "nation"), horizon=("a month", "decades"))
        self.trips()
        self.curve()
        self.us()

    def trips(self):
        rows = VGroup(
            label(r"income $Y$ a month, \ spent evenly; \ bonds pay $i$, \ money pays nothing; \ a trip to the bank "
                  r"costs $b$", font_size=22, color=GREY_A),
            label(r"with $n$ trips, \ you hold $Y/(2n)$ in money on average", font_size=23, color=MONEY),
            MathTex(r"\text{cost} \;=\; i\,\frac{Y}{2n} \;+\; b\,n \quad\Longrightarrow\quad n^* = \sqrt{\frac{iY}{2b}},"
                    r"\qquad M^* = \sqrt{\frac{bY}{2i}}", font_size=40, color=WHITE),
            label(r"the square-root rule: \ income elasticity $\tfrac12$, \ interest elasticity $-\tfrac12$",
                  font_size=24, color=E.ACCENT),
            label(r"double your income, \ and you hold only 41\% more money: \ economies of scale in cash",
                  font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Baumol, QJE 66(4) (1952): \ 545--556; \ Tobin, REStat 38(3) (1956): \ 241--247",
                            corner=DR, font_size=12)
        with self.voiceover(
            "Why hold money at all, when bonds pay interest? Because you need it to pay for things. William Baumol "
            "and James Tobin turned that into arithmetic in the 1950s. <bookmark mark='a'/> You earn Y a month, keep "
            "it in bonds, and spend it evenly. Each trip to the bank to sell bonds for cash costs b. "
            "<bookmark mark='b'/> If you make n trips a month, you hold Y over two n in money on average. "
            "<bookmark mark='c'/> The cost is the interest you give up on that money plus the cost of the trips. "
            "Minimize it, and the best number of trips is the square root of i Y over two b. <bookmark mark='d'/> So "
            "money holdings rise with the square root of income and fall with the square root of the interest rate. "
            "<bookmark mark='e'/> Double your income and you hold only forty-one percent more money: there are "
            "economies of scale in managing cash."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def curve(self):
        b = load("baumol")
        ax = plane([0, 0.02], [0, 1300], center=LEFT * 2.2 + DOWN * 0.3, x_length=7.2, y_length=4.8,
                   xticks=[0, 0.005, 0.01, 0.015, 0.02], yticks=[0, 400, 800, 1200],
                   xlabel=r"interest rate, \ a month", ylabel=r"average money held", xfmt=lambda v: f"{100 * v:.1f}\\%",
                   yfmt=lambda v: f"{v:.0f}", font_size=16)
        line_ = path(ax, b["i"], b["money"], color=MONEY, width=4, yr=(0, 1300))
        k = int(np.argmin(np.abs(np.array(b["i"]) - 0.01)))
        here = dot(ax, b["i"][k], b["money"][k], color=E.ACCENT, r=0.09)
        side = VGroup(
            label(rf"the Island: \ income {commas(b['Y'])} a month, \\ a trip costs {b['b']:g}", font_size=20,
                  color=GREY_A),
            label(rf"at 1\% a month: \ {b['trips'][k]:.1f} trips, \\ {b['money'][k]:.0f} held on average", font_size=21,
                  color=E.ACCENT),
            label(r"higher rates: \ more trips, \\ less money: \ velocity rises", font_size=21, color=PRICE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            f"On the Island, with an income of {b['Y']:,.0f} coconuts a month and a cost of {b['b']:g} per trip, "
            "here is money held against the interest rate. <bookmark mark='a'/> At one percent a month, an "
            f"islander makes about {b['trips'][k]:.1f} trips and holds about {b['money'][k]:.0f} on average. "
            "<bookmark mark='b'/> Raise the rate, and people economize: more trips, less money, and money turns over "
            "faster. That is why velocity rose with interest rates in chapter five."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(line_), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("a")
            self.play(GrowFromCenter(here), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def us(self):
        b = load("baumol")
        t, r, lm = np.array(b["t"]), np.array(b["rate"]), np.array(b["lm"])
        ax = plane([0, 16], [-2.45, -1.25], center=LEFT * 2.0 + DOWN * 0.3, x_length=7.4, y_length=4.8,
                   xticks=[0, 4, 8, 12, 16], yticks=[-2.4, -2.0, -1.6], xlabel=r"three-month bill rate, \ \%",
                   ylabel=r"$\ln(\text{M1} / \text{nominal GDP})$", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}",
                   font_size=16)
        groups = VGroup()
        for a, z, name, c in PERIODS:
            m = (t >= a) & (t < z)
            groups.add(VGroup(*[dot(ax, x, y, color=c, r=0.04) for x, y in zip(r[m], lm[m])]))
        side = VGroup(*[label(name, font_size=20, color=c) for _, _, name, c in PERIODS]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.25)
        notes = VGroup(
            label(rf"slope before 1981: \ {b['semi_pre']:.3f} \\ a point; \ after 1994: \ {b['semi_post']:.3f}",
                  font_size=19, color=GREY_A),
            label(r"in between, \ new accounts \\ that paid interest blurred \\ what counted as money", font_size=19,
                  color=PRICE),
            label(r"by the late 1980s the Fed \\ had stopped targeting M1", font_size=19, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        VGroup(side, notes).arrange(DOWN, aligned_edge=LEFT, buff=0.45).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"M1, \ GDP and the bill rate, \ quarterly, \ 1959--2019 \ (M1 was redefined in 2020), \ via "
                       r"FRED", corner=DR, font_size=12)
        with self.voiceover(
            "Does the American data look like Baumol and Tobin? Plot money relative to income, as a log, against the "
            "interest rate, quarter by quarter. <bookmark mark='a'/> From 1959 to 1980, a tidy downward line: when "
            "rates rose, Americans held less money relative to income, about "
            f"{abs(100 * b['semi_pre']):.1f} percent less for each point. <bookmark mark='b'/> Then, in the 1980s, "
            "the relationship broke. Banks were allowed to offer accounts that paid interest and could be drawn on "
            "like money, and the line jumped. <bookmark mark='c'/> After 1994 a new line appears, flatter, at about "
            f"{abs(100 * b['semi_post']):.1f} percent a point. <bookmark mark='d'/> By the late 1980s the Federal "
            "Reserve had stopped targeting M1 at all. Robert Lucas and Juan Pablo Nicolini argued in 2015 that "
            "adding the new money-market deposit accounts back in restores a stable demand. Money demand is stable "
            "only if you measure the right money."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(groups[0]), FadeIn(side[0]), run_time=1.2)
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(groups[1]), FadeIn(side[1]), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(groups[2]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
        self.clear_scene()
