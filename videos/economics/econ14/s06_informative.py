from __future__ import annotations

from videos.economics.econ14.common import *  # noqa: F403

NEIGHBOUR = "#9FB8F2"


class Informative(VoiceoverScene):
    def construct(self):
        card(self, 5, r"The informativeness principle", r"What should pay depend on, \ and what should it ignore?",
             "Chapter five. The informativeness principle.",
             lit={1979: r"Holmström", 1982: r"Holmström's teams", 2001: r"Bertrand and Mullainathan"},
             scale=("person", "firm"), horizon=("a year",))
        self.weather()
        self.gain()
        self.ceos()

    def weather(self):
        t = load("rpe")
        rng = np.random.default_rng(14)
        n = 16
        m = rng.normal(0, t["common"], n)
        u = rng.normal(0, t["own"], n)
        v = rng.normal(0, t["own"] / np.sqrt(20), n)     # the average of twenty groves: their own luck nearly cancels
        e = 10.0
        y, z = e + m + u, e + m + v
        ks = np.arange(1, n + 1)
        top = plane([0.5, n + 0.5], [-4, 24], center=LEFT * 2.6 + UP * 1.25, x_length=7.4, y_length=2.5, xticks=[],
                    yticks=[0, 10, 20], xlabel="", ylabel=r"harvest", font_size=14, yfmt=lambda v: f"{v:.0f}")
        bot = plane([0.5, n + 0.5], [-14, 14], center=LEFT * 2.6 + DOWN * 2.0, x_length=7.4, y_length=2.5,
                    xticks=[1, 4, 8, 12, 16], yticks=[-10, 0, 10], xlabel=r"season",
                    ylabel=r"Friday's less \\ the average", font_size=14, xfmt=lambda v: f"{v:.0f}",
                    yfmt=lambda v: f"{v:.0f}")
        ly = path(top, ks, y, color=FRIDAY, width=3, smooth=False)
        lz = path(top, ks, z, color=NEIGHBOUR, width=3, smooth=False)
        ld = path(bot, ks, y - z, color=E.ACCENT, width=3, smooth=False)
        zero = seg(bot, 0.5, 0, n + 0.5, 0, color=GREY_C, width=1.2, dashed=True)
        k2 = label(r"the island's average, \ same weather", font_size=15, color=NEIGHBOUR).next_to(top, UP, buff=0.05
                                                                                                 ).align_to(top, RIGHT)
        k1 = label(r"Friday's grove", font_size=15, color=FRIDAY).next_to(k2, LEFT, buff=0.4)
        side = VGroup(
            label(r"each harvest: \\ effort $+$ the weather $+$ its own luck", font_size=20),
            label(rf"the weather swings both: \\ sd {t['common']:.0f} baskets", font_size=20, color=NEIGHBOUR),
            label(rf"its own luck: \ sd {t['own']:.0f}", font_size=20, color=FRIDAY),
            label(r"pay on the difference, \\ and the weather drops out", font_size=21, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.35)
        tag = island_tag(r"simulated: \ the Island", corner=DR, font_size=13)
        with self.voiceover(
            "Suppose Crusoe can also see the average harvest of the island's twenty other groves, worked by others "
            "under the same sky. <bookmark mark='a'/> Each harvest is effort, plus the weather, plus luck of its own: "
            "a pest in one grove, a fallen tree in another. <bookmark mark='b'/> The weather swings every harvest together, by "
            "four baskets or so; <bookmark mark='c'/> each grove's own luck adds three more. Across twenty groves that own "
            "luck nearly averages away. Here are sixteen simulated seasons, with everyone working equally hard. "
            "<bookmark mark='d'/> Pay Friday on the difference between their harvest and the island's average, and "
            "the weather drops out. What is left is Friday's effort, against everyone else's, and Friday's own "
            "luck."
        ) as vo:
            self.play(FadeIn(top), FadeIn(bot), FadeIn(side[0]), FadeIn(tag))
            vo.wait_until("b")
            self.play(Create(lz), FadeIn(k2), FadeIn(side[1]), run_time=2)
            vo.wait_until("c")
            self.play(Create(ly), FadeIn(k1), FadeIn(side[2]), run_time=2)
            vo.wait_until("d")
            self.play(Create(zero), Create(ld), FadeIn(side[3]), run_time=2)
        self.clear_scene()

    def gain(self):
        t = load("rpe")
        cols = [GREY_B, E.ACCENT]
        heads = [r"", r"noise in what \\ the pay is based on", r"the best share", r"what the two \\ make a day"]
        xs = [-4.4, -1.0, 2.0, 4.8]
        head = VGroup(*[label(h, font_size=19, color=GREY_B).move_to(RIGHT * x + UP * 2.2) for h, x in zip(heads, xs)])
        rule = Line(LEFT * 6.2 + UP * 1.65, RIGHT * 6.3 + UP * 1.65, color=GREY_C, stroke_width=1.5)
        rows = VGroup()
        for i, (name, var, b, s) in enumerate(((r"pay on Friday's harvest", t["var_own"], t["beta_own"],
                                                t["surplus_own"]),
                                               (r"pay on the difference \\ from the average", t["var_relative"], t["beta_relative"],
                                                t["surplus_relative"]))):
            y = 0.95 - 1.0 * i
            rows.add(VGroup(
                label(name, font_size=22, color=cols[i]).move_to(RIGHT * xs[0] + UP * y),
                label(rf"variance {var:.0f}", font_size=22, color=RISK).move_to(RIGHT * xs[1] + UP * y),
                label(f"{b:.2f}", font_size=24, color=PAY).move_to(RIGHT * xs[2] + UP * y),
                label(f"{s:.2f}", font_size=24, color=cols[i]).move_to(RIGHT * xs[3] + UP * y)))
        foot = VGroup(
            label(r"Holmström's informativeness principle: \ pay should depend on every signal that tells you about "
                  r"effort", font_size=22, color=E.ACCENT),
            label(r"and on nothing that doesn't: \ a signal that's pure noise only adds risk", font_size=22,
                  color=GREY_A),
            label(r"comparing workers removes what they share: \ the reason sales contests and league tables exist",
                  font_size=21, color=SIGNAL),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Paying on the difference changes the arithmetic. <bookmark mark='a'/> On Friday's harvest alone, the "
            "noise has a variance of twenty-five: sixteen from the weather and nine of its own. The best share is "
            "two-thirds, and the two of them make three and a third baskets a day. <bookmark mark='b'/> On the "
            "difference from the island's average, the variance falls to about nine. Friday "
            "can bear a larger share, eighty-five percent, and works harder, and together they make four and a "
            "quarter. <bookmark mark='c'/> This is Holmström's informativeness principle, from 1979: pay should "
            "depend on every signal that tells you something about effort, <bookmark mark='d'/> and on nothing that "
            "doesn't, because a signal that is pure noise only adds risk. <bookmark mark='e'/> Comparing workers who "
            "share the same conditions removes what they share. It is why firms rank their salespeople against each "
            "other, and why the weather is no excuse for a grove that did worse than its neighbours."
        ) as vo:
            self.play(FadeIn(head), Create(rule), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            self.play(Indicate(rows[1][2], color=PAY))
            for mk, r in zip("cde", foot):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def ceos(self):
        hc = history_card(2001, r"Marianne Bertrand and Sendhil Mullainathan", r"are chief executives paid for luck?",
                          color=SIGNAL, width=11.0, font_size=24).to_edge(UP, buff=0.45)
        rows = VGroup(
            label(r"an oil company's profits rise with the price of oil: \ luck, \ not the chief executive", font_size=23),
            label(r"the principle says: \ filter it out, \ pay on the profit beyond what the oil price explains",
                  font_size=23, color=E.ACCENT),
            label(r"they found pay rose with lucky profits \ about as much as with any others", font_size=23,
                  color=RISK),
            label(r"except where a large shareholder sat on the board", font_size=23, color=SIGNAL),
            label(r"their reading: \ pay is set by the executive, \ unless someone is watching", font_size=24,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.34).next_to(hc, DOWN, buff=0.5)
        tag = published_tag(r"Bertrand and Mullainathan, QJE 116(3) (2001)", corner=DR, font_size=13)
        with self.voiceover(
            "Do real contracts filter out luck? <bookmark mark='a'/> In 2001 Marianne Bertrand and Sendhil "
            "Mullainathan looked at chief executives. An oil company's profits rise when the price of oil rises, and "
            "its chief executive had nothing to do with that. <bookmark mark='b'/> The informativeness principle says "
            "to filter it out: pay on the profits beyond what the oil price explains. <bookmark mark='c'/> They found "
            "that pay rose with lucky profits about as much as with any others. <bookmark mark='d'/> Except in firms "
            "with a large shareholder on the board. <bookmark mark='e'/> Their reading was that, without a principal "
            "watching, executives in effect set their own pay. Their title put it in one line: are CEOs rewarded for "
            "luck? The ones without principals are."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0], shift=UP * 0.1))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
