from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant41.common import ladder
from videos.quant.quant41.common import (BAD, FUND_C, GOOD, HURDLE, LEV_C, NET_C, PART, PRICE_C, SAFE_C, SPIRAL_C, load)


class Research(VoiceoverScene):
    def construct(self):
        r = load("research")
        self.card()
        self.setup_en()
        self.tarski()
        self.tarski_proof()
        self.uniq()
        self.uniq_proof()
        self.uniq_end()
        self.algorithm()
        self.check_unique(r)
        self.cycle(r)
        self.phase()
        self.phase_proof()
        self.check_phase(r)
        self.firesale(r)
        self.related()
        self.open_problems()
        self.question()

    def card(self):
        c = research_card(r"Does a clearing vector exist, and is it unique?", r"When a network of banks cannot all pay, "
                          r"is there one answer to who pays what?", part=PART)
        with self.voiceover('For the researcher. We state a nonnegative-assets, limited-liability, pro-rata clearing model, prove existence and a sufficient regularity condition for uniqueness, and distinguish exact fictitious-default reasoning from the unchanged finite numerical solver. At most n strict additions to a default set may require n plus one outer checks including termination. We then derive the complete-network threshold with its debt and buffer conditions and compare the chosen numerical examples.'):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def setup_en(self):
        rows = [cmath(r"\bar p_i", r"=", r"\textstyle\sum_j L_{ij}", font_size=40, colors={r"\bar p_i": NET_C}),
                cmath(r"\Pi_{ij}", r"=", r"L_{ij} / \bar p_i", font_size=40),
                cmath(r"\Phi(p)", r"=", r"\min\bigl(\bar p,\ e + \Pi^\top p\bigr)", font_size=42, colors={r"\Phi(p)": HURDLE}),
                cmath(r"p^*", r"=", r"\Phi(p^*)", font_size=44, colors={r"p^*": SAFE_C})]
        whys = [why(r"bank $i$ owes $L_{ij}$ to bank $j$; its total obligation"),
                why('for positive total debt, the pro-rata share; define $\\Pi_{ij}=0$ for a zero-debt row'),
                why(r"what each bank can pay: its outside assets $e_i$ plus what it receives, but never more than it owes"),
                why(r"a clearing vector is a fixed point: everyone pays what they owe or everything they have")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Eisenberg and Noe's model, two thousand and one. <bookmark mark='a'/> Bank i owes L i j to bank j, and p bar "
            "i in total. <bookmark mark='b'/> If it cannot pay in full, its creditors share pro rata: pi i j is j's share. "
            "<bookmark mark='c'/> A bank can pay its outside assets plus what it receives, but never more than it owes: "
            "the map phi. <bookmark mark='d'/> A clearing vector is a fixed point of phi. Each bank pays in full, or pays "
            "everything it has."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def tarski(self):
        st = VGroup(MathTex(r"\Phi : [0, \bar p] \to [0, \bar p] \ \text{is monotone} \ \Rightarrow\ "
                            r"\exists\ p^+ \ge p^-:\ \text{every clearing vector } p^* \text{ has } p^- \le p^* \le p^+",
                            font_size=30),
                    wrapped_label(r"a greatest and a least clearing vector exist; iterating $\Phi$ from $\bar p$ falls to "
                                  r"$p^+$, iterating from $0$ rises to $p^-$", 9.8, 20)).arrange(DOWN, buff=0.35)
        card = theorem_card(r"Existence (Eisenberg and Noe 2001, by Tarski 1955)", st, r"this part's proof", width=11.8,
                            font_size=22)
        with self.voiceover(
            "Theorem one, existence. <bookmark mark='a'/> Phi maps the box from zero to p bar into itself, and it is "
            "monotone: if others pay more, you can pay more. So by Tarski's fixed-point theorem, a greatest and a least "
            "clearing vector exist, and every other lies between them. <bookmark mark='b'/> And iteration finds them: "
            "from full payment downward, or from nothing upward."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(Indicate(st[1], color=HURDLE, scale_factor=1.03))
        self.wait(0.5)
        self.clear_scene()

    def tarski_proof(self):
        rows = [cmath(r"p^{(0)} = \bar p", r",", r"p^{(k+1)} = \Phi(p^{(k)})", font_size=40),
                cmath(r"p^{(1)} \le p^{(0)}", r"\Rightarrow", r"p^{(k+1)} \le p^{(k)}\ \ \forall k", font_size=40,
                      colors={r"\Rightarrow": HURDLE}),
                cmath(r"p^{(k)} \downarrow p^+", r",", r"\Phi(p^+) = p^+", font_size=40, colors={r"p^{(k)} \downarrow p^+": SAFE_C}),
                cmath(r"q = \Phi(q)", r"\Rightarrow", r"q \le p^{(k)}\ \forall k \Rightarrow q \le p^+", font_size=38)]
        whys = [why(r"start from everyone paying in full"),
                why(r"$\Phi(\bar p) \le \bar p$ trivially; apply the monotone $\Phi$ to both sides, and repeat"),
                why(r"a bounded decreasing sequence converges; $\Phi$ is continuous, so the limit is a fixed point"),
                why(r"any fixed point $q \le \bar p$ stays below every iterate, by monotonicity: so $p^+$ is the greatest")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The proof, for this map. <bookmark mark='a'/> Start from full payment. <bookmark mark='b'/> The first step "
            "can only lower payments, and applying a monotone map to an inequality keeps it, so the sequence falls. "
            "<bookmark mark='c'/> It is bounded below by zero, so it converges, and since phi is continuous the limit is "
            "a fixed point. <bookmark mark='d'/> Any other fixed point stays below every iterate, so this one is the "
            "greatest. From zero upward, the same argument gives the least."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def uniq(self):
        st = VGroup(MathTex(r"\text{if from every bank some chain of obligations reaches a bank with } e_j > 0, "
                            r"\text{ then } p^+ = p^-", font_size=30),
                    wrapped_label(r"regularity: no group of banks owes only to itself while holding nothing outside; then "
                                  r"the clearing vector is unique", 9.8, 20)).arrange(DOWN, buff=0.35)
        card = theorem_card(r"Uniqueness (Eisenberg and Noe 2001)", st, r"this part's proof", width=11.8, font_size=22)
        with self.voiceover(
            "Theorem two, uniqueness. <bookmark mark='a'/> Suppose that from every bank, some chain of obligations "
            "reaches a bank with positive outside assets. <bookmark mark='b'/> Then the greatest and least clearing "
            "vectors coincide: there is one answer. The condition fails only for a group that owes only to itself and "
            "holds nothing else."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(Indicate(st[1], color=HURDLE, scale_factor=1.03))
        self.wait(0.5)
        self.clear_scene()

    def uniq_proof(self):
        rows = [cmath(r"d = p^+ - p^- \ge 0", r",", r"S = \{i : d_i > 0\}", font_size=40, colors={r"d = p^+ - p^- \ge 0": HURDLE}),
                cmath(r"i \in S", r"\Rightarrow", r"p^-_i = e_i + (\Pi^\top p^-)_i,\ \ p^+_i \le e_i + (\Pi^\top p^+)_i", font_size=34),
                cmath(r"\textstyle\sum_{i\in S} d_i", r"\le", r"\textstyle\sum_{j\in S} d_j \sum_{i\in S}\Pi_{ji}"
                      r"\ \le\ \sum_{j\in S} d_j", font_size=36),
                cmath(r"\Rightarrow", r"", r"\textstyle\sum_{i\in S}\Pi_{ji} = 1\ (j \in S),\ \text{all equalities hold}", font_size=34,
                      colors={r"\Rightarrow": SAFE_C})]
        whys = [why(r"where the two vectors differ"),
                why(r"a bank in $S$ pays less than it owes under $p^-$, so it pays all it has; under $p^+$ it pays at most that"),
                why(r"subtract and sum over $S$: banks outside $S$ have $d_j = 0$, and each row of $\Pi$ sums to at most one"),
                why(r"so every bank in $S$ sends all its payments into $S$, and both inequalities are equalities")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The proof. <bookmark mark='a'/> Let d be the difference between the greatest and least vectors, and S the "
            "banks where it is positive. <bookmark mark='b'/> A bank in S pays less than it owes under the least vector, "
            "so there it pays everything it has; under the greatest it pays at most that. <bookmark mark='c'/> Subtract "
            "and sum over S. Banks outside S contribute nothing, and each row of pi sums to at most one. "
            "<bookmark mark='d'/> So the chain of inequalities is tight: every bank in S pays only to banks in S."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def uniq_end(self):
        rows = [cmath(r"\textstyle\sum_{i\in S} p^+_i", r"=", r"\textstyle\sum_{i\in S} e_i + \sum_{i \in S}\sum_{j}\Pi_{ji}\,p^+_j",
                      font_size=36),
                cmath(r"", r"=", r"\textstyle\sum_{i\in S} e_i + \sum_{j\in S} p^+_j + \sum_{i\in S}\sum_{j\notin S}\Pi_{ji}\,p^+_j",
                      font_size=34),
                cmath(r"\Rightarrow", r"", r"e_i = 0 \text{ on } S,\ \text{and nothing flows into } S", font_size=38,
                      colors={r"\Rightarrow": BAD}),
                cmath(r"\text{regularity}", r"\Rightarrow", r"S = \varnothing,\ \ p^+ = p^-", font_size=40,
                      colors={r"\text{regularity}": SAFE_C})]
        whys = [why(r"banks in $S$ pay all they have under $p^+$ too (the equalities)"),
                why(r"split the inflows: from inside $S$, which sum to $S$'s own payments, and from outside"),
                why(r"cancel $S$'s payments from both sides: what is left is non-negative and sums to zero"),
                why(r"a non-empty $S$ would be a closed group with no outside assets, which regularity rules out")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "And the end. <bookmark mark='a'/> Under the greatest vector, the banks in S also pay all they have. "
            "<bookmark mark='b'/> Split what they receive into payments from inside S, which add up to S's own payments, "
            "and payments from outside. <bookmark mark='c'/> Cancel, and what remains is non-negative and sums to zero: "
            "no outside assets in S, and nothing flowing in. <bookmark mark='d'/> That is a closed group with nothing "
            "outside, which regularity forbids. So S is empty, and the clearing vector is unique."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def algorithm(self):
        rows = [cmath(r"D_0 = \varnothing", r":", r"\text{assume everyone pays in full}", font_size=38),
                cmath(r"D_{k+1}", r"=", r"\{i : e_i + (\Pi^\top p^{(k)})_i < \bar p_i\}", font_size=38, colors={r"D_{k+1}": BAD}),
                cmath(r"p^{(k+1)}", r":", r"\text{solve } p_D = e_D + (\Pi^\top p)_D,\ p_{D^c} = \bar p_{D^c}", font_size=34),
                cmath(r"D_k \subseteq D_{k+1}", r"\Rightarrow", r"\text{at most } n \text{ strict additions}", font_size=38,
                      colors={r"D_k \subseteq D_{k+1}": SAFE_C})]
        whys = [why(r"Eisenberg and Noe's fictitious default algorithm"),
                why(r"the banks that cannot pay given the current payments"),
                why(r"one linear system for the defaulters, the rest paying in full"),
                why('exact default-set enlargement can occur at most $n$ times; a final no-change check may be additional. The code uses finite inner iteration and tolerances')]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Fictitious default in the regular, nonnegative-assets model. <bookmark mark='a'/> Start with all banks paying in full and no defaults. <bookmark mark='b'/> Find newly insolvent banks from outside assets plus incoming payments. <bookmark mark='c'/> With nondefaulters paying in full, solve the defaulting subsystem; under the stated conditions this gives the appropriate reduced payment vector. The unchanged code approximates that step by finite Picard iteration with a tolerance. <bookmark mark='d'/> Payments decrease and the default set grows. At most n strict enlargements are possible, with an additional termination check. Numerical outer-round counts include checks, so the bound is not automatically n total loop evaluations."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def check_unique(self, r):
        rows = VGroup(
            label(rf"random networks: {r['trials']}, of 12 banks each, 30\% of links present", font_size=22, color=GREY_A),
            label(rf"fictitious default = iteration from above = iteration from below: {r['agree']} of {r['trials']}",
                  font_size=24, color=SAFE_C),
            label(rf"outer checks: max {r['rounds_max']}, mean {r['rounds_mean']:.2f}; at most 12 strict default-set additions",
                  font_size=24, color=HURDLE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(ORIGIN)
        with self.voiceover(
            f"""The unchanged numerical check. <bookmark mark='a'/> {r['trials']} chosen random twelve-bank networks have strictly positive outside assets almost surely, satisfying the sufficient regularity condition; zero-debt rows use zero payment shares. <bookmark mark='b'/> In {r['agree']} of {r['trials']}, fictitious default and monotone iteration from the top and bottom agree within ten to the minus eight. This supports the implementation on these cases and is not the proof of uniqueness. <bookmark mark='c'/> The maximum outer-check count is {r['rounds_max']}, averaging {r['rounds_mean']:.2f}. Those counts include the final no-change check and finite numerical stopping; the theorem bounds strict default-set enlargements."""
        ) as vo:
            self.play(FadeIn(rows[0], shift=RIGHT * 0.2))
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
                else:
                    self.play(Indicate(rows[0], color=HURDLE, scale_factor=1.0))
        self.wait(0.4)
        self.clear_scene()

    def cycle(self, r):
        top, bot = r["cycle"]["top"], r["cycle"]["bottom"]
        a = Circle(radius=0.5, color=NET_C).shift(LEFT * 2)
        b = Circle(radius=0.5, color=NET_C).shift(RIGHT * 2)
        ta = label(r"A", font_size=28).move_to(a)
        tb = label(r"B", font_size=28).move_to(b)
        ab = CurvedArrow(a.get_top() + RIGHT * 0.2, b.get_top() + LEFT * 0.2, angle=-PI / 3, color=GREY_B)
        ba = CurvedArrow(b.get_bottom() + LEFT * 0.2, a.get_bottom() + RIGHT * 0.2, angle=-PI / 3, color=GREY_B)
        l1 = label(r"owes 1", font_size=18, color=GREY_B).next_to(ab, UP, buff=0.1)
        l2 = label(r"owes 1", font_size=18, color=GREY_B).next_to(ba, DOWN, buff=0.1)
        net = VGroup(a, b, ta, tb, ab, ba, l1, l2).shift(UP * 0.8)
        res = VGroup(label(rf"$e = (0, 0)$: from above $p = ({top[0]:.0f}, {top[1]:.0f})$; from below $p = "
                           rf"({bot[0]:.0f}, {bot[1]:.0f})$", font_size=22, color=BAD),
                     label(r"both are clearing vectors: the closed group with nothing outside", font_size=20,
                           color=GREY_A)).arrange(DOWN, buff=0.2).next_to(net, DOWN, buff=0.7)
        with self.voiceover(
            "And the counterexample when regularity fails. <bookmark mark='a'/> Two banks owe each other one, and hold "
            "nothing else. <bookmark mark='b'/> Paying in full is a clearing vector: each receives one and pays it on. "
            "So is paying nothing. Iteration from above finds the first, from below the second. The theorem's condition "
            "is not a technicality."
        ) as vo:
            self.play(FadeIn(net))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    def phase(self):
        st = VGroup(MathTex(r"\text{complete network, } n \text{ banks, senior debt } v, \text{ assets } a, \text{ shock } "
                            r"\varepsilon \text{ to one bank}:\quad \text{all default} \iff \varepsilon > n\,(a - v)",
                            font_size=28),
                    wrapped_label('assume $b=a-v>0$ and $y>(n-1)b$: zero defaults for $\\varepsilon\\le b$, one for $b<\\varepsilon\\le nb$, all for $\\varepsilon>nb$', 9.8, 20)
                    ).arrange(DOWN, buff=0.35)
        card = theorem_card(r"The contagion threshold (Acemoglu, Ozdaglar and Tahbaz-Salehi 2015)", st,
                            r"this part's derivation, for the symmetric case", width=11.8, font_size=22)
        with self.voiceover(
            "The symmetric complete-network result needs conditions. <bookmark mark='a'/> Let b equal a minus v, positive; each bank owes y to the others equally. Assume y exceeds n minus one times b and use the stated greatest-clearing senior-resource model. Then all banks default exactly when epsilon exceeds n b. <bookmark mark='b'/> Epsilon at most b causes zero defaults. Between b and n b, only the shocked bank defaults. Above n b, all default. At the threshold equality the other banks can still pay in full. These qualifications exclude low-interbank-debt counterexamples."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(Indicate(st[1], color=HURDLE, scale_factor=1.03))
        self.wait(0.5)
        self.clear_scene()

    def phase_proof(self):
        rows = [cmath(r"x_0", r"=", r"\min(y,\max(0,a-\varepsilon+y-v))", font_size=40, colors={r"x_0": BAD}),
                cmath(r"\text{shortfall}", r"=", r"y-x_0=\min(y,(\varepsilon-(a-v))_+)", font_size=40),
                cmath(r"\text{each creditor loses}", r"", r"\frac{\min(y,(\varepsilon-(a-v))_+)}{n-1}", font_size=40),
                cmath(r"\frac{\varepsilon - (a - v)}{n - 1} > a - v", r"\iff", r"\varepsilon > n\,(a - v)", font_size=40,
                      colors={r"\iff": SAFE_C})]
        whys = [why(r"bank 0 receives $y$ from the others, who are paying in full, and pays its senior debt $v$ first"),
                why(r"it owes $y$ in all to the others; its shortfall is the shock beyond its own buffer $a - v$"),
                why(r"split equally among the $n - 1$ others, who each owe $y/(n-1)$ to each other bank in turn"),
                why(r"each creditor's buffer is $a - v$; by symmetry if one fails all fail, and their failure only lowers "
                    r"payments further: the greatest clearing vector is all-default")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The derivation with clipping made explicit. <bookmark mark='a'/> When all others pay, the hit bank's interbank payment is its net resources clipped between zero and y. Negative net resources mean a shortfall against senior obligations, not literally negative gross assets. <bookmark mark='b'/> Its shortfall is min of y and the positive part of epsilon minus b. <bookmark mark='c'/> Each other bank loses one over n minus one of that amount. <bookmark mark='d'/> Since y exceeds n minus one times b, the other banks' buffers are breached exactly when epsilon exceeds n b. Symmetry and greatest-payment iteration then imply all-default. If y were too small, saturation at zero would prevent this argument."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def check_phase(self, r):
        sw = r["sweeps"]
        p = r["params"]
        g = axes([0, 8], [0, 10.5], x_length=7.4, y_length=4.2, xlabel=r"shock to one bank, $\varepsilon$",
                 ylabel=r"banks in default, of 10", xticks=[0, 2, 4, 6, 8], yticks=[0, 5, 10], font_size=15
                 ).move_to(LEFT * 1.3 + DOWN * 0.2)
        ax = g.ax
        cols = {"ring": HURDLE, "complete": BAD, "clusters": NET_C}
        names = {"ring": r"ring", "complete": r"complete", "clusters": r"two clusters"}
        lines = {}
        for k in ("ring", "complete", "clusters"):
            s = np.asarray(sw[k]["shock"], float)
            dft = np.asarray(sw[k]["defaults"], float)
            xs, ys = [], []
            for i in range(len(s)):
                xs += [s[i], min(s[i] + 0.05, s[-1])]
                ys += [dft[i], dft[i]]
            lines[k] = curve(ax, np.array(xs), np.array(ys), cols[k], stroke_width=3)
        thr = DashedLine(ax.c2p(r["thr"], 0), ax.c2p(r["thr"], 10.5), color=SAFE_C, stroke_width=2)
        thr_l = label(rf"$n(a - v) = {r['thr']:.0f}$", font_size=17, color=SAFE_C).next_to(ax.c2p(r["thr"], 10.5), RIGHT,
                                                                                       buff=0.1)
        leg = legend([(cols[k], names[k]) for k in ("ring", "complete", "clusters")], font_size=17)
        par = label(rf"$n = {p['n']}$, $y = {p['y']:.0f}$, $a = {p['a']:.1f}$, $v = {p['v']:.0f}$", font_size=17,
                    color=GREY_B)
        side = VGroup(leg, par).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(g, RIGHT, buff=0.4)
        fit_right(side)
        with self.voiceover(
            "The check, on a grid of shocks a twentieth apart. <bookmark mark='a'/> The ring loses one bank at a time as "
            "the shock grows. <bookmark mark='b'/> The complete network loses one bank, then all ten, at "
            f"{r['jump']:.2f}: the first grid point above the formula's {r['thr']:.0f}. <bookmark mark='c'/> And two "
            "clusters, weakly linked, stop at five: the loss spreads within a cluster, and the thin link between them "
            "is a firewall."
        ) as vo:
            self.play(FadeIn(g), FadeIn(par), Create(lines['ring']))
            vo.wait_until("a")
            self.play(FadeIn(leg[0]), Indicate(lines['ring'], color=HURDLE), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(leg[1]), Create(lines["complete"]), FadeIn(thr), FadeIn(thr_l), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(leg[2]), Create(lines["clusters"]), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    def firesale(self, r):
        fs = r["firesale"]
        heads = [r"shock", r"ring", r"ring, with fire sales", r"complete", r"complete, with fire sales"]
        tab = VGroup(VGroup(*[label(h_, font_size=19, color=QC.IDEA) for h_ in heads]))
        for row in fs:
            tab.add(VGroup(label(rf"{row['shock']:.0f}", font_size=20),
                           label(rf"{row['ring']}", font_size=20, color=HURDLE),
                           label(rf"{row['ring_fs']}", font_size=20, color=BAD),
                           label(rf"{row['complete']}", font_size=20, color=HURDLE),
                           label(rf"{row['complete_fs']}", font_size=20, color=BAD)))
        xs = [-5.4, -3.6, -1.2, 1.5, 4.3]
        for row in tab:
            for j, c in enumerate(row):
                c.move_to([xs[j], 0, 0])
        tab.arrange(DOWN, buff=0.4).move_to(UP * 0.4)
        for row in tab:
            for j, c in enumerate(row):
                c.set_x(xs[j])
        note_ = wrapped_label('chosen cascade: defaulting banks liquidate one common-asset unit; price $e^{-0.15 \\times \\text{units sold}}$, up to 50 iterations; related to Cifuentes et al., not a reproduction', 11.6, 18,
                              GREY_B).next_to(tab, DOWN, buff=0.5)
        f4 = [x for x in fs if x["shock"] == 4.0][0]
        with self.voiceover(
            f"""Add a chosen common-asset cascade. <bookmark mark='a'/> Each bank owns one asset unit; defaults cause liquidation, and price is exp of minus zero point one five times units sold. The code allows fifty iterations and a finite stopping rule. This is related to the fire-sale literature, not a reproduction or calibration of Cifuentes, Ferrucci and Shin. <bookmark mark='b'/> At the chosen shock four, the complete network has {f4['complete']} default without price effects and {f4['complete_fs']} with them. These selected cases demonstrate how common-asset marks can reduce buffers. They do not prove global convergence, uniqueness or a universal size of amplification."""
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(tab[1]), FadeIn(note_))
            vo.wait_until("a")
            self.play(Indicate(tab[1], color=HURDLE))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[2:]], lag_ratio=0.3), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def related(self):
        cards = VGroup(
            desk_question(r"default costs", r"Rogers and Veraart (2013): if a defaulter's assets lose value in default, "
                          r"uniqueness can fail, and solvent banks can gain by rescuing it", width=12.4, font_size=19),
            desk_question(r"how large can network effects be?", 'Glasserman and Young derive conditional bounds on amplification; aggregate losses and default counts differ, and bounds require their model assumptions', width=12.4,
                          font_size=19),
            desk_question(r"integration and diversification", r"Elliott, Golub and Jackson (2014): cascades are largest "
                          r"at intermediate levels of both, as in Chapter 4's sweeps", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Extensions and their conditions. <bookmark mark='a'/> Rogers and Veraart add default costs, which can change equilibrium multiplicity and incentives for rescues. That is a model mechanism, not proof of individual LTCM creditors' motives. <bookmark mark='b'/> Glasserman and Young derive bounds on network amplification under stated assumptions. Payment redistribution, outside losses and the number of defaults are different quantities; no universal small-contagion theorem follows for our closed-network default counts. <bookmark mark='c'/> Elliott, Golub and Jackson study how integration and diversification affect cascades within specified network models. Their comparisons are not an unrestricted ranking of every topology."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
                else:
                    self.play(Indicate(cards[0], color=HURDLE, scale_factor=1.0))
        self.wait(0.4)
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"the missing data", 'bilateral exposures are often incomplete; maximum-entropy reconstruction can alter contagion in either direction, depending on metric, topology and constraints',
                          width=12.4, font_size=19),
            desk_question(r"networks with prices", r"clearing with fire sales and runs together: when is the equilibrium "
                          r"unique, and how fast can it be computed for real systems?", width=12.4, font_size=19),
            desk_question(r"outside the banks", r"the links among funds, dealers, central counterparties and crypto "
                          r"lenders, where Chapters 7 to 10 began, are the least measured", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three open problems. <bookmark mark='a'/> Incomplete bilateral exposures: maximum-entropy reconstruction spreads links but can understate or overstate the selected contagion metric. Reconstruction assumptions must be evaluated, not treated as a universal directional theorem. <bookmark mark='b'/> Networks with prices, defaults and runs together: existence, multiplicity and computation depend on liquidation and contract rules. <bookmark mark='c'/> Links among funds, dealers, clearing houses and other nonbanks remain unevenly observed. Coverage and stressed valuation matter alongside the network equations."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
                else:
                    self.play(Indicate(cards[0], color=HURDLE, scale_factor=1.0))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"three banks in a ring each owe the next 1 and hold outside assets of 0.5. Is the clearing vector "
                       r"unique, and what is it?")
        with self.voiceover(
            "Pause and predict. Three banks in a ring each owe the next one, and hold outside assets of a half. Is the "
            "clearing vector unique, and what is it?"
        ):
            self.play(FadeIn(q))
        self.wait(6.0)
        self.clear_scene()
