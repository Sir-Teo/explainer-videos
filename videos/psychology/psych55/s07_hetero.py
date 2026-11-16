from __future__ import annotations

from videos.psychology.psych55.common import *  # noqa: F403


class Hetero(VoiceoverScene):
    def construct(self):
        card_section(self, 6, r"Heterogeneity is the finding", r"For whom, \ and where?", scale=("person", "society"))
        self.argument()
        self.quartiles()
        self.sites()

    def argument(self):
        rows_section(self, r"Bryan, \ Tipton and Yeager, \ 2021", [
            (r"behavioural science has treated an average effect as the effect, \ and variation as noise", WHITE),
            (r"but interventions work for some people in some places, \ and not others: \ the mindset study of Part 54 "
             r"worked only in some schools", MODEL),
            (r"their call: \ plan studies to estimate who benefits, \ with samples that span the population, \ and "
             r"report the spread, \ not just the mean", GOOD),
            (r"Part 47 in policy form: \ an average describes a population, \ and may describe no one in it", PERSON),
        ], "Christopher Bryan, Elizabeth Tipton and David Yeager argued in 2021 that heterogeneity is the finding. "
           "<bookmark mark='a'/> Behavioural science has treated an average effect as the effect, and variation as "
           "noise. <bookmark mark='b'/> But interventions work for some people in some places, and not others. Part "
           "54's mindset study worked only in some schools. <bookmark mark='c'/> Their call: plan studies to estimate "
           "who benefits, with samples that span the population, and report the spread, not just the mean. "
           "<bookmark mark='d'/> It's Part 47 in policy form. An average describes a population, and may describe "
           "no one in it.", tag=published_tag(r"Bryan, \ Tipton \& Yeager (2021)"))

    def sites(self):
        chips_section(self, r"Why effects shrink when they scale", [
            (r"site selection", r"the first sites are chosen because they look promising; \ later ones are the "
                                r"rest (Allcott's energy reports)", AUTH),
            (r"voltage drop", r"the original team's care is not delivered by a large organization's busy staff", PERSON),
            (r"ceiling", r"the people who respond easily responded first; \ the rest are harder to move", MODEL),
            (r"the filter", r"chapter five's selection: \ the pilot that got scaled was the one that looked best", SYMP),
        ], "Why do effects shrink when they scale? <bookmark mark='a'/> Site selection: the first sites are chosen "
           "because they look promising, and later ones are the rest. Allcott's energy reports showed it. "
           "<bookmark mark='b'/> Voltage drop: the original team's care isn't delivered by a large organization's "
           "busy staff. <bookmark mark='c'/> Ceilings: the people who respond easily responded first, and the rest "
           "are harder to move. <bookmark mark='d'/> And the filter of chapter five: the pilot that got scaled was "
           "the one that looked best.")

    def quartiles(self):
        d = load("hetero")
        head = heading(r"One average, \ four groups")
        A = axes([0.3, 4.7], [-1.5, 4.6], x_length=5.4, y_length=3.0, xticks=None, yticks=[0, 2, 4],
                 yfmt=lambda v: f"{v:.0f}", ylabel=r"effect (points)", center=[-3.3, 0.4, 0], font_size=12)
        zero = DashedLine(A.ax.c2p(0.3, 0), A.ax.c2p(4.7, 0), color=GREY_C, stroke_width=2)
        est, se, tru = 100 * d["est"], 100 * d["se"], 100 * d["true"]
        cols = [GREY_B, GREY_B, MODEL, GOOD]
        b = bars(A.ax, [1, 2, 3, 4], np.maximum(est, 0.02), cols, width=0.55)
        errs = VGroup(*[Line(A.ax.c2p(i + 1, est[i] - 1.96 * se[i]), A.ax.c2p(i + 1, est[i] + 1.96 * se[i]),
                             color=WHITE, stroke_width=3) for i in range(4)])
        truth = VGroup(*[Dot(A.ax.c2p(i + 1, tru[i]), radius=0.07, color=YOU) for i in range(4)])
        names = VGroup(*[label(t, font_size=12, color=GREY_A).next_to(A.ax.c2p(i + 1, -1.5), DOWN, buff=0.1)
                         for i, t in enumerate([r"least likely to forget", r"", r"", r"most likely to forget"])
                         if t])
        rows = rows_of([
            (rf"a reminder trial on 160{{,}}000 simulated people: \ the average effect is {100 * d['ate']:.1f} "
             rf"points ($\pm${196 * d['ate_se']:.1f})", WHITE),
            (r"split by a baseline score, \ the true effects (gold dots) run from 0.2 to 3.4 points: \ the reminder "
             r"works on people who would have forgotten", MODEL),
            (rf"the most forgetful quarter holds {100 * d['share_top']:.0f}\% of the whole benefit: \ target them and "
             r"most of the gain comes at a quarter of the cost", GOOD),
            (r"but even with 160{,}000 people, \ each quarter's interval is about $\pm$1 point: \ the lower two cannot "
             r"be told from zero, \ or from each other", AUTH),
            (r"so subgroups must be named before the data, \ and powered: \ a subgroup found afterwards among many is "
             r"Part 4's garden", YOU),
        ], 6.0, 18, 0.32).move_to([3.4, -0.2, 0])
        tag = psyche_tag(r"simulated trial, \ true effects known")
        with self.voiceover(
            "Here is what heterogeneity looks like in a trial. <bookmark mark='a'/> A reminder is tested on a hundred "
            "and sixty thousand simulated people, and the average effect is about one and a quarter points. "
            "<bookmark mark='b'/> Split by a baseline score, the true effects, the gold dots, run from zero point two "
            "to three point four points. The reminder works on the people who would have forgotten. "
            "<bookmark mark='c'/> The most forgetful quarter holds sixty-one percent of the whole benefit. Target them, "
            "and most of the gain comes at a quarter of the cost. <bookmark mark='d'/> But even with a hundred and "
            "sixty thousand people, each quarter's interval is about plus or minus one point. The lower two can't be "
            "told from zero, or from each other. <bookmark mark='e'/> So subgroups have to be named before the data, "
            "and powered for. A subgroup found afterwards, among many tried, is Part 4's garden of forking paths."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(zero), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(b), FadeIn(truth))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Indicate(b[3], color=GOOD))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), Create(errs))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()
