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
            [r"stop when the evidence suffices", r"SPRT", r"errors $\le \alpha, \beta$; \ optimal $E N$"],
            [r"a few planned looks", r"spending functions", r"exact, \ for normal data"],
            [r"look at any time", r"test martingales, \ Ville", r"size $\le \alpha$, \ any stopping rule"],
            [r"an interval at any time", r"confidence sequences", r"coverage at all $t$ at once"],
            [r"many experiments", r"e-BH", r"FDR $\le \alpha$, \ any dependence"],
            [r"adaptive designs", r"weighted AIPW, \ IPW martingales", r"asymptotic, \ or anytime-valid"],
        ]
        cols = [GREY_B, SPRTC, SPRTC, WEALTHC, CSC, WEALTHC, BANDITC]
        tab = table_rows([hdr] + body, font_size=28, col_buff=0.8, row_buff=0.3, colors=cols).move_to([0, 0.1, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The part in one table. <bookmark mark='b'/> To stop when the evidence suffices, the SPRT, "
            "with controlled errors and the smallest expected sample size. For a few planned looks, spending functions, exact "
            "for normal data. To look at any time, test martingales and Ville's inequality, whatever the stopping rule. For an "
            "interval at any time, confidence sequences, covering at all times at once. For many experiments, e-BH, under any "
            "dependence. And for adaptive designs, weighted AIPW asymptotically, or inverse-propensity martingales at any time."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in tab[1:]], lag_ratio=0.6), run_time=16.0)
        self.wait(1.0)
        self.clear_scene()

    def op_power(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Problem one: power for composite and nonparametric nulls. <bookmark mark='b'/> For simple "
            "nulls the log-optimal e-value is a likelihood ratio, and for nulls with a group invariance, such as the "
            "t-test's, it is known explicitly. <bookmark mark='c'/> For nonparametric nulls, such as symmetry or "
            "independence, there are valid e-processes, but how close they come to the best possible growth is largely "
            "unknown. <bookmark mark='d'/> A theory of efficiency for e-processes, the analogue of Part forty-nine's "
            "semiparametric bounds, is open.",
            [(r"\text{problem 1}", r":", r"\text{power for composite and nonparametric nulls}", 38),
             (r"\text{known}", r":", r"\text{simple nulls; \ group-invariant nulls}", 38),
             (r"\text{but}", r":", r"\text{nonparametric nulls: \ valid, \ efficiency unknown}", 38),
             (r"\text{open}", r":", r"\text{an efficiency theory for e-processes}", 38)],
            [r"how fast can wealth grow?", r"chapters 4--5", r"symmetry, \ independence", r"Part 49's analogue"],
            colors=[(1, CSC), (2, FIXEDC)])

    def op_asymptotic(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Problem two: asymptotic anytime-validity. <bookmark mark='b'/> Exact confidence sequences "
            "need strong assumptions, such as boundedness or a known variance bound. Ian Waudby-Smith and colleagues have "
            "built asymptotic confidence sequences from a time-uniform central limit theory, valid in a large-sample sense "
            "at every time. <bookmark mark='c'/> But what asymptotic anytime-validity should mean, and when it is "
            "trustworthy at the sample sizes used, is still being worked out. <bookmark mark='d'/> The analogue of Part "
            "forty-seven's local asymptotics, for processes rather than fixed n, is open.",
            [(r"\text{problem 2}", r":", r"\text{asymptotic anytime-validity}", 38),
             (r"\text{known}", r":", r"\text{asymptotic CSs from a time-uniform CLT}", 38),
             (r"\text{but}", r":", r"\text{what it should mean; \ when to trust it}", 38),
             (r"\text{open}", r":", r"\text{local asymptotics for processes}", 38)],
            [r"beyond bounded data", r"Waudby-Smith and colleagues", r"definitions matter", r"Part 47's analogue"],
            colors=[(1, CSC)])

    def op_design(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Problem three: designs that serve several goals. <bookmark mark='b'/> Thompson sampling "
            "serves welfare, exploration sampling serves the final choice, balanced designs serve inference. <bookmark "
            "mark='c'/> Some results characterize the trade-off between regret and estimation error, showing that one cannot "
            "have both at their best. <bookmark mark='d'/> But designs that are near-optimal for a stated mixture of goals, "
            "with valid inference built in, and practical for real platforms, are open.",
            [(r"\text{problem 3}", r":", r"\text{designs for several goals at once}", 38),
             (r"\text{goals}", r":", r"\text{welfare, \ choice, \ inference}", 38),
             (r"\text{known}", r":", r"\text{trade-offs: \ not all can be optimal}", 38),
             (r"\text{open}", r":", r"\text{practical designs for a stated mix}", 38)],
            [r"chapter 11's tension", r"three losses", r"Pareto frontiers", r"with valid inference built in"],
            colors=[(3, BANDITC)])

    def op_regulation(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Problem four: from theory to regulation. <bookmark mark='b'/> Regulators accept "
            "group-sequential designs because their properties are known and their plans are filed in advance. <bookmark "
            "mark='c'/> E-processes give stronger guarantees under weaker plans, but the questions a regulator asks, about "
            "estimation after stopping, about power, about how a sponsor might game the bets, have only partial answers. "
            "<bookmark mark='d'/> Estimation after an anytime-valid stop, and standards for reporting e-values, are open "
            "and practical.",
            [(r"\text{problem 4}", r":", r"\text{anytime-valid trials in regulation}", 38),
             (r"\text{today}", r":", r"\text{group-sequential designs, \ filed in advance}", 38),
             (r"\text{questions}", r":", r"\text{estimation after stopping, \ power, \ gaming}", 38),
             (r"\text{open}", r":", r"\text{standards for reporting e-values}", 38)],
            [r"the practical frontier", r"chapter 2", r"what a regulator asks", r"and estimation after a stop"],
            colors=[(3, WEALTHC)])

    def op_delays(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Problem five: real platforms. <bookmark mark='b'/> Outcomes arrive late, a conversion "
            "days after the visit; units interfere, as sellers and buyers in a marketplace do; and the population drifts "
            "with the seasons. <bookmark mark='c'/> Each breaks an assumption of this part: that outcomes arrive before the "
            "next decision, that units are independent, that the target does not move. <bookmark mark='d'/> Anytime-valid "
            "inference for delayed, interfering, nonstationary experiments is largely open, and it is what the platforms "
            "actually run.",
            [(r"\text{problem 5}", r":", r"\text{delays, \ interference, \ drift}", 38),
             (r"\text{e.g.}", r":", r"\text{late conversions, \ marketplaces, \ seasons}", 38),
             (r"\text{breaks}", r":", r"\text{each a standing assumption}", 38),
             (r"\text{open}", r":", r"\text{anytime-valid inference for real platforms}", 38)],
            [r"the real setting", r"Parts 35 and 39", r"of this part", r"what is actually run"],
            colors=[(3, FIXEDC)])

    def problems(self):
        self.list_voiceover(
            "<bookmark mark='a'/> Five open problems. <bookmark mark='b'/> An efficiency theory for e-processes under "
            "composite and nonparametric nulls. <bookmark mark='c'/> A sound notion of asymptotic anytime-validity. "
            "<bookmark mark='d'/> Adaptive designs that serve welfare, choice and inference together. <bookmark mark='e'/> "
            "Standards that let regulators accept anytime-valid trials. <bookmark mark='f'/> And inference for platforms "
            "with delays, interference and drift.",
            [(r"Open problems", S.ACCENT),
             (r"1. \ efficiency for e-processes under composite and nonparametric nulls", WHITE),
             (r"2. \ what asymptotic anytime-validity should mean, \ and when to trust it", WHITE),
             (r"3. \ designs serving welfare, \ choice and inference at once", WHITE),
             (r"4. \ regulatory standards: \ estimation after a stop, \ reporting e-values", WHITE),
             (r"5. \ delays, \ interference and drift on real platforms", WHITE)],
            buff=0.42, font_size=25, head_size=40)
