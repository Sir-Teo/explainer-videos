from __future__ import annotations

import numpy as np

from videos.stats.stats33.common import *  # noqa: F403


class FWER(VoiceoverScene):
    def construct(self):
        self.card()
        self.bonferroni()
        self.holm()
        self.closed()
        self.lattice()
        self.hochberg()
        self.wy()
        self.results()
        self.verdict()

    def card(self):
        card = chapter_card(2, r"Family-wise error", r"No false positives, \ with high probability", lit=(1979,), part=PART)
        with self.voiceover("Chapter two. The family-wise error rate."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def bonferroni(self):
        rows = [
            cmath(r"P(V \ge 1)", r"=", r"P\big(\textstyle\bigcup_{i \in H_0} \{p_i \le \alpha/m\}\big)", font_size=30),
            cmath(r"", r"\le", r"\textstyle\sum_{i \in H_0} \alpha/m = m_0\alpha/m \le \alpha", font_size=30),
            cmath(r"\text{\v{S}id\'ak}", r":", r"\alpha_m = 1 - (1 - \alpha)^{1/m} \ \ \text{(independence)}", font_size=30),
            cmath(r"m = 5{,}000", r":", r"\alpha/m = 10^{-5}", font_size=32),
        ]
        rows[1][-1].set_color(FWC)
        whys = [why(r"Bonferroni (1936); \ Dunn (1961)"), why(r"valid marginal $p$-values; any dependence"),
                why(r"exact for independent tests"), why(r"barely different: \ $1.03 \times 10^{-5}$")]
        with self.voiceover(
            "<bookmark mark='a'/> The oldest correction is Bonferroni's: test each hypothesis at alpha over m. The chance of "
            "any false discovery is the chance of a union of events, <bookmark mark='b'/> which is at most the sum of their "
            "chances: m zero times alpha over m, at most alpha. No assumption about dependence is needed. "
            "<bookmark mark='c'/> Zbyněk Šidák's version is exact for independent tests, <bookmark mark='d'/> and barely "
            "different: for five thousand genes both test each gene at about one in a hundred thousand."
        ) as vo:
            intro=label('The union bound controls any false rejection with valid marginal p-values',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def holm(self):
        rows = [
            cmath(r"p_{(1)} \le \dots \le p_{(m)}", r":", r"\text{sort the } p\text{-values}", font_size=30),
            cmath(r"\text{step } k", r":", r"\text{reject } H_{(k)} \text{ if } p_{(k)} \le \alpha/(m - k + 1)", font_size=30),
            cmath(r"\text{stop}", r":", r"\text{at the first failure; \ keep the rest}", font_size=30),
            cmath(r"\text{always}", r"\supseteq", r"\text{Bonferroni's rejections, \ same FWER bound}", font_size=30),
        ]
        rows[1][-1].set_color(FWC)
        whys = [why(r"Holm (1979)"), why(r"thresholds loosen as you go"), why(r"step-down"), why(r"uniformly more powerful")]
        with self.voiceover(
            "<bookmark mark='a'/> Sture Holm’s step-down procedure of 1979 can improve power without weakening the "
            "guarantee. Sort the p-values. <bookmark mark='b'/> Compare the smallest with alpha over m, the next with"
            " alpha over m minus one, and so on: the first true null encountered must face a threshold no larger than"
            " alpha divided by the number of true nulls. <bookmark mark='c'/> Stop at the first failure. <bookmark "
            "mark='d'/> Holm rejects everything Bonferroni does, and sometimes more, with the same guarantee and "
            "still no dependence restriction, provided the marginal p-values are valid."
        ) as vo:
            intro=label('Holm stops at the first failed ordered comparison',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def closed(self):
        rows = [
            cmath(r"H_I", r"=", r"\textstyle\bigcap_{i \in I} H_i \ \text{for every } I \subseteq \{1..m\}", font_size=30),
            cmath(r"\text{reject } H_i", r"\iff", r"\text{every } H_I \text{ with } i \in I \text{ is rejected at level } \alpha", font_size=28),
            cmath(r"\text{FWER}", r"\le", r"\alpha \ \text{for any level-}\alpha \text{ local tests}", font_size=30),
            cmath(r"\text{Bonferroni local tests}", r"\Rightarrow", r"\text{exactly Holm}", font_size=30),
        ]
        rows[3][-1].set_color(FWC)
        whys = [why(r"all intersection hypotheses"), why(r"Marcus, \ Peritz \& Gabriel (1976)"),
                why(r"the true intersection must be rejected first"), why(r"a shortcut for $2^m$ tests")]
        with self.voiceover(
            "<bookmark mark='a'/> Holm's procedure is a special case of a powerful principle, closed testing. Form every "
            "intersection hypothesis: that all the nulls in a set I are true. <bookmark mark='b'/> Reject an individual "
            "hypothesis only if every intersection containing it is rejected by its own level alpha test. "
            "<bookmark mark='c'/> This controls the family-wise error rate whatever local tests are used: to make any false "
            "rejection you must first reject the intersection of all the true nulls, which happens with probability at most "
            "alpha. <bookmark mark='d'/> With Bonferroni tests for every intersection, the closed procedure is exactly "
            "Holm's, a shortcut through two to the m tests."
        ) as vo:
            intro=label('Closed testing checks every containing intersection',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def lattice(self):
        p = [0.01, 0.04, 0.03]
        nodes = {
            (1, 2, 3): ([0, 2.3, 0], r"$H_{123}$: \ $3 \times 0.01 = 0.03$"),
            (1, 2): ([-4.0, 0.7, 0], r"$H_{12}$: \ $2 \times 0.01 = 0.02$"), (1, 3): ([0, 0.7, 0], r"$H_{13}$: \ $0.02$"),
            (2, 3): ([4.0, 0.7, 0], r"$H_{23}$: \ $2 \times 0.03 = 0.06$"),
            (1,): ([-4.0, -0.9, 0], r"$H_1$: \ $0.01$"), (2,): ([0, -0.9, 0], r"$H_2$: \ $0.04$"),
            (3,): ([4.0, -0.9, 0], r"$H_3$: \ $0.03$"),
        }
        boxes, labs = VGroup(), VGroup()
        for I, (pos, t) in nodes.items():
            lab = label(t, font_size=22)
            box = SurroundingRectangle(lab, buff=0.12, color=GREY_B, stroke_width=1.5).move_to(pos)
            lab.move_to(pos)
            boxes.add(box)
            labs.add(lab)
        keys = list(nodes)
        edges = VGroup()
        for a in keys:
            for b in keys:
                if len(b) == len(a) - 1 and set(b) <= set(a):
                    edges.add(Line(nodes[a][0], nodes[b][0], color=GREY_D, stroke_width=1.5).set_z_index(-1))
        ok = {I: len(I) * min(p[i - 1] for i in I) <= 0.05 for I in keys}
        recolor = [boxes[k].animate.set_color(TRUEC if ok[I] else FALSEC) for k, I in enumerate(keys)]
        final = [boxes[k].animate.set_stroke(width=5) for k, I in enumerate(keys) if I == (1,)]
        foot = fit_rows(VGroup(
            label(r"$p = (0.01, \ 0.04, \ 0.03)$, \ $\alpha = 0.05$; \ each intersection tested by Bonferroni", font_size=22),
            label(r"green: \ the intersection is rejected; \ red: \ it survives", font_size=22, color=GREY_A),
            label(r"only $H_1$ is rejected: \ $H_2$ and $H_3$ both sit under $H_{23}$, \ which survives", font_size=22, color=FWC),
        ), 12.0, 0.2, [0, -2.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A small example: three hypotheses with p-values point oh one, point oh four and point oh "
            "three. The closure has seven intersections, each tested by Bonferroni. <bookmark mark='b'/> The top "
            "intersection is rejected, three times the smallest p being point oh three; so are H one two and H one three. "
            "But H two three, at twice point oh three, point oh six, survives. <bookmark mark='c'/> So only H one is "
            "rejected. H two and H three would each pass alone, but both sit under the surviving H two three. Holm's steps "
            "say the same: point oh one beats point oh one seven, then point oh three fails against point oh two five."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(edges), FadeIn(boxes), FadeIn(labs), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(*recolor, FadeIn(foot[1]))
            vo.wait_until("c")
            self.play(*final, FadeIn(foot[2]))
        self.clear_scene()

    def hochberg(self):
        rows = [
            cmath(r"\text{Simes}", r":", r"\text{reject } H_{\{1..m\}} \text{ if } p_{(i)} \le i\alpha/m \text{ for some } i", font_size=28),
            cmath(r"\text{Hochberg}", r":", r"\text{step up: \ largest } k \text{ with } p_{(k)} \le \alpha/(m - k + 1)", font_size=28),
            cmath(r"\text{needs}", r":", r"\text{independence or suitable Simes conditions}", font_size=30),
            cmath(r"\text{Westfall--Young}", r":", r"\text{use the actual dependence, \ by permutation}", font_size=30),
        ]
        rows[3][-1].set_color(FWC)
        whys = [why(r"Simes (1986)"), why(r"Hochberg (1988): \ more power than Holm"), why(r"Sarkar (1998)"),
                why(r"(1993): \ next")]
        with self.voiceover(
            "<bookmark mark='a'/> Two refinements. R. J. Simes's test of 1986 rejects the global null if any sorted "
            "p-value falls below i alpha over m. <bookmark mark='b'/> Yosef Hochberg turned it into a step-up "
            "procedure: find the largest k whose p-value is below alpha over m minus k plus one, and reject all up to"
            " it. <bookmark mark='c'/> It is more powerful than Holm's but needs independence or suitable "
            "positive-dependence conditions for its intersection tests. <bookmark mark='d'/> And Westfall and Young's"
            " method uses the actual dependence among the tests, estimated by permutation."
        ) as vo:
            intro=label('Step-up refinements require stronger dependence assumptions',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def wy(self):
        rows = [
            cmath(r"\text{permute}", r":", r"\text{shuffle labels under an exchangeable joint null}", font_size=28),
            cmath(r"M^*", r"=", r"\max_i |t_i^*|: \ \text{the largest statistic by chance}", font_size=30),
            cmath(r"\tilde p_i", r"=", r"P^*(M^* \ge |t_i|) \ \ \text{(step-down over the sorted } t\text{)}", font_size=28),
            cmath(r"\text{correlated tests}", r":", r"\text{fewer effective tests: \ less conservative}", font_size=30),
        ]
        rows[2][-1].set_color(FWC)
        whys = [why(r"keeps the genes' correlation"), why(r"its distribution, \ 1,000 times"),
                why(r"maxT"), why(r"pathways of 25 correlated genes")]
        with self.voiceover(
            "<bookmark mark='a'/> Under an exchangeable global null, shuffling patient and control labels simulates a"
            " joint null reference while retaining gene dependence. <bookmark mark='b'/> Record the largest absolute "
            "t statistic over all genes, and repeat a thousand times. <bookmark mark='c'/> We use a plus-one Monte "
            "Carlo correction to the share of permutation maxima exceeding each statistic, refined step by step down "
            "the sorted list. Strong family-wise control also requires subset pivotality. <bookmark mark='d'/> When "
            "tests are correlated, joint calibration can improve on the union bound. Bonferroni itself makes no "
            "assumption about the maximum’s distribution."
        ) as vo:
            intro=label('Permutation maxT requires exchangeability and a joint null reference',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def results(self):
        d = load("genes")
        r = d["res"]
        hdr = [r"\textbf{$\alpha = 0.05$}", r"\textbf{discoveries}", r"\textbf{false}", r"\textbf{true}", r"\textbf{power}"]
        body = [[nm, str(r[k]["R"]), str(r[k]["V"]), str(r[k]["S"]), f"{100 * r[k]['power']:.0f}\\%"]
                for k, nm in (("uncorrected", r"uncorrected"), ("bonferroni", r"Bonferroni"), ("holm", r"Holm"),
                              ("westfall_young", r"Westfall--Young"))]
        tb = table_rows([hdr] + body, font_size=26, col_buff=0.9, row_buff=0.32, colors=[GREY_A, FALSEC, FWC, FWC, FWC])
        tb.move_to([0, 0.9, 0])
        foot = fit_rows(VGroup(
            label(r"the corrections find about 50 genes, \ almost no false ones", font_size=22, color=FWC),
            label(r"but they miss four fifths of the 250 real ones", font_size=22, color=FALSEC),
        ), 12.0, 0.22, [0, -2.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The genes. Uncorrected: four hundred and thirty discoveries, half false. "
            "Bonferroni: forty-nine, none false. Holm adds one, as it happens a false one, still within its "
            "guarantee. Westfall and Young find fifty-three, using the correlation. <bookmark mark='b'/> Each makes "
            "zero or one false discoveries in this realization. Their promise bounds the chance of any false "
            "discovery across studies, not the number allowed in one study. <bookmark mark='c'/> But they find only "
            "about a fifth of the two hundred and fifty real effects."
        ) as vo:
            self.add(genes_tag())
            vo.wait_until("a")
            self.play(FadeIn(tb))
            vo.wait_until("b")
            self.play(FadeIn(foot[0]))
            vo.wait_until("c")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def verdict(self):
        rows = fit_rows(VGroup(
            label(r"FWER: \ right when a single false claim is costly", font_size=26, color=FWC),
            label(r"a drug's primary endpoints; \ a court; \ a confirmatory trial", font_size=26),
            label(r"FDR may suit exploratory lists with independent follow-up", font_size=26, color=FALSEC),
            label(r"choose the error criterion for the scientific cost", font_size=26, color=BHC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Family-wise control is the right promise when a single false claim is costly: "
            "<bookmark mark='b'/> a drug's primary endpoints, a legal finding, a confirmatory trial. <bookmark "
            "mark='c'/> For exploratory discovery, a less stringent average error criterion may be more useful when "
            "candidates receive independent follow-up. <bookmark mark='d'/> There, a list with a few false entries is"
            " perfectly useful, when the chosen average error criterion suits the scientific loss. That is the false "
            "discovery rate."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
