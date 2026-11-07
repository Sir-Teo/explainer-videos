from __future__ import annotations

from videos.stats.stats58.common import *  # noqa: F403


class EBH(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter nine. Multiple testing with e-values: false discovery rate control under any "
                       "dependence, and for experiments that each stop when they like.", 9, r"Multiple testing with e-values",
                       r"Many bets at once", lit=(2022,))
        self.rule()
        self.proof()
        self.results()
        self.why_use()
        self.closure()
        self.platform()

    def rule(self):
        heading = label('e-BH for a specified family', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> Ruodu Wang and Aaditya Ramdas's e-BH procedure. Given e-values for m hypotheses, "
            "sort them from largest to smallest. <bookmark mark='b'/> Find the largest k for which the k-th largest "
            "e-value is at least m over alpha k. <bookmark mark='c'/> Reject those k hypotheses. <bookmark "
            "mark='d'/> It is Benjamini–Hochberg applied to one over the e-values, and it controls the false "
            'discovery rate at alpha under any dependence whatever, with no correction factor.'
        ),
            [(r"e_{(1)} \ge \dots \ge e_{(m)}", r":", r"\text{sorted}", 40),
             (r"k^*", r"=", r"\max(\{k: e_{(k)} \ge m/(\alpha k)\}\cup\{0\})", 40),
             (r"\text{reject}", r":", r"\text{the } k^* \text{ largest}", 40),
             (r"\mathrm{FDR}", r"\le", r"\alpha \text{ under any dependence}", 40)],
            [r"Wang \& Ramdas (2022)", r"BH on $1/e$", r"the discoveries", r"no $\log m$ penalty"],
            colors=[(1, WEALTHC), (3, CSC)])

    def proof(self):
        heading = label('The error-control proof', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> The proof is three lines. A null hypothesis i is rejected only if its e-value is "
            "at least m over alpha times the number of rejections R. <bookmark mark='b'/> So its contribution to "
            'the false discovery proportion, one over R if rejected, is at most alpha e i over m. <bookmark '
            "mark='c'/> Take expectations: each null's e-value has mean at most one. <bookmark mark='d'/> Summing "
            'over the nulls gives at most alpha times the number of nulls over m, below alpha. Dependence never '
            'entered: only linearity of expectation.'
        ),
            [(r"i \text{ rejected}", r"\Rightarrow", r"e_i \ge m/(\alpha R)", 40),
             (r"\frac{1\{i \text{ rejected}\}}{R \vee 1}", r"\le", r"\frac{\alpha\,e_i}{m}", 40),
             (r"E[\cdot]", r"\le", r"\alpha/m \text{ for each null}", 40),
             (r"\mathrm{FDR}", r"\le", r"\alpha\,m_0/m \le \alpha \qquad \blacksquare", 40)],
            [r"the rule", r"a pointwise bound", r"each $E[e_i] \le 1$", r"linearity only"],
            colors=[(3, CSC)])

    def results(self):
        d = load("ebh")
        hdr = [r"procedure", r"input", r"FDR", r"power"]
        body = [[r"BH", r"$p$-values", f"{100 * d['bh']['fdr']:.1f}\\%", f"{100 * d['bh']['power']:.0f}\\%"],
                [r"e-BH", r"likelihood-ratio e-values", f"{100 * d['ebh']['fdr']:.1f}\\%", f"{100 * d['ebh']['power']:.0f}\\%"]]
        tab = table_rows([hdr] + body, font_size=30, col_buff=1.0, row_buff=0.35, colors=[GREY_B, FIXEDC, WEALTHC]).move_to([0, 0.8, 0])
        foot = fit_rows(VGroup(
            label(rf"{d['m']} metrics, \ {d['k']} real effects of 3 SD, \ equicorrelation {d['rho']}, \ $q = {d['q']}$; \ 4{{,}}000 runs", font_size=24, color=GREY_A),
            label(r"both control the FDR; \ e-BH is conservative, \ and pays in power", font_size=26, color=WEALTHC),
            label(r"BH's guarantee needs positive dependence (PRDS); \ e-BH needs valid null e-values; \ no dependence restriction", font_size=26, color=CSC),
        ), 12.4, 0.25, [0, -1.9, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The two procedures on a simulated platform with {d['m']} correlated metrics, {d['k']} of them with real effects. <bookmark mark='b'/> Benjamini–Hochberg on p-values: false discovery rate {100 * d['bh']['fdr']:.1f} percent, power {100 * d['bh']['power']:.0f} percent. e-BH on likelihood-ratio e-values: {100 * d['ebh']['fdr']:.1f} percent and {100 * d['ebh']['power']:.0f} percent. <bookmark mark='c'/> Both control the rate; e-BH is far more conservative, and pays in power. <bookmark mark='d'/> Here one-sided Gaussian p-values satisfy PRDS, so BH is valid. E-BH allows arbitrary dependence, provided every null input remains a valid e-value for the actual experiment and stopping information."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("a")
            self.play(FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(tab[1]), FadeIn(tab[2]))
            vo.wait_until("c")
            self.play(FadeIn(foot[1]))
            vo.wait_until("d")
            self.play(FadeIn(foot[2]))
        self.clear_scene()

    def why_use(self):
        heading = label('Stopped e-values and dependence', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> So when is e-BH the right tool? When the e-values come from sequential tests: "
            'each experiment on a platform runs its own test martingale and stops on its own schedule. <bookmark '
            "mark='b'/> For stops allowed by each process's filtration, stopped wealth is an e-value. Fix the "
            "family and combine those valid inputs by e-BH. <bookmark mark='c'/> When the dependence is unknown and "
            'possibly negative, where BH would need the Benjamini–Yekutieli factor, about log m. <bookmark '
            "mark='d'/> And when the e-values are not independent of the selection, as with Part fifty-six's "
            'derandomized knockoffs, built by averaging e-values from many knockoff draws.'
        ),
            [(r"\text{sequential tests}", r":", r"\text{each experiment stops on its own schedule}", 38),
             (r"\text{stopped wealth}", r":", r"\text{an e-value: \ combine by e-BH}", 38),
             (r"\text{unknown dependence}", r":", r"\text{BH needs } \textstyle\sum_{i \le m} 1/i \approx \log m", 38),
             (r"\text{derandomized knockoffs}", r":", r"\text{average the e-values of many draws}", 38)],
            [r"anytime-valid platforms", r"chapter 3", r"Benjamini \& Yekutieli (2001)", r"Ren \& Barber (2024)"],
            colors=[(1, WEALTHC), (3, CSC)])

    def closure(self):
        heading = label('The e-closure principle', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> Recent work develops an e-value closure principle for false discovery rate "
            "control. The merged paper is by Xu, Solari, Fischer, de Heide, Ramdas and Goeman. <bookmark mark='b'/> "
            'Its constructions associate e-values with intersections and use them to permit rejection sets, '
            "extending the scope of closed testing. <bookmark mark='c'/> A closed e-BH construction contains the "
            'ordinary e-BH rejection set with the same FDR guarantee, and can add discoveries for some inputs. '
            "<bookmark mark='d'/> The paper also gives uniform improvements of Benjamini-Yekutieli. These are "
            'specific constructions with their own assumptions and computation, not a license to enlarge any '
            'rejection set arbitrarily.'
        ),
            [(r"\text{closure for the FDR}", r":", r"\text{e-values for every intersection}", 38),
             (r"\text{keep}", r":", r"\text{rejection sets the intersections permit}", 38),
             (r"\text{closed e-BH}", r":", r"\supseteq \text{e-BH, \ same guarantee}", 38),
             (r"\text{also}", r":", r"\text{Benjamini--Yekutieli is inadmissible}", 38)],
            [r"Xu, \ Solari, \ Fischer, \ de Heide, \ Ramdas \& Goeman; \ arXiv:2509.02517", r"Part 33's closure", r"uniformly better", r"a corollary"],
            colors=[(2, CSC)])

    def platform(self):
        self.list_voiceover(
            (
            "<bookmark mark='a'/> A valid platform pipeline must define the hypothesis family and the information "
            "available for stopping. <bookmark mark='b'/> An experiment can use a confidence sequence in its valid "
            "filtration. <bookmark mark='c'/> Its stopped e-process value is an e-value only for a stopping rule "
            'allowed by that filtration. If other experiments influence stopping, joint-filtration validity needs '
            "justification. <bookmark mark='d'/> Apply e-BH once to the specified family of valid e-values; "
            "arbitrary dependence is allowed. <bookmark mark='e'/> Do not substitute running maxima for e-values, "
            'select only successful finished experiments and redefine the family size, or repeatedly report the '
            'last significant e-BH set without an additional theorem.'
        ),
            [(r"a platform, \ end to end:", GREY_A),
             (r"each experiment: \ a confidence sequence, \ watched at will", CSC),
             (r"each stopped experiment: \ an e-value", WEALTHC),
             (r"across experiments: \ e-BH, \ FDR under any dependence", WEALTHC),
             (r"stopping filtration and hypothesis-family selection still matter", SPRTC)])
