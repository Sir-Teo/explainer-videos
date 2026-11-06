from __future__ import annotations

import numpy as np

from videos.stats.stats58.common import *  # noqa: F403


class CAST(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter seven. A real trial as a betting test: CAST, which was stopped early because its "
                       "drugs were killing patients.", 7, r"CAST as a betting test", r"Evidence that accumulates, death by death",
                       lit=(1989,))
        self.story()
        self.bet()
        self.chart()
        self.compare()
        self.lessons()

    def story(self):
        c = museum.CAST
        self.list_voiceover(
            f"<bookmark mark='a'/> The Cardiac Arrhythmia Suppression Trial. <bookmark mark='b'/> After a heart attack, "
            f"irregular beats predict sudden death, and the drugs encainide and flecainide suppress them. <bookmark "
            f"mark='c'/> The trial randomized "
            f"{c['n']:,} patients whose arrhythmias the drugs had suppressed, to the drug or to placebo. <bookmark mark='d'/> "
            f"Its monitoring board stopped those arms early, in 1989; the final report counted {c['deaths_drug']} deaths "
            f"on the drugs against {c['deaths_placebo']} on placebo. <bookmark mark='e'/> Suppressing the surrogate had not saved lives; it had "
            f"cost them. Part thirty-five told the story of the surrogate. Here we ask how the evidence accumulated.",
            [(r"CAST \ (Echt et al., \ \emph{NEJM} 1991):", GREY_A),
             (r"after a heart attack, \ arrhythmias predict sudden death; \ the drugs suppress them", GREY_A),
             (rf"{c['n']:,} patients whose arrhythmias were suppressed, \ randomized to drug or placebo", SPRTC),
             (rf"stopped early: \ {c['deaths_drug']} deaths on the drugs, \ {c['deaths_placebo']} on placebo", FIXEDC),
             (r"the surrogate improved; \ survival did not \ (Part 35)", WEALTHC)])

    def bet(self):
        d = load("cast")
        self.lad_voiceover(
            f"<bookmark mark='a'/> A betting test needs only the deaths. The arms were nearly equal in size, so under the null "
            f"of no effect each death is equally likely to fall in either arm. <bookmark mark='b'/> A gambler who does not "
            f"know which way the effect goes bets with a mixture: she averages over the unknown share q of deaths in the drug "
            f"arm, uniformly. <bookmark mark='c'/> After s of n deaths have fallen in the drug arm, her wealth is the Beta "
            f"function of s plus one and n minus s plus one, times two to the n: a test martingale under the null. <bookmark "
            f"mark='d'/> With all {d['n']} deaths, {d['s']} in the drug arm, it is {d['final_e']:.0f}.",
            [(r"H_0", r":", r"\text{each death in either arm w.p. } \tfrac12", 38),
             (r"\text{bet}", r":", r"\text{mix over the share } q \sim \mathrm{Uniform}(0, 1)", 38),
             (r"W_n", r"=", r"2^n\,B(s + 1, n - s + 1)", 40),
             (r"\text{at the end}", r":", rf"n = {d['n']}, \ s = {d['s']}: \ W = {d['final_e']:.0f}", 40)],
            [r"equal arms", r"either direction", r"a mixture martingale", r"exact"],
            colors=[(2, WEALTHC), (3, WEALTHC)])

    def chart(self):
        d = load("cast")
        n = d["n"]
        A = axes([0, n + 1], [-1, 4.3], x_length=8.0, y_length=4.4, xlabel=r"deaths so far", ylabel=r"$\log_{10}$ wealth",
                 xticks=[0, 20, 40, 60, 80], yticks=[0, 1.3, 2, 3, 4], center=[-2.0, 0.2, 0])
        x = np.arange(1, n + 1)
        bp = BettingPaths(A.ax, x, d["paths"], ymin=-1, ymax=4.3)
        thr = math.log10(20)
        firsts = VGroup()
        for path in d["paths"]:
            hit = np.flatnonzero(np.asarray(path) >= thr)
            if len(hit):
                firsts.add(Dot(A.ax.c2p(x[hit[0]], path[hit[0]]), radius=0.06, color=FIXEDC))
        side = fit_rows(VGroup(
            label(r"the order of the 89 deaths is not published:", font_size=22),
            label(r"30 orders consistent with the totals, \ drawn at random", font_size=22, color=WEALTHC),
            label(rf"red dots: \ wealth first reaches 20; \ median {d['first_median']:.0f} deaths", font_size=22, color=FIXEDC),
            label(rf"10\% to 90\% of orders: \ {d['first_q10']:.0f} to {d['first_q90']:.0f} deaths", font_size=22, color=GREY_A),
            label(rf"final wealth {d['final_e']:.0f}: \ anytime-valid $p \le {d['p_from_e']:.4f}$", font_size=22, color=CSC),
        ), 4.4, 0.36, [4.6, 0.3, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The order in which the deaths occurred is not in the published record, so we draw orders "
            f"at random, consistent with the totals. <bookmark mark='b'/> Here are thirty, each the wealth of the mixture "
            f"gambler death by death. <bookmark mark='c'/> Wealth first reaches twenty after a median of "
            f"{d['first_median']:.0f} deaths; <bookmark mark='d'/> for most orders, between {d['first_q10']:.0f} and "
            f"{d['first_q90']:.0f}. <bookmark mark='e'/> At the end it is {d['final_e']:.0f}, an anytime-valid p-value below "
            f"{say(d['p_from_e'], 4)}: valid whenever the board had looked, and whatever made it stop."
        ) as vo:
            self.play(FadeIn(A), FadeIn(bp.threshold(0.05)), FadeIn(museum_tag(r"Echt et al., \ \emph{NEJM} (1991); \ orders simulated")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(bp.paths(WEALTHC, 1.6, 0.6)), FadeIn(side[1]), run_time=3.0)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(f, scale=0.5) for f in firsts], lag_ratio=0.08), FadeIn(side[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def compare(self):
        d = load("cast")
        self.lad_voiceover(
            f"<bookmark mark='a'/> Against the classical analysis. The z statistic for {d['s']} of {d['n']} is "
            f"{say(d['z'], 2)}, a fixed-sample p-value of about {d['p_z'] * 1e4:.0f} in ten thousand. <bookmark mark='b'/> The "
            f"betting test's p-value is about {d['p_from_e'] * 1000:.0f} in a thousand: thirty times weaker on paper. "
            f"<bookmark mark='c'/> But the fixed-sample p-value assumes the analysis was planned at exactly {d['n']} deaths, "
            f"and the trial was stopped because the evidence looked strong, which is precisely when fixed-sample p-values "
            f"overstate. <bookmark mark='d'/> The betting test's number needs no plan: it is the evidence, as money, whenever "
            f"anyone looked.",
            [(r"\text{fixed sample}", r":", rf"z = {d['z']:.2f}, \ p \approx {sci(d['p_z'])}", 38),
             (r"\text{betting}", r":", rf"W = {d['final_e']:.0f}, \ p \le {d['p_from_e']:.4f}", 38),
             (r"\text{but}", r":", r"\text{the fixed } p \text{ assumes a planned } n", 38),
             (r"\text{betting}", r":", r"\text{valid at whatever time the board stopped}", 38)],
            [r"Part 10's test", r"anytime-valid", r"stopped because it looked strong", r"no plan needed"],
            colors=[(0, FIXEDC), (1, CSC)])

    def lessons(self):
        self.list_voiceover(
            "<bookmark mark='a'/> What CAST teaches. <bookmark mark='b'/> Evidence of harm arrived early and clearly; an "
            "anytime-valid test would have flagged it, at a pre-set wealth of twenty, after about half the deaths. <bookmark "
            "mark='c'/> Monitoring boards need exactly this: freedom to look whenever, with honest error rates. <bookmark "
            "mark='d'/> And the strongest lesson is Part thirty-five's: the trial was needed at all because a surrogate had "
            "been trusted. No sequential method rescues the wrong endpoint.",
            [(r"what CAST teaches:", GREY_A),
             (r"harm showed early: \ wealth 20 after about half the deaths", FIXEDC),
             (r"boards need to look whenever, \ with honest error rates", CSC),
             (r"no sequential method rescues the wrong endpoint \ (Part 35)", WEALTHC)])
