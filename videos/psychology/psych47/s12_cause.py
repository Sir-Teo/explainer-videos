from __future__ import annotations

from videos.psychology.psych47.common import *  # noqa: F403


class Cause(VoiceoverScene):
    def construct(self):
        self.card()
        self.repair()
        self.waves()

    def card(self):
        card = chapter_card(11, r"Cause over time", r"Does one change drive another, \ within a person?",
                            lit={2015: r"Hamaker et al."}, part=PART, scale=("person",), marr=("how",))
        with self.voiceover("Chapter eleven. Cause over time."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def repair(self):
        head = heading(r"The panel, \ repaired")
        data = (
            (r"the trap", r"Part 44: \ a cross-lagged panel model found loneliness ``driving'' low mood in people "
                          r"whose traits never touched; \ the stable differences between people leaked into the lags",
             AUTH),
            (r"the repair", r"give each person a random intercept for each trait (Hamaker, \ Kuiper and Grasman, \ "
                            r"2015); \ the lags then describe departures from each person's own level", GOOD),
            (r"what it needs", r"at least three waves, \ better many; \ with few, \ the person's level is poorly "
                               r"known and the lags are biased, \ as chapter 10's inertia was", MODEL),
            (r"what it still cannot do", r"rule out a third variable that changes over time, \ or choose the lag: \ "
                                         r"a day, \ a month and a year give different answers", PERSON),
            (r"the strongest design", r"change one thing for a person, \ at random times, \ and watch: \ a "
                                      r"single-case experiment, \ or a micro-randomized trial", YOU),
        )
        rows = VGroup()
        for name, how, c in data:
            rows.add(VGroup(word_chip(name, color=c, font_size=16, width=3.4), wrapped_label(how, 9.0, 19, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([0, -0.3, 0])
        tag = published_tag(r"Hamaker, Kuiper \& Grasman (2015)")
        with self.voiceover(
            "Back to cause, with what this part has added. <bookmark mark='a'/> Part 44 showed the trap. A "
            "cross-lagged panel found one trait driving another in people whose traits never touched, because the "
            "stable differences between people leaked into the lags. <bookmark mark='b'/> The repair gives each "
            "person their own level of each trait, so the lags describe departures from it. <bookmark mark='c'/> It "
            "needs at least three waves, and better many. With few, a person's level is poorly known and the lags "
            "are biased, just as chapter ten's inertia was. <bookmark mark='d'/> It still can't rule out a third "
            "variable that changes over time, or choose the lag. A day, a month and a year can give different "
            "answers. <bookmark mark='e'/> The strongest design changes one thing for a person, at random times, and "
            "watches: a single-case experiment, or a micro-randomized trial."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def waves(self):
        d = load("waves")
        head = heading(r"How many waves?")
        A = axes([0, 52], [0, 0.25], x_length=5.6, y_length=3.0, xticks=[3, 10, 20, 50], yticks=[0, 0.1, 0.2],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"waves per person",
                 ylabel=r"estimated within-person lag", center=[-3.3, 0.3, 0], font_size=13)
        truth = DashedLine(A.ax.c2p(0, d["true"]), A.ax.c2p(52, d["true"]), color=GOOD, stroke_width=2)
        c = curve(A.ax, d["waves"], d["est"], PERSON, stroke_width=4)
        dots = VGroup(*[Dot(A.ax.c2p(w, e), radius=0.07, color=PERSON) for w, e in zip(d["waves"], d["est"])])
        rows = rows_of([
            (r"Psyche: \ 500 people with stable traits and a real within-person lag of 0.2 from one trait to the "
             r"other", WHITE),
            (r"estimate it from each person's departures from their own observed mean", MODEL),
            (rf"with 3 waves it comes out at {d['est'][0]:.2f}; \ with 10, \ {d['est'][2]:.2f}; \ with 50, \ "
             rf"{d['est'][-1]:.2f}", PERSON),
            (r"few waves bias the within-person lag toward zero: \ the person's mean is too uncertain; \ intensive "
             r"designs fix it", GOOD),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{within.crosslag\_waves}")
        with self.voiceover(
            "How many waves does the repair need? <bookmark mark='a'/> Psyche makes five hundred people with stable "
            "traits and a real within-person lag of zero point two, from one trait to the other. "
            "<bookmark mark='b'/> Estimate it from each person's departures from their own observed mean. "
            "<bookmark mark='c'/> With three waves it comes out at about zero point one two. With ten, nearly right. "
            "With fifty, right. <bookmark mark='d'/> Few waves bias the within-person lag toward zero, because each "
            "person's mean is too uncertain. Intensive designs fix it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(truth))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Create(c), FadeIn(dots))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
