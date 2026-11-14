from __future__ import annotations

import numpy as np

from videos.psychology.psych17.common import *  # noqa: F403

NAMES = {"greedy": r"greedy: \ always the best so far", "epsilon": r"$\epsilon$-greedy: \ random 10\% of the time",
         "softmax": r"softmax on the averages", "ucb": r"UCB: \ add a bonus for uncertainty",
         "thompson": r"Thompson: \ sample a belief, \ act on it"}
COLS = {"greedy": INHIB, "epsilon": REWARD, "softmax": CUE, "ucb": VALUE, "thompson": DELTA}


class Explore(VoiceoverScene):
    def construct(self):
        self.card()
        self.dilemma()
        self.regret()
        self.people()

    def card(self):
        card = chapter_card(6, r"Explore or exploit", r"When should you try something that is probably worse?",
                            lit={1933: r"Thompson", 2002: r"Auer et al."}, part=PART, scale=("mind", "person"),
                            marr=("what", "how"))
        with self.voiceover("Chapter six. Explore or exploit."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def dilemma(self):
        head = heading(r"The dilemma")
        rows = rows_of([
            (r"exploit: \ choose what has paid best so far", REWARD),
            (r"explore: \ try something else, \ because your estimates might be wrong", CUE),
            (r"a pure exploiter can lock onto a bad option after one lucky win", INHIB),
            (r"a pure explorer never cashes in what it has learned", GREY_A),
            (r"the right balance depends on the horizon: \ explore early, \ exploit late", YOU),
        ], 12.4, 30, 0.42).move_to([0, 0.55, 0])
        bar = Rectangle(width=10.0, height=0.45, stroke_width=0, fill_opacity=0.85).set_fill(
            color=[CUE, REWARD]).move_to([0, -2.35, 0])
        bar.set_sheen_direction(RIGHT)
        ends = VGroup(label(r"the first choices: \ explore", font_size=22, color=CUE).next_to(bar, DOWN, buff=0.15)
                      .align_to(bar, LEFT),
                      label(r"the last choices: \ exploit", font_size=22, color=REWARD).next_to(bar, DOWN, buff=0.15)
                      .align_to(bar, RIGHT),
                      label(r"the time you have left to choose", font_size=22, color=GREY_A).next_to(bar, UP, buff=0.15))
        with self.voiceover(
            "Every learner who chooses faces a dilemma. <bookmark mark='a'/> Exploit: take the option that has "
            "paid best so far. <bookmark mark='b'/> Or explore: try something else, because your estimates are "
            "built on few samples and might be wrong. <bookmark mark='c'/> Exploit only, and one lucky early win "
            "can lock you onto a worse option forever. <bookmark mark='d'/> Explore only, and you never cash in on "
            "anything you learn. <bookmark mark='e'/> The right balance depends on how long you'll be choosing. A "
            "new restaurant is worth trying on your first week in a city, not on your last night."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bar), FadeIn(ends))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def regret(self):
        d = load("explore")
        head = heading(r"Five policies on four slot machines")
        A = axes([0, 5000], [0, 350], x_length=7.0, y_length=3.9, xticks=[0, 1000, 2000, 3000, 4000, 5000],
                 yticks=[0, 100, 200, 300], xlabel=r"plays", ylabel=r"regret: \ reward lost to not knowing",
                 center=[-2.4, 0.45, 0])
        ax = A.ax
        x = np.arange(5000)
        cs = VGroup(*[curve(ax, x, d[p], COLS[p], 3) for p in ("greedy", "epsilon", "softmax", "ucb", "thompson")])
        lg = legend([(COLS[p], NAMES[p]) for p in ("greedy", "epsilon", "softmax", "ucb", "thompson")], font_size=20)
        lg.move_to([4.4, 0.6, 0])
        keep_in_frame(lg)
        rows = rows_of([
            (r"machines paying 40, \ 45, \ 50 and 60\%; \ 5,000 plays, \ averaged over 100 runs", GREY_A),
            (r"greedy locks in early, \ often on the wrong machine; \ regret grows for ever", INHIB),
            (r"Thompson sampling does best; \ UCB's textbook bonus explores for a long time before it settles",
             DELTA),
        ], 12.4, 24, 0.2).to_edge(DOWN, buff=0.8)
        tag = psyche_tag(r"computed: \ \texttt{rl.explore\_regret}")
        with self.voiceover(
            "How well do simple policies do? Regret measures the reward lost by not knowing which machine is best. "
            "<bookmark mark='a'/> Four machines paying between forty and sixty percent, played five thousand times, "
            "averaged over a hundred runs. <bookmark mark='b'/> Greedy, always the best so far, often locks onto the "
            "wrong machine early, and its regret keeps growing. <bookmark mark='c'/> Epsilon-greedy explores at "
            "random a tenth of the time: it finds the best machine, but keeps wasting a tenth of its plays for ever, so its "
            "regret keeps climbing in a straight line. Softmax on averages this close together explores far too "
            "much, and does no better than greedy. <bookmark mark='d'/> The upper confidence bound adds a bonus to options you know little about; "
            "with the textbook bonus it's guaranteed to do well in the long run, but it explores for a long time "
            "before it settles, and its curve bends only slowly. Thompson sampling, from 1933, draws a plausible payoff for each machine from "
            "what you know and plays the best draw. It directs its exploring to where uncertainty is, tapers it off as "
            "it learns, and here it does best."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(cs[0]), FadeIn(lg[0]), FadeIn(rows[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(cs[1]), Create(cs[2]), FadeIn(lg[1]), FadeIn(lg[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(Create(cs[3]), Create(cs[4]), FadeIn(lg[3]), FadeIn(lg[4]), FadeIn(rows[2]), run_time=1.5)
        self.clear_scene()

    def people(self):
        head = heading(r"What people do")
        rows = rows_of([
            (r"2014: \ Wilson and colleagues give people a horizon: \ one more choice, \ or six", WHITE),
            (r"with a long horizon people pick the less-known option more: \ directed exploration", DELTA),
            (r"and their choices get noisier too: \ random exploration", CUE),
            (r"people use both, \ and adjust both to the horizon; \ children explore more than adults", YOU),
        ], 6.4, 26, 0.45).to_edge(LEFT, buff=0.6).shift(DOWN * 0.1)
        # a choice model with an information bonus A and decision noise sigma: P(pick the less-known option)
        dm = np.linspace(-30, 30, 121)
        A = axes([-30, 30], [0, 1], x_length=5.0, y_length=3.2, xticks=[-30, 0, 30], yticks=[0, 0.5, 1],
                 xlabel=r"how much better the less-known option looked, \ points",
                 ylabel=r"P(choose the less-known option)", center=[3.6, 0.35, 0], font_size=17)
        ax = A.ax
        h1 = curve(ax, dm, 1 / (1 + np.exp(-dm / 4.0)), GREY_B, 3)
        h6 = curve(ax, dm, 1 / (1 + np.exp(-(dm + 6.0) / 7.0)), DELTA, 4)
        mid = DashedLine(ax.c2p(0, 0), ax.c2p(0, 1), color=GREY_D, stroke_width=1.2)
        lg = legend([(GREY_B, r"one choice left"), (DELTA, r"six choices left")], font_size=18)
        lg.next_to(ax.c2p(-30, 1), RIGHT, buff=0.2).shift(DOWN * 0.35)
        shift = Arrow(ax.c2p(2, 0.5), ax.c2p(-6, 0.5), buff=0, color=DELTA, stroke_width=3,
                      max_tip_length_to_length_ratio=0.35)
        ptag = psyche_tag(r"Psyche: \ a choice model, \ bonus and noise set by hand")
        tag = published_tag(archive.WILSON_2014.cite)
        with self.voiceover(
            "Do people explore like this? <bookmark mark='a'/> In 2014 Robert Wilson and colleagues gave people two "
            "options, some samples of each, and either one more choice to make or six. <bookmark mark='b'/> With "
            "six choices ahead, people picked the option they knew less about more often, even when it looked a "
            "little worse: directed exploration, like the uncertainty bonus. <bookmark mark='c'/> They also became "
            "more random: a softer softmax. <bookmark mark='d'/> So people use both kinds, and tune both to the "
            "horizon, as they should. Later studies find that children explore more than adults, which is what a "
            "long horizon calls for."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(ptag), FadeIn(A), FadeIn(mid))
            vo.wait_until("a")
            self.play(FadeIn(rows[0], shift=RIGHT * 0.15), Create(h1), FadeIn(lg[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1], shift=RIGHT * 0.15), Create(h6), FadeIn(lg[1]), GrowArrow(shift))
            vo.wait_until("c")
            self.play(FadeIn(rows[2], shift=RIGHT * 0.15), Indicate(h6, color=CUE, scale_factor=1.0))
            vo.wait_until("d")
            self.play(FadeIn(rows[3], shift=RIGHT * 0.15))
        self.clear_scene()
