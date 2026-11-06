from __future__ import annotations

import numpy as np

from videos.stats.stats40.common import *  # noqa: F403


def swimmers(d, grp, center, width=5.4, height=5.0, color=None):
    """One lane per patient: a bar to the time of relapse (dot) or of last contact (open ring)."""
    t, e, g = (np.asarray(d[k], float) for k in ("time", "event", "group"))
    k = g == grp
    tt, ee = t[k], e[k]
    o = np.lexsort((-ee, tt))
    tt, ee = tt[o], ee[o]
    n = len(tt)
    s = width / 36.0
    x0 = center[0] - width / 2
    y0 = center[1] + height / 2
    gap = height / n
    out = VGroup()
    for i, (a, b) in enumerate(zip(tt, ee)):
        y = y0 - (i + 0.5) * gap
        bar = Line([x0, y, 0], [x0 + a * s, y, 0], color=color, stroke_width=4)
        end = (Dot([x0 + a * s, y, 0], radius=0.06, color=EVTC) if b else
               Circle(radius=0.06, color=CENSC, stroke_width=2.5).move_to([x0 + a * s, y, 0]))
        out.add(VGroup(bar, end))
    axis = VGroup(Line([x0, y0 - height - 0.05, 0], [x0 + width, y0 - height - 0.05, 0], color=GREY_C, stroke_width=2))
    for w in (0, 10, 20, 30):
        axis.add(MathTex(f"{w}", font_size=20, color=GREY_B).move_to([x0 + w * s, y0 - height - 0.3, 0]))
    axis.add(label(r"weeks in remission", font_size=20, color=GREY_A).move_to([x0 + width / 2, y0 - height - 0.62, 0]))
    return out, axis


