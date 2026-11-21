from __future__ import annotations

from videos.economics.econ60.common import *  # noqa: F403


class Dynamic(VoiceoverScene):
    def construct(self):
        card(self, 6, r"Dynamic pricing as dynamic programming", r"What is the right fare for every day and every "
             r"number of seats left?", "Chapter six. Dynamic pricing as dynamic programming.",
             lit={1994: r"Gallego and van Ryzin", 2022: r"Williams"}, scale=("firm",), horizon=("a day",))
        self.bellman()
        self.policy()
        self.evidence()

    def bellman(self):
        rows = VGroup(
            label(r"the state: \ $t$ days into the sale, \ $x$ seats left", font_size=24, color=WHITE),
            MathTex(r"V_t(x) = \max_{p}\; \mathbb{E}\Big[\, p \min(D, x) + V_{t+1}\big(x - \min(D, x)\big) \Big], "
                    r"\quad D \sim \text{Poisson}\big(\lambda_t e^{-p/\mu_t}\big)", font_size=32, color=E.ACCENT),
            label(r"start at the last day, \ $V_{60}(x) = 0$: \ an empty seat at departure is worth nothing",
                  font_size=21, color=GREY_A),
            label(r"step back one day at a time: \ for every $x$, \ try every fare, \ keep the best", font_size=21,
                  color=GREY_A),
            label(r"$V_t(x) - V_t(x - 1)$: \ the value of one more seat today, \ the fare's floor", font_size=21,
                  color=OPT),
        ).arrange(DOWN, buff=0.4).move_to(DOWN * 0.1)
        tag = published_tag(r"Gallego and van Ryzin, \ Management Science (1994); \ Bellman (1957)", corner=DL,
                            font_size=12)
        with self.voiceover(
            "The Play-it's best policy comes from dynamic programming, the tool of Part fifty-one. <bookmark "
            "mark='a'/> The state is how far into the sale we are, and how many seats are left. <bookmark "
            "mark='b'/> The value of a state is the best expected revenue from here on: choose today's fare, sell "
            "the smaller of demand and the seats left, and add the value of tomorrow's state. Demand on each day "
            "is a Poisson count that falls with the fare. Guillermo Gallego and Garrett van Ryzin set the problem "
            "out this way in 1994. <bookmark mark='c'/> Solve it backwards. On the day of departure an empty "
            "seat is worth nothing. <bookmark mark='d'/> Step back one day at a time: for every number of seats "
            "left, try every fare and keep the best. <bookmark mark='e'/> The difference between the values of x "
            "seats and x minus one is what one more seat is worth today, and no fare below it makes sense: it is "
            "Littlewood's comparison, made every day."
        ) as vo:
            self.play(FadeIn(tag))
            for k, mk in enumerate("abcde"):
                vo.wait_until(mk)
                self.play(FadeIn(rows[k], shift=UP * 0.1))
        self.clear_scene()

    def policy(self):
        D = load("dynamic")
        pol = np.array(D["policy"])            # days x (seats 0, 5, ..., 100)
        seats = D["seats_axis"]
        T = pol.shape[0]
        cw, ch = 0.09, 0.19
        cells = VGroup()
        lo, hi = 80.0, 320.0
        for t in range(T):
            for j in range(1, len(seats)):
                v = float(np.clip((pol[t, j] - lo) / (hi - lo), 0, 1))
                cells.add(Rectangle(width=cw, height=ch, stroke_width=0, fill_opacity=0.95,
                                    fill_color=interpolate_color(ManimColor(LEIS), ManimColor(COST), v)).move_to(
                    [t * cw, (j - 1) * ch, 0]))
        grid = VGroup(cells)
        grid.move_to(LEFT * 3.25 + DOWN * 0.3)
        xl = label(r"day of the sale $\to$ departure", font_size=15, color=GREY_A).next_to(grid, DOWN, buff=0.15)
        yl = label(r"seats left \\ (5 to 100)", font_size=15, color=GREY_A).next_to(grid, LEFT, buff=0.15)
        key = VGroup(label(r"green: \ about \$80", font_size=15, color=LEIS),
                     label(r"red: \ \$320 and above", font_size=15, color=COST)).arrange(RIGHT, buff=0.4).next_to(
            grid, UP, buff=0.15)
        # one simulated flight under the policy
        px = np.array(D["path_x"], float)
        ok = px > 0
        dots_ = VGroup(*[Dot([grid.get_left()[0] + (t + 0.5) * cw, grid.get_bottom()[1] + (px[t] / 5 - 0.5) * ch, 0],
                             radius=0.035, color=WHITE) for t in range(T) if ok[t]])
        F = D["fixed"]
        side = VGroup(
            label(r"early, \ with many seats left: \ low fares for leisure buyers", font_size=19, color=LEIS),
            label(r"late, \ when business buyers arrive: \ the fare jumps", font_size=19, color=COST),
            label(r"and on any day, \ fewer seats left means a higher fare", font_size=19, color=WHITE),
            label(r"white dots: \ one simulated flight's seats left", font_size=17, color=GREY_A),
            label(rf"expected revenue: \ \${D['V0']:,.0f}, \\ against \${F['best']:,.0f} \ for the best single fare "
                  rf"(\${F['best_price']:.0f})".replace(",", "{,}"), font_size=19, color=OPT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        if side.width > 5.9:
            side.width = 5.9
            side.to_edge(RIGHT, buff=0.35)
        tag = island_tag(r"the Island: \ the optimal fare for every day and every number of seats left", corner=DL,
                         font_size=12)
        with self.voiceover(
            "Here is the answer for the Island's flight: the best fare for every day of the sale, left to right, "
            "and every number of seats left, bottom to top. <bookmark mark='a'/> Early in the sale, with plenty of "
            "seats, the fare is low, priced for leisure buyers. <bookmark mark='b'/> When business travellers "
            "start to arrive, three weeks out, it jumps. <bookmark mark='c'/> And on any day, fewer seats left means "
            "a higher fare: each remaining seat is more likely to be wanted by someone who will pay more. "
            "<bookmark mark='d'/> The white dots follow one simulated flight as it fills. <bookmark mark='e'/> "
            f"Following this policy earns {D['V0']:,.0f} dollars on average, against {F['best']:,.0f} for the "
            "best single fare."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(xl), FadeIn(yl), FadeIn(key))
            self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.0005), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(d) for d in dots_], lag_ratio=0.05), FadeIn(side[3]), run_time=2.0)
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def evidence(self):
        cards = VGroup(
            history_card(2022, r"Kevin Williams, \ Econometrica", r"airline fares in monopoly markets: \ relative to "
                         r"one fare, \ dynamic pricing helps early-arriving leisure travellers \ at the expense of "
                         r"late-arriving business travellers, \ who are sure of a seat but pay more; \ summed over "
                         r"markets, \ welfare is higher", color=AIR, width=11.6, font_size=20),
            history_card(r"later", r"and with two airlines", r"Horta\c{c}su, \ \"Ory and Williams find more seats sold "
                         r"but lower welfare when rivals both price dynamically", color=GREY_A, width=11.6,
                         font_size=20),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.3)
        lesson = label(r"who gains depends on who arrives when, \ and on the competition", font_size=22,
                       color=E.ACCENT).next_to(cards, DOWN, buff=0.5)
        tag = published_tag(r"Williams, \ Econometrica 90(2) (2022), \ abstract; \ Horta\c{c}su, \ \"Ory and "
                            r"Williams (working paper)", corner=DL, font_size=12)
        with self.voiceover(
            "Is dynamic pricing good for travellers? <bookmark mark='a'/> Kevin Williams estimated a model of exactly "
            "this kind on American airline markets with one carrier. Compared with a single fare, dynamic pricing "
            "helps early-arriving leisure travellers, at the expense of late-arriving business travellers, who are "
            "sure to find a seat but pay more for it; summed over markets, total welfare is higher. <bookmark "
            "mark='b'/> In later work with Ali Hortaçsu and Aniko Öry on markets with two airlines, he finds more "
            "seats sold but lower welfare when both price dynamically. <bookmark mark='c'/> Who gains depends on "
            "who arrives when, and on the competition; the technique itself is neither kind nor cruel."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(lesson))
        self.clear_scene()
