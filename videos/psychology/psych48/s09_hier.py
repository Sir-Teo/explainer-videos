from __future__ import annotations

from videos.psychology.psych48.common import *  # noqa: F403


class Hier(VoiceoverScene):
    def construct(self):
        self.card()
        self.population()
        self.bytrials()

    def card(self):
        card = chapter_card(8, r"People as a population", r"Can a few trials per person be enough?",
                            lit={2013: r"Lee \& Wagenmakers"}, part=PART, scale=("person", "group"), marr=("how",))
        with self.voiceover("Chapter eight. People as a population."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def population(self):
        d = load("group")
        head = heading(r"Hierarchical fitting")
        A = axes([-2.5, 1.0], [0, 3.2], x_length=6.0, y_length=3.4, xticks=[-2, -1, 0, 1], yticks=None,
                 xfmt=lambda v: f"{v:g}", xlabel=r"learning rate (log-odds)", center=[-3.0, 0.2, 0], font_size=13)
        n = len(d["true"])
        order = np.argsort(d["ml"])
        pts = VGroup()
        for k, i in enumerate(order):
            y = 3.0 - 2.8 * k / n
            ml = float(np.clip(d["ml"][i], -2.5, 1.0))
            pts.add(VGroup(Dot(A.ax.c2p(ml, y), radius=0.05, color=AUTH),
                           Arrow(A.ax.c2p(ml, y), A.ax.c2p(float(d["eb"][i]), y), buff=0, color=MODEL, stroke_width=2,
                                 max_tip_length_to_length_ratio=0.25),
                           Dot(A.ax.c2p(float(d["true"][i]), y), radius=0.04, color=YOU)))
        mu = DashedLine(A.ax.c2p(d["mu"], 0), A.ax.c2p(d["mu"], 3.2), color=GREY_B, stroke_width=1.5)
        key = VGroup(label(r"each alone", font_size=13, color=AUTH), label(r"as a population", font_size=13, color=MODEL),
                     label(r"truth", font_size=13, color=YOU)).arrange(RIGHT, buff=0.4).next_to(A, UP, buff=0.05)
        rows = rows_of([
            (r"Psyche: \ 30 people, \ 60 trials each, \ learning rates that differ around a population average", WHITE),
            (r"fitted alone, \ each estimate is noisy, \ and some run off to the bounds", AUTH),
            (rf"fitted as draws from a population, \ each is pulled toward the group, \ more when it is uncertain: \ "
             rf"error {d['rmse_ml']:.2f} becomes {d['rmse_eb']:.2f}", MODEL),
            (r"a full Bayesian hierarchy does the same with every parameter at once; \ the population's spread is "
             r"itself estimated (Lee and Wagenmakers)", GOOD),
        ], 5.6, 18, 0.36).move_to([3.6, -0.1, 0])
        tag = psyche_tag(r"\texttt{fit.group\_fit}, \ empirical Bayes")
        with self.voiceover(
            "Real studies rarely give each person two hundred trials. <bookmark mark='a'/> Psyche makes thirty "
            "people, sixty trials each, whose learning rates differ around a population average. "
            "<bookmark mark='b'/> Fitted alone, each estimate is noisy, and some run off to the bounds. "
            "<bookmark mark='c'/> Fitted as draws from a population, each estimate is pulled toward the group, more "
            "when it's uncertain. The error falls by almost half. <bookmark mark='d'/> A full Bayesian hierarchy does "
            "the same for every parameter at once, and estimates how much people really differ, as Michael Lee and "
            "Eric-Jan Wagenmakers teach."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(key), FadeIn(mu))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), LaggedStart(*[FadeIn(p[0]) for p in pts], lag_ratio=0.05), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), LaggedStart(*[GrowArrow(p[1]) for p in pts], lag_ratio=0.05), run_time=2.0,)
            self.play(FadeIn(VGroup(*[p[2] for p in pts])))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def bytrials(self):
        d = load("shrinktrials")
        head = heading(r"When does pooling pay?")
        A = axes([0, 260], [0, 1.1], x_length=5.6, y_length=3.0, xticks=[30, 60, 120, 240], yticks=[0, 0.5, 1],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"trials per person",
                 ylabel=r"error in each learning rate", center=[-3.3, 0.3, 0], font_size=12)
        cm = curve(A.ax, d["trials"], d["ml"], AUTH, stroke_width=4)
        ce = curve(A.ax, d["trials"], d["eb"], GOOD, stroke_width=4)
        key = VGroup(label(r"each person alone", font_size=13, color=AUTH),
                     label(r"people as a population", font_size=13, color=GOOD)).arrange(RIGHT, buff=0.4)
        key.next_to(A, UP, buff=0.25)
        rows = rows_of([
            (r"40 people, \ four simulated groups at each length (logit scale)", WHITE),
            (rf"with 30 trials each, \ fitting people alone misses by {d['ml'][0]:.2f}; \ as a population, \ "
             rf"{d['eb'][0]:.2f}: \ half", GOOD),
            (rf"with 240 trials, \ {d['ml'][-1]:.2f} against {d['eb'][-1]:.2f}: \ each person's data speak for "
             rf"themselves", MODEL),
            (r"pooling helps most where data are fewest: \ short tasks, \ patients, \ children", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{fit.group\_fit}, \ empirical Bayes")
        with self.voiceover(
            "When does fitting people as a population pay? <bookmark mark='a'/> Forty people, four simulated groups "
            "at each length. <bookmark mark='b'/> With thirty trials each, fitting people alone misses by about one "
            "unit on the logit scale. As a population, about half that. <bookmark mark='c'/> With two hundred and "
            "forty trials, the two are close: each person's data speak for themselves. <bookmark mark='d'/> Pooling "
            "helps most where data are fewest: short tasks, patients, and children."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Create(cm), Create(ce))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
