from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
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
        with self.voiceover("For the researcher. Chapter four computed who pays what in a network of defaults, as if "
                            "the answer were obvious. This chapter proves that it exists, finds when it is unique, gives "
                            "the algorithm that finds it in at most n rounds, and derives Chapter four's contagion "
                            "threshold in closed form. Then it checks each claim by simulation."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def setup_en(self):
        rows = [cmath(r"\bar p_i", r"=", r"\textstyle\sum_j L_{ij}", font_size=40, colors={r"\bar p_i": NET_C}),
                cmath(r"\Pi_{ij}", r"=", r"L_{ij} / \bar p_i", font_size=40),
                cmath(r"\Phi(p)", r"=", r"\min\bigl(\bar p,\ e + \Pi^\top p\bigr)", font_size=42, colors={r"\Phi(p)": HURDLE}),
                cmath(r"p^*", r"=", r"\Phi(p^*)", font_size=44, colors={r"p^*": SAFE_C})]
        whys = [why(r"bank $i$ owes $L_{ij}$ to bank $j$; its total obligation"),
                why(r"the share of $i$'s payments that goes to $j$: limited liability and equal priority among creditors"),
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
            vo.wait_until("a")
            self.play(FadeIn(card, shift=UP * 0.2))
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
            vo.wait_until("a")
            self.play(FadeIn(card, shift=UP * 0.2))
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
                cmath(r"D_k \subseteq D_{k+1}", r"\Rightarrow", r"\text{at most } n \text{ rounds}", font_size=38,
                      colors={r"D_k \subseteq D_{k+1}": SAFE_C})]
        whys = [why(r"Eisenberg and Noe's fictitious default algorithm"),
                why(r"the banks that cannot pay given the current payments"),
                why(r"one linear system for the defaulters, the rest paying in full"),
                why(r"payments only fall, so the default set only grows; it stops when it stops growing, after at most $n$ "
                    r"rounds. The round in which a bank defaults measures how far down the cascade it sits")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "And the algorithm that finds it, fictitious default. <bookmark mark='a'/> Assume everyone pays in full. "
            "<bookmark mark='b'/> Find the banks that cannot. <bookmark mark='c'/> Solve one linear system: the "
            "defaulters pay all they have, the rest pay in full. <bookmark mark='d'/> Payments can only fall, so the "
            "default set only grows, and the algorithm stops within n rounds. The round in which a bank defaults says "
            "how far down the cascade it sits: Eisenberg and Noe proposed it as a measure of systemic exposure."
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
            label(rf"rounds needed: at most {r['rounds_max']}, mean {r['rounds_mean']:.2f}, against a bound of 12",
                  font_size=24, color=HURDLE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(ORIGIN)
        with self.voiceover(
            f"The check. <bookmark mark='a'/> {r['trials']} random networks of twelve banks, with random obligations and "
            f"positive outside assets, so regular. <bookmark mark='b'/> In {r['agree']} of {r['trials']}, the algorithm's "
            "answer equals iteration from full payment and iteration from zero, to eight decimal places: the greatest and "
            f"least vectors coincide, as theorem two says. <bookmark mark='c'/> And it never needed more than "
            f"{r['rounds_max']} rounds, {r['rounds_mean']:.2f} on average, against the bound of twelve."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
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
            vo.wait_until("a")
            self.play(FadeIn(net))
            vo.wait_until("b")
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    def phase(self):
        st = VGroup(MathTex(r"\text{complete network, } n \text{ banks, senior debt } v, \text{ assets } a, \text{ shock } "
                            r"\varepsilon \text{ to one bank}:\quad \text{all default} \iff \varepsilon > n\,(a - v)",
                            font_size=28),
                    wrapped_label(r"below the threshold one bank fails and the rest absorb its loss; above it every bank "
                                  r"fails: a phase transition, where the ring degrades one bank at a time", 9.8, 20)
                    ).arrange(DOWN, buff=0.35)
        card = theorem_card(r"The contagion threshold (Acemoglu, Ozdaglar and Tahbaz-Salehi 2015)", st,
                            r"this part's derivation, for the symmetric case", width=11.8, font_size=22)
        with self.voiceover(
            "Theorem three, Chapter four's phase transition. <bookmark mark='a'/> In the complete network of n banks, each "
            "with assets a and senior debt v, a shock epsilon to one bank brings down all of them exactly when epsilon "
            "exceeds n times a minus v. <bookmark mark='b'/> Below it, the network shares the loss and only one bank "
            "fails. Above it, every bank fails at once."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(Indicate(st[1], color=HURDLE, scale_factor=1.03))
        self.wait(0.5)
        self.clear_scene()

    def phase_proof(self):
        rows = [cmath(r"x_0", r"=", r"a - \varepsilon + y - v", font_size=40, colors={r"x_0": BAD}),
                cmath(r"\text{shortfall}", r"=", r"y - x_0 = \varepsilon - (a - v)", font_size=40),
                cmath(r"\text{each creditor loses}", r"", r"\frac{\varepsilon - (a - v)}{n - 1}", font_size=40),
                cmath(r"\frac{\varepsilon - (a - v)}{n - 1} > a - v", r"\iff", r"\varepsilon > n\,(a - v)", font_size=40,
                      colors={r"\iff": SAFE_C})]
        whys = [why(r"bank 0 receives $y$ from the others, who are paying in full, and pays its senior debt $v$ first"),
                why(r"it owes $y$ in all to the others; its shortfall is the shock beyond its own buffer $a - v$"),
                why(r"split equally among the $n - 1$ others, who each owe $y/(n-1)$ to each other bank in turn"),
                why(r"each creditor's buffer is $a - v$; by symmetry if one fails all fail, and their failure only lowers "
                    r"payments further: the greatest clearing vector is all-default")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The derivation, for the symmetric case. <bookmark mark='a'/> If the others pay in full, bank zero has its "
            "assets less the shock, plus what it receives, less its senior debt. <bookmark mark='b'/> Its shortfall on "
            "what it owes is the shock beyond its own buffer, a minus v. <bookmark mark='c'/> That shortfall is shared "
            "equally by the n minus one others. <bookmark mark='d'/> Each fails if its share exceeds its own buffer, a "
            "minus v: that is, if epsilon exceeds n times a minus v. And by symmetry, one creditor failing means all do."
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
                xs += [s[i], s[i] + 0.05]
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
            self.play(FadeIn(g), FadeIn(par))
            vo.wait_until("a")
            self.play(FadeIn(leg[0]), Create(lines["ring"]), run_time=1.5)
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
        note_ = wrapped_label(r"each bank also holds one unit of a common asset; defaulters sell it, and its price falls "
                              r"as $e^{-0.15 \times \text{units sold}}$ (Cifuentes, Ferrucci and Shin 2005)", 11.6, 18,
                              GREY_B).next_to(tab, DOWN, buff=0.5)
        f4 = [x for x in fs if x["shock"] == 4.0][0]
        with self.voiceover(
            "Add Chapter three to Chapter four. <bookmark mark='a'/> Each bank also holds one unit of a common asset, "
            "and defaulters sell it, pushing its price down for everyone: Cifuentes, Ferrucci and Shin's model. "
            "<bookmark mark='b'/> Now the complete network, which shared a shock of four with a single default, loses "
            f"all {f4['complete_fs']}: the fire sale lowers every bank's buffer, and the threshold falls below the shock. "
            "The ring, which lost a few, loses all of them. Diversification across counterparties does not diversify a "
            "common asset."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(note_))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def related(self):
        cards = VGroup(
            desk_question(r"default costs", r"Rogers and Veraart (2013): if a defaulter's assets lose value in default, "
                          r"uniqueness can fail, and solvent banks can gain by rescuing it", width=12.4, font_size=19),
            desk_question(r"how large can network effects be?", r"Glasserman and Young (2015): without default costs "
                          r"or fire sales, contagion through payments adds little to the direct losses", width=12.4,
                          font_size=19),
            desk_question(r"integration and diversification", r"Elliott, Golub and Jackson (2014): cascades are largest "
                          r"at intermediate levels of both, as in Chapter 4's sweeps", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Where the literature goes. <bookmark mark='a'/> Rogers and Veraart add default costs: uniqueness can fail, "
            "and healthy banks can profit by rescuing a failing one, as LTCM's creditors did. <bookmark mark='b'/> "
            "Glasserman and Young bound the network's contribution: without default costs or fire sales, contagion "
            "through payments adds little to the direct losses. Which is why this chapter's last table matters. "
            "<bookmark mark='c'/> And Elliott, Golub and Jackson show cascades are worst at intermediate levels of "
            "integration and diversification."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"the missing data", r"bilateral exposures are mostly unobserved; reconstructing them by maximum "
                          r"entropy spreads them evenly and understates contagion (Mistrulli 2011; Anand et al. 2018)",
                          width=12.4, font_size=19),
            desk_question(r"networks with prices", r"clearing with fire sales and runs together: when is the equilibrium "
                          r"unique, and how fast can it be computed for real systems?", width=12.4, font_size=19),
            desk_question(r"outside the banks", r"the links among funds, dealers, central counterparties and crypto "
                          r"lenders, where Chapters 7 to 10 began, are the least measured", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three open problems. <bookmark mark='a'/> The data: bilateral exposures are mostly unobserved, and the usual "
            "reconstruction, maximum entropy, spreads them evenly and understates contagion. <bookmark mark='b'/> Networks "
            "with prices: clearing with fire sales and runs together, when it is unique, and how to compute it for real "
            "systems. <bookmark mark='c'/> And outside the banks: the links among funds, dealers, clearing houses and "
            "crypto lenders, where this part's crises began, are the least measured."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
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
        self.wait(0.5)
        self.clear_scene()
