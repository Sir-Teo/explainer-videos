from __future__ import annotations

from explainer.psychology.psyche import precision as Pr
from videos.psychology.psych59.common import *  # noqa: F403


class Measure(VoiceoverScene):
    def construct(self):
        card_section(self, 6, r"Fixing measurement", r"How many trials does a person need?")
        self.trials()
        self.attenuation()
        self.remedies()

    def trials(self):
        head = heading(r"Reliability is bought with trials")
        n = np.arange(10, 2001, 10)
        r = np.array([Pr.difference_reliability(15.0, 120.0, int(k)) for k in n])
        A = axes([0, 2000], [0, 1.0], x_length=5.6, y_length=3.2, xticks=[0, 500, 1000, 1500, 2000],
                 yticks=[0, 0.5, 0.9], xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}",
                 xlabel=r"trials per condition", ylabel=r"reliability", center=[-3.3, 0.2, 0], font_size=12)
        c = curve(A.ax, n, r, MODEL, stroke_width=4)
        k60 = Dot(A.ax.c2p(60, Pr.difference_reliability(15.0, 120.0, 60)), radius=0.08, color=AUTH)
        line = DashedLine(A.ax.c2p(0, 0.9), A.ax.c2p(2000, 0.9), color=GOOD, stroke_width=2)
        n90 = int(np.ceil(0.9 / 0.1 * 2 * 120 ** 2 / 15 ** 2))
        rows = rows_of([
            (r"Spearman and Brown (Part 3): \ trial noise shrinks as one over the number of trials; \ true "
             r"differences do not", WHITE),
            (rf"Psyche's task at 60 trials: \ reliability {Pr.difference_reliability(15.0, 120.0, 60):.2f}", AUTH),
            (rf"for 0.9: \ about {num(n90)} trials per condition, \ most of an hour on one task", GOOD),
            (r"your first number: \ 0.5 at 200 trials needs nine times as many for 0.9, \ 1,800", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{precision.difference\_reliability}")
        with self.voiceover(
            "How many trials does a person need? <bookmark mark='a'/> Spearman and Brown's formula, from Part 3, says "
            "trial noise shrinks as one over the number of trials, while true differences don't. "
            "<bookmark mark='b'/> Psyche's task at sixty trials has a reliability of about zero point three. "
            "<bookmark mark='c'/> To reach zero point nine takes about eleven hundred and fifty trials per "
            "condition. That's most of an hour on one task. <bookmark mark='d'/> And your first number: a reliability of zero "
            "point five at two hundred trials needs nine times as many for zero point nine. That's eighteen hundred."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Create(c), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(k60, scale=1.5))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Create(line))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def attenuation(self):
        d = load("attenuate")
        head = heading(r"What unreliability does to a correlation")
        A = axes([0.05, 1.15], [0, 0.6], x_length=5.6, y_length=3.0, xticks=None, yticks=[0, 0.25, 0.5],
                 yfmt=lambda v: f"{v:g}", ylabel=r"observed $r$", center=[-3.3, 0.3, 0], font_size=12)
        rel = np.asarray(d["rel"])
        bs = bars(A.ax, rel, d["observed"], MODEL, width=0.13)
        truth = DashedLine(A.ax.c2p(0.05, 0.5), A.ax.c2p(1.15, 0.5), color=GOOD, stroke_width=2)
        tl = label(r"true $r$ = 0.5", font_size=13, color=GOOD).next_to(truth, UP, buff=0.05).align_to(truth, RIGHT)
        names = VGroup(*[label(f"{v:.1f}", font_size=13, color=GREY_A).next_to(A.ax.c2p(v, 0), DOWN, buff=0.1)
                         for v in rel])
        nl = label(r"the task's reliability (symptoms 0.8)", font_size=13, color=GREY_A).next_to(names, DOWN, buff=0.1)
        rows = rows_of([
            (r"Part 3's attenuation: \ observed $r$ = true $r$ times $\sqrt{\text{rel}_x\,\text{rel}_y}$", WHITE),
            (rf"a true link of 0.5 between a parameter and a symptom shows as {d['observed'][0]:.2f} with a task "
             rf"reliability of 0.2", AUTH),
            (r"small samples and low reliability together: \ links are missed, \ and the ones found are "
             r"exaggerated (Part 4's winner's curse)", MODEL),
            (r"many published parameter-symptom correlations sit between 0.1 and 0.3", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        with self.voiceover(
            "What does unreliability do to a correlation? <bookmark mark='a'/> Part 3's attenuation formula: the "
            "observed correlation is the true one times the square root of the two reliabilities. "
            "<bookmark mark='b'/> A true link of zero point five between a parameter and a symptom shows as zero "
            "point two when the task's reliability is zero point two. <bookmark mark='c'/> Put small samples and "
            "low reliability together, and links are missed, and the ones that are found are exaggerated: Part 4's "
            "winner's curse. <bookmark mark='d'/> Many published correlations between a parameter and a symptom sit "
            "between zero point one and zero point three."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(names), FadeIn(nl), Create(truth), FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bs], lag_ratio=0.2))
            for m, r_ in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r_, shift=RIGHT * 0.15))
        self.clear_scene()

    def remedies(self):
        chips_section(self, r"What fixes it", [
            (r"model the trials", r"hierarchical models estimate each person's effect with its noise, \ instead of "
                                  r"a difference of two means (Rouder and Haaf, \ Part 48)", MODEL),
            (r"skip the difference", r"use the model's parameters, \ or the raw speed and accuracy, \ which are often "
                                     r"more reliable than a difference", PERSON),
            (r"spread the trials", r"short sessions on many days, \ at home on a phone, \ average out bad days", GOOD),
            (r"report reliability", r"every individual-differences study should report its measure's reliability "
                                    r"in its own sample", SYMP),
            (r"design for people", r"choose conditions where people differ, \ not where everyone shows the effect", AUTH),
        ], "What fixes it? <bookmark mark='a'/> Model the trials. Hierarchical models estimate each person's effect "
           "along with its noise, instead of taking a difference of two means. That's Jeffrey Rouder and Julia "
           "Haaf's point, and Part 48's tools. <bookmark mark='b'/> Skip the difference. Use the model's parameters, "
           "or raw speed and accuracy, which are often more reliable than a difference score. <bookmark mark='c'/> "
           "Spread the trials. Short sessions on many days, at home on a phone, average out bad days. "
           "<bookmark mark='d'/> Report reliability. Every individual-differences study should report its measure's "
           "reliability in its own sample. <bookmark mark='e'/> And design for people: choose conditions where "
           "people differ, not where everyone shows the effect.")
