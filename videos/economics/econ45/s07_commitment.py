from __future__ import annotations

from videos.economics.econ45.common import *  # noqa: F403


class Commitment(VoiceoverScene):
    def construct(self):
        card(self, 6, r"Commitment, \ demanded", r"Would anyone pay to have fewer choices?",
             "Chapter six. Commitment, demanded.", lit={2006: r"Ashraf, Karlan and Yin"},
             scale=("person", "household"), horizon=("a year",))
        self.puzzle()
        self.seed()
        self.trial()

    def puzzle(self):
        cards = point_cards([
            (r"Part 5's agent", r"never pays to \\ lose an option: \\ it can always \\ choose not to use it", TC),
            (r"Ulysses", r"has himself tied \\ to the mast before \\ the sirens sing", SOPH),
            (r"savers", r"accounts that lock \\ money until a date \\ or a goal", GYM),
            (r"the test", r"demand for commitment \\ reveals present bias, \\ and knowing it", E.ACCENT),
        ], width=12.8, cols=4, font_size=18).move_to(DOWN * 0.2)
        head = label(r"why would anyone want fewer choices?", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.SEED_2006.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Here is a sharp test. <bookmark mark='a'/> The agent of Part five never pays to give up an option. An "
            "option it does not want, it simply does not use. <bookmark mark='b'/> But a sophisticate, who knows "
            "tomorrow's self will be tempted, may want to bind that self in advance, like Ulysses, who had his crew "
            "tie him to the mast before the sirens began to sing. <bookmark mark='c'/> In money, that is an account "
            "you cannot touch until a date, or until a goal is reached, even though it pays no more interest than "
            "an ordinary one. <bookmark mark='d'/> So if people choose such an account, the choice itself is "
            "evidence: of present bias, and of knowing it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cards.cards[0], shift=UP * 0.1))
            for mk, c in zip("bcd", cards.cards[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def seed(self):
        steps = flow_chain([(r"a rural bank's \\ clients", GYM),
                            (r"some offered the \\ locked account, \\ at random", SOPH),
                            (r"a minority take it", PLAN), (r"savings a year \\ later", GAIN)],
                           notes=[r"Mindanao, \\ the Philippines",
                                  r"no extra interest; \\ money locked until \\ a date or an amount",
                                  r"more often those whose \\ survey answers showed \\ a reversal",
                                  r"compared with \\ those not offered"], box_w=2.8, font_size=19, note_size=16)
        steps.move_to(UP * 0.4)
        foot = label(r"SEED: \ Save, \ Earn, \ Enjoy Deposits", font_size=22, color=E.ACCENT).to_edge(DOWN, buff=0.9)
        survey = label(r"first, \ a survey: \ patient about next year against the year after, \\ but impatient "
                       r"about today against next month?", font_size=19, color=NAIF).to_edge(UP, buff=0.6)
        tag = published_tag(tables.SEED_2006.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Nava Ashraf, Dean Karlan and Wesley Yin ran the test with a rural bank on Mindanao, in the Philippines. "
            "<bookmark mark='a'/> The bank's clients were surveyed first, including questions that revealed whether "
            "they were patient for the far future but impatient for the near one. <bookmark mark='b'/> Then some of "
            "them, chosen at random, were offered a new account: money deposited could not be withdrawn until a date "
            "or an amount the client set, and it earned no extra interest. <bookmark mark='c'/> Of the 710 clients "
            "offered it, 202, twenty-eight percent, took it, and women whose survey answers showed the tell-tale "
            "reversal were more likely to. <bookmark mark='d'/> A year later, the average savings balance of those "
            "offered the account had risen by 81 percentage points more than that of those not offered. Commitment "
            "was demanded, and it worked."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(foot), FadeIn(steps.boxes[0]), FadeIn(steps.notes[0]))
            vo.wait_until("a")
            self.play(FadeIn(survey, shift=DOWN * 0.1))
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                self.play(GrowArrow(steps.arrows[k]), FadeIn(steps.boxes[k + 1]), FadeIn(steps.notes[k + 1]))
        self.clear_scene()

    def trial(self):
        S = load("seed")
        ctrl, itt, tot = S["control_mean"], S["itt"], S["tot"]
        ax = plane([0, 3], [0, 120], center=LEFT * 2.6 + DOWN * 0.4, x_length=5.6, y_length=4.6, xticks=[],
                   yticks=[0, 40, 80, 120], ylabel=r"savings after a year \ (index)", yfmt=lambda v: f"{v:.0f}",
                   font_size=14)
        vals = [(r"not offered", ctrl, GREY_B), (r"offered", ctrl + itt, SOPH)]
        bars = VGroup()
        for i, (nm, v, col) in enumerate(vals):
            p0, p1 = ax.ax.c2p(0.5 + 1.2 * i, 0), ax.ax.c2p(1.3 + 1.2 * i, v)
            r = Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=col,
                          fill_opacity=0.85).move_to((p0 + p1) / 2)
            bars.add(VGroup(r, label(nm, font_size=17, color=col).next_to(r, DOWN, buff=0.12),
                            label(f"{v:.0f}", font_size=18, color=WHITE).next_to(r, UP, buff=0.08)))
        eq = MathTex(r"\text{effect on takers} = \frac{\text{effect of the offer}}{\text{take-up}}"
                     rf" = \frac{{{itt:.1f}}}{{{S['take_up']:.2f}}} = {tot:.0f}", font_size=30, color=THEORY)
        side = VGroup(
            label(rf"take-up: \ {100 * S['take_up']:.0f}\% of those offered", font_size=19, color=PLAN),
            label(rf"the offer's effect: \ +{itt:.1f}", font_size=19, color=SOPH),
            eq,
            label(rf"takers' $\beta$: \ {S['beta_takers']:.2f}; \ others' {S['beta_others']:.2f}", font_size=19,
                  color=NAIF),
            label(rf"{100 * S['soph_takers']:.0f}\% of takers are sophisticates; \\ naifs see no use for it",
                  font_size=18, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            f"The Island runs the same trial, with {S['n']:,} clients. <bookmark mark='a'/> Of those offered the "
            f"locked account, {100 * S['take_up']:.0f} percent take it. <bookmark mark='b'/> Comparing everyone "
            f"offered with everyone not offered, savings are {itt:.1f} points higher: the effect of the offer, "
            "which randomization makes clean. <bookmark mark='c'/> Only the takers can have been changed by the "
            "account, so the effect on a taker is the effect of the offer divided by the take-up: "
            f"{tot:.0f} points, the Wald ratio of Part four. <bookmark mark='d'/> And the takers are the more "
            f"present-biased, with an average beta of {S['beta_takers']:.2f} against {S['beta_others']:.2f}. "
            f"<bookmark mark='e'/> They are mostly sophisticates. Naifs, sure they will save anyway, see no use for "
            "a lock, which is why the people who might need commitment most are the least likely to ask for it."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(bars[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[1][0], DOWN), FadeIn(bars[1][1:]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Write(side[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()
