from __future__ import annotations

import numpy as np

from videos.psychology.psych9.common import *  # noqa: F403


class Gwas(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.manhattan()
        self.real()

    def card(self):
        card = chapter_card(9, r"A million tests", r"If you cannot guess the gene, can you test them all?",
                            lit={2013: r"126{,}559 people"}, part=PART, scale=("molecule", "group"), marr=("how",))
        with self.voiceover(
            "Chapter nine. A million tests."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def idea(self):
        head = heading(r"Do not guess the gene. \ Test every position")
        g = np.random.default_rng(4)
        n = 60
        differ = g.random(n) < 0.15
        strip = VGroup(*[Square(side_length=0.17, stroke_width=0, fill_color=GENE if differ[i] else OWN,
                                fill_opacity=1.0 if differ[i] else 0.3) for i in range(n)]).arrange(RIGHT, buff=0.035)
        strip.move_to([0, 2.15, 0])
        sl = label(r"a person's DNA: \ a chip reads about a million of the positions where people differ", font_size=29,
                   color=GENE).next_to(strip, DOWN, buff=0.18)
        rows = rows_of([
            (r"at each position: \ do people with more copies of one version score higher? \ One regression", WHITE),
            (r"a million positions: \ a million tests. \ Part 8 had a hundred thousand voxels, and the same cure", GREY_A),
        ], 12.4, 30, 0.22).move_to([0, 0.35, 0])
        eq = label(r"$\dfrac{0.05}{1{,}000{,}000} = 5 \times 10^{-8}$", font_size=52, color=THRESH).move_to([-2.8, -1.55, 0])
        el = wrapped_label(r"``genome-wide significance''. \ A result must clear it, \ and then be found again in a second "
                           r"sample", 5.6, 30, THRESH).move_to([3.4, -1.55, 0])
        end = wrapped_label(r"A bar that high and effects that small: \ the samples have to be enormous.", 12.4, 31,
                            P.ACCENT).to_edge(DOWN, buff=0.5)
        tag = note(r"schematic").to_corner(DR, buff=0.2)
        with self.voiceover(
            "If you can't guess the gene, test them all. One person's DNA differs from another's at "
            "millions of positions, and a chip can read about a million of them at once. "
            "<bookmark mark='a'/> At each position, ask the candidate-gene question. Do people with more "
            "copies of one version score higher? That's one regression for each position. A million "
            "tests. <bookmark mark='b'/> You met this problem in the last part, in the brain: a hundred "
            "thousand voxels. The cure is the same. Divide the threshold by the number of tests. Point oh "
            "five, divided by a million, is five in a hundred million. <bookmark mark='c'/> That line is "
            "called genome-wide significance. A result that hasn't crossed it, and then been found again "
            "in a second sample, isn't believed. <bookmark mark='d'/> The price is the one you'd predict. "
            "With a bar that high, and effects that small, the samples have to be enormous."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(strip, lag_ratio=0.01), FadeIn(sl), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(eq))
            vo.wait_until("c")
            self.play(FadeIn(el))
            vo.wait_until("d")
            self.play(FadeIn(end, shift=UP * 0.1))
        self.clear_scene()

    def manhattan(self):
        d = load("gwas")
        head = heading(r"A genome in miniature: \ 2{,}500 positions, \ 500 of them real")
        g = np.random.default_rng(6)
        m = d["m"]
        top = 32.0
        panels = VGroup()
        for k, n in enumerate(d["sizes"]):
            n = int(n)
            A = axes([0, m], [0, top], x_length=7.4, y_length=1.6, xticks=[], yticks=[0, 10, 20],
                     yfmt=lambda v: f"{v:.0f}", xlabel=r"position along the genome" if k == 2 else r"", ylabel=r"",
                     center=[-2.85, 1.75 - 1.95 * k, 0])
            lp = np.minimum(d[f"logp_{n}"], top)
            keep = (lp > 1.3) | (g.random(m) < 0.2)
            hit = lp > d["logline"]
            dots = VGroup(*[Dot(A.ax.c2p(float(i), float(lp[i])), radius=0.035 if hit[i] else 0.022,
                                color=GENE if hit[i] else OWN, fill_opacity=1.0 if hit[i] else 0.6)
                            for i in np.where(keep)[0]])
            line = DashedLine(A.ax.c2p(0, d["logline"]), A.ax.c2p(m, d["logline"]), color=THRESH, stroke_width=2)
            lab = VGroup(label(rf"{n:,} people".replace(",", "{,}"), font_size=29, color=WHITE),
                         label(rf"{d[f'hits_{n}']} hits", font_size=34, color=GENE)).arrange(DOWN, buff=0.08)
            lab.next_to(A.ax.c2p(m, top / 2), RIGHT, buff=0.3)
            panels.add(VGroup(A, line, dots, lab))
        n0, n2 = int(d["sizes"][0]), int(d["sizes"][2])
        h0, h1, h2 = (d[f"hits_{int(n)}"] for n in d["sizes"])
        infl = d[f"inflation_{n0}"]
        rows = rows_of([
            (r"height of a dot: \ how surprising that position's association is", GREY_A),
            (rf"no false alarms at any size: \ what it finds is real", MODEL),
            (rf"but {d['causal']} positions matter, \ and most stay invisible", BAD),
            (rf"the first hits are exaggerated: \ {d[f'inflation_{n0}']:.1f} times their true size at "
             rf"{n0:,} people".replace(",", "{,}"), BAD),
        ], 3.5, 28, 0.26).move_to([5.2, -0.25, 0])
        keep_in_frame(rows)
        for p_ in panels:
            p_[3].set_x(2.05)
        tag = psyche_tag(r"simulated: a trait half of whose variation is carried by 500 positions")
        with self.voiceover(
            "Here's a genome in miniature. Twenty-five hundred positions. Five hundred of them truly "
            "affect a trait, each a little, and together they carry half of its variation. "
            f"<bookmark mark='a'/> Study {n0:,} people. Each dot is a position, and its height says how "
            "surprising its association with the trait is. The dashed line is the corrected threshold. "
            f"{h0} positions clear it. <bookmark mark='b'/> Six thousand people: "
            f"{h1}. <bookmark mark='c'/> Twenty thousand: "
            f"{h2}, and not one of them a false alarm. The method is strict, and what it "
            f"finds is real. <bookmark mark='d'/> But look at what it misses. {d['causal']} positions "
            f"matter, and with twenty thousand people we've found {h2}. The rest are real "
            "and invisible. And the first hits to appear are exaggerated. At two thousand people, the "
            f"estimated effects of the hits are {infl:.1f} times their true size. That's "
            "Part 4's winner's curse: to clear a high bar with a small sample, an estimate has to be "
            "lucky as well as real."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(panels[0][0]), Create(panels[0][1]), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(panels[0][2], lag_ratio=0.002), FadeIn(panels[0][3]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(panels[1][0]), Create(panels[1][1]), FadeIn(panels[1][2], lag_ratio=0.002), FadeIn(panels[1][3]),
                      run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(panels[2][0]), Create(panels[2][1]), FadeIn(panels[2][2], lag_ratio=0.002), FadeIn(panels[2][3]),
                      FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]))
        self.clear_scene()

    def real(self):
        d = load("gwas")
        rv, lee = archive.RIETVELD_2013.data, archive.LEE_2018.data
        t = archive.TURKHEIMER_2000.data
        head = heading(r"The real history has the same shape: \ years of schooling")
        A = axes([5, 6.7], [0, 4], x_length=5.6, y_length=3.9, xticks=[5, 6], yticks=[0, 1, 2, 3, 4],
                 xfmt=lambda v: rf"10^{{{int(v)}}}", yfmt=lambda v: rf"10^{{{int(v)}}}", xlabel=r"people in the study",
                 ylabel=r"positions found", center=[-3.7, -0.5, 0])
        ax = A.ax
        pts = [(np.log10(n), np.log10(h)) for n, h in zip(d["real_n"], d["real_hits"])]
        dots = VGroup(*[Dot(ax.c2p(x, y), radius=0.11, color=DATA) for x, y in pts])
        seg = VMobject(color=DATA, stroke_width=3).set_points_as_corners([ax.c2p(x, y) for x, y in pts])
        years = (2013, 2018, 2022)
        labs = VGroup(*[label(str(yr), font_size=28, color=DATA).next_to(ax.c2p(x, y), DR if i == 0 else UL, buff=0.2)
                        for i, (yr, (x, y)) in enumerate(zip(years, pts))])
        items = [
            (rf"2013: \ {rv['n']:,} people".replace(",", "{,}"), rf"{rv['snps']} positions, \ each worth about "
                                                                  rf"{rv['months_per_allele']} month of schooling"),
            (r"2018: \ 1.1 million people", rf"{lee['snps']:,} positions".replace(",", "{,}")),
            (r"2022: \ 3 million people", rf"{lee['okbay_snps']:,} positions".replace(",", "{,}")),
        ]
        rows = VGroup(*[VGroup(label(a, font_size=31, color=DATA), label(b, font_size=30, color=WHITE)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08) for a, b in items]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        rows.move_to([3.6, 1.0, 0])
        law = wrapped_label(r"A fourth law: \ " + t["fourth"], 6.2, 30, P.ACCENT).move_to([3.6, -1.75, 0])
        keep_in_frame(VGroup(rows, law))
        src = published_tag(archive.RIETVELD_2013.cite + r"; \ " + archive.LEE_2018.cite)
        with self.voiceover(
            "The real history has the same shape. Take years of schooling. <bookmark mark='a'/> In 2013: "
            f"{rv['n']:,} people, and {rv['snps']} positions found, each one worth about a month of "
            f"schooling. <bookmark mark='b'/> In 2018: one point one million people, and "
            f"{lee['snps']:,} positions. <bookmark mark='c'/> In 2022: three million people, and "
            f"{lee['okbay_snps']:,}. <bookmark mark='d'/> Thousands of positions, each with an effect "
            "too small to matter by itself, spread across the whole genome. It's been called the fourth "
            "law of behaviour genetics: a typical human trait is associated with very many genetic "
            "variants, each of very small effect. That's Fisher's picture from 1918, confirmed one "
            "position at a time."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(dots[0], scale=2.0), FadeIn(labs[0]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(dots[1], scale=2.0), FadeIn(labs[1]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(dots[2], scale=2.0), FadeIn(labs[2]), FadeIn(rows[2]), Create(seg))
            vo.wait_until("d")
            self.play(FadeIn(law, shift=UP * 0.1))
        self.clear_scene()
