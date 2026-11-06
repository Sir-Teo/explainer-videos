from __future__ import annotations

import numpy as np

from videos.stats.stats33.common import *  # noqa: F403


class FDR(VoiceoverScene):
    def construct(self):
        self.card()
        self.history()
        self.procedure()
        self.sea()
        self.results()
        self.plugin()
        self.proof_setup()
        self.proof()
        self.dependence()
        self.by_results()

    def card(self):
        card = chapter_card(3, r"The false discovery rate", r"Control the share of errors, \ not their existence", lit=(1995,), part=PART)
        with self.voiceover("Chapter three. The false discovery rate."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def history(self):
        rows = fit_rows(VGroup(
            label(r"Yoav Benjamini and Yosef Hochberg, \ Tel Aviv, \ late 1980s", font_size=24),
            label(r"the paper was rejected by several journals before 1995", font_size=24, color=FALSEC),
            label(r"`Controlling the false discovery rate', \ JRSS B 57 (1995)", font_size=24, color=BHC),
            label(r"now among the most cited papers in all of statistics", font_size=24, color=SIGC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Yoav Benjamini and Yosef Hochberg, in Tel Aviv in the late 1980s, proposed changing the "
            "promise: control not the chance of any false discovery, but the expected share of discoveries that are false. "
            "<bookmark mark='b'/> The idea was resisted; the paper was turned down by several journals over five years. "
            "<bookmark mark='c'/> It appeared in the Journal of the Royal Statistical Society in 1995, <bookmark mark='d'/> "
            "just before genomics made it indispensable, and it is now among the most cited papers in statistics."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def procedure(self):
        rows = [
            cmath(r"p_{(1)} \le \dots \le p_{(m)}", r":", r"\text{sort}", font_size=32),
            cmath(r"k", r"=", r"\max\{i : p_{(i)} \le q\, i/m\}", font_size=34),
            cmath(r"\text{reject}", r":", r"H_{(1)}, \dots, H_{(k)}", font_size=32),
            cmath(r"\text{FDR}", r"\le", r"\pi_0 q \ \ \text{(independent tests)}", font_size=32),
        ]
        rows[1][-1].set_color(BHC)
        whys = [why(r"as for Holm"), why(r"the last crossing of a line"), why(r"step up"), why(r"the theorem")]
        with self.voiceover(
            "<bookmark mark='a'/> The procedure is as simple as Holm's. Sort the p-values. <bookmark mark='b'/> Find the "
            "largest i for which the i-th smallest p-value is below q times i over m: below a straight line through the "
            "origin with slope q over m. <bookmark mark='c'/> Reject everything up to that point, even hypotheses whose own "
            "p-values sit above the line. <bookmark mark='d'/> For independent tests, the false discovery rate is then at "
            "most pi zero times q."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def sea(self):
        d = load("genes")
        p = np.asarray(d["p_all"])
        sea = PValueSea(p, width=7.2, height=4.6, center=[-2.0, 0.2, 0], ranks=300, pmax=0.008)
        nn = np.asarray(d["nonnull_sorted"], bool)
        line = sea.bh_line(0.1, color=BHC)
        marks = sea.mark(0.1, color=SIGC)
        cols = VGroup(*[mk.copy().set_color(TRUEC if nn[i] else FALSEC) for i, mk in enumerate(marks)])
        k = sea.k(0.1)
        rows = fit_rows(VGroup(
            label(r"the 300 smallest of 5{,}000 $p$-values", font_size=22),
            label(r"blue: \ the BH line $p = q\, i/m$, \ $q = 0.1$", font_size=22, color=BHC),
            label(rf"the last crossing: \ $k = {k}$", font_size=22, color=SIGC),
            label(r"green: \ real; \ red: \ false", font_size=22, color=GREY_A),
        ), 4.0, 0.42, [4.8, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The p-value sea of the genes, zoomed to the three hundred smallest p-values, sorted. "
            "<bookmark mark='b'/> The Benjamini–Hochberg line, at q of ten percent, rises with slope q over m. "
            "<bookmark mark='c'/> The sorted p-values stay below it up to rank one hundred and eighty-four, and above it "
            "after: BH rejects those one hundred and eighty-four. <bookmark mark='d'/> Coloured by the truth: most are real, "
            "with false ones scattered through the list, more of them towards the end."
        ) as vo:
            self.add(genes_tag())
            self.play(FadeIn(sea))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(line), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(marks), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeTransform(marks, cols), FadeIn(rows[3]))
        self.clear_scene()

    def results(self):
        d = load("genes")
        r = d["res"]
        hdr = [r"\textbf{genes}", r"\textbf{discoveries}", r"\textbf{false}", r"\textbf{FDP}", r"\textbf{power}"]
        body = [[nm, str(r[k]["R"]), str(r[k]["V"]), f"{100 * r[k]['fdp']:.1f}\\%", f"{100 * r[k]['power']:.0f}\\%"]
                for k, nm in (("holm", r"Holm, \ $\alpha = 0.05$"), ("bh05", r"BH, \ $q = 0.05$"), ("bh10", r"BH, \ $q = 0.1$"))]
        tb = table_rows([hdr] + body, font_size=26, col_buff=0.9, row_buff=0.32, colors=[GREY_A, FWC, BHC, BHC])
        tb.move_to([0, 0.9, 0])
        foot = fit_rows(VGroup(
            label(r"BH finds three to four times as many real genes", font_size=22, color=BHC),
            label(r"and the false share is close to $q$: \ the promise, \ kept on this data set", font_size=22, color=SIGC),
        ), 12.0, 0.22, [0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Against Holm's fifty discoveries, BH at five percent makes a hundred and fifty-five, with "
            "six false; at ten percent, a hundred and eighty-four, with nineteen false, a false discovery proportion of ten "
            "point three percent. <bookmark mark='b'/> Three to four times as many real genes found, <bookmark mark='c'/> "
            "and the share of false ones close to the promised q."
        ) as vo:
            self.add(genes_tag())
            vo.wait_until("a")
            self.play(FadeIn(tb))
            vo.wait_until("b")
            self.play(FadeIn(foot[0]))
            vo.wait_until("c")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def proof_setup(self):
        rows = [
            cmath(r"V/R", r"=", r"\textstyle\sum_{i \in H_0} \mathbf 1\{H_i \text{ rejected}\}/R", font_size=30),
            cmath(r"H_i \text{ rejected}, \ R = k", r"\iff", r"p_i \le qk/m \text{ and } R^{(i)} = k", font_size=30),
            cmath(r"R^{(i)}", r":", r"\text{BH's count with } p_i \text{ set to } 0", font_size=30),
            cmath(r"p_i", r"\perp", r"R^{(i)} \ \ \text{(independence)}", font_size=32),
        ]
        rows[1][-1].set_color(BHC)
        whys = [why(r"split by hypothesis"), why(r"the key observation"), why(r"depends only on the other $p$-values"),
                why(r"the only assumption")]
        with self.voiceover(
            "<bookmark mark='a'/> The proof under independence is short. Write V over R as a sum over the true nulls of the "
            "indicator that each is rejected, divided by R. <bookmark mark='b'/> A null H i is rejected with exactly k "
            "rejections when its p-value is below q k over m and the procedure, run with p i replaced by zero, would also "
            "reject k. <bookmark mark='c'/> That second count depends only on the other p-values. <bookmark mark='d'/> So "
            "under independence it is independent of p i, which is uniform."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def proof(self):
        rows = [
            cmath(r"E\big[\tfrac{\mathbf 1\{i \text{ rej.}\}}{R}\big]", r"=", r"\textstyle\sum_k \tfrac1k P(p_i \le \tfrac{qk}{m})\, P(R^{(i)} = k)", font_size=28),
            cmath(r"", r"=", r"\textstyle\sum_k \tfrac1k \cdot \tfrac{qk}{m} \cdot P(R^{(i)} = k)", font_size=30),
            cmath(r"", r"=", r"\tfrac{q}{m} \textstyle\sum_k P(R^{(i)} = k) = \tfrac{q}{m}", font_size=30),
            cmath(r"\text{FDR}", r"=", r"m_0 \cdot \tfrac{q}{m} = \pi_0 q", font_size=34),
        ]
        rows[3][-1].set_color(BHC)
        whys = [why(r"independence"), why(r"$p_i$ uniform"), why(r"the $k$'s cancel"), why(r"exactly, \ for independent nulls")]
        with self.voiceover(
            "<bookmark mark='a'/> For one true null, condition on the count: the expected value is a sum over k of one over "
            "k, times the chance that p i is below q k over m, times the chance of the count. <bookmark mark='b'/> A uniform "
            "p-value is below q k over m with probability q k over m. <bookmark mark='c'/> The k's cancel, and the sum of "
            "probabilities is one: each true null contributes exactly q over m. <bookmark mark='d'/> Adding over the m zero "
            "true nulls, the false discovery rate is exactly pi zero times q. Not a bound: an equality, for independent "
            "continuous p-values."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def dependence(self):
        rows = [
            cmath(r"\text{PRDS}", r":", r"\text{positive regression dependence: \ BH still} \le \pi_0 q", font_size=28),
            cmath(r"\text{any dependence}", r":", r"\text{BH at } q / \textstyle\sum_{i=1}^m \tfrac1i", font_size=30),
            cmath(r"\textstyle\sum_{i \le m} \tfrac1i", r"\approx", r"\log m + 0.577: \ 9.1 \text{ for } m = 5{,}000", font_size=30),
            cmath(r"\text{in practice}", r":", r"\text{BH is robust; \ BY is very conservative}", font_size=30),
        ]
        rows[1][-1].set_color(BYC)
        whys = [why(r"Benjamini \& Yekutieli (2001)"), why(r"the BY procedure"), why(r"the harmonic number"),
                why(r"chapter six measures it")]
        with self.voiceover(
            "<bookmark mark='a'/> What about dependence? Benjamini and Daniel Yekutieli proved in 2001 that BH still "
            "controls the false discovery rate under positive regression dependence, which covers positively correlated "
            "one-sided tests like co-expressed genes. <bookmark mark='b'/> For arbitrary dependence, dividing q by the "
            "harmonic sum restores the guarantee: the BY procedure. <bookmark mark='c'/> For five thousand tests that "
            "factor is about nine. <bookmark mark='d'/> In practice BH is remarkably robust to dependence, and BY is very "
            "conservative."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def by_results(self):
        d = load("genes")
        r = d["res"]
        rows = fit_rows(VGroup(
            label(r"the genes, \ $q = 0.1$", font_size=28),
            label(rf"BH: \ {r['bh10']['R']} discoveries, \ {r['bh10']['V']} false", font_size=28, color=BHC),
            label(rf"BY: \ {r['by10']['R']} discoveries, \ {r['by10']['V']} false", font_size=28, color=BYC),
            label(r"BY's guarantee holds for any dependence, \ and costs a third of the discoveries", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> On the genes, whose pathways are correlated, at q of ten percent: <bookmark mark='b'/> BH "
            "makes a hundred and eighty-four discoveries, nineteen of them false. <bookmark mark='c'/> BY makes a hundred and "
            "twelve, two of them false. <bookmark mark='d'/> BY's guarantee holds whatever the dependence, and it costs "
            "about a third of the discoveries."
        ) as vo:
            self.add(genes_tag())
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def plugin(self):
        rows = [
            cmath(r"R(t)", r"=", r"\#\{p_i \le t\}", font_size=32),
            cmath(r"E\,V(t)", r"\approx", r"m_0 t \le m t", font_size=32),
            cmath(r"\widehat{\mathrm{FDR}}(t)", r"=", r"m t / R(t)", font_size=32),
            cmath(r"\text{BH}", r"=", r"\text{the largest } t \text{ with } \widehat{\mathrm{FDR}}(t) \le q", font_size=30),
        ]
        rows[2][-1].set_color(BHC)
        whys = [why(r"discoveries at threshold $t$"), why(r"nulls are uniform"), why(r"a plug-in estimate"), why(r"Storey's reading of BH")]
        with self.voiceover(
            "<bookmark mark='a'/> There is a second way to see BH. Reject every p-value below a threshold t, and count "
            "the rejections. <bookmark mark='b'/> Since null p-values are uniform, the expected number of false "
            "rejections is m zero times t, at most m times t. <bookmark mark='c'/> So m t over the number of "
            "rejections is a conservative estimate of the false discovery proportion. <bookmark mark='d'/> BH chooses "
            "the largest threshold for which that estimate is below q: at the i-th sorted p-value it is exactly m p "
            "over i. This is Storey's reading of the procedure, and the reason replacing m by an estimate of m zero "
            "gives chapter four's adaptive version."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
