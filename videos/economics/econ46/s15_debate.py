from __future__ import annotations

from videos.economics.econ46.common import *  # noqa: F403


class Debate(VoiceoverScene):
    def construct(self):
        card(self, 13, r"The debate over experiments", r"What can a randomized trial tell us, and what can it not?",
             "Chapter thirteen. The debate over experiments.",
             lit={2010: r"Deaton", 2011: r"Banerjee and Duflo", 2019: r"the Nobel prize", 2020: r"Vivalt"},
             scale=("village", "world"), horizon=("decades",))
        self.prize()
        self.critique()
        self.sites()
        self.growth()

    def prize(self):
        chain = flow_chain([(r"a big question: \\ why are people \\ poor?", POOR),
                            (r"many small ones: \\ does this pill, \\ this price, \ work?", TRIAL),
                            (r"randomize, \\ measure", TRIAL), (r"build up \\ from the answers", GAIN)],
                           notes=[r"too large to test", r"Kremer in Kenya, \\ from the 1990s",
                                  r"thousands of trials \\ since", r"\emph{Poor Economics}, \\ 2011"],
                           box_w=2.8, font_size=19, note_size=16).move_to(UP * 0.8)
        foot = label(r"2019: \ the prize to Banerjee, \ Duflo and Kremer, \ ``for their experimental approach to "
                     r"alleviating global poverty''", font_size=20, color=E.ACCENT).to_edge(DOWN, buff=0.9)
        tag = published_tag(tables.DEBATE_46.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Most of this part has rested on randomized experiments, and that is new. <bookmark mark='a'/> For "
            "decades development economics asked big questions, like why some countries are poor, that no "
            "experiment can answer. <bookmark mark='b'/> From the 1990s, starting with Michael Kremer's school "
            "trials in Kenya, a new generation broke them into small ones: does this pill, this price, this kind "
            "of teaching, work? <bookmark mark='c'/> Randomize, and measure. Thousands of trials have followed. "
            "<bookmark mark='d'/> Abhijit Banerjee and Esther Duflo's book Poor Economics argued that answers "
            "built up this way, one question at a time, change policy more than grand theories. <bookmark "
            "mark='e'/> In 2019 the three of them shared the Nobel prize, for their experimental approach to "
            "alleviating global poverty."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(chain.boxes[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(chain.notes[0]))
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                self.play(GrowArrow(chain.arrows[k]), FadeIn(chain.boxes[k + 1]), FadeIn(chain.notes[k + 1]))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def critique(self):
        cards = point_cards([
            (r"an average", r"a trial measures \\ an average effect \\ in one place, \\ at one time", HOLD),
            (r"elsewhere?", r"the next place \\ differs: \ external \\ validity", LOSS),
            (r"at scale?", r"prices, \ wages \\ and governments \\ respond: \ chapter \\ six's multiplier", TOWN),
            (r"why?", r"without a model, \\ a result does not \\ say why it worked", THEORY),
        ], width=12.8, cols=4, font_size=18).move_to(DOWN * 0.2)
        head = label(r"Deaton's objections, \ 2010", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.DEBATE_46.tag, corner=DR, font_size=11)
        with self.voiceover(
            "The approach has serious critics, and the most eloquent is Angus Deaton, himself a Nobel laureate. "
            "<bookmark mark='a'/> A randomized trial measures an average effect, in one place, at one time, with "
            "one organization running the programme. <bookmark mark='b'/> Whether it holds anywhere else is a "
            "separate question, which randomization does nothing to answer. <bookmark mark='c'/> A programme "
            "scaled up to a whole country changes prices and wages, as chapter six's multiplier did, and is run by "
            "a government rather than a motivated charity. <bookmark mark='d'/> And a result without a model of "
            "why it worked cannot tell you what will happen when anything changes. None of this says experiments "
            "are useless. It says they are a beginning, not an end."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cards.cards[0], shift=UP * 0.1))
            vo.wait_until("a")
            self.play(Circumscribe(cards.cards[0], color=WHITE, buff=0.05))
            for mk, c in zip("bcd", cards.cards[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def sites(self):
        S = load("sites")
        k = len(S["x"])
        x, sh = np.array(S["x"]), np.array(S["shrunk"])
        order = np.argsort(x)
        ax = plane([-0.5, k - 0.5], [-0.2, 0.6], center=LEFT * 1.9 + DOWN * 0.35, x_length=8.0, y_length=4.8,
                   xticks=[], yticks=[-0.2, 0, 0.2, 0.4, 0.6], ylabel=r"the effect, \ standard deviations",
                   yfmt=lambda v: f"{v:+.1f}".replace("-", "{-}") if v else "0", font_size=14)
        zero = DashedLine(ax.ax.c2p(-0.5, 0), ax.ax.c2p(k - 0.5, 0), color=GREY_C, stroke_width=1.4)
        est, bars, shr = VGroup(), VGroup(), VGroup()
        for j, i in enumerate(order):
            bars.add(Line(ax.ax.c2p(j, x[i] - 1.96 * S["se"]), ax.ax.c2p(j, x[i] + 1.96 * S["se"]), color=TRIAL,
                          stroke_width=3))
            est.add(dot(ax, j, x[i], TRIAL, 0.075))
            shr.add(dot(ax, j, sh[i], GAIN, 0.06).shift(RIGHT * 0.12))
        mean = DashedLine(ax.ax.c2p(-0.5, S["mean"]), ax.ax.c2p(k - 0.5, S["mean"]), color=E.ACCENT,
                          stroke_width=2.2)
        pred = band(ax, [-0.5, k - 0.5], [S["next_lo"]] * 2, [S["next_hi"]] * 2, E.ACCENT, 0.12)
        side = VGroup(
            label(rf"{k} trials of one \\ programme, \ each \\ with s.e. {S['se']:.2f}", font_size=18, color=TRIAL),
            label(rf"the average: \ {S['mean']:.2f}", font_size=18, color=E.ACCENT),
            label(rf"the spread of true \\ effects: \ {S['tau_hat']:.2f}", font_size=18, color=LOSS),
            label(r"green: \ each pulled \\ toward the average", font_size=18, color=GAIN),
            label(rf"the next site: \\ {S['next_lo']:+.2f} to {S['next_hi']:+.2f}".replace("-", "{-}"),
                  font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            f"Here is the problem in numbers. The Island runs the same programme in {k} places, and evaluates each "
            f"with a good trial, a standard error of {S['se']:.2f}. <bookmark mark='a'/> The estimates, with their "
            f"intervals, spread far more widely than their errors allow. <bookmark mark='b'/> The average is "
            f"{S['mean']:.2f}, <bookmark mark='c'/> but the true effects themselves differ from place to place, "
            f"with a spread estimated at {S['tau_hat']:.2f}, larger than any trial's error. <bookmark mark='d'/> "
            "Statistics, Built's shrinkage pulls each estimate toward the average, by more where the trial is "
            "noisy relative to that spread. <bookmark mark='e'/> And for the next place, where no trial has been "
            f"run, the honest forecast runs from {say_num(S['next_lo'])} to {say_num(S['next_hi'])}: it could be "
            "harmful, or twice the average. The precision of each trial does not carry over. Eva Vivalt, "
            "collecting hundreds of impact evaluations, found exactly this: large differences between studies of "
            "the same kind of programme, with smaller effects when governments, rather than researchers or "
            "charities, ran them."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(zero), FadeIn(side[0]), run_time=1.0)
            self.play(LaggedStart(*[AnimationGroup(Create(b), FadeIn(e)) for b, e in zip(bars, est)],
                                  lag_ratio=0.15), run_time=2.5)
            vo.wait_until("a")
            self.play(*[Indicate(b, color=WHITE) for b in bars])
            vo.wait_until("b")
            self.play(Create(mean), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in shr], lag_ratio=0.1), FadeIn(side[3]), run_time=1.5)
            vo.wait_until("e")
            self.play(FadeIn(pred), FadeIn(side[4]))
        self.clear_scene()

    def growth(self):
        P = load("poverty")
        T = tables.DEBATE_46.data
        C = P["CHN"]
        rows = VGroup(
            label(rf"China: \ close to {T['china_m']} million people out of extreme poverty \ in four decades",
                  font_size=23, color=LOSS),
            label(rf"about {T['china_share']}\% of the world's fall, \ by the World Bank's count", font_size=23,
                  color=GREY_A),
            label(r"no randomized trial produced it: \ farm reform, \ factories, \ trade, \ migration to cities",
                  font_size=23, color=TOWN),
            label(r"the experiments say what works in a village; \ growth decides how many villages are poor",
                  font_size=23, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to(DOWN * 0.3)
        head = label(rf"the largest fall in poverty in history: \ {C['first']:.0f}\% to under 1\%", font_size=28,
                     color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.DEBATE_46.tag, corner=DR, font_size=11)
        with self.voiceover(
            "And there is the elephant in the room. <bookmark mark='a'/> In four decades China lifted close to "
            f"{T['china_m']} million people out of extreme poverty, <bookmark mark='b'/> about "
            f"{T['china_share']} percent of the fall in the whole world, by the World Bank's count. <bookmark "
            "mark='c'/> No randomized trial produced it. It came with the reform of farms, factories built for "
            "export, and hundreds of millions of people moving to cities, the subjects of Parts twenty, "
            "twenty-one, thirty-five and thirty-seven. <bookmark mark='d'/> The two traditions answer different "
            "questions. Experiments say what works in a village, and how much; growth decides how many villages "
            "are poor in the first place. A serious development economist needs both."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(rows[0], shift=RIGHT * 0.1))
            vo.wait_until("a")
            self.play(Indicate(rows[0], color=WHITE, scale_factor=1.03))
            for mk, r_ in zip("bcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()
