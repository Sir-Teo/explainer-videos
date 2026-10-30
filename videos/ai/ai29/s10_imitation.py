from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai29.common import AGENT, EXPERT, FAIL, GOOD, HIST, OBS, PART, load, spread_band
from videos.ai.ai29.lanes import LaneView, table_strip

BC = C.MODEL_Q


class Imitation(VoiceoverScene):
    def construct(self):
        self.card()
        self.define()
        self.lane()
        self.drift()
        self.derive()
        self.measured()

    def card(self):
        card = chapter_card(9, r"Learning by imitation", r"Why does copying an expert go wrong?", lit=(), part=PART)
        with self.voiceover("Chapter nine. Learning by imitation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def define(self):
        hist = history_card(1989, r"ALVINN \ (Dean Pomerleau, Carnegie Mellon)", r"a network with one hidden layer "
                            r"watches the road through a $30 \times 32$ camera image and copies the steering of a "
                            r"human driver", width=6.2, color=HIST, font_size=25).move_to([-3.4, 1.6, 0])
        card = definition_card(r"Behaviour cloning", r"collect the expert's observations and actions; \ fit a policy to "
                               r"them by supervised learning: \ $\hat\pi = \arg\min_\pi \ \mathbb E_{s \sim d_{\pi^*}}"
                               r"\big[\ell(\pi(s), \pi^*(s))\big]$", width=6.4, color=BC, font_size=27).move_to([3.4, 1.6, 0])
        note_ = label(r"$d_{\pi^*}$: \ the states the expert visits", font_size=28, color=EXPERT).move_to([3.4, -0.5, 0])
        use = label(r"how every robot policy of chapter 15 starts: \ demonstrations, \ then supervised learning",
                    font_size=28, color=GREY_A).to_edge(DOWN, buff=0.7)
        catch = label(r"the catch: \ the learner is tested on the states \emph{it} visits", font_size=32,
                      color=FAIL).next_to(use, UP, buff=0.45)
        with self.voiceover(
            "The simplest way to teach an agent is to show it. <bookmark mark='a'/> In 1989 Dean Pomerleau's ALVINN "
            "watched the road through a small camera and learned to steer a van by copying a human driver. "
            "<bookmark mark='b'/> This is behaviour cloning: record what the expert saw and what it did, and fit a "
            "policy by ordinary supervised learning. <bookmark mark='c'/> The average is over the states the expert "
            "visits. <bookmark mark='d'/> It is how robot policies start to this day. <bookmark mark='e'/> But there "
            "is a catch. Once the learner drives, it visits its own states, not the expert's, and a small mistake "
            "takes it somewhere the expert never went."
        ) as vo:
            self.play(FadeIn(hist, shift=UP * 0.15))
            vo.wait_until("b")
            self.play(FadeIn(card, shift=UP * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(note_))
            vo.wait_until("d")
            self.play(FadeIn(use))
            vo.wait_until("e")
            self.play(FadeIn(catch))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lane(self):
        L = load("lane")
        P = L["params"]
        D = int(P["D"])
        ex = np.asarray(L["drives_expert"])
        view = LaneView(D, ex.shape[1] - 1, cell=0.3, height=5.2, center=[-2.7, 0.2, 0])
        wind = view.wind()
        wl = label(r"wind", font_size=20, color=GREY_B).next_to(wind, UP, buff=0.1)
        drives = VGroup(*[view.drive(d, EXPERT, 2) for d in ex])
        tl = label(r"time $\to$", font_size=20, color=GREY_A).rotate(PI / 2).next_to(view, LEFT, buff=1.2)
        rules = VGroup(
            label(rf"each step: \ steer left, \ straight, \ or right; \\ the wind pushes right ${100 * P['wind']:.0f}\%$ "
                  r"of the time", font_size=26),
            label(r"cost: \ $1$ for every step off the lane", font_size=26, color=FAIL),
            label(r"the expert knows where the car is, \\ and steers back", font_size=26, color=EXPERT),
            label(rf"the learner sees a camera reading, \\ one cell off ${100 * P['noise']:.0f}\%$ of the time", font_size=26,
                  color=OBS),
        )
        for r_ in rules:
            if r_.width > 5.6:
                r_.width = 5.6
        rules.arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([3.8, 0.6, 0])
        Je = float(np.asarray(L["J_expert"])[-1])
        stays = "never leaves the lane" if Je < 1e-9 else f"leaves it only {Je:.1f} steps in {int(L['T'])}"
        tag = note(r"a lane of $21$ cells; \ the three in the middle are the road", font_size=18).to_corner(DR, buff=0.3)
        with self.voiceover(
            "Here is a small driving task we can solve exactly. <bookmark mark='a'/> A car drives up a lane, and each "
            "step it can steer left, go straight, or steer right, while a wind keeps pushing it to the right. "
            "<bookmark mark='b'/> Every step off the lane costs one. <bookmark mark='c'/> The expert knows exactly "
            f"where the car is and steers back, so it {stays}. Here are twelve of its drives. "
            "<bookmark mark='d'/> The learner sees the road through a camera that is sometimes one cell off. That "
            "noise is what makes even a perfect copy make occasional mistakes."
        ) as vo:
            self.play(FadeIn(view), FadeIn(tl), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rules[0]), FadeIn(wind), FadeIn(wl))
            vo.wait_until("b")
            self.play(FadeIn(rules[1]))
            vo.wait_until("c")
            self.play(FadeIn(rules[2]), LaggedStart(*[Create(d_) for d_ in drives], lag_ratio=0.1), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(rules[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def drift(self):
        L = load("lane")
        D = int(L["params"]["D"])
        bc = np.asarray(L["drives_bc"])
        T = bc.shape[1] - 1
        view = LaneView(D, T, cell=0.3, height=5.0, center=[-3.2, 0.4, 0])
        hist = np.asarray(L["bc_hist"])
        S = 2 * D + 1
        tab, seen = hist[-1][:S], hist[-1][S:]
        strip = table_strip(view, tab, seen, color=BC)
        sl = label(r"the cloned policy, \ reading by reading \\ (grey: \ never shown)", font_size=24, color=BC)
        sl.next_to(strip, DOWN, buff=0.15)
        drives = VGroup(*[view.drive(d, BC, 2) for d in bc])
        lost = [k for k, d in enumerate(bc) if abs(d[-1]) >= 2]
        n_seen = int(seen.sum())
        right = label(rf"$\ {int(L['N'])}$ expert labels, \ {int(L['N']) // int(L['params']['demo_len'])} drives; "
                      rf"\\ readings seen: \ ${n_seen}$ of ${S}$", font_size=27, color=GREY_A).move_to([3.4, 2.3, 0])
        why_ = VGroup(label(r"the expert never leaves the lane, \\ so its drives never show \\ what to do off it",
                            font_size=27, color=EXPERT),
                      label(r"off the lane, \ the learner's \\ actions are arbitrary: \\ it drifts, \ or sits at the "
                            r"verge", font_size=27, color=FAIL)).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        why_.move_to([3.4, 0.0, 0])
        eps = float(np.mean(L["bc_eps"]))
        with self.voiceover(
            "Behaviour cloning: give the learner the expert's drives, and for each camera reading it copies the "
            f"expert's most common action. <bookmark mark='a'/> It only ever saw {n_seen} of the {S} possible "
            "readings, the ones near the middle of the road, because those are the only places the expert goes. "
            "<bookmark mark='b'/> Now let it drive. Most of the time it copies well: on the expert's own states it "
            f"chooses differently only {100 * eps:.1f} percent of the time. <bookmark mark='c'/> But one gust at the "
            "wrong moment, a misread camera, and it is off the lane, in readings it never saw, "
            f"<bookmark mark='d'/> and there it has no idea what to do. Of these twelve drives, {len(lost)} end off "
            "the lane."
        ) as vo:
            self.play(FadeIn(view), FadeIn(right))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(a_) for a_ in strip], lag_ratio=0.05), FadeIn(sl))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(d_) for d_ in drives], lag_ratio=0.15), run_time=4.0)
            vo.wait_until("c")
            self.play(FadeIn(why_[0]), *[drives[k].animate.set_stroke(FAIL, width=3) for k in lost])
            vo.wait_until("d")
            self.play(FadeIn(why_[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        rows = [
            cmath(r"\varepsilon", r"=", r"\tfrac1T \sum_t \Pr_{s \sim d_t^{\pi^*}}\big[\hat\pi(s) \ne \pi^*(s)\big]", font_size=32),
            cmath(r"\Pr[\text{no mistake in steps } 1..t]", r"\ge", r"1 - \textstyle\sum_{k \le t} \varepsilon_k", font_size=32),
            cmath(r"\mathbb E[c_t(\hat\pi)]", r"\le", r"\mathbb E[c_t(\pi^*)] + \Pr[\text{a mistake by } t]", font_size=32),
            cmath(r"J(\hat\pi)", r"\le", r"J(\pi^*) + \textstyle\sum_{t=1}^{T} \sum_{k \le t} \varepsilon_k", font_size=32),
            cmath(r"J(\hat\pi)", r"\le", r"J(\pi^*) + T^2 \varepsilon", font_size=36),
        ]
        rows[4][2].set_color(FAIL)
        whys = [why(r"the learner's error rate, \ on the expert's states"), why(r"union bound"),
                why(r"until the first mistake, \ it is where the expert would be; \ after, \ cost $\le 1$ a step"),
                why(r"sum over the $T$ steps"), why(r"each inner sum $\le T\varepsilon$")]
        step = ladder(self, rows, whys, keep=5, top=3.1, x=-2.6, buff=0.42, edge=6.9)
        thm = label(r"Ross \& Bagnell (2010): \ and there are tasks where it is this bad", font_size=24,
                    color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "How bad can this get? Let epsilon be the learner's error rate, measured on the states the expert "
            "visits: exactly what supervised learning makes small. <bookmark mark='a'/> The chance it has made no "
            "mistake in the first t steps is at least one minus the sum of the error rates so far: a union bound. "
            "<bookmark mark='b'/> Until its first mistake, the learner is exactly where the expert would be. After "
            "it, the worst it can do is pay the full cost every step. <bookmark mark='c'/> Add that up over a task "
            "of T steps. <bookmark mark='d'/> Each inner sum is at most T epsilon, so the extra cost is at most T "
            "squared epsilon. Stéphane Ross and Drew Bagnell proved this in 2010, and showed tasks where it is "
            "reached: twice the horizon, four times the extra cost."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            step(4)
            self.play(FadeIn(thm))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def measured(self):
        L = load("lane")
        T = int(L["T"])
        J = np.asarray(L["bc_J"])
        ts = np.arange(1, T + 1)
        eps = float(np.mean(L["bc_eps"]))
        ymax = float(J.max()) * 1.05
        g = axes([0, T, 100], [0, ymax, 100], x_length=6.6, y_length=4.4, xlabel=r"horizon $T$ \ (steps)",
                 ylabel=r"expected steps off the lane, \ $J(T)$", xticks=[0, 100, 200, 300, 400],
                 yticks=[v for v in (0, 100, 200, 300) if v <= ymax], center=[-2.6, -0.4, 0])
        ax = g.ax
        bcl = spread_band(ax, ts, J, BC)
        bound = curve(ax, ts[ts * ts * eps <= ymax], (ts * ts * eps)[ts * ts * eps <= ymax], FAIL, 2.5)
        bl = label(r"$T^2\varepsilon$", font_size=26, color=FAIL).next_to(bound.get_end(), RIGHT, buff=0.1)
        lin = DashedLine(ax.c2p(0, 0), ax.c2p(T, T * eps), color=GREY_B)
        ll = label(r"$T\varepsilon$", font_size=24, color=GREY_B).next_to(ax.c2p(T, T * eps), UP, buff=0.1)
        # the chance of being off the lane at step t: it climbs
        per = np.diff(np.concatenate([np.zeros((J.shape[0], 1)), J], 1), axis=1)
        g2 = axes([0, T, 100], [0, 1, 0.5], x_length=4.0, y_length=2.2, xlabel=r"step $t$",
                  ylabel=r"P(off the lane at step $t$)", xticks=[0, 200, 400], yticks=[0, 0.5, 1], font_size=18,
                  center=[4.3, 1.4, 0])
        perl = spread_band(g2.ax, ts, per, BC)
        s1, s2 = float(L["bc_slope_early"]), float(L["bc_slope_late"])
        stats = VGroup(label(rf"measured $\varepsilon = {eps:.3f}$", font_size=27, color=BC),
                       label(rf"log-log slope: \\ ${s1:.2f}$ (steps $10$--$60$), \\ ${s2:.2f}$ (steps $200$--$400$)", font_size=24,
                             color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.3, -1.5, 0])
        tag = note(rf"exact expectations, \ 8 seeds: \ band min--max, \ line the mean; \ the expert: \ $0$",
                   font_size=18).to_corner(DR, buff=0.25)
        grows = per.mean(0)[-1] > 2 * per.mean(0)[20]
        if s1 > 1.15 or s2 > 1.15:
            shape = ("It bends upward: the cost grows faster than the horizon, "
                     f"with a slope of {max(s1, s2):.1f} on log-log axes, where linear growth would give one.")
        else:
            shape = "It grows about in proportion to the horizon here, slower than the bound allows."
        climb = ("The reason is on the right: the chance of being off the lane keeps climbing step after step, "
                 "because a learner that leaves the lane rarely comes back." if grows else
                 "The chance of being off the lane levels off early here.")
        with self.voiceover(
            "Here is our learner's expected cost, computed exactly, for every horizon up to four hundred steps, "
            "over eight seeds. <bookmark mark='a'/> " + shape + " <bookmark mark='b'/> The bound, T squared "
            f"epsilon, with the measured epsilon of {eps:.3f}, is far above it: it is a worst case. If errors "
            "simply added up, the cost would follow T epsilon. <bookmark mark='c'/> " + climb
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag), FadeIn(stats[0]))
            self.play(FadeIn(bcl[0]), Create(bcl[1]), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(stats[1]))
            vo.wait_until("b")
            self.play(Create(bound), FadeIn(bl), Create(lin), FadeIn(ll))
            vo.wait_until("c")
            self.play(FadeIn(g2), FadeIn(perl[0]), Create(perl[1]), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()
