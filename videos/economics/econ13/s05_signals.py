from __future__ import annotations

from videos.economics.econ13.common import *  # noqa: F403

WEAK = "#F2A65A"
STRONG = "#7BD88F"


class Signals(VoiceoverScene):
    def construct(self):
        card(self, 4, r"Signalling: \ education that teaches nothing", r"If employers can't see how good you are, \ "
             r"can you prove it by paying for something useless?", "Chapter four. Signalling: education that teaches "
             "nothing.", lit={1973: r"Spence's job market signaling"}, scale=("person", "market"),
             horizon=("a year", "a decade"))
        self.setup()
        self.separate()
        self.pooling()

    def setup(self):
        hc = history_card(1973, r"Michael Spence, \ ``Job Market Signaling''", r"a doctoral thesis at Harvard: \ the "
                          r"informed side moves first, \ and spends money to be believed", color=SIGNAL, width=11.4,
                          font_size=24).to_edge(UP, buff=0.45)
        s = load("spence")
        rows = VGroup(
            label(rf"two kinds of fisher: \ weak ones land {s['theta_low']:.0f} basket a day, \ strong ones "
                  rf"{s['theta_high']:.0f}", font_size=24),
            label(r"a boat owner hiring a crew can't tell them apart, \ so pays what a crew member lands on average",
                  font_size=24, color=GREY_A),
            label(rf"a season at the Island's school teaches nothing about fishing, \ but costs a weak fisher "
                  rf"{s['cost_low']:.0f} basket a day \\ and a strong one {s['cost_high']:.1f}: \ studying is harder "
                  r"for the weak", font_size=23, color=SIGNAL),
            label(r"can schooling sort them, \ though it changes nothing about how they fish?", font_size=25,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.32).next_to(hc, DOWN, buff=0.5)
        tag = published_tag(r"Spence, QJE 87(3) (1973)", corner=DR, font_size=13)
        with self.voiceover(
            "Guarantees work because they are cheap only for the honest. In 1973 Michael Spence, in a thesis written "
            "at Harvard, turned that into a theory of signals: the informed side moves first, and spends money to "
            "be believed. <bookmark mark='a'/> On the Island, there are two kinds of fisher. Weak ones land one "
            "basket a day, strong ones two. <bookmark mark='b'/> A boat owner hiring a crew cannot tell them apart, "
            "so pays what the average crew member lands. <bookmark mark='c'/> The Island also has a school. A season "
            "there teaches nothing about fishing, but it costs a weak fisher a basket a day and a strong one half a "
            "basket, because studying comes harder to those who find the work harder. "
            "<bookmark mark='d'/> Can schooling sort the fishers, though it changes nothing about how they fish?"
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(tag))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def separate(self):
        s = load("spence")
        es = np.array(s["es"])
        ax = plane([0, 3], [0, 3], center=LEFT * 3.1 + DOWN * 0.3, x_length=5.4, y_length=5.0,
                   xticks=[0, 1, 2, 3], yticks=[0, 1, 1.5, 2, 3], xlabel=r"seasons of school",
                   ylabel=r"wage, \ baskets a day", font_size=16, xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:g}")
        a = ax.ax
        e1 = s["least_cost"]
        wage = VGroup(Line(a.c2p(0, s["theta_low"]), a.c2p(e1, s["theta_low"]), color=WHITE, stroke_width=4),
                      Line(a.c2p(e1, s["theta_high"]), a.c2p(3, s["theta_high"]), color=WHITE, stroke_width=4))
        wl = label(r"the boat owners' pay: \\ 2 with a season of school, \ else 1", font_size=15).next_to(
            a.c2p(1.6, 2.0), UP, buff=0.1)
        low = path(ax, es, s["low_line"], color=WEAK, width=2.5, smooth=False, yr=(0, 3))
        high = path(ax, es, s["high_line"], color=STRONG, width=2.5, smooth=False, yr=(0, 3))
        pl = Dot(a.c2p(0, s["theta_low"]), radius=0.09, color=WEAK)
        ph = Dot(a.c2p(e1, s["theta_high"]), radius=0.09, color=STRONG)
        rng = Line(a.c2p(s["e_min"], 0.12), a.c2p(s["e_max"], 0.12), color=SIGNAL, stroke_width=8)
        rl = label(r"any requirement from 1 to 2 seasons separates", font_size=15, color=SIGNAL).next_to(rng, UP,
                                                                                                     buff=0.08)
        side = VGroup(
            label(r"suppose owners pay 2 to anyone with a season of school, \\ and 1 to anyone without", font_size=20),
            label(r"a weak fisher: \ school costs 1, \ gains 1: \\ not worth it, \ so stays out \ (orange: "
                  r"indifference)", font_size=20, color=WEAK),
            label(r"a strong fisher: \ school costs 0.5, \ gains 1: \ goes \\ (green: indifference)", font_size=20,
                  color=STRONG),
            label(r"the owners' beliefs come true: \ a separating equilibrium", font_size=21, color=EQ),
            label(r"the strong pay half a basket a day for nothing \\ but being believed: \ a social waste", font_size=20,
                  color=LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Suppose the boat owners pay two baskets a day to anyone with a season of school, and one to anyone "
            "without. <bookmark mark='a'/> For a weak fisher, a season costs one basket a day and gains one: not "
            "worth it, so they stay out. Their indifference line, in orange, passes above the owners' offer. "
            "<bookmark mark='b'/> For a strong fisher it costs half a basket and gains one, so they go. "
            "<bookmark mark='c'/> And then the owners' beliefs come true: everyone with schooling is strong, and "
            "everyone without is weak. This is a separating equilibrium. In fact any requirement from one to two "
            "seasons would separate them. <bookmark mark='d'/> But notice what it costs: the strong spend half a "
            "basket a day on something that adds nothing to the catch, purely to be believed. Signals can be "
            "privately rational and socially wasteful."
        ) as vo:
            self.play(FadeIn(ax), Create(wage), FadeIn(wl), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(low), FadeIn(pl), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(Create(high), FadeIn(ph), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]), Create(rng), FadeIn(rl))
            vo.wait_until("d")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def pooling(self):
        s = load("spence")
        rows = VGroup(
            label(rf"there is also a pooling equilibrium: \ nobody studies, \ and everyone earns the average, "
                  rf"{s['pool_wage']:.1f}", font_size=23, color=POOL),
            label(r"with many equilibria, \ which is it? \ beliefs about people who study must be pinned down",
                  font_size=23),
            label(r"Cho and Kreps's intuitive criterion (1987): \ a season of school is something only a strong "
                  r"fisher could gain from", font_size=23, color=SIGNAL),
            label(r"so the owners should believe it, \ and only the cheapest separating requirement survives: \ 1 "
                  r"season", font_size=23, color=EQ),
            label(rf"if 90\% were strong, \ pooling would pay the strong {s['pool_wage_many']:.1f}, \ more than "
                  rf"separating's {s['sep_high_net']:.1f}: \\ yet the criterion still picks separation", font_size=22,
                  color=LOSS),
            label(r"a ban on the signal could make everyone better off: \ a theme of Part 45", font_size=23,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.3).move_to(UP * 0.1)
        tag = published_tag(r"Cho and Kreps, QJE 102(2) (1987); \ Riley, Econometrica 47(2) (1979)", corner=DR,
                            font_size=13)
        with self.voiceover(
            "There are other equilibria. <bookmark mark='a'/> If the owners pay everyone the same whatever their "
            "schooling, nobody studies, and everyone earns the average, one and a half baskets. This is a pooling "
            "equilibrium. <bookmark mark='b'/> With so many equilibria, which one happens? It depends on what the "
            "owners would believe about someone who studies when nobody is supposed to. <bookmark mark='c'/> In 1987 "
            "In-Koo Cho and David Kreps proposed the intuitive criterion: a season of school could only pay off for a "
            "strong fisher, so an owner who saw one should believe the student is strong. "
            "<bookmark mark='d'/> That rules out pooling, and every separating equilibrium but the cheapest, a single "
            "season, the outcome John Riley had singled out in 1979. <bookmark mark='e'/> The result can be "
            "perverse. If nine fishers in ten were strong, pooling would pay the strong one point nine baskets, more "
            "than the one point five they keep after paying for school; yet the criterion still picks separation. "
            "<bookmark mark='f'/> Everyone could be better off if the signal were banned, a theme Part forty-five "
            "returns to."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(rows[0]))
            for mk, r in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
