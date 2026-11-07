from __future__ import annotations

import numpy as np

from videos.stats.stats35.common import *  # noqa: F403


class Sequential(VoiceoverScene):
    def construct(self):
        self.card()
        self.why_()
        self.peek()
        self.boundaries()
        self.path()
        self.cost()
        self.spending_()
        self.board()
        self.dsmb()

    def card(self):
        card = chapter_card(12, r"Sequential trials", r"Looking early without cheating", lit=(1977, 1979, 1983), part=PART)
        with self.voiceover("Chapter twelve. Sequential trials."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def why_(self):
        rows = fit_rows(VGroup(
            label(r"a trial runs for years; \ patients keep arriving", font_size=26),
            label(r"if the drug clearly works, \ or clearly harms, \ it is unethical to continue", font_size=26, color=TAUC),
            label(r"so data monitoring committees look at the data as it accumulates", font_size=26),
            label(r"but each look is another chance for noise to cross 1.96", font_size=26, color=MISSC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A large trial runs for years, with patients enrolling throughout. <bookmark mark='b'/> If "
            "the drug clearly works, it is unethical to keep giving placebo; if it clearly harms, unethical to keep giving "
            "the drug. <bookmark mark='c'/> So independent data monitoring committees look at the accumulating data at "
            "planned interim analyses. <bookmark mark='d'/> But every look is another chance for random noise to cross the "
            "significance line."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def peek(self):
        d = load("sequential")
        ks = [1, 2, 3, 5, 10, 20]
        v = [d["peek"][str(k)] for k in ks]
        A = axes([0, 6], [0, 0.3], x_length=7.0, y_length=4.2, xlabel=r"number of looks, \ each at $|z| > 1.96$",
                 ylabel=r"false-positive rate", xticks=[], yticks=[0, 0.05, 0.1, 0.2, 0.3], yfmt=lambda x: rf"{100 * x:.0f}\%",
                 center=[-2.2, 0.2, 0])
        ax = A.ax
        bars = bars_at(ax, np.arange(6) + 0.5, v, 0.6, MISSC)
        labs = VGroup(*[label(rf"{k}", font_size=20, color=GREY_A).next_to(ax.c2p(i + 0.5, 0), DOWN, buff=0.15) for i, k in enumerate(ks)])
        nums = VGroup(*[label(rf"{100 * x:.1f}\%", font_size=18, color=MISSC).next_to(b, UP, buff=0.08) for x, b in zip(v, bars)])
        five = DashedLine(ax.c2p(0, 0.05), ax.c2p(6, 0.05), color=BANDC, stroke_width=2)
        side = fit_rows(VGroup(
            label(r"null trials, \ 20,000 each", font_size=22),
            label(r"looks equally spaced", font_size=22, color=GREY_A),
            label(r"Armitage, \ McPherson \& Rowe (1969)", font_size=22, color=GREY_A),
            label(r"looking forever: \ certain rejection", font_size=22, color=MISSC),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> How bad is it? Twenty thousand trials of a drug that does nothing, each tested at the "
            "usual five percent level after every equally spaced batch of patients. <bookmark mark='b'/> With one look, five "
            "percent of them declare success. With two, eight percent; five looks, fourteen; ten, nineteen; twenty, "
            "twenty-four. Peter Armitage and his colleagues published this table in 1969. <bookmark mark='c'/> By the law of "
            "the iterated logarithm, a trial that looks forever is certain eventually to cross: Part 33's forking paths, "
            "unfolding in time."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A), FadeIn(labs), Create(five), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.3), FadeIn(nums), FadeIn(side[2]), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def boundaries(self):
        d = load("sequential")
        K = d["K"]
        A = axes([0.5, 5.5], [0, 5], x_length=7.4, y_length=4.4, xlabel=r"look $k$ (of 5)", ylabel=r"boundary for $|z_k|$",
                 xticks=[1, 2, 3, 4, 5], yticks=[0, 1.96, 2.41, 4.56], yfmt=lambda v: rf"{v:.2f}", center=[-2.0, 0.2, 0])
        ax = A.ax
        ks = np.arange(1, K + 1)
        poc = VGroup(polyline(ax, ks, [d["pocock"]] * K, ESTC, 3), *[Dot(ax.c2p(k, d["pocock"]), radius=0.07, color=ESTC) for k in ks])
        obf = VGroup(polyline(ax, ks, d["obf"], SEQC, 3), *[Dot(ax.c2p(k, b), radius=0.07, color=SEQC) for k, b in zip(ks, d["obf"])])
        fix = DashedLine(ax.c2p(0.5, 1.96), ax.c2p(5.5, 1.96), color=GREY_B, stroke_width=2)
        side = fit_rows(VGroup(
            label(r"dashed: \ 1.96, \ the fixed design's", font_size=22, color=GREY_B),
            label(rf"Pocock (1977): \ {d['pocock']:.2f} at every look", font_size=22, color=ESTC),
            label(rf"O'Brien \& Fleming (1979): \ {d['obf'][0]:.2f} $\to$ {d['obf'][-1]:.2f}", font_size=22, color=SEQC),
            label(r"each keeps the total false-positive rate at 5\%", font_size=22, color=BANDC),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The cure is to raise the bar at each look, so that the chance of ever crossing it, under "
            "the null, is five percent in total. <bookmark mark='b'/> Stuart Pocock proposed in 1977 a constant bar: with "
            "five looks, a z of " + say(d["pocock"], 2) + " at every one. <bookmark mark='c'/> Peter O'Brien and Thomas Fleming "
            "proposed in 1979 a bar that starts very high, " + say(d["obf"][0], 2) + " at the first look, and falls to "
            + say(d["obf"][-1], 2) + " at the last, barely above the fixed design's one point nine six. <bookmark mark='d'/> Both are computed"
            " by numerical integration of a joint normal reference model. The z statistics are Brownian motion "
            "divided by the square root of information; the canonical model is exact here and often asymptotic in "
            "real trials."
        ) as vo:
            self.play(FadeIn(A), Create(fix), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(poc), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(obf), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def path(self):
        d = load("sequential")
        K = d["K"]
        ks = np.arange(1, K + 1)
        A = axes([0.5, 5.5], [-2, 5], x_length=7.4, y_length=4.4, xlabel=r"look $k$", ylabel=r"$z_k$",
                 xticks=[1, 2, 3, 4, 5], yticks=[-2, 0, 2, 4], center=[-2.0, 0.2, 0])
        ax = A.ax
        obf = polyline(ax, ks, d["obf"], SEQC, 2.5)
        stop = next((k for k, (z, b) in enumerate(zip(d["zpath"], d["obf"]), 1) if abs(z) >= b), K)
        zp = d["zpath"][:stop]
        p1 = VGroup(polyline(ax, ks[:stop], zp, Y1C, 3), *[Dot(ax.c2p(k, z), radius=0.07, color=Y1C) for k, z in zip(ks, zp)],
                    Star(n=5, outer_radius=0.16, color=Y1C, fill_opacity=1).move_to(ax.c2p(stop, zp[-1])))
        p0 = VGroup(polyline(ax, ks, d["zpath0"], Y0C, 3), *[Dot(ax.c2p(k, z), radius=0.07, color=Y0C) for k, z in zip(ks, d["zpath0"])])
        side = fit_rows(VGroup(
            label(r"purple: \ the O'Brien--Fleming boundary", font_size=22, color=SEQC),
            label(rf"red: \ a drug that works: \ stops at look {stop}", font_size=22, color=Y1C),
            label(r"blue: \ a drug that does nothing: \ runs to the end", font_size=22, color=Y0C),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Two simulated trials against the O'Brien–Fleming boundary. <bookmark mark='b'/> In red, a "
            "drug with a real effect: its z statistic climbs, and crosses the boundary at look " + str(stop) + ", so the "
            "trial stops early and the drug reaches patients sooner. <bookmark mark='c'/> In blue, a drug that does nothing: "
            "its z statistic wanders, never comes near the high early boundaries, and the trial runs to its planned end."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A), Create(obf))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(p1), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(p0), FadeIn(side[2]))
        self.clear_scene()

    def cost(self):
        d = load("sequential")
        r = d["res"]
        rows = [[r"design", r"false-positive rate", r"power", r"expected information"],
                [r"fixed, \ one look", rf"{100 * r['fixed']['alpha']:.1f}\%", rf"{100 * r['fixed']['power']:.0f}\%", r"100\%"],
                [r"Pocock", rf"{100 * r['pocock']['alpha']:.1f}\%", rf"{100 * r['pocock']['power']:.0f}\%", rf"{100 * r['pocock']['e_info']:.0f}\%"],
                [r"O'Brien--Fleming", rf"{100 * r['obf']['alpha']:.1f}\%", rf"{100 * r['obf']['power']:.0f}\%", rf"{100 * r['obf']['e_info']:.0f}\%"]]
        tab = table_rows(rows, font_size=26, col_buff=0.7, row_buff=0.3, colors=[GREY_A, GREY_B, ESTC, SEQC]).move_to([0, 0.9, 0])
        foot = fit_rows(VGroup(
            label(r"same maximum sample size; \ an effect the fixed design detects 80\% of the time", font_size=24, color=GREY_A),
            label(r"Pocock stops sooner but loses power; \ O'Brien--Fleming keeps nearly all of it", font_size=24, color=SEQC),
        ), 12.4, 0.35, [0, -1.7, 0])
        with self.voiceover(
            "<bookmark mark='a'/> What does looking cost? Take an effect that the fixed design, with one analysis at the end, "
            "detects eighty percent of the time. <bookmark mark='b'/> Pocock's constant bar has power of only "
            + f"{100 * r['pocock']['power']:.0f}" + " percent with the same maximum size, though when the drug works it tends "
            "to stop early, using on average " + f"{100 * r['pocock']['e_info']:.0f}" + " percent of the planned patients. "
            "<bookmark mark='c'/> O'Brien and Fleming's bar keeps almost all the power, " + f"{100 * r['obf']['power']:.0f}"
            + " percent, because it spends almost nothing early, and still stops early often enough to save a fifth of the "
            "patients. That is why it became the standard."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(tab[1]), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(tab[2]))
            vo.wait_until("c")
            self.play(FadeIn(tab[3]), FadeIn(foot[1]))
        self.clear_scene()

    def spending_(self):
        d = load("sequential")
        t = np.asarray(d["spend_t"], float)
        A = axes([0, 1], [0, 0.05], x_length=6.6, y_length=4.2, xlabel=r"information fraction $t$",
                 ylabel=r"$\alpha$ spent by $t$", xticks=[0, 0.5, 1], yticks=[0, 0.025, 0.05], center=[-2.6, 0.2, 0])
        ax = A.ax
        o = curve(ax, t, d["spend_obf"], SEQC, 3.5)
        p = curve(ax, t, d["spend_poc"], ESTC, 3.5)
        rows = [
            cmath(r"\alpha_{OF}(t)", r"=", r"4 - 4\,\Phi\big(z_{1 - \alpha/4} / \sqrt t\big)", font_size=26),
            cmath(r"\alpha_{P}(t)", r"=", r"\alpha \log\big(1 + (e - 1)t\big)", font_size=26),
        ]
        g = VGroup(*[VGroup(*r).arrange(RIGHT, buff=0.15) for r in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([3.9, 0.9, 0])
        g[0].set_color(SEQC)
        g[1].set_color(ESTC)
        if g.width > 5.6:
            g.width = 5.6
        side = label(r"valid information-based timing: \ spend $\alpha(t_k) - \alpha(t_{k-1})$ at each", font_size=22, color=GREY_A).move_to([3.9, -1.4, 0])
        if side.width > 5.6:
            side.width = 5.6
        with self.voiceover(
            "<bookmark mark='a'/> Real committees cannot always look at exactly planned times. Gordon Lan and David "
            "DeMets solved that in 1983 with alpha-spending functions: decide in advance how much of the five percent"
            " may have been spent by each fraction of the information. <bookmark mark='b'/> One spending function "
            "mimics O'Brien and Fleming, spending almost nothing early; <bookmark mark='c'/> another mimics Pocock. "
            "<bookmark mark='d'/> At each look, the boundary is chosen to spend the increment under the canonical "
            "model. Timing must be fixed or depend on information in a way that preserves that null model; "
            "outcome-driven looks are not automatically licensed. For five equal looks the O'Brien–Fleming-type "
            "function gives boundaries of four point eight eight down to two point oh three, close to the original."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("b")
            self.play(Create(o), FadeIn(g[0]))
            vo.wait_until("c")
            self.play(Create(p), FadeIn(g[1]))
            vo.wait_until("d")
            self.play(FadeIn(side))
        self.clear_scene()

    def board(self):
        rows = board_rows("peeking", "Pocock boundary", "O'Brien")
        show_board(self, rows,
                   "<bookmark mark='a'/> On the Board, as false-positive rates, twenty thousand null trials each. Peeking "
                   "five times at one point nine six: broken, fourteen percent. <bookmark mark='b'/> Pocock's and O'Brien "
                   "and Fleming's boundaries: both kept, at five.",
                   [("a", [0]), ("b", [1, 2])])

    def dsmb(self):
        rows = fit_rows(VGroup(
            label(r"stopping for benefit overstates the effect: \ the winner's curse again", font_size=26, color=MISSC),
            label(r"futility boundaries: \ stop when success has become unlikely", font_size=26),
            label(r"the committee weighs safety, \ external evidence, \ and the boundary", font_size=26, color=GREY_A),
            label(r"Part 58: \ e-values and always-valid inference, \ for looking at any time", font_size=26, color=TAUC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Two cautions. A trial stopped early for benefit tends to overstate the effect, because it "
            "stopped at a lucky high point: Part 33's winner's curse, in time. <bookmark mark='b'/> Trials also use "
            "futility boundaries, stopping when success has become unlikely. <bookmark mark='c'/> And a real monitoring "
            "committee weighs safety and outside evidence as well as the boundary. <bookmark mark='d'/> Part 58 goes further, "
            "with e-values and always-valid inference that allow looking at any time, as often as you like."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
