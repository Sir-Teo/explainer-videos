from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai25.common import (HIST, KIND_COLOR, KIND_NAME, MSA_C, PAIR_C, PART, PLAIN, PRED_C, STRUCT, SYM,
                                   TRUE_C, crossfade, hbars, load, matrix_image, node_box, take_away)


class Evoformer(VoiceoverScene):
    def construct(self):
        self.card()
        self.overview()
        self.exchange()
        self.triangles()
        self.experiment()
        self.replay()
        self.casp14()

    def card(self):
        card = chapter_card(9, r"AlphaFold 2: \ the Evoformer", r"How do you reason about pairs?", lit=(), part=PART)
        with self.voiceover("Chapter nine. AlphaFold 2: the Evoformer."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def overview(self):
        b = [node_box(r"sequence", GREY_A, font_size=24),
             node_box(r"related sequences \ (MSA) \ + templates", MSA_C, font_size=22),
             node_box(r"Evoformer \ $\times 48$", PAIR_C, font_size=26, height=1.0),
             node_box(r"structure module \ $\times 8$", STRUCT, font_size=24, height=1.0),
             node_box(r"3D coordinates \ + confidence", TRUE_C, font_size=22)]
        b[0].move_to([-5.6, 1.6, 0])
        b[1].move_to([-5.0, -0.2, 0])
        b[2].move_to([-1.2, 0.7, 0])
        b[3].move_to([2.5, 0.7, 0])
        b[4].move_to([5.6, 0.7, 0])
        arr = VGroup(Arrow(b[0].get_bottom(), b[1].get_top(), buff=0.08, color=GREY_B, stroke_width=2.5),
                     Arrow(b[1].get_right(), b[2].get_left(), buff=0.08, color=GREY_B, stroke_width=2.5),
                     Arrow(b[2].get_right(), b[3].get_left(), buff=0.08, color=GREY_B, stroke_width=2.5),
                     Arrow(b[3].get_right(), b[4].get_left(), buff=0.08, color=GREY_B, stroke_width=2.5))
        rec = CurvedArrow(b[4].get_bottom() + DOWN * 0.05, b[2].get_bottom() + DOWN * 0.05, angle=-0.7,
                          color=PRED_C, stroke_width=2.5, tip_length=0.18)
        rl = label(r"recycling: \ the output goes round again", font_size=22, color=PRED_C).next_to(rec, DOWN,
                                                                                                buff=0.1)
        reps = VGroup(
            label(r"MSA representation: \ $s$ sequences $\times$ $r$ residues $\times$ $c$ channels", font_size=22,
                  color=MSA_C),
            label(r"pair representation: \ $r \times r \times c$: \ a vector for every pair of residues", font_size=22,
                  color=PAIR_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.4)
        sch = note(r"schematic, \ after Jumper et al.\ (2021)", font_size=20).to_corner(UR, buff=0.25)
        with self.voiceover(
            "AlphaFold 2, which John Jumper and colleagues at DeepMind entered in CASP14 in 2020, works in two "
            "stages. <bookmark mark='a'/> It starts from the sequence and searches genetic databases for related "
            "sequences, lined up in a multiple sequence alignment, plus known structures of similar proteins. "
            "<bookmark mark='b'/> The first stage, the Evoformer, forty-eight blocks deep, reasons about these, "
            "<bookmark mark='c'/> and the second, the structure module, turns the result into coordinates for every "
            "atom, with a confidence for each residue. <bookmark mark='d'/> Then the whole thing runs again, fed its "
            "own output. <bookmark mark='e'/> The Evoformer keeps two representations: one for the alignment, a "
            "vector for every residue of every sequence; and one for pairs, a vector for every pair of residues, "
            "the learned descendant of AlphaFold 1's distance histograms."
        ) as vo:
            self.play(FadeIn(b[0]), FadeIn(sch))
            vo.wait_until("a")
            self.play(GrowArrow(arr[0]), FadeIn(b[1]))
            vo.wait_until("b")
            self.play(GrowArrow(arr[1]), FadeIn(b[2]))
            vo.wait_until("c")
            self.play(GrowArrow(arr[2]), FadeIn(b[3]), GrowArrow(arr[3]), FadeIn(b[4]))
            vo.wait_until("d")
            self.play(Create(rec), FadeIn(rl))
            vo.wait_until("e")
            self.play(FadeIn(reps))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def exchange(self):
        r, s = 12, 7
        cell = 0.26
        msa = VGroup(*[Square(cell, stroke_width=0.6, stroke_color=GREY_D, fill_color=MSA_C,
                              fill_opacity=0.15 + 0.5 * ((i * 7 + j * 3) % 5) / 5) for i in range(s) for j in range(r)])
        msa.arrange_in_grid(s, r, buff=0.02).move_to([-3.6, 0.4, 0])
        pair = VGroup(*[Square(cell, stroke_width=0.6, stroke_color=GREY_D, fill_color=PAIR_C,
                               fill_opacity=0.1 + 0.6 * np.exp(-abs(i - j) / 3)) for i in range(r) for j in range(r)])
        pair.arrange_in_grid(r, r, buff=0.02).move_to([3.4, 0.4, 0])
        ml = label(r"MSA: \ sequences $\times$ residues", font_size=22, color=MSA_C).next_to(msa, UP, buff=0.2)
        pl = label(r"pairs: \ residues $\times$ residues", font_size=22, color=PAIR_C).next_to(pair, UP, buff=0.2)
        row = SurroundingRectangle(VGroup(*msa[2 * r:3 * r]), color=WHITE, buff=0.03, stroke_width=2)
        col = SurroundingRectangle(VGroup(*[msa[i * r + 5] for i in range(s)]), color=WHITE, buff=0.03,
                                   stroke_width=2)
        a1 = CurvedArrow(pair.get_left() + UP * 0.6, msa.get_right() + UP * 0.6, angle=0.5, color=PAIR_C,
                         stroke_width=3, tip_length=0.18)
        a2 = CurvedArrow(msa.get_right() + DOWN * 0.6, pair.get_left() + DOWN * 0.6, angle=0.5, color=MSA_C,
                         stroke_width=3, tip_length=0.18)
        l1 = label(r"attention along each sequence, \\ biased by the pairs", font_size=20, color=PAIR_C)
        l1.next_to(a1, UP, buff=0.08)
        l2 = label(r"outer products of columns: \\ which positions vary together", font_size=20, color=MSA_C)
        l2.next_to(a2, DOWN, buff=0.08)
        lc = label(r"attention down each column: \ across species", font_size=20, color=GREY_A).next_to(msa, DOWN,
                                                                                                    buff=0.9)
        with self.voiceover(
            "Each Evoformer block passes information both ways between them. <bookmark mark='a'/> Along each "
            "sequence, the residues attend to one another, and the pair representation biases that attention: "
            "what the network believes about pairs shapes how it reads the sequences. <bookmark mark='b'/> Down each "
            "column, the same position attends across species. <bookmark mark='c'/> And back the other way, an outer "
            "product of two columns of the alignment, averaged over the sequences, updates the pair of those two "
            "positions: the learned version of co-evolution, two columns that vary together."
        ) as vo:
            self.play(FadeIn(msa), FadeIn(pair), FadeIn(ml), FadeIn(pl))
            vo.wait_until("a")
            self.play(Create(row), Create(a1), FadeIn(l1))
            vo.wait_until("b")
            self.play(ReplacementTransform(row, col), FadeIn(lc))
            vo.wait_until("c")
            self.play(Create(a2), FadeIn(l2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def triangles(self):
        P = {"i": np.array([-5.4, -0.4, 0]), "j": np.array([-2.4, -0.4, 0]), "k": np.array([-3.9, 1.9, 0])}
        dots = VGroup(*[Dot(P[k], radius=0.12, color=SYM) for k in "ijk"])
        names = VGroup(*[MathTex(k, font_size=34, color=SYM).next_to(P[k], DOWN if k != "k" else UP, buff=0.12)
                         for k in "ijk"])
        e_ij = Line(P["i"], P["j"], color=PAIR_C, stroke_width=5)
        e_ik = Line(P["i"], P["k"], color=GREY_B, stroke_width=3)
        e_jk = Line(P["j"], P["k"], color=GREY_B, stroke_width=3)
        ineq = MathTex(r"d_{ij} \le d_{ik} + d_{kj}", font_size=34).next_to(VGroup(dots, names), DOWN, buff=0.4)
        rows = [
            cmath(r"z_{ij}", r"\mathrel{+}=", r"g_{ij} \odot \mathrm{Lin}\Big(\mathrm{LN}\Big(\sum_k a_{ik} \odot "
                  r"b_{jk}\Big)\Big)", font_size=32),
            cmath(r"z_{ij}", r"\mathrel{+}=", r"g_{ij} \odot \mathrm{Lin}\Big(\mathrm{LN}\Big(\sum_k a_{ki} \odot "
                  r"b_{kj}\Big)\Big)", font_size=32),
        ]
        for r_ in rows:
            r_[0].set_color(PAIR_C)
        whys = [why(r"`outgoing': \ the edges $ik$ and $jk$"), why(r"`incoming': \ the edges $ki$ and $kj$")]
        step = ladder(self, rows, whys, keep=2, top=2.4, x=2.3, buff=0.7, edge=6.9)
        n = 10
        cell = 0.24
        grid = VGroup(*[Square(cell, stroke_width=0.6, stroke_color=GREY_D, fill_color="#121722", fill_opacity=1)
                        for _ in range(n * n)]).arrange_in_grid(n, n, buff=0.02).move_to([2.3, -1.6, 0])
        i_, j_ = 2, 6
        tgt = grid[i_ * n + j_].copy().set_fill(PAIR_C, 0.9)
        att = label(r"plus triangle attention: \ pair $ij$ attends over the pairs $ik$", font_size=20, color=GREY_A)
        att.next_to(grid, RIGHT, buff=0.3)
        att.width = min(att.width, 2.6)
        link = label(r"a pair, \ updated through a third node: \ chapter 5's network that saw triangles",
                     font_size=22, color=STRUCT).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The new idea is in how the pairs update each other. Think of the pair representation as a guess at the "
            "distance between every two residues. <bookmark mark='a'/> Those guesses can't be independent: for any "
            "third residue k, the distance from i to j is at most the distance from i to k plus the distance from k "
            "to j. <bookmark mark='b'/> So the Evoformer updates each pair, i j, from the two other edges of every "
            "triangle it sits in: a sum over k of products of the pairs i k and j k, gated, the 'outgoing' update. "
            "<bookmark mark='c'/> And the same with the edges pointing in. <bookmark mark='d'/> In the pair matrix, "
            "entry i j collects row i and row j, position by position. <bookmark mark='e'/> Triangle attention does "
            "the same with attention weights. <bookmark mark='f'/> This is chapter five's lesson put to work: a "
            "network on pairs, updated through a third node, sees structure that message passing on single nodes "
            "cannot."
        ) as vo:
            self.play(FadeIn(dots), FadeIn(names), Create(e_ij))
            vo.wait_until("a")
            self.play(Create(e_ik), Create(e_jk), Write(ineq))
            vo.wait_until("b")
            step(0)
            vo.wait_until("c")
            step(1)
            vo.wait_until("d")
            self.play(FadeIn(grid), FadeIn(tgt))
            for k in range(n):
                hi = VGroup(grid[i_ * n + k].copy().set_fill(SYM, 0.8), grid[j_ * n + k].copy().set_fill(SYM, 0.8))
                self.play(FadeIn(hi), run_time=0.15)
                self.play(FadeOut(hi), run_time=0.1)
            vo.wait_until("e")
            self.play(FadeIn(att))
            vo.wait_until("f")
            self.play(FadeIn(link))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def experiment(self):
        p = load("pair")
        D = np.asarray(p["ex_true"])
        M = np.asarray(p["ex_mask"]).astype(bool)
        seen = np.asarray(p["ex_seen"])
        vmax = float(D.max())
        S = 2.5
        imgs = Group(
            matrix_image(D, S, 0, vmax),
            matrix_image(np.where(M, seen, 0), S, 0, vmax, mask=M | np.eye(len(D), dtype=bool)),
            matrix_image(np.asarray(p["ex_pairwise"]), S, 0, vmax),
            matrix_image(np.asarray(p["ex_triangle"]), S, 0, vmax),
        ).arrange(RIGHT, buff=0.35).move_to([0, 1.2, 0])
        caps = [(r"true distances", TRUE_C), (r"what the model sees", GREY_A), (KIND_NAME["pairwise"], PLAIN),
                (KIND_NAME["triangle"], STRUCT)]
        cl = VGroup(*[label(t, font_size=21, color=c).next_to(im, UP, buff=0.12) for (t, c), im in zip(caps, imgs)])
        kinds = ["pairwise", "triangle"]
        res = {k: [p[f"{k}_s{s}"]["hidden"] for s in (0, 1, 2)] for k in kinds}
        viol = {k: np.mean([p[f"{k}_s{s}"]["viol"] for s in (0, 1, 2)]) for k in kinds}
        par = {k: p[f"{k}_s0"]["params"] for k in kinds}
        sep = p["sep_baseline"]
        rows = hbars([(r"guess from the gap $|i - j|$ alone", sep, GREY_B),
                      (KIND_NAME["pairwise"], float(np.mean(res["pairwise"])), PLAIN),
                      (KIND_NAME["triangle"], float(np.mean(res["triangle"])), STRUCT)],
                     vmax=max(sep, max(np.mean(v) for v in res.values())) * 1.1, width=4.6, row_h=0.55,
                     name_w=3.8, fmt=lambda v: rf"${v:.1f}$\,\AA",
                     spread=[(sep, sep), (min(res["pairwise"]), max(res["pairwise"])),
                             (min(res["triangle"]), max(res["triangle"]))])
        rows.move_to([0.6, -1.8, 0])
        rl = label(r"error on the pairs it didn't see \ (RMSD of distances)", font_size=21, color=GREY_A)
        rl.next_to(rows, UP, buff=0.2)
        tag = note(rf"computed: \ random chains of ${p['n']}$ residues; \ ${par['pairwise']:,}$ and "
                   rf"${par['triangle']:,}$ weights; \ three seeds".replace(",", "{,}"), font_size=18)
        tag.to_corner(DR, buff=0.15)
        mp, mt = np.mean(res["pairwise"]), np.mean(res["triangle"])
        verdict = (f"Triangle updates cut it to {mt:.1f}, {mp / mt:.1f} times smaller" if mt < mp else
                   f"Triangle updates don't help here: {mt:.1f}")
        vtxt = (f"and their guesses break the triangle inequality {viol['pairwise'] / max(viol['triangle'], 1e-9):.0f} "
                "times less often" if viol["triangle"] < viol["pairwise"] else
                "though their guesses break the triangle inequality no less often")
        with self.voiceover(
            "Does it work? A small test, computed here. Random protein-like chains of "
            f"{p['n']} residues; the model sees a quarter of the pairs' distances, with noise, and must fill in all "
            "of them, a stand-in for what an alignment tells AlphaFold. <bookmark mark='a'/> Two models of the same "
            "size and the same training: one updates each pair on its own; the other with triangle updates. "
            f"<bookmark mark='b'/> Guessing each missing distance from how far apart the two residues are along the "
            f"chain gives an error of {sep:.1f} ångströms. Updating each pair on its own gets {mp:.1f}: it can't do "
            f"better, because it never looks at the other pairs. <bookmark mark='c'/> {verdict}, {vtxt}."
        ) as vo:
            self.play(FadeIn(imgs[0]), FadeIn(cl[0]), FadeIn(imgs[1]), FadeIn(cl[1]), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(imgs[2]), FadeIn(cl[2]), FadeIn(imgs[3]), FadeIn(cl[3]))
            vo.wait_until("b")
            self.play(FadeIn(rl), FadeIn(rows.rows[0]), FadeIn(rows.rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows.rows[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def replay(self):
        p = load("pair")
        snaps = [int(v) for v in p["snaps"]]
        D = np.asarray(p["ex_true"])
        vmax = float(D.max())
        kinds = ("pairwise", "triangle")
        fr = {k: np.asarray(p[f"{k}_s0"]["frames"]) for k in kinds}
        cv = {k: np.asarray(p[f"{k}_s0"]["curve"]) for k in kinds}
        S = 2.6
        xs = (-4.4, -0.9, 2.6)
        true_im = matrix_image(D, S, 0, vmax).move_to([xs[0], 1.45, 0])
        ims = {k: matrix_image(fr[k][0], S, 0, vmax).move_to([x, 1.45, 0]) for k, x in zip(kinds, xs[1:])}
        caps = VGroup(label(r"true distances", font_size=21, color=TRUE_C).next_to(true_im, UP, buff=0.12),
                      *[label(KIND_NAME[k], font_size=21, color=KIND_COLOR[k]).next_to(ims[k], UP, buff=0.12)
                        for k in kinds])
        stepl = label(r"step $0$", font_size=26, color=GREY_A).move_to([5.3, 1.45, 0])
        ymax = float(max(c_[:, 1].max() for c_ in cv.values())) * 1.05
        g = axes([0, snaps[-1]], [0, ymax], x_length=8.0, y_length=2.1, xlabel=r"training step",
                 ylabel=r"error, hidden pairs (\AA)", xticks=[0, snaps[-1] // 2, snaps[-1]],
                 yticks=[0, round(ymax / 2), round(ymax)], xfmt=lambda v: f"{v:,.0f}".replace(",", "{,}"),
                 font_size=18, center=[-0.6, -2.1, 0])
        tracker = ValueTracker(0)

        def upto(k):
            t = tracker.get_value()
            x, y = cv[k][:, 0], cv[k][:, 1]
            keep = x < t
            return curve(g.ax, [0.0, *x[keep][1:], t], [y[0], *y[keep][1:], float(np.interp(t, x, y))], KIND_COLOR[k], 3)

        lines = {k: always_redraw(lambda k=k: upto(k)) for k in kinds}
        cursor = always_redraw(lambda: DashedLine(g.ax.c2p(tracker.get_value(), 0), g.ax.c2p(tracker.get_value(), ymax),
                                                  color=GREY_B, stroke_width=1.5))
        tag = note(r"computed: \ seed $0$ of each, \ one held-out chain; \ error on $200$ held-out chains",
                   font_size=18).to_corner(DR, buff=0.15)
        fin = {k: float(cv[k][-1, 1]) for k in kinds}
        # when does the triangle model first beat the per-pair model's final error?
        beat = np.flatnonzero(cv["triangle"][:, 1] < fin["pairwise"])
        if fin["triangle"] >= fin["pairwise"]:
            beat_txt = "the triangle model never gets below the per-pair model"
        else:
            b_step, e_tri, e_pw = int(cv["triangle"][beat[0], 0]), fin["triangle"], fin["pairwise"]
            beat_txt = (f"the triangle model passes the per-pair model's final error by step {b_step:,}, and keeps "
                        f"going, to {e_tri:.1f} ångströms against {e_pw:.1f}")
        with self.voiceover(
            "Here is the training itself, replayed: both models' guesses for one held-out chain, as training goes "
            f"on. <bookmark mark='a'/> At step zero both guess nothing in particular. <bookmark mark='b'/> Within a "
            "few hundred steps both learn the easy part, that residues close along the chain are close in space: the "
            "bright band along the diagonal. <bookmark mark='c'/> The rest, which residues far apart along the chain "
            "come back together, needs the other pairs; <bookmark mark='d'/> on the curve below, "
            f"{beat_txt}."
        ) as vo:
            self.play(FadeIn(true_im), FadeIn(caps), *[FadeIn(im) for im in ims.values()], FadeIn(stepl), FadeIn(g),
                      FadeIn(tag), FadeIn(cursor))
            self.add(*lines.values())
            vo.wait_until("a")
            marks = {1: "b", len(snaps) - 2: "c", len(snaps) - 1: "d"}
            for i in range(1, len(snaps)):
                if i in marks:
                    vo.wait_until(marks[i])
                new = {k: matrix_image(fr[k][i], S, 0, vmax).move_to(ims[k]) for k in kinds}
                nstep = label(rf"step ${snaps[i]:,}$".replace(",", "{,}"), font_size=26, color=GREY_A).move_to(stepl)
                parts = [crossfade(ims[k], new[k]) for k in kinds] + [crossfade(stepl, nstep)]
                self.play(*parts, tracker.animate.set_value(snaps[i]), run_time=1.2)
                ims, stepl = new, nstep
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def casp14(self):
        rows = [(r"AlphaFold 2", 92.4, PAIR_C)]
        g = VGroup()
        head = label(r"CASP14, \ 2020", font_size=36).to_edge(UP, buff=0.45)
        facts = VGroup(
            label(r"median GDT: \ $92.4$ over all targets, \ $87.0$ on the hardest", font_size=28, color=PAIR_C),
            label(r"around $90$: \ informally, \ competitive with experiment", font_size=24, color=GREY_A),
            label(r"backbone error \ (median, $95\%$ of residues): \ $0.96$\,\AA, \ against $2.8$\,\AA\ for the next "
                  r"best", font_size=24, color=STRUCT),
            label(r"a carbon atom is about $1.4$\,\AA\ across \ (its covalent diameter)", font_size=22,
                  color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(UP * 0.4)
        cite_ = cite(r"DeepMind (30 November 2020); \ Jumper et al., \textit{Nature} (2021)", corner=DR)
        hc = history_card(2020, r"John Moult, \ CASP's co-founder", r"``We have been stuck on this one problem -- how do "
                          r"proteins fold up -- for nearly 50 years.'' \ CASP's organizers recognized AlphaFold 2 as a "
                          r"solution to it, \ for single protein chains", width=8.4, color=HIST)
        hc.to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "And at CASP14, in 2020, it worked. <bookmark mark='a'/> AlphaFold 2's median score was 92.4 GDT over "
            "all targets, and 87.0 on the hardest, where around ninety is informally reckoned competitive with an "
            "experiment. <bookmark mark='b'/> Its median backbone error was under one ångström, 0.96, against 2.8 "
            "for the next best entry; for scale, a carbon atom is about one and a half ångströms across. <bookmark "
            "mark='c'/> \"We have been stuck on this one problem, how do proteins fold up, for nearly fifty years,\" "
            "said John Moult; CASP's organizers recognized AlphaFold 2 as a solution, for single protein chains."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(facts[0]), FadeIn(facts[1]))
            vo.wait_until("b")
            self.play(FadeIn(facts[2]), FadeIn(facts[3]))
            vo.wait_until("c")
            self.play(FadeIn(hc, shift=UP * 0.1))
        self.wait(0.6)
        tk = take_away(r"the Evoformer: \ sequences and pairs talking, \ pairs kept consistent through triangles")
        with self.voiceover(
            "So the Evoformer's two ideas: let the alignment and the pairs inform each other, and keep the pairs "
            "consistent through triangles. What remains is to turn pairs into a structure, without losing left from "
            "right."
        ):
            self.play(FadeOut(hc), FadeIn(tk, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
