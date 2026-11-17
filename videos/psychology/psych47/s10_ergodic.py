from __future__ import annotations

from videos.psychology.psych47.common import *  # noqa: F403


class Ergodic(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.population()
        self.predict()

    def card(self):
        card = chapter_card(9, r"Ergodicity", r"When do group statistics describe individuals?",
                            lit={2004: r"Molenaar", 2018: r"Fisher et al."}, part=PART, scale=("person", "group"),
                            marr=("what",))
        with self.voiceover("Chapter nine. Ergodicity."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def idea(self):
        head = heading(r"Molenaar's manifesto")
        rows = rows_of([
            (r"a process is ergodic when its statistics across a population equal its statistics over time within a "
             r"member", WHITE),
            (r"two conditions: \ every person follows the same model (homogeneity), \ and the model does not change "
             r"over time (stationarity)", MODEL),
            (r"Molenaar, \ 2004: \ psychological processes almost never meet both; \ people differ, \ and they "
             r"develop", AUTH),
            (r"so group analyses, \ however large, \ do not by themselves describe any individual", PERSON),
        ], 12.4, 22, 0.44).move_to([0, -0.3, 0])
        tag = published_tag(r"Molenaar (2004)")
        with self.voiceover(
            "Peter Molenaar gave the problem a mathematical name. <bookmark mark='a'/> A process is ergodic when its "
            "statistics across a population equal its statistics over time within a member. <bookmark mark='b'/> That "
            "needs two conditions: every person follows the same model, and the model doesn't change over time. "
            "<bookmark mark='c'/> In 2004 Molenaar argued that psychological processes almost never meet both. People "
            "differ, and they develop. <bookmark mark='d'/> So group analyses, however large, don't by themselves "
            "describe any individual."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def population(self):
        d = load("ergodic")
        head = heading(r"A population that describes no one")
        A = axes([-1, 1], [0, 22], x_length=5.6, y_length=3.0, xticks=[-1, -0.5, 0, 0.5, 1], yticks=[0, 10, 20],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:.0f}", xlabel=r"each person's own correlation, \ over time",
                 ylabel=r"people", center=[-3.3, 0.3, 0], font_size=13)
        edges = np.linspace(-1, 1, 21)
        b = bars(A.ax, (edges[:-1] + edges[1:]) / 2, d["within_hist"], [MODEL] * 20, width=0.09)
        cross = DashedLine(A.ax.c2p(d["cross_mean"], 0), A.ax.c2p(d["cross_mean"], 22), color=AUTH, stroke_width=3)
        c_l = label(r"across people", font_size=13, color=AUTH).next_to(A.ax.c2p(d["cross_mean"], 22), UP, buff=0.05)
        rows = rows_of([
            (r"Psyche: \ 200 people, \ 100 occasions; \ people differ stably in two traits, \ and each person's two "
             r"traits move together in their own way", WHITE),
            (rf"at any moment, \ across people, \ the traits correlate {d['cross_mean']:.2f}", AUTH),
            (rf"within people the correlations spread from strongly negative to strongly positive; \ only "
             rf"{100 * d['share_near']:.0f}\% are within 0.1 of the group's, \ and {100 * d['share_negative']:.0f}\% "
             rf"are negative", MODEL),
            (r"Fisher, \ Medaglia and Jeronimus, \ 2018, \ found real samples behaving like this: \ individual "
             r"variation several times the group's", PERSON),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{within.nonergodic}")
        with self.voiceover(
            "Psyche builds a population to see what that means. <bookmark mark='a'/> Two hundred people, a hundred "
            "occasions each. People differ stably in two traits, and each person's two traits move together in their "
            "own way. <bookmark mark='b'/> At any moment, across people, the traits correlate about zero point six. "
            "<bookmark mark='c'/> Within people, the correlations spread from strongly negative to strongly positive. "
            "Fewer than one in ten are close to the group's, and almost half are negative. <bookmark mark='d'/> Aaron "
            "Fisher, John Medaglia and Bertus Jeronimus found real samples behaving like this in 2018, with variation "
            "between individuals several times larger than the group's would suggest."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(cross), FadeIn(c_l))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(b))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def predict(self):
        d = load("owngroup")
        head = heading(r"Your own few days, \ or everyone's?")
        A = axes([0, 44], [0, 0.75], x_length=5.6, y_length=3.0, xticks=[5, 10, 20, 40], yticks=[0, 0.25, 0.5, 0.75],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"a person's own occasions used",
                 ylabel=r"error predicting their later correlation", center=[-3.3, 0.3, 0], font_size=12)
        co = curve(A.ax, d["k"], d["own_err"], GOOD, stroke_width=4)
        cg = curve(A.ax, d["k"], d["group_err"], AUTH, stroke_width=4)
        key = VGroup(label(r"the person's own", font_size=13, color=GOOD), label(r"the group's", font_size=13,
                                                                              color=AUTH)).arrange(RIGHT, buff=0.4)
        key.next_to(A, UP, buff=0.3)
        rows = rows_of([
            (r"predict how a person's two traits will move together later: \ from the group's correlation, \ or "
             r"from the person's own first few occasions?", WHITE),
            (rf"in this population the group's number is off by {d['group_err'][0]:.2f} on average, \ however much "
             rf"data the group has", AUTH),
            (rf"five occasions of the person's own are off by {d['own_err'][0]:.2f}; \ forty by {d['own_err'][-1]:.2f}",
             GOOD),
            (r"when people differ this much, \ a little data about the person beats a lot about everyone else", YOU),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{within.own\_vs\_group}")
        with self.voiceover(
            "So what should you use to predict one person? <bookmark mark='a'/> Say you want to predict how a "
            "person's two traits will move together later. Use the group's correlation, or the person's own first "
            "few occasions? <bookmark mark='b'/> In this population the group's number is off by about zero point six "
            "five on average, however much data the group has. <bookmark mark='c'/> Five occasions of the person's "
            "own are off by about zero point four; forty, by about zero point one three. <bookmark mark='d'/> When "
            "people differ this much, a little data about the person beats a lot of data about everyone else."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(cg))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Create(co))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
