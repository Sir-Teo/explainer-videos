from __future__ import annotations

from videos.stats.stats58.common import *  # noqa: F403


class OpenProblems(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter fourteen. Open problems in anytime-valid inference and adaptive experiments.", 14,
                       r"Open problems", r"Where the theory is still being written")
        self.map_()
        self.op_power()
        self.op_asymptotic()
        self.op_design()
        self.op_regulation()
        self.op_delays()
        self.problems()

    def map_(self):
        hdr = [r"question", r"tool", r"guarantee"]
        body = [
            [r"stop when the evidence suffices", r"SPRT", r"calibrated actual errors; \ optimal $E_0N,E_1N$"],
            [r"a few planned looks", r"spending functions", r"known-variance Gaussian joint law, \ valid timing"],
            [r"look at any time", r"test martingales, \ Ville", r"size $\le \alpha$, \ any stopping rule"],
            [r"an interval at any time", r"confidence sequences", r"coverage at all $t$ at once"],
            [r"many experiments", r"e-BH", r"FDR $\le \alpha$, \ any dependence"],
            [r"adaptive designs", r"weighted AIPW, \ IPW martingales", r"asymptotic, \ or anytime-valid"],
        ]
        cols = [GREY_B, SPRTC, SPRTC, WEALTHC, CSC, WEALTHC, BANDITC]
        tab = table_rows([hdr] + body, font_size=28, col_buff=0.8, row_buff=0.3, colors=cols).move_to([0, 0.1, 0])
        with self.voiceover(
            (
            "<bookmark mark='a'/> The part in one table. <bookmark mark='b'/> To stop when the evidence suffices, "
            'the SPRT, with calibrated actual errors and optimal expected sample size at its two simple hypotheses. '
            'For a few planned looks, spending functions, exact in the known-variance Gaussian model with valid '
            "timing. To look at any time, test martingales and Ville's inequality, whatever the stopping rule. For "
            'an interval at any time, confidence sequences, covering at all times at once. For many experiments, '
            'e-BH, under any dependence. And for adaptive designs, weighted AIPW asymptotically, or '
            'inverse-propensity martingales at any time.'
        )
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in tab[1:]], lag_ratio=0.6), run_time=16.0)
        self.wait(1.0)
        self.clear_scene()

    def op_power(self):
        heading = label('A specified efficiency question', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> A research direction is efficiency for broad composite and nonparametric nulls. "
            "<bookmark mark='b'/> Simple-null likelihood ratios and some invariant problems have log-growth "
            'optimality results, with their stated alternatives and filtrations. A group symmetry alone is not a '
            "universal solution. <bookmark mark='c'/> Valid processes for symmetry and independence are available, "
            'as are several efficiency results. What remains problem dependent is how closely practical '
            "constructions approach a specified optimality benchmark. <bookmark mark='d'/> A useful project should "
            'identify its model, alternatives and loss, then establish a precise gap. It should not claim that the '
            'entire efficiency theory is missing.'
        ),
            [(r"\text{problem 1}", r":", r"\text{power for composite and nonparametric nulls}", 38),
             (r"\text{known}", r":", r"\text{simple nulls; \ group-invariant nulls}", 38),
             (r"\text{but}", r":", r"\text{nonparametric nulls: \ problem-specific efficiency questions}", 38),
             (r"\text{open}", r":", r"\text{an efficiency theory for e-processes}", 38)],
            [r"how fast can wealth grow?", r"chapters 4--5", r"symmetry, \ independence", r"Part 49's analogue"],
            colors=[(1, CSC), (2, FIXEDC)])

    def op_asymptotic(self):
        heading = label('Finite-sample accuracy of asymptotic inference', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> Another direction is understanding finite-sample reliability of asymptotic "
            "anytime-valid inference. <bookmark mark='b'/> Waudby-Smith and colleagues give formal definitions and "
            'constructions of asymptotic confidence sequences using time-uniform approximation. Exact sequences can '
            "also rely on parametric or conditional-moment assumptions, not only boundedness. <bookmark mark='c'/> "
            'Existing theory does not by itself quantify the accuracy for every realistic sample size, dependence '
            "pattern or estimated nuisance parameter. <bookmark mark='d'/> A concrete open project can study "
            'approximation rates or diagnostics in a specified model. Definitions and an entire process asymptotic '
            'theory are not simply absent.'
        ),
            [(r"\text{problem 2}", r":", r"\text{asymptotic anytime-validity}", 38),
             (r"\text{known}", r":", r"\text{asymptotic CSs from a time-uniform CLT}", 38),
             (r"\text{but}", r":", r"\text{finite-sample accuracy of formal asymptotic definitions}", 38),
             (r"\text{open}", r":", r"\text{accuracy and rates in specified process models}", 38)],
            [r"beyond bounded data", r"Waudby-Smith and colleagues", r"definitions matter", r"Part 47's analogue"],
            colors=[(1, CSC)])

    def op_design(self):
        heading = label('A stated mixture of design objectives', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> Problem three: designs that serve several goals. <bookmark mark='b'/> Thompson "
            'sampling serves welfare, exploration sampling serves the final choice, balanced designs serve '
            "inference. <bookmark mark='c'/> Some results characterize the trade-off between regret and estimation "
            "error, showing that one cannot have both at their best. <bookmark mark='d'/> But designs that are "
            'near-optimal for a stated mixture of goals, with valid inference built in, and practical for real '
            'platforms, are open.'
        ),
            [(r"\text{problem 3}", r":", r"\text{designs for several goals at once}", 38),
             (r"\text{goals}", r":", r"\text{welfare, \ choice, \ inference}", 38),
             (r"\text{known}", r":", r"\text{trade-offs: \ not all can be optimal}", 38),
             (r"\text{open}", r":", r"\text{practical designs for a stated mix}", 38)],
            [r"chapter 11's tension", r"three losses", r"Pareto frontiers", r"with valid inference built in"],
            colors=[(3, BANDITC)])

    def op_regulation(self):
        heading = label('Reporting and regulatory standards', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> Problem four: from theory to regulation. <bookmark mark='b'/> Regulators accept "
            'group-sequential designs because their properties are known and their plans are filed in advance. '
            "<bookmark mark='c'/> E-processes give stronger guarantees under weaker plans, but the questions a "
            'regulator asks, about estimation after stopping, about power, about how a sponsor might game the bets, '
            "have only partial answers. <bookmark mark='d'/> Estimation after an anytime-valid stop, and standards "
            'for reporting e-values, are open and practical.'
        ),
            [(r"\text{problem 4}", r":", r"\text{anytime-valid trials in regulation}", 38),
             (r"\text{today}", r":", r"\text{group-sequential designs, \ filed in advance}", 38),
             (r"\text{questions}", r":", r"\text{estimation after stopping, \ power, \ gaming}", 38),
             (r"\text{open}", r":", r"\text{standards for reporting e-values}", 38)],
            [r"the practical frontier", r"chapter 2", r"what a regulator asks", r"and estimation after a stop"],
            colors=[(3, WEALTHC)])

    def op_delays(self):
        heading = label('Delays, interference and changing targets', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> Practical extensions include delayed outcomes, interference and changing "
            "populations. <bookmark mark='b'/> A delayed conversion may arrive after the next assignment; "
            "interference changes the response model; drift can change the estimand. <bookmark mark='c'/> These "
            'require revisiting the filtration and conditional means. Delay alone need not invalidate a martingale '
            'if only revealed information is used, and existing methods address several such settings. <bookmark '
            "mark='d'/> The research challenge is a useful guarantee for a specified combination of these features, "
            'rather than a claim that anytime-valid inference for real platforms is wholly undeveloped.'
        ),
            [(r"\text{problem 5}", r":", r"\text{delays, \ interference, \ drift}", 38),
             (r"\text{e.g.}", r":", r"\text{late conversions, \ marketplaces, \ seasons}", 38),
             (r"\text{breaks}", r":", r"\text{revisit the response model and filtration}", 38),
             (r"\text{open}", r":", r"\text{anytime-valid inference for real platforms}", 38)],
            [r"the real setting", r"Parts 35 and 39", r"of this part", r"what is actually run"],
            colors=[(3, FIXEDC)])

    def problems(self):
        self.list_voiceover(
            (
            "<bookmark mark='a'/> Five open problems. <bookmark mark='b'/> An efficiency theory for e-processes "
            "under composite and nonparametric nulls. <bookmark mark='c'/> Finite-sample accuracy of asymptotic "
            "anytime-validity. <bookmark mark='d'/> Adaptive designs that serve welfare, choice and inference "
            "together. <bookmark mark='e'/> Standards that let regulators accept anytime-valid trials. <bookmark "
            "mark='f'/> And inference for platforms with delays, interference and drift."
        ),
            [(r"Open problems", S.ACCENT),
             (r"1. \ efficiency for e-processes under composite and nonparametric nulls", WHITE),
             (r"2. \ when asymptotic anytime-validity is accurate at practical sample sizes", WHITE),
             (r"3. \ designs serving welfare, \ choice and inference at once", WHITE),
             (r"4. \ regulatory standards: \ estimation after a stop, \ reporting e-values", WHITE),
             (r"5. \ delays, \ interference and drift on real platforms", WHITE)],
            buff=0.42, font_size=25, head_size=40)
