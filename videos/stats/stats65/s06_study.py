from __future__ import annotations

import numpy as np

from videos.stats.stats65.common import *  # noqa: F403

MUS = [0.5, 1.0, 1.5]
METHS = ["none", "oracle", "estimated", "tempered", "misspecified"]


def cells():
    return {(x["mu"], x["gamma"], x["method"]): x for x in load("study")["rows"]}


class Study(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter five. The simulation study, written down before it ran.", 5, r"A preregistered study",
                            r"Protocol first, \ results second")
        self.why_pre()
        self.ademp()
        self.mc()
        self.chart()
        self.gap_chart()
        self.widths()
        self.zero()
        self.scorecard()
        self.failure()
        self.limits()

    def why_pre(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Simulation studies are experiments, and they can be run badly in the same ways. "
            "<bookmark mark='b'/> A method's author chooses the settings, and settings that flatter the method are easy to "
            "find after the fact: Part fifty-six's selection, applied to a research design. <bookmark mark='c'/> The "
            "remedy is the clinical trial's: write the protocol down, with the predictions, before running anything. "
            "<bookmark mark='d'/> This study's protocol, with five predictions, was saved in the repository before the main "
            "run; only a fifty-replicate pilot, to check the code, had been seen.",
            [(r"\text{simulations}", r":", r"\text{experiments, \ with the same risks}", 40),
             (r"\text{the risk}", r":", r"\text{flattering settings, \ found afterwards}", 40),
             (r"\text{remedy}", r":", r"\text{protocol and predictions first}", 40),
             (r"\text{here}", r":", r"\texttt{PROTOCOL.md}, \ \text{before the run}", 40)],
            [r"Part 7", r"Part 56", r"preregistration", r"in the repository"],
            colors=[(2, HONC)])

    def ademp(self):
        self.list_voiceover(
            "<bookmark mark='a'/> The protocol follows Tim Morris, Ian White and Michael Crowther's ADEMP, from 2019. "
            "<bookmark mark='b'/> Aims: measure the coverage lost with estimated or wrong weights, and check the bound. "
            "<bookmark mark='c'/> Data: source N of zero and one, target N of mu and one, mu of a half, one, or one and a "
            "half; the outcome sine x plus x over two plus noise whose scale is e to the gamma x, with gamma zero, a half or "
            "one. <bookmark mark='d'/> Estimand: coverage of the target at ninety percent. Methods: no weights, true "
            "weights, logistic estimated weights, tempered weights, and weights from a classifier that sees only the size "
            "of x. <bookmark mark='e'/> Performance: mean coverage with its Monte Carlo error over a thousand replicates "
            "per cell, widths, infinite intervals, and the bound.",
            [(r"ADEMP:", GREY_A),
             (r"Aims: \ the coverage lost; \ is the bound right, \ and tight?", THESISC),
             (r"Data: \ $\mu \in \{0.5, 1, 1.5\}$; \ noise $e^{\gamma x}$, \ $\gamma \in \{0, 0.5, 1\}$", GREY_A),
             (r"Estimand: \ target coverage; \ Methods: \ none, \ true, \ estimated, \ tempered, \ misspecified", GREY_A),
             (r"Performance: \ coverage $\pm$ MC SE, \ 1{,}000 replicates per cell", HONC)],
            buff=0.4, font_size=24, head_size=32)

    def mc(self):
        st = cells()
        se = max(x["mcse"] for x in st.values())
        self.lad_voiceover(
            f"<bookmark mark='a'/> How many replicates? Part seven's rule: decide the Monte Carlo error you can tolerate, "
            f"then the number of runs. <bookmark mark='b'/> The pilot's error, with fifty replicates, was about half a "
            f"point. <bookmark mark='c'/> A thousand replicates bring it to about a tenth of a point; the largest in the "
            f"study was {100 * se:.2f} points. <bookmark mark='d'/> Forty-five cells, forty-five thousand replicates, each "
            f"with five hundred calibration points and two hundred test points. Every seed is fixed.",
            [(r"\text{rule}", r":", r"\text{choose the MC error, \ then } R", 40),
             (r"\text{pilot}", r":", r"R = 50, \ \ \mathrm{MCSE} \approx 0.005", 40),
             (r"\text{main}", r":", rf"R = 1{{,}}000, \ \ \max \mathrm{{MCSE}} = {se:.4f}", 40),
             (r"\text{size}", r":", r"45 \text{ cells} \times 1{,}000", 40)],
            [r"Part 7", r"to check the code", r"precise enough", r"reproducible"],
            colors=[(2, HONC)])

    def chart(self):
        st = cells()
        g = 1.0
        A = axes([0.35, 1.65], [0.3, 0.95], x_length=7.0, y_length=4.4, xlabel=r"shift $\mu$ (target $N(\mu, 1)$)",
                 ylabel=r"target coverage, \ $\gamma = 1$", xticks=MUS, yticks=[0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], yfmt=lambda v: f"{100 * v:.0f}\\%",
                 center=[-2.5, 0.2, 0])
        ax = A.ax
        nom = DashedLine(ax.c2p(0.35, 0.9), ax.c2p(1.65, 0.9), color=GREY_B, stroke_width=2)
        lines, bounds = {}, {}
        for m in METHS:
            ys = [st[(mu, g, m)]["coverage"] for mu in MUS]
            lines[m] = VGroup(polyline(ax, MUS, ys, METHC[m], 3.5), *[Dot(ax.c2p(a, b), radius=0.07, color=METHC[m]) for a, b in zip(MUS, ys)])
            bs = [st[(mu, g, m)]["bound"] for mu in MUS]
            bounds[m] = DashedVMobject(polyline(ax, MUS, bs, METHC[m], 2.0, 0.8), num_dashes=16)
        n15 = st[(1.5, g, "none")]["coverage"]
        side = side_groups([
            [(rf"red: \ no weights, \ {100 * n15:.0f}\% at $\mu = 1.5$", NAIVEC)],
            [(r"green and blue: \ true and estimated", HONC), (r"weights, \ at or above 90\%", ESTC)],
            [(r"gold and teal: \ tempered and", WRONGC), (r"misspecified weights", METHC["misspecified"])],
            [(r"dashes: \ each method's bound;", WHITE), (r"every curve stays above its own", WHITE)],
        ])
        with self.voiceover(
            f"<bookmark mark='a'/> The results, for the strongest dependence of the noise on x, gamma of one. <bookmark "
            f"mark='b'/> Without weights, coverage falls as the shift grows, to {100 * n15:.0f} percent at mu of one and a "
            f"half. <bookmark mark='c'/> With true or estimated weights, coverage is at or above ninety percent everywhere. "
            f"<bookmark mark='d'/> Tempered and misspecified weights lose part of the coverage. <bookmark mark='e'/> And the "
            f"dashed lines are each method's bound from the theorem, computed exactly from its own weights. Every curve stays "
            f"above its own bound, as it must, and well above it."
        ) as vo:
            self.play(FadeIn(A), Create(nom), FadeIn(seeded_tag()))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(Create(lines["none"][0]), FadeIn(VGroup(*lines["none"][1:])), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(*[Create(lines[m][0]) for m in ("oracle", "estimated")], *[FadeIn(VGroup(*lines[m][1:])) for m in ("oracle", "estimated")], FadeIn(side[1]))
            vo.wait_until("d")
            self.play(*[Create(lines[m][0]) for m in ("tempered", "misspecified")], *[FadeIn(VGroup(*lines[m][1:])) for m in ("tempered", "misspecified")], FadeIn(side[2]))
            vo.wait_until("e")
            self.play(*[Create(bounds[m]) for m in ("none", "tempered", "misspecified")], FadeIn(side[3]))
        self.wait(1.0)
        self.clear_scene()

    def gap_chart(self):
        st = cells()
        gams = [0.0, 0.5, 1.0]
        A = axes([-0.1, 1.1], [0, 0.45], x_length=7.0, y_length=4.4, xlabel=r"how strongly the noise depends on $x$, \ $\gamma$",
                 ylabel=r"coverage minus the bound, \ $\mu = 1$", xticks=gams, yticks=[0, 0.1, 0.2, 0.3, 0.4], center=[-2.5, 0.2, 0])
        ax = A.ax
        ls = {}
        for m in ("none", "tempered", "misspecified"):
            ys = [st[(1.0, gm, m)]["coverage"] - st[(1.0, gm, m)]["bound"] for gm in gams]
            ls[m] = (VGroup(polyline(ax, gams, ys, METHC[m], 3.5), *[Dot(ax.c2p(a, b), radius=0.07, color=METHC[m]) for a, b in zip(gams, ys)]), ys)
        side = side_groups([
            [(r"the slack in the bound,", WHITE), (r"for the three imperfect methods", WHITE)],
            [(rf"no weights: \ {ls['none'][1][0]:.2f} at $\gamma = 0$, \ {ls['none'][1][2]:.2f} at $\gamma = 1$", NAIVEC)],
            [(rf"tempered: \ {ls['tempered'][1][0]:.2f} to {ls['tempered'][1][2]:.2f}", WRONGC),
             (rf"misspecified: \ {ls['misspecified'][1][0]:.2f} to {ls['misspecified'][1][2]:.2f}", METHC["misspecified"])],
            [(r"tightest at $\gamma = 1$, \ never tight", HONC)],
        ])
        with self.voiceover(
            f"<bookmark mark='a'/> How loose is the bound? The slack, coverage minus bound, at a shift of one, against "
            f"gamma. <bookmark mark='b'/> For no weights, the slack falls from {ls['none'][1][0]:.2f} when the noise ignores x "
            f"to {ls['none'][1][2]:.2f} when it depends strongly on x. <bookmark mark='c'/> The tempered and misspecified "
            f"weights show the same pattern. <bookmark mark='d'/> So the bound is tightest exactly where chapter three "
            f"predicted, and never tight: even at gamma of one it leaves more than ten points of slack. It is a safe "
            f"guarantee, and a pessimistic estimate."
        ) as vo:
            self.play(FadeIn(A), FadeIn(seeded_tag()))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(ls["none"][0][0]), FadeIn(VGroup(*ls["none"][0][1:])), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(*[Create(ls[m][0][0]) for m in ("tempered", "misspecified")], *[FadeIn(VGroup(*ls[m][0][1:])) for m in ("tempered", "misspecified")], FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.wait(1.0)
        self.clear_scene()

    def scorecard(self):
        st = cells()
        e15 = st[(1.5, 1.0, "estimated")]["coverage"]
        self.list_voiceover(
            f"<bookmark mark='a'/> The predictions, scored. <bookmark mark='b'/> One: no weights under-cover, more as the "
            f"shift and gamma grow, and cover ninety percent when gamma is zero. Held. <bookmark mark='c'/> Two: true weights "
            f"within three Monte Carlo errors of ninety percent, or above. Held. <bookmark mark='d'/> Three: estimated weights "
            f"within one point of ninety percent in every cell. Failed: at mu of one and a half they cover up to "
            f"{100 * e15:.1f} percent. <bookmark mark='e'/> Four: tempered and misspecified weights under-cover but stay above "
            f"the bound. Held. <bookmark mark='f'/> Five: the bound is loosest at gamma zero and tightest at gamma one. Held.",
            [(r"the predictions, \ scored:", GREY_A),
             (r"P1 \ no weights fail with shift and $\gamma$; \ fine at $\gamma = 0$: \ held", HONC),
             (r"P2 \ true weights at or above 90\%: \ held", HONC),
             (rf"P3 \ estimated within a point of 90\%: \ failed, \ up to {100 * e15:.1f}\%", NAIVEC),
             (r"P4 \ wrong weights above the bound: \ held", HONC),
             (r"P5 \ bound tightest at $\gamma = 1$: \ held", HONC)],
            buff=0.38, font_size=24, head_size=32)

    def failure(self):
        st = cells()
        inf = st[(1.5, 1.0, "estimated")]["inf"]
        self.lad_voiceover(
            f"<bookmark mark='a'/> Why prediction three failed. <bookmark mark='b'/> At the largest shift, some test points "
            f"lie where the source has almost no data, and their weight is huge. <bookmark mark='c'/> Then the test point's "
            f"own weight, placed at infinity, outweighs the whole calibration set, and the interval is infinite: "
            f"{100 * inf:.1f} percent of intervals, against none without weights. <bookmark mark='d'/> Infinite intervals "
            f"always cover, so coverage rises above ninety percent. The failure is in the safe direction, but it is a real "
            f"cost: an interval of infinite width tells a user nothing. That is worth reporting, and it was not predicted.",
            [(r"\text{large shift}", r":", r"\text{test points where the source is thin}", 40),
             (r"\text{huge weight}", r":", r"\text{the test point outweighs the calibration set}", 40),
             (r"\text{infinite intervals}", r":", rf"{100 * inf:.1f}\% \ \text{{at }} \mu = 1.5", 40),
             (r"\text{so}", r":", r"\text{over-coverage: \ safe, \ but uninformative}", 40)],
            [r"overlap", r"Part 36's extreme weights", r"the mechanism", r"reported, \ not hidden"],
            colors=[(2, NAIVEC)])

    def widths(self):
        st = cells()
        A = axes([0.35, 1.65], [0, 28], x_length=7.0, y_length=4.4, xlabel=r"shift $\mu$", ylabel=r"median interval width, \ $\gamma = 1$",
                 xticks=MUS, yticks=[0, 5, 10, 15, 20, 25], center=[-2.5, 0.2, 0])
        ax = A.ax
        ls = VGroup()
        for m in METHS:
            ys = [st[(mu, 1.0, m)]["width"] for mu in MUS]
            ls.add(VGroup(polyline(ax, MUS, ys, METHC[m], 3.5), *[Dot(ax.c2p(a, b), radius=0.07, color=METHC[m]) for a, b in zip(MUS, ys)]))
        o15, n15 = st[(1.5, 1.0, "oracle")]["width"], st[(1.5, 1.0, "none")]["width"]
        side = side_groups([
            [(r"the price of coverage", WHITE)],
            [(rf"red: \ no weights, \ {n15:.1f} wide at $\mu = 1.5$", NAIVEC), (r"narrow, \ and wrong", NAIVEC)],
            [(rf"green, \ blue: \ {o15:.1f} wide", HONC), (r"the target's noise is larger", HONC)],
            [(r"gold, \ teal: \ in between", WRONGC)],
        ])
        with self.voiceover(
            f"<bookmark mark='a'/> The price of the coverage, in width. <bookmark mark='b'/> Without weights the interval "
            f"stays about {n15:.0f} units wide whatever the shift: it is calibrated to the source, where the noise is small. "
            f"<bookmark mark='c'/> With correct weights it widens to about {o15:.0f} at the largest shift, because the target "
            f"lives where exp of x makes the noise large. Correct intervals are wide when the truth is uncertain. <bookmark "
            f"mark='d'/> Wrong weights land in between, in coverage and in width. No method beats the trade: honest coverage "
            f"costs exactly the width the target's noise requires."
        ) as vo:
            self.play(FadeIn(A), FadeIn(seeded_tag()))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(ls[0][0]), FadeIn(VGroup(*ls[0][1:])), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(*[Create(ls[k][0]) for k in (1, 2)], *[FadeIn(VGroup(*ls[k][1:])) for k in (1, 2)], FadeIn(side[2]))
            vo.wait_until("d")
            self.play(*[Create(ls[k][0]) for k in (3, 4)], *[FadeIn(VGroup(*ls[k][1:])) for k in (3, 4)], FadeIn(side[3]))
        self.wait(1.0)
        self.clear_scene()

    def zero(self):
        st = cells()
        c = [st[(mu, 0.0, "none")]["coverage"] for mu in MUS]
        b = [st[(mu, 0.0, "none")]["bound"] for mu in MUS]
        self.lad_voiceover(
            f"<bookmark mark='a'/> The cells with gamma of zero deserve their own look. <bookmark mark='b'/> There the "
            f"noise does not depend on x, so the scores are exchangeable between source and target whatever the shift. "
            f"<bookmark mark='c'/> Unweighted conformal covers {100 * c[0]:.1f}, {100 * c[1]:.1f} and {100 * c[2]:.1f} percent "
            f"at the three shifts, exactly as Part fifty-seven promises for exchangeable data. <bookmark mark='d'/> But the "
            f"theorem's bound for it falls to {100 * b[2]:.0f} percent at the largest shift. It is a bound that cannot see the "
            f"scores. A sharper theorem would measure the distance between the score distributions, not the covariates.",
            [(r"\gamma = 0", r":", r"\text{scores } \perp X", 40),
             (r"\text{so}", r":", r"\text{exchangeable under any shift}", 40),
             (r"\text{no weights}", r":", rf"{100 * c[0]:.1f}\%, \ {100 * c[1]:.1f}\%, \ {100 * c[2]:.1f}\%", 40),
             (r"\text{bound}", r":", rf"\text{{down to }} {100 * b[2]:.0f}\%: \ \text{{blind to the scores}}", 40)],
            [r"a control", r"Part 57", r"exact", r"the next theorem"],
            colors=[(2, HONC), (3, NAIVEC)])

    def limits(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> What the study did not vary, stated as limitations. <bookmark mark='b'/> One covariate. "
            "In many dimensions, density-ratio estimation is far harder, and the classifier's errors far larger: Part "
            "fifty-two's curse. <bookmark mark='c'/> One calibration size, five hundred. Smaller sets make the weighted "
            "quantile noisier and infinite intervals more common. <bookmark mark='d'/> And the true mean function as the "
            "model, which isolates the conformal step but hides how a fitted model's errors interact with the shift. Each is "
            "a natural next study, and the protocol's code makes each a small change.",
            [(r"\text{dimension}", r":", r"\text{one covariate only}", 40),
             (r"\text{calibration size}", r":", r"n = 500 \ \text{only}", 40),
             (r"\text{the model}", r":", r"\text{the true mean, \ not a fit}", 40),
             (r"\text{next}", r":", r"\text{small changes to the protocol}", 40)],
            [r"Part 52", r"noisier quantiles", r"isolation", r"future work"],
            colors=[(0, NAIVEC)])
