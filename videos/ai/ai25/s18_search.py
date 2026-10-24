from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai25.common import (AUG, HIST, LEAN_C, PAIR_C, PART, PLAIN, PRED_C, SEARCH_C, STRUCT, SYM, TRUE_C,
                                   load, matrix_image, node_box, take_away, takeaway_anims, tiny_words, words_num)


class Search(VoiceoverScene):
    def construct(self):
        self.card()
        self.loop()
        self.binpack()
        self.tensor()
        self.alphaevolve()

    def card(self):
        card = chapter_card(17, r"Discovery by search", r"What can a machine find when every guess is checked?",
                            lit=(), part=PART)
        with self.voiceover("Chapter seventeen. Discovery by search."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def loop(self):
        boxes = VGroup(node_box(r"propose: \ a program, \ a construction", PRED_C, font_size=24, height=0.9),
                       node_box(r"evaluate: \ an exact score", LEAN_C, font_size=24, height=0.9),
                       node_box(r"keep the best, \ vary them", SEARCH_C, font_size=24, height=0.9))
        boxes[0].move_to([-3.6, 1.8, 0])
        boxes[1].move_to([3.2, 1.8, 0])
        boxes[2].move_to([0, -0.2, 0])
        arr = VGroup(Arrow(boxes[0].get_right(), boxes[1].get_left(), buff=0.1, color=GREY_B, stroke_width=3),
                     Arrow(boxes[1].get_bottom(), boxes[2].get_right(), buff=0.1, color=GREY_B, stroke_width=3),
                     Arrow(boxes[2].get_left(), boxes[0].get_bottom(), buff=0.1, color=GREY_B, stroke_width=3))
        ex = VGroup(
            label(r"AlphaTensor (2022): \ the proposer is an AlphaZero network \ (Part 26)", font_size=22,
                  color=GREY_A),
            label(r"FunSearch (2023): \ a language model writes Python; \ an island-based database of programs",
                  font_size=22, color=GREY_A),
            label(r"cap sets in dimension $8$: \ $512$ points with no three on a line, \ up from $496$", font_size=22,
                  color=PAIR_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.45)
        cite_ = cite(r"Fawzi et al.\ (2022); \ Romera-Paredes et al., \textit{Nature} (2024)", corner=UR)
        with self.voiceover(
            "When the checker is exact, discovery becomes a loop. <bookmark mark='a'/> Propose a candidate, a "
            "program or a construction; <bookmark mark='b'/> score it exactly; <bookmark mark='c'/> keep the best "
            "and vary them. <bookmark mark='d'/> AlphaTensor, in Part 26, used an AlphaZero network as the proposer. "
            "In December 2023 Bernardino Romera-Paredes and colleagues at Google DeepMind made the proposer a "
            "language model writing Python, in FunSearch, with a database of programs kept on separate islands, "
            "like populations in evolution. <bookmark mark='e'/> It found a cap set in eight dimensions, five "
            "hundred and twelve points with no three in a line, beating the four hundred and ninety-six known, the "
            "largest jump in that problem in twenty years."
        ) as vo:
            self.play(FadeIn(boxes[0]), FadeIn(cite_))
            vo.wait_until("a")
            self.play(GrowArrow(arr[0]), FadeIn(boxes[1]))
            vo.wait_until("b")
            self.play(GrowArrow(arr[1]), FadeIn(boxes[2]))
            vo.wait_until("c")
            self.play(GrowArrow(arr[2]))
            vo.wait_until("d")
            self.play(FadeIn(ex[0]), FadeIn(ex[1]))
            vo.wait_until("e")
            self.play(FadeIn(ex[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def binpack(self):
        b = load("binpack")
        hist = b["s0"]["history"]
        gens = np.array([h["gen"] for h in hist])
        best = np.array([h["score"] for h in hist])
        med = np.array([h["median"] for h in hist])
        bf_tr, ff_tr = b["bf_train"], b["ff_train"]
        lo = float(np.floor(min(best.min(), bf_tr) - 0.5))
        hi = float(np.ceil(max(ff_tr, min(np.percentile(med, 80), ff_tr + 4)) + 0.5))
        g = axes([0, gens[-1]], [lo, hi], x_length=5.4, y_length=3.4, xlabel=r"generation",
                 ylabel=r"extra bins \ (\% above the lower bound)", xticks=[0, gens[-1]], yticks=[lo, hi],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", center=[-3.1, 0.6, 0])
        bf = DashedLine(g.ax.c2p(0, bf_tr), g.ax.c2p(gens[-1], bf_tr), color=PLAIN)
        ff = DashedLine(g.ax.c2p(0, min(ff_tr, hi)), g.ax.c2p(gens[-1], min(ff_tr, hi)), color=GREY_C)
        bfl = label(r"best fit", font_size=20, color=PLAIN).next_to(bf, UP, buff=0.06).align_to(bf, LEFT).shift(RIGHT * 0.15)
        ffl = label(r"first fit", font_size=20, color=GREY_C).next_to(ff, UP, buff=0.06).align_to(ff, LEFT).shift(RIGHT * 0.15)
        cb = curve(g.ax, gens, best, SEARCH_C, 3.5)
        what = VGroup(
            label(r"items arrive one at a time; \\ each must go in a bin of size $100$ at once", font_size=22),
            label(r"a \textit{priority function} scores every bin it fits in: \\ $s$ the item, \ $r$ the room left, \ "
                  r"$g = r - s$", font_size=22),
            label(r"best fit: \ priority $-g$, \ the tightest bin", font_size=22, color=PLAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        for w_ in what:
            if w_.width > 6.3:
                w_.width = 6.3
        what.move_to([0, 2.0, 0]).align_to(np.array([0.6, 0, 0]), LEFT)
        seeds = [k for k in ("s0", "s1") if k in b]
        tests = [b[k]["test"] for k in seeds]
        bf_te, ff_te = b["bf_test"], b["ff_test"]
        formula = label(r"evolved, \ seed $0$: \ " + "$" + b["s0"]["best"].replace("|", r"|").replace("*", r"\cdot ")
                        + "$", font_size=20, color=SEARCH_C)
        formula.width = min(formula.width, 6.3)
        formula.move_to([0, -0.2, 0]).align_to(np.array([0.6, 0, 0]), LEFT)
        res = VGroup(
            label(rf"held-out, \ $1{{,}}000$ items: \ first fit ${ff_te:.2f}\%$, \ best fit ${bf_te:.2f}\%$",
                  font_size=21, color=GREY_A),
            label(r"evolved: \ " + r", \ ".join(rf"${t:.2f}\%$" for t in tests), font_size=21, color=SEARCH_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        res.move_to([0, -1.3, 0]).align_to(np.array([0.6, 0, 0]), LEFT)
        caveat = label(r"Sim, Renau \& Hart (2025): \ heuristics evolved this way often fail to generalize beyond "
                       r"their benchmark", font_size=20, color=GREY_B).to_edge(DOWN, buff=0.35)
        better = [t for t in tests if t < bf_te - 0.02]
        if len(better) == len(tests):
            res_line = (f"On new, longer sequences of items, both evolved rules still beat best fit: {tests[0]:.2f} "
                        f"and {tests[-1]:.2f} percent against {bf_te:.2f}")
        elif better:
            res_line = (f"On new, longer sequences, {words_num(len(better))} of the {words_num(len(tests))} evolved "
                        f"rules beats best fit, {min(better):.2f} percent against {bf_te:.2f}; the other doesn't")
        else:
            res_line = (f"On new, longer sequences of items, neither evolved rule beats best fit's {bf_te:.2f} "
                        "percent: what evolution found was tuned to its training instances")
        if len(better) == len(tests):
            gen_line = ("Ours carried over; but an independent study in 2025 found that heuristics evolved by language "
                        "models often don't generalize beyond the instances they were bred on")
        else:
            gen_line = ("An independent study in 2025 found the same of heuristics evolved by language models: they "
                        "often don't generalize beyond the instances they were bred on")
        gain = bf_tr - best[-1]
        evo_line = (f"Within {int(gens[-1])} generations it beats best fit on its training instances by "
                    f"{gain:.2f} points" if gain > 0.02 else
                    f"In {int(gens[-1])} generations it never beats best fit on its training instances")
        tag = note(r"computed: \ random mutation in place of the language model; \ $60$ formulas a generation",
                   font_size=18).to_corner(DR, buff=0.15)
        with self.voiceover(
            "Let's run that loop ourselves, on one of FunSearch's problems: online bin packing. <bookmark mark='a'/> "
            "Items arrive one at a time, and each must go into a bin at once. A rule decides: score every bin the "
            "item fits in, and pick the highest. <bookmark mark='b'/> The classic is best fit: the bin with the "
            "least room left. <bookmark mark='c'/> We evolve such scores as formulas, with random mutations and "
            "crossings standing in for the language model, judged by how many bins they use on eight training "
            f"sequences. {evo_line}. <bookmark mark='d'/> {res_line}. <bookmark mark='e'/> {gen_line}."
        ) as vo:
            self.play(FadeIn(g), FadeIn(what[0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(what[1]))
            vo.wait_until("b")
            self.play(FadeIn(what[2]), Create(bf), FadeIn(bfl), Create(ff), FadeIn(ffl))
            vo.wait_until("c")
            self.play(Create(cb), run_time=2.5)
            self.play(FadeIn(formula))
            vo.wait_until("d")
            self.play(FadeIn(res))
            vo.wait_until("e")
            self.play(FadeIn(caveat))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tensor(self):
        mm = load("matmul")
        rows = [
            cmath(r"c_{ik}", r"=", r"\sum_j a_{ij}\, b_{jk}", font_size=34),
            cmath(r"T", r"=", r"\sum_{r=1}^{R} u_r \otimes v_r \otimes w_r", font_size=34),
            cmath(r"m_r", r"=", r"(u_r \cdot a)\,(v_r \cdot b)", r",\quad", r"c = \sum_r m_r\, w_r", font_size=34),
        ]
        rows[1][2].set_color(SEARCH_C)
        whys = [why(r"$n^3$ multiplications, \ the schoolbook way"),
                why(r"matrix multiplication as a $n^2 \times n^2 \times n^2$ tensor"),
                why(r"rank $R$: \ an algorithm with $R$ multiplications")]
        step = ladder(self, rows, whys, keep=3, top=2.8, x=-1.4, buff=0.5, edge=6.9)
        hist = VGroup(
            label(r"Strassen (1969): \ $2 \times 2$ in $7$, \ not $8$; \ Winograd (1971): \ $7$ is the minimum",
                  font_size=22, color=HIST),
        ).move_to([0, -1.2, 0])
        res = []
        for R in (6, 7, 8):
            r_ = mm[f"n2_r{R}"]
            res.append((R, r_["success"], len(r_["res"]), r_["best"]))
        tab = VGroup(label(r"our search: \ alternating least squares, \ $30$ random starts per rank", font_size=22,
                           color=GREY_A))
        for R, s_, n_, best in res:
            col = SEARCH_C if s_ else PLAIN
            tab.add(label(rf"rank ${R}$: \ ${s_}$ of ${n_}$ reach zero error \ (best ${sci(best, 1)}$)",
                          font_size=22, color=col))
        n3a, n3b = mm["n3_r23"], mm["n3_r26"]
        n3_tries = len(n3a["res"])
        tab.add(label(rf"$3 \times 3$, \ rank $23$ \ (Laderman, 1976): \ ${n3a['success']}$ of ${n3_tries}$ \ "
                      rf"(best ${sci(min(n3a['best'], n3b['best']), 1)}$, \ even at rank $26$)", font_size=22,
                      color=SEARCH_C if n3a["success"] else GREY_B))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.13).move_to([0, -2.65, 0])
        ver = mm["n2_r7_verify"]
        vdp = int(np.floor(-np.log10(max(ver, 1e-300))))
        r6, r7, r8 = res
        s6 = (f"At rank six, none of the {r6[2]} starts gets below an error of {r6[3]:.2f}: there is no "
              "six-multiplication algorithm to find" if r6[1] == 0 else
              f"At rank six, {r6[1]} starts report zero error, which would contradict the theorem: a numerical "
              "artefact")
        s7 = (f"At rank seven, {r7[1]} of {r7[2]} starts find one: a Strassen-like algorithm, which multiplies "
              f"random matrices correctly to {vdp} decimal places" if r7[1] else "At rank seven our search found none")
        n3_ok = n3a["success"]
        if n3_ok:
            s3 = (f"For three by three matrices the record, Julian Laderman's from 1976, is twenty-three "
                  f"multiplications, and {n3_ok} of our {n3_tries} starts at that rank found one")
        else:
            tiny3 = tiny_words(min(n3a["best"], n3b["best"]))
            s3 = (f"For three by three matrices the record, Julian Laderman's from 1976, is twenty-three "
                  f"multiplications; from {n3_tries} starts at that rank, and as many at twenty-six, our search got "
                  f"within {tiny3} of zero but never exactly there: as the matrices grow, exact decompositions become "
                  "needles in a haystack")
        tag = note(r"computed", font_size=20).to_corner(DR, buff=0.2)
        head = label(r"matrix multiplication as a tensor", font_size=30, color=SEARCH_C).to_edge(UP, buff=0.25)
        with self.voiceover(
            "Matrix multiplication is the purest case. <bookmark mark='a'/> The schoolbook way to multiply two n by "
            "n matrices uses n cubed multiplications. <bookmark mark='b'/> Write the product as a three-way tensor; "
            "<bookmark mark='c'/> then every way of writing that tensor as a sum of R simple products is an "
            "algorithm with R multiplications. <bookmark mark='d'/> In 1969 Volker Strassen found seven for two by "
            "two matrices, not eight, and Shmuel Winograd proved two years later that seven is the minimum. "
            "<bookmark mark='e'/> We searched for these decompositions numerically, from thirty random starts at "
            f"each rank. {s6}. {s7}. <bookmark mark='f'/> {s3}."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                step(k)
            vo.wait_until("d")
            self.play(FadeIn(hist))
            vo.wait_until("e")
            self.play(FadeIn(tab[0]), LaggedStart(*[FadeIn(t_) for t_ in tab[1:4]], lag_ratio=0.4), FadeIn(tag),
                      run_time=2.5)
            vo.wait_until("f")
            self.play(FadeIn(tab[4]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def alphaevolve(self):
        head = label(r"AlphaEvolve \ (Google DeepMind, May 2025)", font_size=34, color=SEARCH_C).to_edge(UP, buff=0.4)
        facts = VGroup(
            label(r"Gemini models propose changes to whole programs; \ evaluators score them; \ evolution keeps the "
                  r"best", font_size=22, color=GREY_A),
            label(r"$4 \times 4$ complex matrices in $48$ multiplications, \ beating $49$ \ (Strassen's, applied "
                  r"twice, 1969)", font_size=24, color=PAIR_C),
            label(r"found by evolving the code of a gradient-based search for decompositions, \ $15$ mutations "
                  r"deep", font_size=21, color=GREY_A),
            label(r"weeks later: \ $48$ with rational coefficients \ (Dumas, Pernet \& Sedoglavic, 2025)",
                  font_size=21, color=HIST),
            label(r"kissing number in $11$ dimensions: \ $593$; \ of $50$+ open problems: \ $75\%$ matched, \ $20\%$ "
                  r"improved", font_size=22, color=STRUCT),
            label(r"Google's own systems: \ $0.7\%$ of its compute recovered; \ a kernel $23\%$ faster, \ $1\%$ of "
                  r"Gemini's training time", font_size=22, color=GREY_A),
            label(r"67 problems with Tao, \ Georgiev, \ G\'omez-Serrano \& Wagner \ (November 2025)", font_size=22,
                  color=HIST),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.34)
        facts.width = min(facts.width * 1.15, 13.2)
        facts.next_to(head, DOWN, buff=0.45)
        for f_ in facts:
            if f_.width > 13.0:
                f_.width = 13.0
        facts.set_x(0)
        cite_ = cite(r"Novikov et al.\ (2025); \ Dumas et al.\ (2025); \ Georgiev et al.\ (2025)", corner=DR)
        with self.voiceover(
            "In May 2025 Google DeepMind combined both lines in AlphaEvolve. <bookmark mark='a'/> Gemini models "
            "propose changes to whole programs, evaluators score them, and evolution keeps the best. <bookmark "
            "mark='b'/> Among its results: four by four complex matrices multiplied with forty-eight "
            "multiplications, beating the forty-nine of applying Strassen's trick twice, the record since 1969. "
            "<bookmark mark='c'/> It got there by evolving the code of exactly the kind of decomposition search we "
            "just ran. <bookmark mark='d'/> Within weeks, three researchers in France found a forty-eight with "
            "rational coefficients. <bookmark mark='e'/> It also set a record for spheres touching a central one in "
            "eleven dimensions, 593, and on more than fifty open problems matched the best known answer in three "
            "quarters and improved it in a fifth. <bookmark mark='f'/> Inside Google, a scheduling rule it found "
            "recovers 0.7 percent of the company's computing. <bookmark mark='g'/> In November 2025 Terence Tao and "
            "colleagues turned it loose on sixty-seven problems, and published where it succeeded and where it "
            "failed."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cite_))
            for k, mk in enumerate("abcdefg"):
                vo.wait_until(mk)
                self.play(FadeIn(facts[k], shift=UP * 0.1))
        self.wait(0.6)
        tk = take_away(r"discovery by search: \ propose freely, \ check exactly, \ keep what survives")
        with self.voiceover(
            "Discovery by search, then: propose freely, check exactly, keep what survives. It works wherever the "
            "checking is exact, which is why mathematics and algorithms went first."
        ):
            self.play(FadeIn(tk, shift=UP * 0.1), *takeaway_anims(self, tk))
        self.wait(0.3)
        self.clear_scene()
