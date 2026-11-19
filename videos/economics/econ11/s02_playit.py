from __future__ import annotations

from videos.economics.econ11.common import *  # noqa: F403

CROWD = "#9FB8F2"
FT = "#F2A65A"


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 1, r"Play it: \ guess two-thirds of the average", r"What number would you choose, if the winner "
             r"is the one closest to two-thirds of everyone's average?", "Chapter one. Play it: guess two-thirds of "
             "the average.", lit={1995: r"Nagel's experiment"}, scale=("person", "market"), horizon=("a day",))
        self.rules()
        self.reveal()
        self.others()

    def rules(self):
        stage = game_stage(12.0, 5.6, center=DOWN * 0.2)
        rules = VGroup(
            label(r"everyone writes down a whole number from 0 to 100", font_size=28),
            label(r"the average is worked out, \ and multiplied by two-thirds", font_size=28),
            label(r"whoever is closest to that target wins the prize", font_size=28, color=E.ACCENT),
        ).arrange(DOWN, buff=0.35).move_to(stage.box.get_center() + UP * 1.2)
        line = NumberLine(x_range=[0, 100, 10], length=9.5, include_numbers=True, font_size=22, color=GREY_B
                          ).next_to(rules, DOWN, buff=0.6)
        ring = countdown().next_to(line, DOWN, buff=0.45)
        with self.voiceover(
            "Here is a game to play before we name any of its ideas. Everyone in a room writes down a whole number "
            "from nought to a hundred. The numbers are averaged, and the average is multiplied by two-thirds. "
            "Whoever is closest to that target wins. You are playing against a roomful of people who have heard the "
            "same rules. What number do you write? Pause, and choose."
        ):
            self.play(FadeIn(stage), FadeIn(rules[0]))
            self.play(FadeIn(rules[1]), FadeIn(rules[2]), Create(line), run_time=2)
            self.play(FadeIn(ring))
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=8.0, rate_func=linear)
        self.clear_scene()

    def reveal(self):
        g = load("guess")
        x = np.array(g["crowd"])
        w = g["winner"]
        edges = np.arange(0, 105, 5)
        counts, _ = np.histogram(x, bins=edges)
        ax = plane([0, 100], [0, 14], center=LEFT * 2.6 + DOWN * 0.3, x_length=7.0, y_length=4.6,
                   xticks=[0, 20, 40, 60, 80, 100], yticks=[0, 5, 10], xlabel=r"number chosen",
                   ylabel=r"islanders", font_size=16)
        a = ax.ax
        bars = VGroup(*[Rectangle(width=a.c2p(4.4, 0)[0] - a.c2p(0, 0)[0], height=max(a.c2p(0, c)[1] - a.c2p(0, 0)[1],
                                                                                       1e-3),
                                  stroke_width=0, fill_color=CROWD, fill_opacity=0.85).move_to(a.c2p(e + 2.5, 0),
                                                                                             aligned_edge=DOWN)
                        for e, c in zip(edges[:-1], counts)])
        mean = DashedLine(a.c2p(w["mean"], 0), a.c2p(w["mean"], 13.5), color=WHITE, stroke_width=2)
        ml = label(rf"average {w['mean']:.1f}", font_size=17).next_to(a.c2p(w["mean"], 13.5), RIGHT, buff=0.08)
        tgt = DashedLine(a.c2p(w["target"], 0), a.c2p(w["target"], 12.5), color=E.ACCENT, stroke_width=3)
        tl = label(rf"two-thirds: \ {w['target']:.1f}", font_size=17, color=E.ACCENT).next_to(a.c2p(w["target"], 12.5),
                                                                                               LEFT, buff=0.08)
        side = VGroup(
            label(rf"an Island crowd of {len(x)}, \ simulated", font_size=22, color=CROWD),
            label(rf"they average {w['mean']:.1f}; \ two-thirds of that is {w['target']:.1f}", font_size=22),
            label(rf"the winner wrote {w['winner']:.0f}", font_size=24, color=E.ACCENT),
            label(r"if you wrote 50, \ you assumed the others choose at random", font_size=21, color=GREY_A),
            label(r"if 33, \ that they write 50; \ if 22, \ that they write 33 \dots", font_size=21, color=LEVEL),
            label(r"and if 0, \ that everyone reasons all the way down", font_size=21, color=EQ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).to_edge(RIGHT, buff=0.35)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Here is what an Island crowd of sixty-seven might write, simulated by Agora with a model of how people "
            "think that we'll meet in chapter twelve. <bookmark mark='a'/> Their numbers average about thirty-six, "
            "and two-thirds of that is about twenty-four. <bookmark mark='b'/> The winner wrote twenty-four. "
            "<bookmark mark='c'/> Where did your number fall? If you wrote fifty, you probably assumed the others "
            "would choose at random. <bookmark mark='d'/> If you wrote thirty-three, you thought one step ahead of "
            "them; twenty-two, two steps. <bookmark mark='e'/> And if you wrote nought, you assumed that everyone "
            "reasons all the way down, and that everyone knows that everyone does."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]),
                      LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.05), run_time=2.5)
            vo.wait_until("a")
            self.play(Create(mean), FadeIn(ml), Create(tgt), FadeIn(tl), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(side[4]))
            vo.wait_until("e")
            self.play(FadeIn(side[5]))
        self.clear_scene()

    def others(self):
        g = load("guess")
        nz, ft = g["nagel"], g["ft"]
        line = NumberLine(x_range=[0, 100, 10], length=11.0, include_numbers=True, font_size=22, color=GREY_B
                          ).move_to(DOWN * 0.2)

        def pin(v, text, col, h):
            d = Dot(line.n2p(v), radius=0.09, color=col)
            t = label(text, font_size=20, color=col).move_to(line.n2p(v) + UP * h)
            end = t.get_bottom() if h > 0 else t.get_top()
            return VGroup(d, Line(d.get_center(), [d.get_center()[0], end[1], 0], color=col, stroke_width=1.5), t)

        pins = VGroup(
            pin(nz["mean"], rf"Nagel's students' average: \ {nz['mean']:.2f}", ANA, 0.75),
            pin(g["nagel_target"], rf"so the target: \ {g['nagel_target']:.1f}", ANA, -0.75),
            pin(ft["mean"], rf"Financial Times readers' average: \ {ft['mean']:.1f}", FT, 1.55),
            pin(ft["winner"], rf"winning number: \ {ft['winner']:.0f}", FT, -1.55),
            pin(0, r"the equilibrium: \ 0", EQ, 2.35),
        )
        for pn in pins:
            if pn[2].get_left()[0] < -6.9:
                pn[2].shift(RIGHT * (-6.9 - pn[2].get_left()[0]))
        head = label(r"the game, \ played for real", font_size=32, color=E.ACCENT).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(rf"Rosemarie Nagel (1995): \ {nz['subjects']} students in {nz['sessions']} sessions, \ a prize of "
                  rf"{tables.NAGEL_1995.data['prize_dm']} DM a round; \ median {nz['median']}", font_size=21,
                  color=ANA),
            label(r"Richard Thaler's contest in the Financial Times (1997): \ its readers, \ whole numbers from 0 to 100", font_size=21,
                  color=FT),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.55)
        tag = published_tag(r"Nagel, AER 85(5) (1995), Figure 1B; \ Thaler's FT contest (1997), as reported", corner=DR,
                            font_size=13)
        with self.voiceover(
            "The game has been played for real many times. <bookmark mark='a'/> In 1995 Rosemarie Nagel reported "
            "the first careful experiments: sixty-seven students in four sessions, playing for twenty marks a round. "
            "In the first round their numbers averaged thirty-six point seven three, so the winning target was about "
            "twenty-four and a half. <bookmark mark='b'/> In 1997 Richard Thaler ran the game in the Financial "
            "Times. Its readers averaged eighteen point nine, and the winning number was thirteen. "
            "<bookmark mark='c'/> And the prediction of game theory, if everyone is rational and knows that everyone "
            "else is: nought. Nobody who wins writes nought. The next chapter explains where nought comes from, and "
            "why it is the wrong guess."
        ) as vo:
            self.play(FadeIn(head), Create(line), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(pins[0]), FadeIn(pins[1]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(pins[2]), FadeIn(pins[3]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(pins[4]))
        self.clear_scene()
