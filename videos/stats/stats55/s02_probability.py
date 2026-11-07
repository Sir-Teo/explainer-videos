from __future__ import annotations

import numpy as np

from videos.stats.stats55.common import *  # noqa: F403


class ExamProbability(ExamMixin, VoiceoverScene):
    def construct(self):
        self.card()
        self.p1()
        self.p2()

    def card(self):
        card = chapter_card(1, r"Sitting I: \ probability", r"Problems 1 and 2", lit=(1909, 1939), part=PART)
        with self.voiceover("Sitting one: probability. Two problems, on Borel–Cantelli and on optional stopping."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------------------------------ Problem 1
    def p1(self):
        d = load("bc")
        card = ExamCard(1, r"the maximum of exponentials", r"Part 43", [
            r"Let $X_1, X_2, \dots$ be independent Exponential(1), \ and $M_n = \max_{i \le n} X_i$.",
            r"Prove that $M_n / \log n \to 1$ almost surely.",
            r"(Hint: \ two Borel--Cantelli arguments, \ one for each side.)"], marks=10, color=PROBC)
        self.pose_voiceover(
            "Problem one. Let X one, X two, and so on be independent exponential random variables with mean one, and let M n "
            "be the largest of the first n. Prove that M n divided by log n converges to one, almost surely. The hint: two "
            "Borel–Cantelli arguments, one for each side. Pause the video and try it.", card)
        rows = [
            cmath(r"P(X_n > c\log n)", r"=", r"e^{-c\log n} = n^{-c}", font_size=34),
            cmath(r"c > 1", r":", r"\textstyle\sum_n n^{-c} < \infty \ \Rightarrow \ X_n \le c\log n \text{ eventually, \ a.s.}", font_size=32),
            cmath(r"\text{so}", r":", r"M_n \le \max(M_N, c\log n) \ \Rightarrow \ \limsup M_n/\log n \le c", font_size=32),
            cmath(r"c \downarrow 1", r":", r"\limsup_n M_n/\log n \le 1 \text{ a.s.} \ \ (\text{a countable intersection})", font_size=32),
        ]
        rows[1][-1].set_color(PROBC)
        rows[3][-1].set_color(PROOFC)
        whys = [why(r"the exponential tail"), why(r"the first Borel--Cantelli lemma"), why(r"after the last exceedance $N$"), why(r"$c = 1 + 1/k$, \ $k = 1, 2, \dots$")]
        self.steps_voiceover("<bookmark mark='a'/> The upper side first. The chance that X n exceeds c log n is e to the minus c log n: n "
                   "to the minus c. <bookmark mark='b'/> For c above one these probabilities are summable, so by the first "
                   "Borel–Cantelli lemma, only finitely many X n exceed c log n, almost surely. <bookmark mark='c'/> After the "
                   "last exceedance, at some random N, the maximum is at most the larger of M N and c log n, so the limit "
                   "superior of M n over log n is at most c. <bookmark mark='d'/> Take c equal to one plus one over k, for "
                   "each k: a countable intersection of almost-sure events, so the limit superior is at most one.", rows, whys)
        self.clear_but(card)
        rows = [
            cmath(r"P(M_n \le c\log n)", r"=", r"(1 - n^{-c})^n \le \exp(-n^{1-c})", font_size=34),
            cmath(r"0<c<1", r":", r"\textstyle\sum_n \exp(-n^{1-c}) < \infty \ \Rightarrow \ M_n > c\log n \text{ eventually}", font_size=32),
            cmath(r"\text{so}", r":", r"\liminf_n M_n/\log n \ge 1 \text{ a.s.}, \ \ \text{and } M_n/\log n \to 1", font_size=32),
            cmath(r"\text{note}", r":", r"\text{no independence needed for the upper side; \ the lower side uses it}", font_size=30),
        ]
        rows[2][-1].set_color(PROOFC)
        whys = [why(r"independence: \ $1 - x \le e^{-x}$"), why(r"Borel--Cantelli again"), why(r"$c = 1 - 1/k$"), why(r"which hypothesis is used where")]
        self.steps_voiceover("<bookmark mark='a'/> The lower side. The maximum is at most c log n only if every one of the n variables is, and by independence that has probability one minus n to the minus c, to the n: at most e to the minus n to the one minus c. <bookmark mark='b'/> For c strictly between zero and one, these are summable too, so the first lemma applies again: eventually the maximum exceeds c log n. <bookmark mark='c'/> Letting c rise to one along a sequence, the limit inferior is at least one, and the two sides meet. <bookmark mark='d'/> Notice where independence was used: not at all for the upper bound, which holds for any exponential variables, dependent or not, but essentially for the lower one.", rows, whys)
        self.clear_but(card)
        self.p1_chart(d, card)
        self.p1_bc2(d, card)
        self.solved(card)
        self.wait(0.5)
        self.clear_scene()
        self.map_voiceover("<bookmark mark='a'/> The proof, mapped. A tail bound for one n, <bookmark mark='b'/> summed over n, "
                       "<bookmark mark='c'/> Borel–Cantelli to turn a finite sum into almost-sure eventual behaviour, <bookmark "
                       "mark='d'/> and independence for the other side. Everything here is Part forty-three's.", [(r"the exponential tail \ $n^{-c}$", 43), (r"summable for $c > 1$", 43),
                        (r"Borel--Cantelli: \ finitely many", 43), (r"independence: \ the lower side", 43)], "abcd", color=PROBC)

    def p1_chart(self, d, card):
        n = np.asarray(d["scatter_n"])
        r = np.asarray(d["scatter_r"])
        ymax = max(2.6, float(np.ceil(np.max(r)*10)/10+.1))
        A = axes([0, 10000], [0, ymax], x_length=6.8, y_length=3.4, xlabel=r"$n$", ylabel=r"$X_n / \log n$",
                 xticks=[0, 5000, 10000], yticks=[0, 1, 2], center=CHART)
        ax = A.ax
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.025, color=PROBC, fill_opacity=0.7) for a, b in zip(n, r)])
        l12 = DashedLine(ax.c2p(0, 1.2), ax.c2p(10000, 1.2), color=S.RESID, stroke_width=2)
        l1 = Line(ax.c2p(0, 1.0), ax.c2p(10000, 1.0), color=WHITE, stroke_width=2)
        e = {c: d[f"exc_{c}"] for c in ("2.0", "1.2", "1.0", "0.8")}
        side = fit_rows(VGroup(
            label(r"$X_n/\log n$ for $n \le 10^4$ \ (every 7th point)", font_size=22),
            label(rf"exceedances of $c\log n$ up to $n = 10^6$:", font_size=22, color=GREY_A),
            label(rf"$c = 2$: \ {e['2.0']['count']}; \ \ $c = 1.2$: \ {e['1.2']['count']}, \ last observed at $n = {e['1.2']['last']:,}$", font_size=22, color=S.RESID),
            label(rf"$c = 1$: \ {e['1.0']['count']}; \ \ $c = 0.8$: \ {e['0.8']['count']} \ (and counting)", font_size=22, color=PROBC),
            label(r"summable: \ finitely many; \ not summable: \ infinitely many", font_size=22, color=PROOFC),
        ), 4.6, 0.36, SIDE)
        with self.voiceover(
            f"<bookmark mark='a'/> Here are the ratios X n over log n for the first ten thousand draws. <bookmark mark='b'/> Counting exceedances over a million draws: above two log n, none at all. <bookmark mark='c'/> Above one point two log n, {e['1.2']['count']}, the last at n equal to {e['1.2']['last']:,}: the last observed by this finite horizon. The first lemma does not identify the eventual last exceedance from this simulation. <bookmark mark='d'/> Above log n itself, {e['1.0']['count']}, and above zero point eight log n, {e['0.8']['count']}, still arriving: for c at most one the sum diverges, and by the second Borel–Cantelli lemma, which needs independence, there are infinitely many. <bookmark mark='e'/> The boundary between finitely and infinitely many is exactly where the series stops converging."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated, \ seeded")))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x_) for x_ in dots], lag_ratio=0.002), FadeIn(side[0]), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(side[1]), Create(l1))
            vo.wait_until("c")
            self.play(Create(l12), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_but(card)

    def p1_bc2(self, d, card):
        ns = np.log10(np.asarray(d["ns"], float))
        ymax = max(3., float(np.ceil(np.max(d["ratio"])*10)/10+.1))
        A = axes([0.3, 6], [min(.8, min(d["ratio"])-.05), ymax], x_length=6.8, y_length=3.4, xlabel=r"$n$ \ (log scale)", ylabel=r"$M_n / \log n$",
                 xticks=[1, 2, 3, 4, 5, 6], xfmt=lambda v: f"10^{{{int(v)}}}", yticks=[1, 2, 3], center=CHART)
        ax = A.ax
        c = polyline(ax, ns, d["ratio"], PROBC, 4)
        one = DashedLine(ax.c2p(0.3, 1), ax.c2p(6, 1), color=WHITE, stroke_width=2)
        side = fit_rows(VGroup(
            label(r"the running maximum, \ divided by $\log n$", font_size=22),
            label(rf"{d['ratio'][0]:.2f} at $n = 2$; \ {d['ratio'][-1]:.3f} at $n = 10^6$", font_size=22, color=PROBC),
            label(r"slowly: \ $M_n - \log n$ converges in law (Gumbel)", font_size=22, color=GREY_A),
            label(r"so $M_n/\log n - 1 = O_P(1/\log n)$", font_size=22, color=PROOFC),
        ), 4.6, 0.4, SIDE)
        with self.voiceover(
            f"<bookmark mark='a'/> And the theorem itself: the running maximum divided by log n, on a logarithmic axis. "
            f"<bookmark mark='b'/> It starts at {say(d['ratio'][0], 2)} and is at {say(d['ratio'][-1], 3)} after a million "
            f"draws. <bookmark mark='c'/> Convergence is slow, because M n minus log n does not shrink at all: it converges "
            f"in distribution to the Gumbel law of Part forty-three. <bookmark mark='d'/> So the ratio's error is of order "
            f"one over log n, which explains the crawl."
        ) as vo:
            self.play(FadeIn(A), FadeIn(one))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(c), FadeIn(side[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_but(card)

    # ------------------------------------------------------------------------------------------ Problem 2
    def p2(self):
        d = load("walk")
        card = ExamCard(2, r"optional stopping, \ unbounded", r"Part 44", [
            r"$S_n$ is a simple random walk from 0, \ and $T = \inf\{n: S_n = 1\}$.",
            r"Show $T < \infty$ a.s., \ yet $E S_T = 1 \ne 0 = E S_0$. \ Which hypothesis of optional stopping fails?",
            r"Then stop instead at $-a$ or $b$: \ find $P(S_T = b)$ and $E T$."], marks=10, color=PROBC)
        self.pose_voiceover(
            "Problem two. A simple random walk starts at zero and steps up or down by one with equal chances. Let T be the "
            "first time it reaches one. Show that T is finite almost surely, and yet the expected value of S at T is one, not "
            "zero. Which hypothesis of the optional stopping theorem fails? Then stop the walk instead at minus a or b, and "
            "find the probability of reaching b first, and the expected time. Pause and try it.", card)
        rows = [
            cmath(r"S_{T \wedge n}", r":", r"\text{a martingale} \ \Rightarrow \ E S_{T \wedge n} = 0 \text{ for every } n", font_size=34),
            cmath(r"P(T > 2k - 1)", r"=", r"\tbinom{2k}{k} 4^{-k} \sim 1/\sqrt{\pi k} \to 0: \ \ T < \infty \text{ a.s.}", font_size=32),
            cmath(r"S_T = 1", r"\Rightarrow", r"E S_T = 1 \ne \lim_n E S_{T \wedge n} = 0", font_size=34),
            cmath(r"\text{fails}", r":", r"\{S_{T\wedge n}\} \text{ is not uniformly integrable; \ and } E T = \infty", font_size=32),
        ]
        rows[2][-1].set_color(S.RESID)
        rows[3][-1].set_color(S.RESID)
        whys = [why(r"stopped martingales are martingales"), why(r"the reflection principle"), why(r"the limit and $E$ do not commute"), why(r"Doob's theorem needs one of these")]
        self.steps_voiceover("<bookmark mark='a'/> The walk stopped at T is still a martingale, so its mean at any fixed time n is zero. "
                   "<bookmark mark='b'/> By the reflection principle, the chance that T exceeds two k minus one is two k choose "
                   "k over four to the k, about one over the root of pi k: it tends to zero, so T is finite almost surely. "
                   "<bookmark mark='c'/> At T the walk is at one, so the mean of S T is one. But it is the limit of means "
                   "that are all zero: the limit and the expectation do not commute. <bookmark mark='d'/> Optional stopping "
                   "needs a bounded time, or bounded increments with a finite expected time, or uniform integrability. Here "
                   "the stopped walk is not uniformly integrable, and the expected time is infinite.", rows, whys)
        self.clear_but(card)
        self.p2_paths(d, card)
        self.p2_chart(d, card)
        rows = [
            cmath(r"T = \inf\{n: S_n \in \{-a, b\}\}", r":", r"|S_{T\wedge n}| \le \max(a, b): \ \text{bounded, \ so UI}", font_size=32),
            cmath(r"0 = E S_T", r"=", r"b\,p - a(1 - p) \ \Rightarrow \ p = P(S_T = b) = \frac{a}{a + b}", font_size=34),
            cmath(r"S_n^2 - n", r":", r"\text{a martingale} \ \Rightarrow \ E T = E S_T^2 = b^2 p + a^2(1 - p) = ab", font_size=32),
            cmath(r"a = 3, \ b = 7", r":", rf"p = {d['ruin']['p_b']:.1f}, \ \ E T = {d['ruin']['ET']}", font_size=36),
        ]
        rows[1][-1].set_color(PROOFC)
        rows[2][-1].set_color(PROOFC)
        whys = [why(r"now the theorem applies"), why(r"gambler's ruin"), why(r"Wald's second identity"), why(r"and as $a \to \infty$: \ $p \to 1$, \ $E T \to \infty$")]
        self.steps_voiceover("<bookmark mark='a'/> Now stop at minus a or b instead. The stopped walk never leaves the interval, so it is bounded and uniformly integrable, and optional stopping applies. <bookmark mark='b'/> Zero equals the mean at T: b times p minus a times one minus p, so the chance of reaching b first is a over a plus b. <bookmark mark='c'/> At each bounded time, the squared stopped walk has expectation equal to the truncated stopping time. Bounded convergence on the squared position and monotone convergence on the time then give expected T equal to a times b, without assuming integrability in advance. <bookmark mark='d'/> With a equal to three and b to seven: a chance of three tenths, and twenty-one steps on average. Let a grow, and p tends to one while the expected time blows up: the first problem's walk is the limit, and that is exactly where the theorem stops applying.", rows, whys)
        self.solved(card)
        self.wait(0.5)
        self.clear_scene()
        self.map_voiceover("<bookmark mark='a'/> The proof, mapped. A stopped martingale, <bookmark mark='b'/> the reflection "
                       "principle for the hitting time, <bookmark mark='c'/> uniform integrability, the measure-theoretic "
                       "condition of Part forty-three that decides whether a limit and an expectation commute, <bookmark "
                       "mark='d'/> and the bounded case, where optional stopping gives the gambler's ruin and Wald's identity.", [(r"the stopped walk \ is a martingale", 44), (r"reflection: \ $T < \infty$", 44),
                        (r"no UI: \ $E S_T \ne 0$", 43), (r"bounded: \ ruin and Wald", 44)], "abcd", color=PROBC)

    def p2_paths(self, d, card):
        paths = d["paths"]
        L = max(len(p) for p in paths)
        lo = min(min(p) for p in paths)
        A = axes([0, L], [lo - 2, 4], x_length=6.8, y_length=3.4, xlabel=r"step $n$", ylabel=r"$S_n$",
                 xticks=[0, 100, 200, 300, 400], yticks=[-40, -20, 0], center=CHART)
        ax = A.ax
        cols = [PROBC, S.ACCENT, S.RESID, S.ALT, S.PRIOR]
        lines = VGroup(*[polyline(ax, np.arange(len(p)), p, c, 2.5) for p, c in zip(paths, cols)])
        one = DashedLine(ax.c2p(0, 1), ax.c2p(L, 1), color=WHITE, stroke_width=2)
        ends = [("hit 1" if p[-1] == 1 else "not yet") + f" ({len(p) - 1})" for p in paths]
        side = fit_rows(VGroup(
            label(r"five walks that took a while \ (half stop at step 1)", font_size=22),
            label(rf"steps to reach 1: \ {', '.join(ends[:3])}", font_size=22, color=GREY_A),
            label(rf"{', '.join(ends[3:])}", font_size=22, color=GREY_A),
            label(r"almost-sure hitting; \ rare long negative excursions", font_size=22, color=S.RESID),
        ), 4.6, 0.4, SIDE)
        hit = sorted(len(p) - 1 for p in paths if p[-1] == 1)
        miss = sum(1 for p in paths if p[-1] != 1)
        with self.voiceover(
            f"<bookmark mark='a'/> Five walks, chosen among those that did not reach one quickly; half of all walks stop at the first step. <bookmark mark='b'/> These took {', '.join((str(h) for h in hit[:-1]))} and {hit[-1]} steps, and {miss} had not arrived after four hundred. <bookmark mark='c'/> The hitting time is finite almost surely, but some go very far down first, and those rare, deep excursions carry exactly the missing mean."
        ) as vo:
            self.play(FadeIn(A), FadeIn(one), FadeIn(simulated_tag(r"simulated, \ seeded")))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l) for l in lines], lag_ratio=0.3), FadeIn(side[0]), run_time=4.0)
            vo.wait_until("b")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.clear_but(card)

    def p2_chart(self, d, card):
        lm = np.log10(np.asarray(d["ms"], float))
        A = axes([0, 3.7], [-1.1, 1.1], x_length=6.8, y_length=3.4, xlabel=r"$m$ \ (log scale)", ylabel=r"exact",
                 xticks=[0, 1, 2, 3], xfmt=lambda v: f"{10 ** v:,.0f}", yticks=[-1, 0, 1], center=CHART)
        ax = A.ax
        ch = polyline(ax, lm, d["hit"], PROOFC, 4)
        ct = polyline(ax, lm, d["tail_mean"], S.RESID, 4)
        side = fit_rows(VGroup(
            label(r"by dynamic programming, \ exactly", font_size=22),
            label(rf"green: \ $P(T \le m) \cdot 1$, \ {d['hit'][-1]:.3f} at $m = 4{{,}}001$", font_size=22, color=PROOFC),
            label(rf"red: \ $E[S_m; T > m]$, \ {d['tail_mean'][-1]:.3f}", font_size=22, color=S.RESID),
            label(r"they cancel at every $m$: \ $E S_{T \wedge m} = 0$", font_size=22, color=WHITE),
            label(rf"$E[T \wedge m] = {d['e_min'][-1]:.1f}$, \ growing like $\sqrt{{8m/\pi}}$", font_size=22, color=GREY_A),
        ), 4.6, 0.36, SIDE)
        with self.voiceover(
            f"<bookmark mark='a'/> The bookkeeping, computed exactly by dynamic programming. <bookmark mark='b'/> In green, "
            f"the contribution of walks that have stopped: one times the chance of stopping by time m, {say(d['hit'][-1], 3)} "
            f"by step four thousand. <bookmark mark='c'/> In red, the contribution of the walks still going: their mean "
            f"position times their probability, {say(d['tail_mean'][-1], 3)}. <bookmark mark='d'/> They cancel at every m. "
            f"As m grows, the red mass shrinks in probability but not in mean: it is pushed further and further down, which "
            f"is what failing uniform integrability looks like. <bookmark mark='e'/> And the expected stopping time, "
            f"truncated at m, is already {say(d['e_min'][-1], 1)} and grows like the root of m: E T is infinite."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"exact")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(ch), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(ct), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_but(card)
