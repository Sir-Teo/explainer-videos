from __future__ import annotations

from videos.economics.econ52.common import *  # noqa: F403

NAMES = (r"Ada", r"Ben", r"Cleo")


class Aggregation(VoiceoverScene):
    def construct(self):
        card(self, 1, r"Aggregation: \ when one household is exact", r"When does the average behave like a person?",
             "Chapter one. Aggregation: when one household is exact.", lit={1953: r"Gorman"},
             scale=("household", "nation"), horizon=("a year",))
        self.engel(same=True)
        self.engel(same=False)
        self.gorman()
        self.mpcs()

    def engel(self, same: bool):
        G = load("gorman")
        b = G["b_same"] if same else G["b_diff"]
        res = G["same"] if same else G["diff"]
        m = np.array(G["incomes"])
        a0 = np.array(G["a"])
        x = G["transfer"]
        ax = plane([0, 140], [0, 140], center=LEFT * 2.3 + DOWN * 0.3, x_length=6.6, y_length=5.0,
                   xticks=[0, 40, 80, 120], yticks=[0, 40, 80, 120], xlabel=r"income", ylabel=r"spending",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=15)
        cols = (POOR, MANY, RICH)
        lines = VGroup(*[seg(ax, 0, a0[i], 140, a0[i] + b[i] * 140, cols[i], 2.6) for i in range(3)])
        dots = VGroup(*[dot(ax, m[i], a0[i] + b[i] * m[i], cols[i], 0.1) for i in range(3)])
        names = VGroup(*[label(rf"{NAMES[i]}: \ spends {b[i]:.1f} of each extra dollar", font_size=17,
                               color=cols[i]) for i in range(3)])
        names.arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.4).shift(UP * 2.0)
        tot = VGroup(label(r"total spending", font_size=22, color=WHITE),
                     DecimalNumber(res["before"], num_decimal_places=0, font_size=40, color=WHITE)).arrange(
            DOWN, buff=0.15).to_edge(RIGHT, buff=1.4).shift(DOWN * 0.6)
        move = label(rf"Cleo gives Ada {x:.0f}", font_size=22, color=E.ACCENT).next_to(tot, UP, buff=0.5)
        after = [m[0] + x, m[1], m[2] - x]
        verdict = (label(r"unchanged: \ the average \\ is a person", font_size=22, color=GAIN) if same else
                   label(rf"up by {res['change']:.0f}: \ who has the \\ money matters", font_size=22, color=ERR))
        verdict.next_to(tot, DOWN, buff=0.45)
        if same:
            say = (
                "Start with three households, Ada, Ben and Cleo, with incomes of twenty, sixty and a hundred and "
                "twenty. <bookmark mark='a'/> Suppose each spends a fixed amount plus half of every extra dollar: "
                "straight Engel curves with the same slope. <bookmark mark='b'/> Their total spending is "
                f"{res['before']:.0f}. <bookmark mark='c'/> Now Cleo gives Ada twenty. Cleo spends ten less, "
                "Ada ten more, <bookmark mark='d'/> and the total does not move. Whatever the distribution of income, "
                "total spending depends only on total income. In this economy one household could stand for all "
                "three."
            )
        else:
            say = (
                "Now give them different slopes, as real households have. <bookmark mark='a'/> Ada, with little, "
                "spends nine tenths of an extra dollar; Ben, six tenths; Cleo, three tenths. <bookmark mark='b'/> "
                f"Total spending starts at {res['before']:.0f}. <bookmark mark='c'/> The same transfer: Cleo spends "
                "six less, Ada eighteen more, <bookmark mark='d'/> and total spending rises by twelve. Same total "
                "income, different total spending. Now the distribution matters, and no single household can stand "
                "for the three."
            )
        with self.voiceover(say) as vo:
            self.play(FadeIn(ax))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(ln) for ln in lines], lag_ratio=0.3), FadeIn(names), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(dots, scale=1.3), FadeIn(tot))
            vo.wait_until("c")
            self.play(FadeIn(move))
            self.play(*[dots[i].animate.move_to(ax.ax.c2p(after[i], a0[i] + b[i] * after[i])) for i in (0, 2)],
                      tot[1].animate.set_value(res["after"]), run_time=2.2)
            vo.wait_until("d")
            self.play(FadeIn(verdict, shift=UP * 0.1), Indicate(tot[1], color=GAIN if same else ERR))
        self.clear_scene()

    def gorman(self):
        eq = MathTex(r"c_i = a_i(p) + b(p)\, m_i \quad\Longrightarrow\quad "
                     r"\sum_i c_i = \sum_i a_i(p) + b(p) \sum_i m_i",
                     font_size=40, color=THEORY).move_to(UP * 1.9)
        rows = VGroup(
            label(r"each household's spending is a straight line in its income", font_size=22, color=WHITE),
            label(r"with the same slope for everyone", font_size=22, color=WHITE),
            label(r"then total spending depends only on total income, \ and a representative household is exact",
                  font_size=22, color=GAIN),
        ).arrange(DOWN, buff=0.3).next_to(eq, DOWN, buff=0.6)
        hc = history_card(1953, r"W. M. Gorman, \ \emph{Econometrica}",
                          r"``Community preference fields'': \ the condition under which a society's demand behaves "
                          r"like one consumer's", color=E.ACCENT, width=10.4, font_size=21).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "William Gorman stated the condition in 1953. <bookmark mark='a'/> If every household's spending is a "
            "straight line in its income, <bookmark mark='b'/> and the lines have the same slope, the same "
            "marginal propensity to spend, <bookmark mark='c'/> then total spending depends only on total income, "
            "and a single representative household reproduces the aggregate exactly. <bookmark mark='d'/> It is a "
            "knife-edge. It fails as soon as the poor spend a larger share of an extra dollar than the rich, and "
            "they do."
        ) as vo:
            self.play(Write(eq), run_time=1.8)
            for mk, r_ in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(hc, shift=UP * 0.1))
        self.clear_scene()

    def mpcs(self):
        A = load("aiyagari")
        a = np.array(A["a"])
        ax = plane([0, 20], [0, 0.8], center=LEFT * 1.6 + DOWN * 0.3, x_length=7.6, y_length=4.8,
                   xticks=[0, 5, 10, 15, 20], yticks=[0, 0.2, 0.4, 0.6, 0.8],
                   xlabel=r"wealth, \ in years of the average wage",
                   ylabel=r"share of a windfall spent within the year",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}", font_size=14)
        lo = path(ax, a, A["mpc_low"], POOR, 3.0, xr=(0, 20), smooth=False)
        hi = path(ax, a, A["mpc_high"], RICH, 3.0, xr=(0, 20), smooth=False)
        side = VGroup(
            label(r"orange: \ the lowest wage", font_size=19, color=POOR),
            label(r"blue: \ the highest wage", font_size=19, color=RICH),
            label(rf"on average: \ {100 * A['mean_mpc']:.0f}\% \\ a representative \\ household: \ about "
                  rf"{100 * A['rho_time']:.0f}\%", font_size=19, color=WHITE),
            label(r"the slopes differ, \\ so Gorman fails", font_size=21, color=ERR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        tag = island_tag(r"this part's Aiyagari economy \ (computed)", corner=DR, font_size=12)
        with self.voiceover(
            "Here is that fact inside the economy this part will build, in which households face income risk they "
            "cannot insure. The curves show how much of a small windfall a household spends within the year, "
            "against its wealth. <bookmark mark='a'/> A household with nothing saved and the lowest wage spends "
            f"about {100 * A['mpc_low'][0]:.0f} percent of it, and the share falls steeply as savings build up. "
            "<bookmark mark='b'/> A household with the highest wage spends little even with nothing saved: it is "
            "busy building a buffer while times are good. <bookmark mark='c'/> Averaged over the population it is "
            f"{100 * A['mean_mpc']:.0f} percent, against about {100 * A['rho_time']:.0f} percent for a "
            "representative household, who spends only the interest on a windfall. <bookmark mark='d'/> The "
            "slopes differ, so Gorman's condition fails, and the distribution of wealth becomes part of the state "
            "of the economy."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(lo), FadeIn(side[0]), run_time=1.6)
            vo.wait_until("b")
            self.play(Create(hi), FadeIn(side[1]), run_time=1.6)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3], shift=UP * 0.1))
        self.clear_scene()
