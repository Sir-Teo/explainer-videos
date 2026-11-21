from __future__ import annotations

from videos.economics.econ51.common import *  # noqa: F403

FREE = "#9AA3B2"
BOUND = "#F25F5C"


class Bounds(VoiceoverScene):
    def construct(self):
        card(self, 11, r"Occasionally binding constraints", r"What happens when a limit binds only sometimes?",
             "Chapter eleven. Occasionally binding constraints.", lit={2015: r"Guerrieri and Iacoviello"},
             scale=("household", "nation"), horizon=("a year",))
        self.kink()
        self.zlb()
        self.lesson()

    def kink(self):
        Hh = load("household")
        a = np.array(Hh["a"])
        c = np.array(Hh["egm_c"])[:, 0]
        R = TRUTH["household"]["R"]
        y0 = Hh["y"][0]
        eat = R * a + y0
        free = np.where(c < eat - 1e-6)[0]
        k_at = a[free[0]] if len(free) else a[-1]
        sel = a <= 3
        ax = plane([0, 3], [0, 1.6], center=LEFT * 1.6 + DOWN * 0.3, x_length=7.6, y_length=4.6,
                   xticks=[0, 1, 2, 3], yticks=[0, 0.5, 1.0, 1.5], xlabel=r"assets", ylabel=r"consumption, \ lowest "
                                                                                       r"income",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}", font_size=14)
        rule = path(ax, a[sel], c[sel], EGM, 3.0, smooth=False)
        e_line = DashedVMobject(path(ax, a[sel], eat[sel], GREY_B, 1.6, yr=(0, 1.6)), num_dashes=24)
        kp = dot(ax, k_at, float(np.interp(k_at, a, c)), WHITE, 0.09)
        kl = label(rf"the kink: \ assets {k_at:.2f}", font_size=16, color=WHITE).next_to(kp, UR, buff=0.12)
        side = VGroup(
            label(r"left of the kink: \\ the limit binds, \\ spend everything", font_size=18, color=GREY_B),
            label(r"right of it: \\ the Euler equation", font_size=18, color=EGM),
            label(r"a polynomial smooths \\ the corner away; \\ the endogenous grid \\ finds it exactly", font_size=18,
                  color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "Many economic constraints bind only sometimes. <bookmark mark='a'/> The household's borrowing limit is "
            "one: with little wealth and low income, it would like to borrow and cannot, so it spends everything. "
            "<bookmark mark='b'/> With a little more wealth it starts to save, and its rule follows the Euler "
            "equation. <bookmark mark='c'/> Where one regime gives way to the other, the rule has a kink. A single "
            "smooth polynomial cannot bend that sharply and smears the corner, which is why this household was "
            "solved on a grid. The endogenous grid method finds the kink exactly: it is the first point of the "
            "endogenous grid, below which the limit binds."
        ) as vo:
            self.play(FadeIn(ax), Create(e_line))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), Create(rule), run_time=1.8)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(kp, scale=1.5), FadeIn(kl), FadeIn(side[2]))
        self.clear_scene()

    def zlb(self):
        Z = load("zlb")
        q = np.array(Z["q"])[:12]
        ax1 = plane([0, 11], [-5, 5], center=LEFT * 3.3 + DOWN * 0.4, x_length=5.2, y_length=4.0,
                    xticks=[0, 4, 8], yticks=[-4, -2, 0, 2, 4], xlabel=r"quarters", ylabel=r"policy rate, \ \%",
                    xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}".replace("-", "{-}"), font_size=13)
        ax2 = plane([0, 11], [-4, 0.5], center=RIGHT * 3.1 + DOWN * 0.4, x_length=5.2, y_length=4.0,
                    xticks=[0, 4, 8], yticks=[-4, -3, -2, -1, 0], xlabel=r"quarters", ylabel=r"output gap, \ \%",
                    xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}".replace("-", "{-}"), font_size=13)
        z1 = DashedLine(ax1.ax.c2p(0, 0), ax1.ax.c2p(11, 0), color=GREY_B, stroke_width=1.4)
        i_free = path(ax1, q, Z["i_free"][:12], FREE, 2.6, smooth=False)
        i_b = path(ax1, q, Z["i"][:12], BOUND, 2.8, smooth=False)
        x_free = path(ax2, q, Z["x_free"][:12], FREE, 2.6, smooth=False)
        x_b = path(ax2, q, Z["x"][:12], BOUND, 2.8, smooth=False)
        head = label(rf"the natural rate falls to {TRUTH['zlb']['rn_low']:.0f}\% for a year".replace("-", "{-}"),
                     font_size=22, color=WHITE).to_edge(UP, buff=0.4)
        key = VGroup(label(r"grey: \ the bound ignored", font_size=17, color=FREE),
                     label(r"red: \ the bound respected", font_size=17, color=BOUND)).arrange(RIGHT, buff=0.8).next_to(
            head, DOWN, buff=0.2)
        note_ = label(rf"guess the quarters at zero, \ solve, \ check, \ repeat: \ {Z['iters']} guesses, \ "
                      rf"{Z['bound_quarters']} quarters at zero", font_size=18, color=GREY_A).to_edge(DOWN, buff=0.3)
        tag = published_tag(r"Guerrieri and Iacoviello, \ JME (2015)", corner=DR, font_size=11)
        with self.voiceover(
            "The zero bound on interest rates, from Part thirty, is the other famous case. Take the New Keynesian "
            "economy of that part, and let the natural rate of interest fall to minus two percent for a year. "
            "<bookmark mark='a'/> A linear solution that ignores the bound has the central bank cut its rate to "
            f"about {say_num(Z['i_free'][0], 1)} percent, and the output gap falls to about "
            f"{say_num(Z['x_free'][0], 1)} percent. <bookmark mark='b'/> But the rate cannot go below zero. Luca "
            "Guerrieri and Matteo Iacoviello's method guesses which quarters the bound binds in, solves the linear "
            "model for that sequence, checks whether the rule would ask for a negative rate anywhere else, and "
            f"repeats. Here it settles after {Z['iters']} guesses, with the rate at zero for "
            f"{Z['bound_quarters']} quarters. <bookmark mark='c'/> Respecting the bound, the output gap falls to "
            f"{say_num(Z['x'][0], 1)} percent, twice as deep. The constraint that binds only sometimes is exactly "
            "the one that decides how bad the recession is."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax1), FadeIn(ax2), Create(z1), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(key[0]), Create(i_free), Create(x_free), run_time=1.8)
            vo.wait_until("b")
            self.play(FadeIn(key[1]), Create(i_b), FadeIn(note_), run_time=1.8)
            vo.wait_until("c")
            self.play(Create(x_b), run_time=1.6)
            self.play(Indicate(x_b, color=WHITE, scale_factor=1.0))
        self.clear_scene()

    def lesson(self):
        cards = point_cards([
            (r"kinks break smooth methods", r"a polynomial or a Taylor series assumes the rule is smooth \ "
                                            r"everywhere", PROJ),
            (r"grids and regimes cope", r"the endogenous grid finds the kink; \ guess and verify finds the regime",
             EGM),
            (r"the global way", r"solve the whole nonlinear model, \ with the constraint inside it, \ at a higher "
                                r"cost", VALUE),
            (r"check the answer", r"Euler errors on each side of the kink, \ and at the corner itself", ERR),
        ], width=12.4, cols=2, font_size=21).move_to(DOWN * 0.2)
        head = label(r"what to take away", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        with self.voiceover(
            "What to take away. <bookmark mark='a'/> Kinks break the smooth methods: a polynomial or a Taylor "
            "series assumes the rule is smooth everywhere. <bookmark mark='b'/> Grids and regime methods cope: the "
            "endogenous grid finds the kink, and guess and verify finds the regime. <bookmark mark='c'/> The "
            "safest way solves the whole nonlinear model with the constraint inside it, at a higher cost. "
            "<bookmark mark='d'/> And whichever is used, the errors must be checked on both sides of the kink and "
            "at the corner itself, where approximations are worst."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
