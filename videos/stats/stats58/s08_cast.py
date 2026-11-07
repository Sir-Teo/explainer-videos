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
        heading = label('A working death-label model', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> The extract gives aggregate deaths, not individual risk sets, follow-up times, or "
            'their sequence. We illustrate a working model in which successive death labels are IID fair coins '
            "under the null. Nearly equal trial arms do not by themselves justify that model. <bookmark mark='b'/> "
            "Mix alternative death-label probabilities uniformly between zero and one. <bookmark mark='c'/> After s "
            'drug labels among n deaths, the mixture likelihood ratio is two to the n times the Beta function of s '
            'plus one and n minus s plus one. It is a test martingale under this working label model. <bookmark '
            "mark='d'/> At the recorded totals, sixty-three of eighty-nine deaths, the terminal wealth is about "
            "three hundred and thirty-three. This does not reconstruct the clinical trial's sequential analysis."
        ),
            [(r"H_0", r":", r"\text{working model: IID fair death labels}", 38),
             (r"\text{bet}", r":", r"\text{mix over the share } q \sim \mathrm{Uniform}(0, 1)", 38),
             (r"W_n", r"=", r"2^n\,B(s + 1, n - s + 1)", 40),
             (r"\text{at the end}", r":", rf"n = {d['n']}, \ s = {d['s']}: \ W = {d['final_e']:.0f}", 40)],
            [r"a working label model", r"either direction", r"a mixture martingale", r"exact"],
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
            label(r"actual order unavailable in this extract:", font_size=22),
            label(r"30 of 2,000 simulated orders conditional on totals", font_size=22, color=WEALTHC),
            label(rf"red dots: \ wealth first reaches 20; \ median {d['first_median']:.0f} deaths", font_size=22, color=FIXEDC),
            label(rf"10\% to 90\% of orders: \ {d['first_q10']:.0f} to {d['first_q90']:.0f} deaths", font_size=22, color=GREY_A),
            label(rf"final wealth {d['final_e']:.0f}: \ anytime-valid $p \le {d['p_from_e']:.4f}$", font_size=22, color=CSC),
        ), 4.4, 0.36, [4.6, 0.3, 0])
        with self.voiceover(
            (
            "<bookmark mark='a'/> The actual death order is unavailable in our extract. We simulate two thousand "
            "orders conditional on the final totals. <bookmark mark='b'/> Thirty are shown; these are illustrative "
            "paths, not recovered patient histories. <bookmark mark='c'/> Across the two thousand simulated orders, "
            "the median first crossing of wealth twenty is forty-five deaths. <bookmark mark='d'/> The tenth to "
            'ninetieth percentiles describe those random permutations only. They do not establish when the actual '
            "monitoring board could have acted. <bookmark mark='e'/> Every ordering ends at the same wealth, about "
            'three hundred and thirty-three. Its reciprocal bounds the anytime p-value under the working fair-label '
            'model; an actual running maximum requires the actual sequence.'
        )
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
        heading = label('Contrasting guarantees', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> A normal approximation to a fixed-size fair-label count gives z about three point "
            "nine two for sixty-three of eighty-nine labels. This is not the original clinical trial's two-arm "
            "analysis. <bookmark mark='b'/> Under the same illustrative label model, terminal mixture wealth is "
            'about three hundred and thirty-three; its reciprocal is about point zero zero three. <bookmark '
            "mark='c'/> The count test is a fixed-n comparison, while a properly specified mixture process permits "
            'monitoring over time. The difference here reflects both construction and monitoring, and is not a '
            "universal loss of power for e-values. <bookmark mark='d'/> A clinical guarantee would need the trial's "
            'randomization, evolving exposures and risk sets. The aggregate totals alone do not supply them.'
        ),
            [(r"\text{fixed sample}", r":", rf"z = {d['z']:.2f}, \ p \approx {sci(d['p_z'])}", 38),
             (r"\text{betting}", r":", rf"W = {d['final_e']:.0f}, \ p \le {d['p_from_e']:.4f}", 38),
             (r"\text{but}", r":", r"\text{the fixed } p \text{ assumes a planned } n", 38),
             (r"\text{betting}", r":", r"\text{anytime under the working label model only}", 38)],
            [r"Part 10's test", r"anytime-valid", r"stopped because it looked strong", r"no plan needed"],
            colors=[(0, FIXEDC), (1, CSC)])

    def lessons(self):
        self.list_voiceover(
            (
            "<bookmark mark='a'/> CAST demonstrates the importance of mortality endpoints and safety monitoring. "
            "<bookmark mark='b'/> The aggregate totals also support an illustrative betting calculation under an "
            'explicit working model, but the simulated paths cannot locate the actual earliest warning. <bookmark '
            "mark='c'/> Monitoring boards need sequential methods matched to the trial's assignment and outcome "
            "processes. <bookmark mark='d'/> The central clinical lesson remains: improvement in a surrogate did "
            'not establish improved survival. A sequential method cannot repair a scientifically inappropriate '
            'endpoint.'
        ),
            [(r"what CAST teaches:", GREY_A),
             (r"illustrative simulated paths cannot date the actual warning", FIXEDC),
             (r"boards need to look whenever, \ with honest error rates", CSC),
             (r"no sequential method rescues the wrong endpoint \ (Part 35)", WEALTHC)])