class Hook(VoiceoverScene):
    def construct(self):
        self.story()
        self.lanes()
        self.problem()
        self.question()
        self.objectives()

    def story(self):
        tl = timeline(lit=(1963,)).to_edge(UP, buff=0.35)
        hc = history_card(1963, r"Emil Freireich and colleagues, \ \emph{The effect of 6-mercaptopurine on the duration of steroid-induced remissions in acute leukemia}",
                          r"Acute leukaemia in children was almost always fatal. \ Steroids could push it into remission for a while; \ "
                          r"the question was whether a drug, \ 6-mercaptopurine, \ would keep it there longer. \ Patients in remission were "
                          r"paired and, \ within each pair, \ one was given 6-MP and the other a placebo, \ by chance and without either "
                          r"knowing which. \ A sequential design let the trial stop as soon as the answer was clear",
                          color=MPC, width=11.2, font_size=22).move_to([0, 0.8, 0])
        rows = fit_rows(VGroup(
            label(r"one of the first randomized, \ placebo-controlled trials in cancer", font_size=24, color=TAUC),
            label(r"and the data that Gehan, \ Cox and many others would analyse again", font_size=24, color=GREY_A),
        ), 12.0, 0.35, [0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 1963 Emil Freireich and colleagues at the National Cancer Institute reported a trial "
            "in acute leukaemia, then almost always fatal for children. Steroids could push the disease into remission for "
            "a few weeks. The question was whether a drug, six-mercaptopurine, would keep it there longer. Patients in "
            "remission were paired, and within each pair one received the drug and the other a placebo, by chance, with "
            "neither patient nor doctor knowing which. <bookmark mark='b'/> It was one of the first randomized, "
            "placebo-controlled trials in cancer, <bookmark mark='c'/> and its numbers became the most re-analysed little "
            "data set in survival analysis."
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def lanes(self):
        d = load("gehan")
        L1, ax1 = swimmers(d, 0, [-3.4, 0.5, 0], color=PLC)
        L2, ax2 = swimmers(d, 1, [3.4, 0.5, 0], color=MPC)
        t1 = label(r"placebo: \ 21 patients", font_size=24, color=PLC).move_to([-3.4, 3.35, 0])
        t2 = label(r"6-MP: \ 21 patients", font_size=24, color=MPC).move_to([3.4, 3.35, 0])
        key = label(r"red dot: \ relapse \quad open ring: \ still in remission when last seen", font_size=20, color=GREY_A).move_to([-3.2, -3.45, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here are the forty-two patients, one lane each, ending at relapse, a red dot. On "
            "placebo, every one of the twenty-one relapsed, the last at twenty-three weeks. <bookmark mark='b'/> On the "
            "drug, nine relapsed. <bookmark mark='c'/> The other twelve, the open rings, were still in remission when the "
            "trial ended or when they were last seen: we know only that their remission lasted at least that long."
        ) as vo:
            self.add(gehan_tag())
            vo.wait_until("a")
            self.play(FadeIn(t1), FadeIn(ax1), LaggedStart(*[Create(r[0]) for r in L1], lag_ratio=0.05), run_time=3)
            self.play(*[FadeIn(r[1]) for r in L1], FadeIn(key))
            vo.wait_until("b")
            self.play(FadeIn(t2), FadeIn(ax2), LaggedStart(*[Create(r[0]) for r in L2], lag_ratio=0.05), run_time=3)
            self.play(*[FadeIn(r[1]) for r in L2 if isinstance(r[1], Dot)])
            vo.wait_until("c")
            self.play(*[Indicate(r[1], color=WHITE) for r in L2 if not isinstance(r[1], Dot)], *[FadeIn(r[1]) for r in L2 if not isinstance(r[1], Dot)])
        self.clear_scene()

    def problem(self):
        d = load("gehan")
        nv = d["naive"]
        rows = fit_rows(VGroup(
            label(r"how long does remission last on 6-MP?", font_size=28, color=TAUC),
            label(rf"average the 21 times, \ as if all had relapsed: \ {nv['mean_all_as_events']:.1f} weeks \ (too short)", font_size=26, color=MISSC),
            label(rf"average only the 9 relapses: \ {nv['mean_events_only']:.1f} weeks \ (shorter still)", font_size=26, color=MISSC),
            label(r"wait until everyone relapses: \ unethical, \ and too late to help anyone", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> So how long does remission last on the drug? <bookmark mark='b'/> Averaging the "
            "twenty-one times as if all had relapsed gives " + say(nv["mean_all_as_events"], 1) + " weeks, which is too "
            "short, since twelve of them had not. <bookmark mark='c'/> Averaging only the nine relapses gives "
            + say(nv["mean_events_only"], 1) + ", shorter still, since it throws away the patients who did best. "
            "<bookmark mark='d'/> And waiting until everyone relapses is neither ethical nor useful."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def question(self):
        rows = fit_rows(VGroup(
            label(r"censoring: \ an observation that says \ ``at least this long''", font_size=26, color=CENSC),
            label(r"it is information, \ not missing data to throw away", font_size=26, color=TAUC),
            label(r"the tools: \ the risk set, \ the hazard, \ Kaplan--Meier, \ Cox", font_size=26, color=SURVC),
            label(r"and the traps: \ hazard ratios, \ immortal time, \ competing risks", font_size=26, color=MISSC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The open rings are censored observations: each says, at least this long. <bookmark "
            "mark='b'/> That is real information, and the whole subject is about using it rather than throwing it away. "
            "<bookmark mark='c'/> The tools are the risk set, the hazard, Kaplan and Meier's curve, and Cox's model. "
            "<bookmark mark='d'/> And there are traps, famous ones, in what hazard ratios mean, in time that cannot kill "
            "you, and in risks that compete."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 40", font_size=34, color=GREY_B), label(r"Time to Event", font_size=56)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"lifetimes: \ survival, \ hazard, \ cumulative hazard; \ censoring and truncation",
            r"Kaplan--Meier, \ Greenwood, \ Nelson--Aalen; \ counting processes and martingales",
            r"the log-rank test; \ Cox's partial likelihood, \ and checking it",
            r"what hazard ratios mean; \ immortal time; \ parametric and AFT models",
            r"competing risks; \ frailty; \ prediction, \ and conformal bounds",
        ], color=TAUC, font_size=26)
        prereq = note(r"prerequisites: \ Parts 22 and 24").to_corner(DL, buff=0.3)
        built = note(r"built: \ \texttt{statkit.survival}; \ the KM staircase; \ data: \ Gehan, \ PBC, \ Stanford, \ MGUS").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part forty: time to event. <bookmark mark='b'/> We'll define survival and the hazard; "
            "build the Kaplan-Meier curve and its intervals, and the counting process theory beneath them; derive the "
            "log-rank test and Cox's partial likelihood, and check them; ask what hazard ratios mean and meet the trap of "
            "immortal time; fit parametric models; handle competing risks and frailty; and end with prediction."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()
