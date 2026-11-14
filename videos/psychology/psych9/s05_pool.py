from __future__ import annotations

import numpy as np

from videos.psychology.psych9.common import *  # noqa: F403


class PoolTest(VoiceoverScene):
    def construct(self):
        self.card()
        self.recover()
        self.one_study()
        self.violate()
        self.checks()

    def card(self):
        card = chapter_card(4, r"On the Pool: when the design is right, and when it is wrong",
                            r"Does the formula give back what was planted?", lit=(), part=PART, scale=("group",),
                            marr=("how",))
        with self.voiceover(
            "Chapter four. On the Pool: when the design is right, and when it is wrong."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def recover(self):
        d = load("recover")
        head = heading(r"The twin study, run 2{,}000 times at each size")
        sizes = [50, 200, 1000]
        idx = {int(n): i for i, n in enumerate(d["sizes"])}
        top = max(float(d[f"hist_{n}"].max()) for n in sizes)
        panels = VGroup()
        for k, n in enumerate(sizes):
            A = axes([-0.6, 1.6], [0, top * 1.05], x_length=6.4, y_length=1.5, xticks=[0, 0.5, 1.0] if k == 2 else [],
                     yticks=[], xfmt=lambda v: f"{v:.1f}", xlabel=r"the heritability the study reports" if k == 2 else r"",
                     ylabel=r"", center=[-3.2, 1.75 - 1.85 * k, 0])
            h = hist(A.ax, d["edges"], d[f"hist_{n}"], MODEL)
            truth = DashedLine(A.ax.c2p(0.5, 0), A.ax.c2p(0.5, top), color=WHITE, stroke_width=2)
            lab = label(rf"{n:,} pairs".replace(",", "{,}"), font_size=28, color=MODEL).next_to(
                A.ax.c2p(-0.6, top), DR, buff=0.08)
            panels.add(VGroup(A, h, truth, lab))
        i50, i1000 = idx[50], idx[1000]
        rows = rows_of([
            (rf"50 pairs of each kind: \ 95\% of studies report between ${d['lo'][i50]:.2f}$ and ${d['hi'][i50]:.2f}$; \ "
             rf"{pct(d['impossible'][i50])} report something impossible", BAD),
            (rf"1{{,}}000 pairs: \ between ${d['lo'][i1000]:.2f}$ and ${d['hi'][i1000]:.2f}$", MODEL),
            (r"right on average at every size (the dashed line is the truth, 0.5)", WHITE),
            (r"the formula doubles a difference of two correlations, \ so precision comes slowly", P.ACCENT),
        ], 5.6, 29, 0.28).move_to([3.95, -0.4, 0])
        keep_in_frame(rows)
        tag = simulated_tag(r"simulated: the Pool's twin registry")
        with self.voiceover(
            "First, the good news. On the Pool we know the answer, so we can run the twin study two "
            "thousand times and see what it reports. <bookmark mark='a'/> With fifty pairs of each kind, "
            "the estimates are all over the place. Ninety-five percent of the studies report something "
            f"between {d['lo'][i50]:.2f} and {d['hi'][i50]:.2f}, and {100 * d['impossible'][i50]:.0f} "
            "percent report a heritability that's impossible: below zero, or above one. "
            "<bookmark mark='b'/> Two hundred pairs of each: better. <bookmark mark='c'/> A thousand of "
            f"each: between {d['lo'][i1000]:.2f} and {d['hi'][i1000]:.2f}. <bookmark mark='d'/> At every "
            "size the estimate is right on average. What a bigger sample buys is precision, and because "
            "the formula doubles a difference between two correlations, it buys it slowly. To pin a "
            "heritability to within a tenth, a twin study needs thousands of pairs."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(panels[0][0]), FadeIn(panels[0][2]), FadeIn(panels[0][3]))
            vo.wait_until("a")
            self.play(FadeIn(panels[0][1]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(panels[1]))
            vo.wait_until("c")
            self.play(FadeIn(panels[2]), FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]))
        self.clear_scene()

    def one_study(self):
        d = load("recover")
        head = heading(r"One study, \ fitted the modern way")
        truth = [d["a2"], d["c2"], d["e2"]]
        names = [(r"genes", GENE, "a2"), (r"shared home", HOME, "c2"), (r"everything else", OWN, "e2")]
        A = axes([0, 0.8], [0, 3.4], x_length=7.2, y_length=3.6, xticks=[0, 0.2, 0.4, 0.6, 0.8], yticks=[],
                 xfmt=lambda v: f"{v:.1f}", xlabel=r"share of the variance", ylabel=r"", center=[-2.6, -0.4, 0])
        ax = A.ax
        marks = VGroup()
        for k, (name, col, key) in enumerate(names):
            y = 2.8 - 1.1 * k
            lo, hi, est = float(d["fit_lo"][k]), float(d["fit_hi"][k]), float(d[f"fit_{key}"])
            whisk = Line(ax.c2p(lo, y), ax.c2p(hi, y), color=col, stroke_width=5)
            ends = VGroup(*[Line(ax.c2p(v, y - 0.14), ax.c2p(v, y + 0.14), color=col, stroke_width=4) for v in (lo, hi)])
            dot = Dot(ax.c2p(est, y), radius=0.11, color=col)
            tr = Line(ax.c2p(truth[k], y - 0.3), ax.c2p(truth[k], y + 0.3), color=WHITE, stroke_width=3)
            lab = label(rf"{name}: \ ${est:.2f}$", font_size=29, color=col).next_to(ax.c2p(hi, y), RIGHT, buff=0.25)
            marks.add(VGroup(whisk, ends, dot, lab, tr))
        rows = rows_of([
            (rf"a study of 1{{,}}000 pairs of each kind, \ picked by rule: \ the middle one of 101", WHITE),
            (rf"the napkin formula: \ ${d['one_h2']:.2f}$ for genes", GREY_A),
            (r"maximum likelihood fits the diagram: \ it uses all the data, \ keeps every share between 0 and 1, \ "
             r"and gives intervals", P.ACCENT),
            (r"white ticks: \ the truth. \ It is inside every interval", WHITE),
        ], 4.6, 29, 0.28).move_to([4.6, -0.3, 0])
        keep_in_frame(rows)
        tag = simulated_tag(r"simulated: the Pool's twin registry; \ 95\% intervals by bootstrap")
        with self.voiceover(
            "Here's one study of a thousand pairs of each kind, picked by rule: of a hundred and one such "
            f"studies, the one with the middle estimate. <bookmark mark='a'/> The napkin formula gives "
            f"{d['one_h2']:.2f} for the genes. <bookmark mark='b'/> Modern studies don't use the napkin. "
            "They fit the path diagram by maximum likelihood, which uses all of the data, keeps every "
            "share between zero and one, and gives an interval for each. The fit: genes "
            f"{d['fit_a2']:.2f}, somewhere between {d['fit_lo'][0]:.2f} and {d['fit_hi'][0]:.2f}. Shared "
            f"home, {d['fit_c2']:.2f}. Everything else, {d['fit_e2']:.2f}. <bookmark mark='c'/> The truth "
            "is inside every interval. <bookmark mark='d'/> So when its assumptions hold, the design "
            "works. Now for the assumptions. There are four, and on the Pool each one can be switched off."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(*m[:4])) for m in marks], lag_ratio=0.5), FadeIn(rows[2]), run_time=3.0)
            vo.wait_until("c")
            self.play(*[Create(m[4]) for m in marks], FadeIn(rows[3]))
            vo.wait_until("d")
            self.wait(0.5)
        self.clear_scene()

    def violate(self):
        d = load("violate")
        head = heading(r"Four assumptions, \ switched off one at a time")
        short = [r"as assumed", r"identical twins treated more alike", r"like marries like", r"genes that do not just add",
                 r"parents' genes shape the home"]
        A = axes([-0.3, 1.0], [0, 5.2], x_length=6.6, y_length=4.9, xticks=[0, 0.5, 1.0], yticks=[],
                 xfmt=lambda v: f"{v:.1f}", xlabel=r"what the twin formula reports", ylabel=r"", center=[2.9, -0.45, 0])
        ax = A.ax
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(0, 5.2), color=GREY_D, stroke_width=2)
        unit = abs(ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0])
        groups, names = VGroup(), VGroup()
        for k in range(5):
            y = 4.6 - 1.0 * k
            g = VGroup()
            for off, val, truth, col in ((0.17, d["est_h2"][k], d["truth_genes"][k], GENE), (-0.17, d["est_c2"][k], d["truth_home"][k], HOME)):
                w = max(abs(float(val)) * unit, 0.01)
                bar = Rectangle(width=w, height=0.27, stroke_width=0, fill_color=col, fill_opacity=0.9)
                bar.move_to(ax.c2p(float(val) / 2, y + off))
                tick = Line(ax.c2p(float(truth), y + off - 0.19), ax.c2p(float(truth), y + off + 0.19), color=WHITE, stroke_width=3)
                num = label(rf"${val:.2f}$", font_size=25, color=col).next_to(ax.c2p(max(float(val), float(truth)), y + off), RIGHT,
                                                                            buff=0.12)
                g.add(VGroup(bar, tick, num))
            groups.add(g)
            names.add(wrapped_label(short[k], 4.6, 29, WHITE if k else GREY_A).move_to([-3.75, ax.c2p(0, y)[1], 0]))
        keep_in_frame(names)
        lg = legend([(GENE, r"genes"), (HOME, r"shared home"), (WHITE, r"the truth (white ticks)")], font_size=26)
        lg.arrange(RIGHT, buff=0.5).next_to(head, DOWN, buff=0.22)
        tag = simulated_tag(r"simulated: 150{,}000 pairs of each kind in each case")
        with self.voiceover(
            "With everything as assumed, the formula gives back what we planted. <bookmark mark='a'/> One. "
            "Equal environments. The formula assumes identical twins share their surroundings no more "
            "than fraternal twins do. If identical twins are treated more alike, dressed alike, mistaken "
            f"for each other, that extra likeness is counted as genes. The formula reports {d['est_h2'][1]:.2f} "
            f"when the truth is {d['truth_genes'][1]:.2f}. <bookmark mark='b'/> Two. Random mating. In "
            "fact people tend to marry people like themselves. Then fraternal twins share more than half "
            "of the genes that matter, the two kinds of twin look more similar than they should, and the "
            f"formula undercounts the genes and overcounts the home. <bookmark mark='c'/> Three. Genes "
            "that simply add. If some genes work only in combination, identical twins, who share every "
            f"combination, are far more alike than fraternal twins. The formula reports {d['est_h2'][3]:.2f} "
            f"for genes, when the truth is {d['truth_genes'][3]:.2f}, and {abs(d['est_c2'][3]):.2f} below zero for "
            "the home. A negative share is the "
            "design telling you that its model is wrong. <bookmark mark='d'/> Four. Genes independent of "
            "the home. If parents' genes shape the home they make, by the books on the shelf, say, that "
            f"part of the genes' influence is counted as home. The home's share goes from "
            f"{d['est_c2'][0]:.2f} to {d['est_c2'][4]:.2f}. <bookmark mark='e'/> So the errors don't all push "
            "the same way. Two of them inflate the genes' share, and two inflate the home's. A real twin "
            "study has some of each, and nobody knows exactly how much."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(zero), FadeIn(lg), FadeIn(names[0]), FadeIn(groups[0]))
            for k, mark_ in enumerate("abcd", start=1):
                vo.wait_until(mark_)
                self.play(FadeIn(names[k], shift=RIGHT * 0.15), FadeIn(groups[k]))
            vo.wait_until("e")
            self.wait(0.5)
        self.clear_scene()

    def checks(self):
        d = load("violate")
        head = heading(r"So use several designs, \ with different weak points")
        items = [
            (r"adoptive brothers and sisters", r"a home, and no genes in common: \ their correlation is the shared home's "
                                               r"share", d["adopt_adoptive_siblings"], HOME),
            (r"a parent and the child they did not raise", r"genes, and no home: \ half the heritability",
             d["adopt_parent_child_apart"], GENE),
            (r"identical twins raised apart", r"all the genes, and no home: \ the heritability itself",
             d["adopt_mz_apart"], MZC),
        ]
        rows = VGroup()
        for i, (name, what, val, col) in enumerate(items):
            y = 1.75 - 1.3 * i
            left = VGroup(label(name, font_size=33, color=col), wrapped_label(what, 8.6, 29, WHITE)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.1)
            left.move_to([0, y, 0]).align_to(np.array([-6.5, 0, 0]), LEFT)
            rows.add(VGroup(left, label(rf"${r2(val)}$", font_size=48, color=col).move_to([4.7, y, 0])))
        weak = wrapped_label(rf"its weak point: \ if agencies place twins in similar homes, \ the answer is too high. \ "
                             rf"With homes half alike: \ ${r2(d['placed_mz_apart'])}$ instead of "
                             rf"${r2(d['adopt_mz_apart'])}$", 12.4, 30, BAD).move_to([0, -2.1, 0])
        end = wrapped_label(r"When the designs agree, the number has earned some trust. \ When they disagree, the "
                            r"disagreement is the finding.", 12.4, 30, P.ACCENT).next_to(weak, DOWN, buff=0.2)
        tag = simulated_tag(r"simulated: the Pool, 200{,}000 families in each design")
        with self.voiceover(
            "No single design is safe. So the field uses several, with different weak points, and looks "
            "for agreement. <bookmark mark='a'/> Adoptive brothers and sisters share a home and no genes. "
            "Their correlation is the shared home's share, directly. On the Pool: "
            f"{d['adopt_adoptive_siblings']:.2f}. <bookmark mark='b'/> A parent and the child they didn't "
            f"raise share genes and no home. That gives half the heritability: "
            f"{d['adopt_parent_child_apart']:.2f}. <bookmark mark='c'/> And identical twins raised apart, "
            f"the design the two Jims began. Their correlation is the heritability itself: "
            f"{d['adopt_mz_apart']:.2f}. <bookmark mark='d'/> That design has its own weak point. If the "
            "two homes are alike, because agencies place children with similar families, the answer comes "
            f"out too high. With homes half alike, it's {d['placed_mz_apart']:.2f}. "
            "<bookmark mark='e'/> When twins, adoptees and ordinary families all point to the same "
            "number, the number has earned some trust. When they disagree, the disagreement is the "
            "finding."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(rows[0][0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[0][1], scale=1.2))
            vo.wait_until("b")
            self.play(FadeIn(rows[1][0]), FadeIn(rows[1][1], scale=1.2))
            vo.wait_until("c")
            self.play(FadeIn(rows[2][0]), FadeIn(rows[2][1], scale=1.2))
            vo.wait_until("d")
            self.play(FadeIn(weak))
            vo.wait_until("e")
            self.play(FadeIn(end, shift=UP * 0.1))
        self.clear_scene()
