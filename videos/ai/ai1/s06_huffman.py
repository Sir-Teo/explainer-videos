from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai1.common import ALPHA27, MONO, PART, area_slivers, code_tree, letter, load


class Huffman(VoiceoverScene):
    def construct(self):
        self.card()
        self.bound()
        self.huffman()
        self.exchange()
        self.induction()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(5, r"The best code: Huffman, and why it is optimal",
                            r"How close to the entropy can a code get?", lit=(1948, 1952), part=PART)
        with self.voiceover("Chapter five. The best code, and the proof that it is the best."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def bound(self):
        hf = load("huffman")
        lt = load("letters")
        p, order = lt["p"], list(lt["order"])
        H = float(lt["H"])
        W, y0, sc = 11.4, -3.25, 0.25
        sky = area_slivers(p, W=W, y0=y0, scale=sc, order=order, color=C.SURPRISE, opacity=0.85)
        base = Line([-W / 2, y0, 0], [W / 2, y0, 0], color=GREY_C, stroke_width=1.5)
        head = label(r"No prefix code beats the entropy", font_size=36).to_edge(UP, buff=0.35)
        setup = mtex(r"L = \sum_i p_i\, \ell_i \quad \text{(average length)}, \qquad H = \sum_i p_i \log_2 \tfrac{1}{p_i}",
                     font_size=32, color=GREY_A).next_to(head, DOWN, buff=0.3)
        colors = {r"p_i": C.TRUE_P, r"2^{-\ell_i}": C.BITS, "1": C.BITS}
        steps = [
            ["H - L", "=", r"\sum_i", r"p_i", r"\log_2", r"\frac{2^{-\ell_i}}{p_i}"],
            ["H - L", r"\le", r"\log_2", r"\sum_i", r"p_i", r"\frac{2^{-\ell_i}}{p_i}"],
            ["H - L", r"\le", r"\log_2", r"\sum_i", r"2^{-\ell_i}"],
            ["H - L", r"\le", r"\log_2", "1", "= 0"],
        ]
        eqs = [cmath(*st, colors=colors, font_size=50).move_to(UP * 1.25) for st in steps]
        whys = [why(r"combine the two sums"), why(r"Jensen, as in Chapter 3"), why(r"the $p_i$ cancel"),
                why(r"Kraft")]
        for w in whys:
            w.scale(1.15).move_to(UP * 0.3)
        res = label(r"$L \ge H$, \ with equality only if every $\ell_i = \log_2 \frac{1}{p_i}$", font_size=34,
                    color=C.BITS).move_to(UP * 1.25)
        h_lab = MathTex(rf"H = {H:.2f}", font_size=34, color=C.SURPRISE).move_to([-4.3, -1.6, 0])
        with self.voiceover(
            "Now we can prove a speed limit. Let L be the average codeword length, and H the entropy. "
            "<bookmark mark='a'/> Write their difference as one sum. <bookmark mark='b'/> Jensen's inequality, "
            "exactly as in chapter three, moves the log outside. <bookmark mark='c'/> The probabilities cancel, "
            "<bookmark mark='d'/> and Kraft's inequality says what's left is at most log one: zero. "
            "<bookmark mark='e'/> So the average length can never be less than the entropy, and it equals the "
            "entropy only if each symbol gets exactly log one over p bits: its surprise."
        ) as vo:
            self.play(FadeIn(head), FadeIn(setup), Create(base),
                      LaggedStart(*[GrowFromEdge(sky[i], DOWN) for i in order], lag_ratio=0.03), run_time=1.8)
            self.play(FadeIn(h_lab))
            vo.wait_until("a")
            self.play(Write(eqs[0]), FadeIn(whys[0]))
            for k, mark in enumerate("bcd"):
                vo.wait_until(mark)
                self.play(FadeOut(whys[k]), FadeIn(whys[k + 1]), run_time=0.4)
                morph(self, eqs[k], eqs[k + 1], run_time=1.2, path_arc=-0.6 if k == 0 else 0.0)
            vo.wait_until("e")
            self.play(FadeOut(whys[3]), eqs[3].animate.scale(0.7).move_to(UP * 2.0), FadeIn(res, shift=DOWN * 0.1))
        ell = np.ceil(-np.log2(p))
        Ls = float((p * ell).sum())
        assert abs(Ls - hf["L_shannon"]) < 1e-9
        steps_up, cum = {}, 0.0
        for i in order:
            h = sc * ell[i]
            steps_up[i] = Rectangle(width=max(W * p[i], 0.003), height=h, stroke_width=1.2, stroke_color=C.BITS,
                                    fill_color=C.BITS, fill_opacity=0.3).move_to([-W / 2 + (cum + p[i] / 2) * W, y0 + h / 2, 0])
            cum += p[i]
        stair = VGroup(*[steps_up[i] for i in order])
        l_lab = MathTex(rf"L = {Ls:.2f}", font_size=34, color=C.BITS).next_to(h_lab, UP, buff=0.2).align_to(h_lab, LEFT)
        sh = label(rf"Shannon's code: \ $\ell_i = \lceil \log_2 \frac{{1}}{{p_i}} \rceil$, \ "
                   rf"$H \le L < H + 1$. \ Letters: ${Ls:.2f}$ bits", font_size=28, color=GREY_A)
        sh.next_to(res, DOWN, buff=0.35)
        with self.voiceover(
            "Codeword lengths must be whole numbers, so round the surprises up. We saw in the last chapter that "
            f"those lengths fit Kraft's budget, and it costs less than one extra bit per symbol. For our letters, "
            f"{Ls:.2f} bits."
        ):
            self.add(stair)
            self.bring_to_front(sky)
            self.play(LaggedStart(*[GrowFromEdge(r, DOWN) for r in stair], lag_ratio=0.04), run_time=2.0)
            self.play(FadeIn(l_lab), FadeIn(sh))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def huffman(self):
        hf = load("huffman")
        codes = {ALPHA27[i]: c for i, c in enumerate(hf["codes"])}
        merges = [list(map(float, m)) for m in hf["merges"]]
        children = {int(m[2]): (int(m[0]), int(m[1])) for m in merges}
        prefix = {int(hf["root"]): ""}
        stack = [int(hf["root"])]
        while stack:
            n = stack.pop()
            if n in children:
                a, b = children[n]
                prefix[a], prefix[b] = prefix[n] + "0", prefix[n] + "1"
                stack += [a, b]
        assert all(prefix[i] == codes[ALPHA27[i]] for i in range(27))
        tree = code_tree(codes, x_range=(-6.5, 6.5), y_top=2.2, dy=0.43, leaf_font=20, show_bits=False,
                         edge_width=2.2, dot_r=0.035)
        head = label(r"Huffman's algorithm (1952): \ merge the two least likely, repeat", font_size=32)
        head.to_edge(UP, buff=0.3)
        first = merges[0]
        f0, f1 = ALPHA27[int(first[0])], ALPHA27[int(first[1])]
        side = VGroup(*[MathTex(rf"\texttt{{{ALPHA27[int(m[0])] if m[0] < 27 else '*'}}} + "
                                rf"\texttt{{{ALPHA27[int(m[1])] if m[1] < 27 else '*'}}} \to {m[3]:.4f}", font_size=24,
                                color=GREY_A) for m in merges[:3]])
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(DL, buff=0.45)
        src = cite(r"G.~Stix, \textit{Profile: David A. Huffman}, Scientific American (1991)", corner=DR)
        with self.voiceover(
            "Which code gets closest? In 1951 David Huffman, a graduate student in Robert Fano's class at MIT, was "
            "offered a choice: sit the final exam, or write a paper on finding the most efficient code. He chose "
            f"the paper. <bookmark mark='a'/> His answer: take the two least likely symbols, here {f0} and {f1}, and "
            "join them under a new node whose probability is their sum. Then do it again with the two least likely "
            f"of what's left, and again, <bookmark mark='b'/> {len(merges)} times, until one tree holds everything."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tree.leaves.values())), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(side), FadeOut(src))
            groups = []
            for m in merges:
                pre = prefix[int(m[2])]
                groups.append(AnimationGroup(Create(tree.edges[pre + "0"]), Create(tree.edges[pre + "1"]),
                                             FadeIn(tree.nodes[pre])))
            vo.wait_until("b")
            self.play(LaggedStart(*groups, lag_ratio=0.5), run_time=max(3.0, vo.remaining() - 0.3))
        L, H = float(hf["L"]), float(hf["H"])
        nb, nf = len(hf["word_bits"]), int(hf["fixed_bits"])
        tab = VGroup()
        for s in " etaz":
            tab.add(VGroup(letter(s, font_size=24), Text(codes[s], font=MONO, font_size=22, color=C.BITS))
                    .arrange(RIGHT, buff=0.25))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_corner(DR, buff=0.45)
        res = VGroup(
            label(rf"average: \ $L = {L:.3f}$ bits per symbol", font_size=28, color=C.BITS),
            label(rf"entropy: \ $H = {H:.3f}$", font_size=28, color=C.ENTROPY),
            label(rf"\texttt{{the falcon}}: \ ${nb}$ bits, \ not ${nf}$", font_size=28, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(DL, buff=0.45)
        ln = {s: len(codes[s]) for s in " ez"}
        with self.voiceover(
            f"Read off the codewords: <bookmark mark='a'/> the space gets {ln[' ']} bits, e gets {ln['e']}, and z gets "
            f"{ln['z']}. <bookmark mark='b'/> On average, {L:.3f} bits per symbol, just {L - H:.3f} above the entropy. "
            f"The falcon now costs {nb} bits instead of {nf}."
        ) as vo:
            self.play(FadeOut(side))
            vo.wait_until("a")
            self.play(FadeIn(tab))
            vo.wait_until("b")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def exchange(self):
        ho = load("huffopt")
        p = load("letters")["p"]
        le, lz, cost = int(ho["le"]), int(ho["lz"]), float(ho["swap_cost"])
        pe, pz = float(p[ALPHA27.index("e")]), float(p[ALPHA27.index("z")])
        head = label(r"Why nothing beats it: \ three exchanges", font_size=36).to_edge(UP, buff=0.35)
        # 1. likelier symbols never get longer codewords
        swap = mtex(r"\Delta L = p_i\,\ell_j + p_j\,\ell_i - p_i\,\ell_i - p_j\,\ell_j = -(p_i - p_j)(\ell_i - \ell_j)",
                    font_size=32).next_to(head, DOWN, buff=0.4)
        cond = label(r"if $p_i > p_j$ but $\ell_i > \ell_j$: \ swapping their codewords makes $\Delta L < 0$",
                     font_size=26, color=GREY_A).next_to(swap, DOWN, buff=0.2)
        ex = label(rf"\texttt{{e}} with \texttt{{z}}'s ${lz}$ bits, \ \texttt{{z}} with \texttt{{e}}'s ${le}$: \ "
                   rf"$({pe:.4f} - {pz:.4f}) \times ({lz} - {le}) = {cost:.3f}$ bits worse", font_size=26, color=C.SURPRISE)
        ex.next_to(cond, DOWN, buff=0.25)
        # 2 and 3: the deepest leaves come in pairs, and the two rarest can be put there
        def mini(lone: bool):
            r = np.array([0, 0, 0])
            pts = {"": r, "0": r + np.array([-0.8, -0.7, 0]), "1": r + np.array([0.8, -0.7, 0]),
                   "10": r + np.array([0.3, -1.4, 0]), "11": r + np.array([1.3, -1.4, 0])}
            keys = ["0", "1", "10"] + ([] if lone else ["11"])
            g = VGroup(*[Line(pts[k[:-1]], pts[k], color=C.BIT0 if k[-1] == "0" else C.BIT1, stroke_width=3)
                         for k in keys])
            g.add(*[Dot(pts[k], radius=0.07, color=GREY_A) for k in [""] + keys])
            return g, pts

        lone, lp = mini(True)
        lone.move_to([-4.2, -1.7, 0])
        fix = Arrow(lone[-1].get_center() + UP * 0.1, lone[-2].get_center() + DOWN * 0.05, buff=0.1, color=C.BITS,
                    stroke_width=3, max_tip_length_to_length_ratio=0.25)
        t2 = label(r"a deepest leaf with no sibling: \\ move it up a level, \ $L$ drops", font_size=22, color=GREY_A)
        t2.next_to(lone, DOWN, buff=0.25)
        pair, pp = mini(False)
        pair.move_to([1.0, -1.7, 0])
        rx = VGroup(letter(ho["rare"][0], font_size=26, color=C.BITS).next_to(pair[-2], DOWN, buff=0.1),
                    letter(ho["rare"][1], font_size=26, color=C.BITS).next_to(pair[-1], DOWN, buff=0.1))
        t3 = label(r"so the deepest leaves come in pairs, \\ and the two rarest symbols can sit there", font_size=22,
                   color=GREY_A).next_to(pair, DOWN, buff=0.55)
        rare_codes = VGroup(*[Text(c, font=MONO, font_size=22, color=C.BITS) for c in ho["rare_codes"]])
        rare_codes.arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([5.2, -1.4, 0])
        rc_l = label(rf"in Huffman's code: \ \texttt{{{ho['rare'][0]}}} and \texttt{{{ho['rare'][1]}}}", font_size=22,
                     color=GREY_A).next_to(rare_codes, UP, buff=0.15)
        with self.voiceover(
            "Huffman proved that no prefix code does better, with a few exchanges. <bookmark mark='a'/> First: if "
            "a likelier symbol had a longer codeword than a rarer one, swapping the two codewords would shorten the "
            f"average. Give e the {lz} bits of z, and z the {le} bits of e, and every letter costs {cost:.2f} bits "
            "more on average. So in a best code, likelier symbols never get longer codewords. "
            "<bookmark mark='b'/> Second: a codeword at the bottom of the tree with no sibling could just move up a "
            "level, and be shorter. So the deepest codewords come in pairs. <bookmark mark='c'/> And by the first "
            "exchange, the two rarest symbols can be put in such a pair: in Huffman's code, they are "
            f"{ho['rare'][0]} and {ho['rare'][1]}, differing only in the last bit."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(swap), FadeIn(cond))
            self.play(FadeIn(ex))
            vo.wait_until("b")
            self.play(Create(lone), FadeIn(t2))
            self.play(GrowArrow(fix))
            vo.wait_until("c")
            self.play(Create(pair), FadeIn(rx), FadeIn(t3))
            self.play(FadeIn(rc_l), FadeIn(rare_codes))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def induction(self):
        ho = load("huffopt")
        L, opt, merged = float(ho["L"]), float(ho["opt27"]), float(ho["merged"])
        n_tr, n_bf = int(ho["n_trials"]), int(ho["brute_checked"])
        n_sizes = sorted({int(n) for n in ho["trial_n"]})
        head = label(r"Merge, and the problem shrinks by one", font_size=36).to_edge(UP, buff=0.35)
        rows = [
            cmath(r"L(\text{code})", r"=", r"L(\text{merged code})", r"+", r"p_x + p_y", font_size=40,
                  colors={r"p_x + p_y": C.BITS}),
        ]
        expl = label(r"split the merged leaf $xy$ into $x$ and $y$: \ both get one more bit", font_size=26,
                     color=GREY_A).next_to(rows[0], DOWN, buff=0.3)
        VGroup(rows[0], expl).next_to(head, DOWN, buff=0.45)
        th = theorem_card(r"Huffman's code is optimal", r"no prefix code for single symbols has a smaller average length",
                          who=r"D.~A.~Huffman, \textit{A Method for the Construction of Minimum-Redundancy Codes} (1952)",
                          width=9.0, color=C.BITS).move_to(DOWN * 0.5)
        checks = VGroup(
            label(rf"its $26$ merged weights add up to $L$: \ ${merged:.3f}$", font_size=24, color=GREY_A),
            label(rf"every tree shape, searched: \ the best for the $27$ letters is ${opt:.3f}$", font_size=24,
                  color=GREY_A),
            label(rf"${n_tr}$ random alphabets of ${n_sizes[0]}$ to ${n_sizes[-1]}$ symbols: \ Huffman matched the "
                  rf"exhaustive optimum every time", font_size=24, color=C.BITS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(DOWN, buff=0.35)
        tag = computed_tag().to_corner(UR, buff=0.3)
        same = "the same" if abs(opt - L) < 1e-9 else f"{opt:.3f}"
        with self.voiceover(
            "Now merge those two rarest symbols into one, whose probability is their sum. <bookmark mark='a'/> Any "
            "code for the smaller alphabet becomes a code for the original by splitting that leaf in two, and the "
            "average length goes up by exactly the merged probability, whatever the rest of the code. So the best "
            "code for the original is the best code for the smaller problem, plus that split. <bookmark mark='b'/> "
            "That's Huffman's first merge, and the same argument covers every merge after it: the tree he builds "
            "is optimal. <bookmark mark='c'/> We checked. Add up the weights of the merges: "
            f"{merged:.3f}, Huffman's average. Search every possible shape of code tree for the letters: the best "
            f"is {same}. And on {n_tr} random alphabets, Huffman's code matched the exhaustive search every time."
        ) as vo:
            self.play(FadeIn(head), Write(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(expl))
            vo.wait_until("b")
            self.play(FadeIn(th, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(c) for c in checks], lag_ratio=0.5), FadeIn(tag), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()
