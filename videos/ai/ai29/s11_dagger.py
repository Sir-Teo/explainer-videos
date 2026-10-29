from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai29.common import AGENT, EXPERT, FAIL, GOOD, HIST, PART, REWARD, load, node_box, spread_band
from videos.ai.ai29.lanes import LaneView, table_strip

BC = C.MODEL_Q
DAG = C.INTERVAL


class DAgger(VoiceoverScene):
    def construct(self):
        self.card()
        self.algorithm()
        self.replay()
        self.theorem()
        self.compare()
        self.practice()

    def card(self):
        card = chapter_card(10, r"DAgger", r"How do you learn to recover?", part=PART)
        with self.voiceover("Chapter ten. DAgger."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def algorithm(self):
        steps = VGroup(node_box(r"the learner drives", DAG, 24), node_box(r"the expert labels \\ every state it "
                                                                         r"visited", EXPERT, 24),
                       node_box(r"add them to \\ all the data so far", GREY_B, 24), node_box(r"retrain", DAG, 24))
        steps.arrange(RIGHT, buff=0.6).move_to([0, 1.2, 0])
        if steps.width > 13.0:
            steps.width = 13.0
        arr = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.08, color=GREY_B, stroke_width=2.5)
                       for a, b in zip(steps, steps[1:])])
        back = CurvedArrow(steps[-1].get_bottom() + DOWN * 0.05, steps[0].get_bottom() + DOWN * 0.05, angle=-0.5,
                           color=GREY_B)
        thm = theorem_card(r"DAgger", r"for $i = 1, \ldots, N$: \ drive with $\pi_i$ \ (mixed with the expert at first), \ "
                           r"collect the states, \ label them with $\pi^*$, \ $\mathcal D \leftarrow \mathcal D \cup "
                           r"\{(s, \pi^*(s))\}$, \ $\pi_{i+1} \leftarrow$ supervised learning on $\mathcal D$",
                           who=r"Ross, Gordon \& Bagnell (2011): \ dataset aggregation", width=10.6, color=DAG,
                           kind=r"Algorithm").move_to([0, -1.9, 0])
        with self.voiceover(
            "The cure, from Stéphane Ross, Geoff Gordon and Drew Bagnell in 2011, is to ask the expert about the "
            "learner's own mistakes. <bookmark mark='a'/> Let the learner drive. <bookmark mark='b'/> Afterwards, "
            "the expert labels every state the learner visited: here is what I would have done. "
            "<bookmark mark='c'/> Add those labels to everything collected so far, <bookmark mark='d'/> retrain, and "
            "drive again. They called it DAgger, for dataset aggregation. Each round, the data moves towards the "
            "states the learner actually reaches, including the ones off the road."
        ) as vo:
            self.play(FadeIn(thm, shift=UP * 0.15))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]))
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                self.play(GrowArrow(arr[k]), FadeIn(steps[k + 1]))
            self.play(Create(back))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def replay(self):
        L = load("lane")
        D = int(L["params"]["D"])
        S = 2 * D + 1
        hist = np.asarray(L["dagger_hist"])
        drives = np.asarray(L["dagger_drives"])
        Jh = np.asarray(L["dagger_hist_J"])
        T = int(L["T"])
        view = LaneView(D, drives.shape[1] - 1, cell=0.3, height=4.2, center=[-3.0, 0.6, 0])
        strip = table_strip(view, hist[0][:S], hist[0][S:], color=DAG)
        sl = label(r"the learner's actions \ (grey: \ never labelled)", font_size=20, color=DAG).next_to(strip, DOWN,
                                                                                                         buff=0.15)
        rl = VGroup(label(r"round", font_size=24, color=GREY_A), Integer(1, font_size=30, color=DAG)).arrange(RIGHT, buff=0.15)
        rl.next_to(view, UP, buff=0.2)
        g = axes([0.5, len(Jh) + 0.5, 1], [0, max(float(Jh.max()), 1) * 1.1, 100], x_length=5.0, y_length=3.4,
                 xlabel=r"round", ylabel=rf"expected steps off the lane in ${T}$", xticks=list(range(1, len(Jh) + 1)),
                 yticks=[0, 100, 200, 300], center=[3.6, 0.2, 0])
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(k + 1, v), radius=0.08, color=DAG) for k, v in enumerate(Jh)])
        line = VMobject(color=DAG, stroke_width=3).set_points_as_corners([d.get_center() for d in dots])
        best = int(np.argmin(Jh))
        first_good = int(np.argmax(Jh <= Jh.min() + 1e-6))
        tag = note(r"seed $0$; \ each round: \ one $50$-step drive by the learner, \ labelled", font_size=18)
        tag.to_corner(DR, buff=0.25)
        with self.voiceover(
            "Here is DAgger on our lane, round by round. <bookmark mark='a'/> Round one is an expert drive, so the "
            "learner knows only the middle of the road. <bookmark mark='b'/> In the next rounds it drives itself, "
            "wanders off, and the expert labels the readings it saw out there: steer back. Grey arrows turn into "
            f"real ones. <bookmark mark='c'/> By round {first_good + 1} its expected cost over {T} steps has "
            f"fallen from {Jh[0]:.0f} to {Jh[first_good]:.0f}, and the later rounds keep it there."
        ) as vo:
            self.play(FadeIn(view), FadeIn(strip), FadeIn(sl), FadeIn(rl), FadeIn(g), FadeIn(tag), FadeIn(dots[0]))
            vo.wait_until("a")
            self.wait(0.5)
            vo.wait_until("b")
            cur = None
            for k in range(len(drives)):
                dr = view.drive(drives[k], DAG, 2.5)
                new = table_strip(view, hist[k + 1][:S], hist[k + 1][S:], color=DAG)
                anims = [Create(dr), rl[1].animate.set_value(k + 2)]
                if cur is not None:
                    anims.append(FadeOut(cur))
                self.play(*anims, run_time=0.9)
                self.play(Transform(strip, new), FadeIn(dots[k + 1], scale=1.4), dr.animate.set_stroke(opacity=0.25),
                          run_time=0.6)
                cur = dr
            vo.wait_until("c")
            self.play(Create(line), Indicate(dots[first_good], color=WHITE))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def theorem(self):
        rows = [
            cmath(r"\varepsilon_N", r"=", r"\min_\pi \tfrac1N \sum_i \mathbb E_{s \sim d_{\pi_i}}\big[\ell(\pi(s), "
                  r"\pi^*(s))\big]", font_size=32),
            cmath(r"\tfrac1N \sum_i \mathbb E_{d_{\pi_i}}[\ell(\pi_i)]", r"\le", r"\varepsilon_N + \text{regret}_N / N",
                  font_size=32),
            cmath(r"J(\hat\pi)", r"\le", r"J(\pi^*) + u\, T\, \varepsilon_N + O(1)", font_size=34),
        ]
        rows[2][2].set_color(DAG)
        whys = [why(r"the best policy's error, \ on the learner's own states"),
                why(r"no-regret online learning: \ each round, \ fit all the data"),
                why(r"after $O(uT \log T)$ rounds; \ $u$: \ how much one wrong action can cost later")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-2.0, buff=0.55, edge=6.9)
        tail = label(r"linear in $T$: \ errors are measured where the learner goes", font_size=28, color=DAG)
        tail.to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Why does this fix the T squared? The trick is to treat the rounds as an online learning game. "
            "<bookmark mark='a'/> Now the error that matters is measured on the learner's own states, the ones its "
            "own policies visit. <bookmark mark='b'/> Retraining on all the data so far is a no-regret algorithm: "
            "on average over the rounds, it does as well as the single best policy in hindsight. "
            "<bookmark mark='c'/> And the cost then grows only linearly with the horizon, times u, how much one wrong "
            "action can cost later, if the task lets you recover. <bookmark mark='d'/> The difference is where the "
            "errors are counted."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.3)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            self.play(FadeIn(tail))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def compare(self):
        L = load("lane")
        T = int(L["T"])
        ts = np.arange(1, T + 1)
        Jb, Jd = np.asarray(L["bc_J"]), np.asarray(L["dagger_J"])
        ymax = float(max(Jb.max(), Jd.max())) * 1.05
        g = axes([0, T, 100], [0, ymax, 100], x_length=6.0, y_length=4.2, xlabel=r"horizon $T$",
                 ylabel=r"expected steps off the lane", xticks=[0, 200, 400], yticks=[0, 100, 200, 300],
                 center=[-3.3, -0.3, 0])
        b1, d1 = spread_band(g.ax, ts, Jb, BC), spread_band(g.ax, ts, Jd, DAG)
        budgets = np.asarray(L["budgets"], float)
        Bb, Bd = np.asarray(L["bc_budget"]), np.asarray(L["dagger_budget"])
        lx = np.log2(budgets)
        g2 = axes([lx[0] - 0.2, lx[-1] + 0.2, 1], [0, max(Bb.max(), Bd.max()) * 1.05, 100], x_length=5.0, y_length=3.6,
                  xlabel=r"expert labels \ (log scale)", ylabel=rf"steps off the lane in ${T}$",
                  xticks=list(lx), xfmt=lambda v: f"{int(round(2 ** v))}", yticks=[0, 100, 200, 300], font_size=18,
                  center=[3.6, -0.3, 0])
        b2, d2 = spread_band(g2.ax, lx, Bb.T, BC), spread_band(g2.ax, lx, Bd.T, DAG)
        leg = legend([(BC, r"behaviour cloning"), (DAG, r"DAgger")], font_size=22).to_corner(UL, buff=0.35)
        N = int(L["N"])
        fb, fd = float(Jb[:, -1].mean()), float(Jd[:, -1].mean())
        sb, sd = float(L["bc_slope_early"]), float(L["dagger_slope_early"])
        tag = note(rf"equal budgets: \ ${N}$ expert labels each (left); \ 8 seeds, \ band min--max", font_size=18)
        tag.to_corner(DR, buff=0.25)
        if fd < 0.8 * fb:
            v1 = (f"With the same {N} expert labels, DAgger's cost at {T} steps averages {fd:.0f} steps off the lane, "
                  f"against {fb:.0f} for behaviour cloning.")
        else:
            v1 = (f"With the same {N} expert labels, DAgger averages {fd:.0f} steps off the lane at {T} steps, and "
                  f"behaviour cloning {fb:.0f}: not a clear win at this budget.")
        flat = Bb.mean(1)
        bc_flat = flat[-1] > 0.8 * flat[2]
        dag_falls = Bd.mean(1)[-1] < 0.6 * Bd.mean(1)[0]
        v2 = ("More demonstrations barely help behaviour cloning: the expert's drives never leave the lane, so they "
              "never show the way back." if bc_flat else "More demonstrations help behaviour cloning too, slowly.")
        v3 = (f" DAgger keeps improving with labels, to {Bd.mean(1)[-1]:.0f} at {int(budgets[-1])}." if dag_falls else "")
        spread = float(Jd[:, -1].max() - Jd[:, -1].min())
        with self.voiceover(
            "Now the fair comparison: the same number of expert labels for both, eight seeds each. "
            f"<bookmark mark='a'/> {v1} <bookmark mark='b'/> Its cost grows more nearly in a straight line, a "
            f"log-log slope of {sd:.2f} over the first steps against {sb:.2f}. The spread across seeds is wide, "
            f"{spread:.0f} steps for DAgger, because which readings a learner happens to see matters. "
            f"<bookmark mark='c'/> {v2}{v3}"
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), FadeIn(tag))
            self.play(FadeIn(b1[0]), Create(b1[1]), run_time=1.2)
            vo.wait_until("a")
            self.play(FadeIn(d1[0]), Create(d1[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(g2), FadeIn(b2[0]), Create(b2[1]), FadeIn(d2[0]), Create(d2[1]), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def practice(self):
        cards = VGroup(
            history_card(r"the catch", r"an expert on call", r"someone must label the learner's mistakes: \ hard for "
                         r"a human driver at speed, \ easy for a program", width=4.2, color=HIST, font_size=19),
            history_card(r"2019", r"HG-DAgger \ (Kelly et al.)", r"the human takes over only when the learner drifts, "
                         r"\ and those corrections become the data", width=4.2, color=HIST, font_size=19),
            history_card(r"Part 27", r"on-policy distillation", r"a student writes, \ the teacher scores the student's "
                         r"own tokens: \ DAgger for language models", width=4.2, color=HIST, font_size=19),
        ).arrange(RIGHT, buff=0.25).move_to([0, 0.9, 0])
        tail = label(r"learn from where you actually end up, \ not only from where the expert goes", font_size=28,
                     color=DAG).to_edge(DOWN, buff=0.9)
        with self.voiceover(
            "DAgger has a price: an expert on call to label the learner's states. <bookmark mark='a'/> A person "
            "cannot easily say, after the fact, how they would have steered at every moment of someone else's "
            "drive. <bookmark mark='b'/> So practical versions let the human take over only when the learner goes "
            "wrong, and train on the corrections. <bookmark mark='c'/> When the expert is a program, it is easy, and "
            "the idea is everywhere: Part 27's on-policy distillation, where the teacher grades the student's own "
            "answers, is DAgger for language models. <bookmark mark='d'/> The lesson: learn from where you actually "
            "end up."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.15))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(cards[2], shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(tail))
        self.wait(0.3)
        self.clear_scene()
