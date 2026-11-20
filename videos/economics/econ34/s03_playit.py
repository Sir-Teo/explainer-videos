from __future__ import annotations

from videos.economics.econ34.common import *  # noqa: F403

CHIP = ("#E8A0B4", "#F2C14E", "#7FD1B9")


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Play it: \ the governor", r"Reserves are draining. Defend the peg, or let it go?",
             "Chapter two. Play it: the governor.", lit={1992: r"Black Wednesday"}, scale=("nation",),
             horizon=("a day", "a year"))
        self.desk()
        self.choose()
        self.reveal()

    def _chips(self):
        P = load("playit")
        chips = VGroup(*[VGroup(RoundedRectangle(width=4.0, height=0.95, corner_radius=0.12, stroke_color=c,
                                                 stroke_width=3, fill_color=c, fill_opacity=0.12),
                                label(rf"{ch}: \ {tex_safe(t)}", font_size=21, color=c))
                         for c, ch, t in zip(CHIP, "ABC", P["options"])]).arrange(RIGHT, buff=0.3)
        for ch in chips:
            ch[1].move_to(ch[0])
        return chips

    def desk(self):
        board = VGroup(
            label(r"you govern the Island's central bank", font_size=28, color=E.ACCENT),
            label(r"the Island's currency is pegged to the Archipelago's", font_size=24, color=DEM),
            label(r"the Archipelago has raised its interest rate; \ the Island is in a recession", font_size=24,
                  color=RATE),
            label(r"traders are selling the Island's currency; \ your reserves are draining", font_size=24,
                  color=RES),
            label(r"to defend the peg you must match their rate, \ or raise it further", font_size=24, color=WHITE),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Your turn. You govern the Island's central bank. <bookmark mark='a'/> The Island's currency is pegged "
            "to that of its larger neighbour, the Archipelago. <bookmark mark='b'/> The Archipelago has raised its "
            "interest rate to fight its own inflation, and the Island is in a recession. <bookmark mark='c'/> "
            "Traders are selling the Island's currency, and you are buying it with your reserves to hold the peg. "
            "<bookmark mark='d'/> To stop them you would have to match the Archipelago's rate, or go higher, in a "
            "recession."
        ) as vo:
            self.play(FadeIn(board[0]), FadeIn(tag))
            for mk, r_ in zip("abcd", board[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def choose(self):
        q = label(r"what do you do?", font_size=30, color=E.ACCENT).move_to(UP * 1.6)
        chips = self._chips().move_to(DOWN * 0.4)
        ring = countdown().scale(0.7).next_to(chips, DOWN, buff=0.45)
        with self.voiceover(
            "What do you do? <bookmark mark='a'/> Raise rates and keep spending reserves; ask the Archipelago to "
            "cut its rate; or let the currency float. Pause, and choose."
        ) as vo:
            self.play(FadeIn(q))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in chips], lag_ratio=0.3), FadeIn(ring),
                      run_time=1.5)
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=8.0, rate_func=linear)
        self.clear_scene()

    def reveal(self):
        P = load("playit")
        lo, hi, g, dl = P["safe_below"], P["doomed_above"], P["gamma"], P["delta"]
        ax = plane([0, 1.4], [0, 3.7], center=LEFT * 1.6 + DOWN * 0.5, x_length=9.0, y_length=4.4,
                   xticks=[0, 0.5, 1.0], yticks=[0, 1, 2, 3], xlabel=r"how deep the recession is (slack, $u$)",
                   ylabel=r"the pain of defending the peg", xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.0f}",
                   font_size=14)
        us = np.linspace(0, 1.4, 141)
        calm = path(ax, us, us ** 2, CALM, 3.2)
        attack = path(ax, us, (us + g * dl) ** 2, CRISIS, 3.2, yr=(0, 3.7))
        cost = seg(ax, 0, P["cost"], 1.4, P["cost"], DEM, 2.5, dashed=True)

        def zone(a, b, col):
            p0, p1 = ax.ax.c2p(a, 0), ax.ax.c2p(b, 3.7)
            return Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], fill_color=col, fill_opacity=0.14,
                             stroke_width=0).move_to((p0 + p1) / 2)

        z1, z2, z3 = zone(0, lo, CALM), zone(lo, hi, DEM), zone(hi, 1.4, CRISIS)
        isl = VGroup(DashedLine(ax.ax.c2p(P["u_island"], 0), ax.ax.c2p(P["u_island"], 3.7), color=WHITE,
                                stroke_width=2.5),
                     label(r"the Island", font_size=18, color=WHITE).next_to(ax.ax.c2p(P["u_island"], 3.7), UP,
                                                                           buff=0.05))
        side = VGroup(
            label(r"teal: \\ if no one expects \\ a devaluation", font_size=17, color=CALM),
            label(r"red: \\ if everyone does", font_size=17, color=CRISIS),
            label(r"gold: \\ the cost of giving up", font_size=17, color=DEM),
            label(rf"below {lo:.1f}: \\ the peg holds \\ whatever traders think", font_size=17, color=CALM),
            label(rf"above {hi:.1f}: \\ it falls \\ whatever they think", font_size=17, color=CRISIS),
            label(r"between: \\ it falls if they \\ expect it to", font_size=17, color=DEM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.3)
        foot = VGroup(
            label(r"A fails when traders expect it to; \ B is up to the Archipelago; \ C is what Britain did, \ "
                  r"that evening", font_size=20, color=WHITE),
            label(r"and British interest rates were 6\% five months later", font_size=19, color=CALM),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.2)
        tag = published_tag(r"Obstfeld, \ \emph{European Economic Review} 40 (1996); \ the Island", corner=DR,
                            font_size=12)
        with self.voiceover(
            "Here is the logic of your choice, in a model Maurice Obstfeld wrote down after 1992. "
            "<bookmark mark='a'/> A government defends a peg as long as the pain of defending is less than the cost "
            "of giving up. The pain grows with the depth of the recession, the teal curve, <bookmark mark='b'/> and "
            "it grows again if traders expect a devaluation, the red curve, because then the interest rate needed "
            "to hold them off is higher still. <bookmark mark='c'/> The gold line is the cost of giving up. "
            "<bookmark mark='d'/> If the recession is mild, both curves are below the line: the peg holds whatever "
            "traders think. <bookmark mark='e'/> If it is deep, both are above it: the peg falls whatever they "
            "think. <bookmark mark='f'/> In between, the answer depends on the traders themselves: if nobody "
            "attacks, defending is bearable and the peg holds; if everyone expects it to fall, defending becomes "
            "unbearable and it does fall. The attack succeeds because it is expected. <bookmark mark='g'/> The "
            "Island is in that middle zone. So was Britain. <bookmark mark='h'/> Raising rates works only if "
            "traders believe you will keep doing it, and they know the recession makes that costly. Britain tried "
            "it, and by the evening chose to float. Five months later its interest rates were six percent, and its "
            "recovery had begun."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(calm), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(attack), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(cost), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(z1), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(z3), FadeIn(side[4]))
            vo.wait_until("f")
            self.play(FadeIn(z2), FadeIn(side[5]))
            vo.wait_until("g")
            self.play(FadeIn(isl))
            vo.wait_until("h")
            self.play(FadeIn(foot))
        self.clear_scene()
