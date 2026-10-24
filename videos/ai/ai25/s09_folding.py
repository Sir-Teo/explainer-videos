from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai25.common import (CHAIN_GRAD, HIST, MIRROR_C, MSA_C, PAIR_C, PART, PRED_C, SEQ, STRUCT, TRUE_C,
                                   chain3d, load, matrix_image, node_box, take_away, takeaway_anims, words_num)

AA = "MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQAPILSRVGDGTQDNLSGAEKAVQVKVKALPDAQFEVVHSLAKWKRQTLGQHDFSAGEGLYTHMKALRPDEDRLSP"


class Folding(VoiceoverScene):
    def construct(self):
        self.card()
        self.proteins()
        self.paradox()
        self.casp()
        self.distances()
        self.descent()

    def card(self):
        card = chapter_card(8, r"The protein-folding problem", r"Can you read a shape from a sequence?", lit=(2011,),
                            part=PART)
        with self.voiceover("Chapter eight. The protein-folding problem."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def proteins(self):
        f = load("fold")
        X = np.asarray(f["X"])
        n = len(X)
        seq = data_text(AA[:n], font="DejaVu Sans Mono", font_size=20, color=MSA_C)
        if seq.width > 12.8:
            seq.width = 12.8
        seq.to_edge(UP, buff=0.5)
        sl = label(rf"a sequence: \ ${n}$ amino acids, \ each one of $20$ kinds \ (illustrative)", font_size=22,
                   color=GREY_A).next_to(seq, DOWN, buff=0.15)
        chain = chain3d(X, scale=0.16, center=[-3.4, -0.9, 0], angle=0.6, tilt=0.5, gradient=CHAIN_GRAD, width=4)
        cl = label(r"its fold: \ one atom per residue, \ C$\alpha$", font_size=22, color=GREY_A).next_to(chain, DOWN,
                                                                                                    buff=0.15)
        facts = VGroup(
            label(r"the shape decides the job: \ enzymes, \ antibodies, \ channels, \ motors", font_size=22),
            label(r"1958: \ Kendrew, \ myoglobin by X-ray crystallography \\ (Nobel 1962, with Perutz)", font_size=22,
                  color=HIST),
            label(r"1971: \ the Protein Data Bank opens \ with $7$ structures", font_size=22, color=HIST),
            label(r"2026: \ more than $250{,}000$ entries", font_size=22, color=HIST),
            label(r"sequences known: \ billions \ (Jumper et al.\ 2021)", font_size=22, color=MSA_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        facts.move_to([0, -0.9, 0]).align_to(np.array([-0.6, 0, 0]), LEFT)
        cite_ = cite(r"PDBj, \ June 2026", corner=DR)
        with self.voiceover(
            "A protein is a chain of amino acids, of twenty kinds, written by a gene. <bookmark mark='a'/> In water it folds "
            "into a precise shape, and the shape decides what it does: cut a molecule, grip a virus, open a channel. "
            "<bookmark mark='b'/> In 1958 John Kendrew saw the first, myoglobin, by X-ray crystallography. <bookmark "
            "mark='c'/> The Protein Data Bank opened in 1971 with seven structures; <bookmark mark='d'/> today it holds more "
            "than a quarter of a million. <bookmark mark='e'/> But we know billions of sequences, and a structure can take "
            "years to measure. Hence the problem: read the shape from the sequence."
        ) as vo:
            self.play(FadeIn(seq), FadeIn(sl))
            vo.wait_until("a")
            self.play(Create(chain.segs, lag_ratio=0.02), FadeIn(chain.dots), FadeIn(cl), FadeIn(facts[0]),
                      run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(facts[1]))
            vo.wait_until("c")
            self.play(FadeIn(facts[2]))
            vo.wait_until("d")
            self.play(FadeIn(facts[3]), FadeIn(cite_))
            vo.wait_until("e")
            self.play(FadeIn(facts[4]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def paradox(self):
        anf = history_card(1961, r"Christian Anfinsen", r"unfolds ribonuclease with urea; \ washed out, \ it "
                           r"folds back and works again: \ the sequence holds the shape \ (Nobel 1972)", width=5.8,
                           color=HIST).move_to([-3.5, 1.4, 0])
        N = 100
        states = 3
        conf = states ** (N - 1)
        rate = 1e13
        secs = conf / rate
        years = secs / 3.156e7
        age = 1.38e10
        rows = VGroup(
            label(rf"${N}$ residues, \ $3$ shapes for each joint: \ $3^{{{N - 1}}} \approx {sci(conf, 1)}$ "
                  r"conformations", font_size=24),
            label(rf"at $10^{{13}}$ a second: \ ${sci(years, 1)}$ years", font_size=24, color=PRED_C),
            label(rf"the age of the universe: \ ${sci(age, 2)}$ years", font_size=24, color=GREY_B),
            label(r"real proteins fold in microseconds to seconds", font_size=24, color=STRUCT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([2.6, -1.2, 0])
        lev = label(r"Levinthal (1969): \ folding can't be a random search", font_size=26, color=PAIR_C)
        lev.next_to(rows, UP, buff=0.35).align_to(rows, LEFT)
        tag = note(r"illustrative arithmetic, \ after Levinthal", font_size=20).to_corner(DR, buff=0.25)
        head = label(r"two facts", font_size=34, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Two facts frame the problem. <bookmark mark='a'/> In 1961 Christian Anfinsen unfolded the enzyme ribonuclease "
            "with urea; washed out, it refolded by itself and worked again: the sequence holds the shape. <bookmark "
            "mark='b'/> But in 1969 Cyrus Levinthal pointed out that a chain can't find its shape by trying them all. "
            f"<bookmark mark='c'/> Give each joint of a {N}-residue chain three choices: about ten to the "
            f"{int(math.log10(conf))} shapes. <bookmark mark='d'/> At ten trillion a second, that is ten to the "
            f"{int(math.log10(years))} years; the universe is ten to the ten years old. <bookmark mark='e'/> Yet proteins "
            "fold in microseconds to seconds. Nature doesn't search blindly, and neither should a computer."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(anf, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(lev))
            vo.wait_until("c")
            self.play(FadeIn(rows[0]), FadeIn(tag))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]), FadeIn(rows[2]))
            vo.wait_until("e")
            self.play(FadeIn(rows[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def casp(self):
        d = definition_card(r"GDT\_TS", r"the share of residues within $1$, $2$, $4$ and $8$\,\AA\ of their true "
                            r"place after the best superposition, \ averaged over the four cutoffs: \ $0$ to $100$",
                            width=6.0, font_size=22, kind=r"CASP's score").move_to([-3.6, 1.9, 0])
        # an alignment: two columns that change together
        rng = np.random.default_rng(3)
        rows_ = []
        base = list("MKVLAAGIEKLRSG")
        pairs = {"E": "K", "K": "E", "R": "D", "D": "R"}
        for r in range(7):
            s = base.copy()
            for j in rng.choice(len(s), 4, replace=False):
                s[j] = "ACDEFGHIKLMNPQRSTVWY"[rng.integers(20)]
            a = "EKRD"[r % 4]
            s[3], s[10] = a, pairs[a]
            rows_.append("".join(s))
        msa = VGroup(*[data_text(r_, font="DejaVu Sans Mono", font_size=24, color=GREY_A) for r_ in rows_])
        msa.arrange(DOWN, buff=0.08).move_to([-3.6, -1.3, 0])
        cw = msa[0].width / len(rows_[0])
        hl = VGroup(*[Rectangle(width=cw * 1.1, height=msa.height + 0.12, stroke_color=MSA_C, stroke_width=2)
                      .move_to([msa.get_left()[0] + cw * (j + 0.5), msa.get_y(), 0]) for j in (3, 10)])
        ml = label(r"related sequences, \ aligned: \ two columns that change together \ are likely in contact",
                   font_size=20, color=MSA_C).next_to(msa, DOWN, buff=0.2)
        ml.width = min(ml.width, 6.2)
        ml.set_x(msa.get_x())
        hist = VGroup(
            history_card(1994, r"CASP begins", r"Moult \& Fidelis: \ predict structures \ before they are "
                         r"published", width=5.6, color=HIST),
            history_card(2011, r"contacts from co-evolution", r"Marks et al.; \ Morcos et al.: \ correlated "
                         r"mutations, \ statistically untangled", width=5.6, color=HIST),
            history_card(2018, r"AlphaFold at CASP13", r"a network predicts a histogram of distances for every pair; "
                         r"\ gradient descent folds a chain to match: \ high accuracy on $24$ of $43$ hard domains, "
                         r"\ against $14$ for the next best", width=5.6, color=HIST),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.5, -0.2, 0])
        cite_ = cite(r"Senior et al., \textit{Nature} (2020)", corner=DR)
        with self.voiceover(
            "In 1994 John Moult and Krzysztof Fidelis turned the problem into a contest, CASP: every two years, predict "
            "structures measured but not yet published. <bookmark mark='a'/> Predictions are scored by GDT, roughly the "
            "percentage of residues within a few ångströms of their true place. <bookmark mark='b'/> Progress was slow for "
            "two decades; then evolution offered a clue. <bookmark mark='c'/> Line up the same protein from many species: "
            "when two positions touch, a mutation at one is often compensated at the other, so their columns change "
            "together; from around 2011, statistics could read contacts from them. <bookmark mark='d'/> At CASP13, in 2018, "
            "DeepMind's first AlphaFold predicted a histogram of distances for every residue pair, then folded a chain by "
            "gradient descent to match: high accuracy on 24 of the 43 hardest domains, against 14 for the next best."
        ) as vo:
            self.play(FadeIn(hist[0], shift=UP * 0.1))
            vo.wait_until("a")
            self.play(FadeIn(d, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(msa))
            vo.wait_until("c")
            self.play(Create(hl), FadeIn(ml), FadeIn(hist[1], shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(hist[2], shift=UP * 0.1), FadeIn(cite_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def distances(self):
        f = load("fold")
        X = np.asarray(f["X"])
        D = np.asarray(f["D"])
        eig = np.asarray(f["eig"])
        img = matrix_image(D, size=3.4, vmin=0, vmax=float(D.max())).move_to([-4.1, -0.2, 0])
        il = label(r"all pairwise distances: \ $d_{ij} = |x_i - x_j|$", font_size=22, color=PAIR_C)
        il.next_to(img, UP, buff=0.2)
        rows = [
            cmath(r"G", r"=", r"-\tfrac12 \, J D^{\circ 2} J", font_size=34),
            cmath(r"G_{ij}", r"=", r"(x_i - \bar x) \cdot (x_j - \bar x)", font_size=34),
            cmath(r"G", r"=", r"V \Lambda V^\top", r",\quad", r"\hat X = V_3 \Lambda_3^{1/2}", font_size=34),
        ]
        whys = [why(r"square the distances, \ centre them \ ($J = I - \tfrac1n \mathbf 1 \mathbf 1^\top$)"),
                why(r"$|a - b|^2 = |a|^2 + |b|^2 - 2a \cdot b$"),
                why(r"three nonzero eigenvalues: \ three dimensions")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=1.7, buff=0.45, edge=6.9)
        ev = VGroup(*[MathTex(f"{v:,.0f}".replace(",", "{,}"), font_size=24, color=STRUCT if k < 3 else GREY_C)
                      for k, v in enumerate(eig[:6])]).arrange(RIGHT, buff=0.3)
        evl = label(r"eigenvalues of $G$:", font_size=22, color=GREY_A)
        evs = VGroup(evl, ev).arrange(RIGHT, buff=0.3).move_to([1.6, -1.45, 0])
        m_best = min(f["mds_rmsd"], f["mds_rmsd_mirror"])
        which = r"the fold itself" if f["mds_rmsd"] <= f["mds_rmsd_mirror"] else r"the fold's mirror image"
        res = label(rf"rebuilt: \ RMSD ${sci(m_best, 0)}$\,\AA\ \ to {which} \ (which of the two: \ a coin flip)",
                    font_size=22, color=GREY_A).move_to([1.6, -2.15, 0])
        mir = label(r"distances can't tell left from right", font_size=26, color=MIRROR_C).to_edge(DOWN, buff=0.5)
        tag = note(r"computed: \ our bundle's $52$ C$\alpha$ atoms", font_size=20).to_corner(DR, buff=0.2)
        with self.voiceover(
            "Why distances? Because a full table of distances fixes a shape. Here are all the distances between our bundle's "
            "fifty-two atoms. <bookmark mark='a'/> Square them and centre them, <bookmark mark='b'/> and you get the dot "
            "products of the atoms' positions, since a squared distance is two squared lengths minus twice a dot product. "
            "<bookmark mark='c'/> Its eigenvectors give the coordinates back: classical multidimensional scaling, 1952. "
            "Three eigenvalues are nonzero, one per dimension, <bookmark mark='d'/> and the rebuilt chain matches to rounding "
            "error. <bookmark mark='e'/> But only up to a mirror image, which has the same distances; and proteins are not "
            "mirror-symmetric: their helices are right-handed."
        ) as vo:
            self.play(FadeIn(img), FadeIn(il), FadeIn(tag))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            self.play(FadeIn(evs))
            vo.wait_until("d")
            self.play(FadeIn(res))
            vo.wait_until("e")
            self.play(FadeIn(mir))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def descent(self):
        f = load("fold")
        X = np.asarray(f["X"])
        runs = f["runs"]
        snaps = list(f["snaps"])
        show = runs[0]
        frames = [np.asarray(fr) for fr in show["frames"]]
        mirror_run = next((r for r in runs if r["rmsd"] > r["rmsd_mirror"] and "final" in r), None)
        c = np.array([-3.4, -0.3, 0])
        truth = chain3d(X, scale=0.13, center=c, angle=0.6, tilt=0.5, color=TRUE_C, width=7, dots=False)
        truth.set_opacity(0.25)
        cur = chain3d(frames[0], scale=0.13, center=c, angle=0.6, tilt=0.5, color=PRED_C, width=3.5, dots=False)
        steps_l = label(r"step $0$", font_size=22, color=GREY_A).next_to(truth, UP, buff=0.3)
        lg = VGroup(label(r"the true fold", font_size=20, color=TRUE_C),
                    label(r"gradient descent", font_size=20, color=PRED_C)).arrange(RIGHT, buff=0.4)
        lg.next_to(truth, DOWN, buff=0.3)
        n = len(runs)
        good = [r for r in runs if r["rmsd"] < r["rmsd_mirror"]]
        bad = [r for r in runs if r["rmsd"] >= r["rmsd_mirror"]]
        frac = f["frac_seen"]
        res = VGroup(label(rf"${n}$ random starts:", font_size=24, color=GREY_A),
                     label(rf"${len(good)}$ land on the fold \ (RMSD ${min(r['rmsd'] for r in good):.1f}$--"
                           rf"${max(r['rmsd'] for r in good):.1f}$\,\AA)" if good else r"none land on the fold",
                           font_size=24, color=TRUE_C),
                     label(rf"${len(bad)}$ on its mirror image \ (${min(r['rmsd_mirror'] for r in bad):.1f}$--"
                           rf"${max(r['rmsd_mirror'] for r in bad):.1f}$\,\AA\ from it, \ "
                           rf"${min(r['rmsd'] for r in bad):.0f}$\,\AA\ from the fold)" if bad else
                           r"none on its mirror image", font_size=24, color=MIRROR_C),
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.3, 0.9, 0])
        if res.width > 6.4:
            res.width = 6.4
        res.set_x(3.4)
        mpic = None
        if mirror_run is not None:
            mpic = chain3d(np.asarray(mirror_run["final"]), scale=0.07, center=[3.4, -1.9, 0], angle=0.6, tilt=0.5,
                           color=MIRROR_C, width=2.5, dots=False)
            mtrue = chain3d(X, scale=0.07, center=[3.4, -1.9, 0], angle=0.6, tilt=0.5, color=TRUE_C, width=5,
                            dots=False).set_opacity(0.3)
            mpic = VGroup(mtrue, mpic)
        tag = note(rf"computed: \ ${100 * frac:.0f}\%$ of the pairs seen \ (those under ${f['cut']:.0f}$\,\AA), "
                   rf"\ each with $\pm {f['noise']:.0f}$\,\AA\ of noise", font_size=20).to_corner(DR, buff=0.2)
        recipe = VGroup(label(r"AlphaFold 1's recipe, \ on our bundle:", font_size=24, color=GREY_A),
                        label(rf"keep the pairs under ${f['cut']:.0f}$\,\AA \ (${100 * frac:.0f}\%$ of them)",
                              font_size=22),
                        label(rf"add $\pm {f['noise']:.0f}$\,\AA\ of noise to each distance", font_size=22),
                        label(r"start from a random tangle", font_size=22),
                        label(r"gradient descent on $\sum (|x_i - x_j| - \hat d_{ij})^2$", font_size=22),
                        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.3, 0.4, 0])
        verdict = (f"{words_num(len(good))} of the {n} land on the true fold, and {words_num(len(bad))} on its mirror "
                   "image, which fits the distances just as well")
        with self.voiceover(
            "AlphaFold 1 predicted only distances, noisy, and only for pairs it was sure were close. So do the same with ours: "
            f"keep the pairs under {f['cut']:.0f} ångströms, {100 * frac:.0f} percent of them, add {f['noise']:.0f} "
            "ångström of noise, <bookmark mark='a'/> and from a random tangle, move the atoms by gradient descent until "
            f"their distances match. <bookmark mark='b'/> From {n} random starts, {verdict}. <bookmark "
            "mark='c'/> Nothing a reflection leaves unchanged, distances included, can tell which. AlphaFold 2 needed a "
            "representation that knows left from right."
        ) as vo:
            self.play(FadeIn(truth), FadeIn(cur), FadeIn(steps_l), FadeIn(lg), FadeIn(tag), FadeIn(recipe[0]))
            self.play(LaggedStart(*[FadeIn(r) for r in recipe[1:3]], lag_ratio=0.5), run_time=1.5)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in recipe[3:]], lag_ratio=0.5), run_time=1.0)
            per = max(0.4, vo.until("b") / max(1, len(frames) - 1))
            for k in range(1, len(frames)):
                new = chain3d(frames[k], scale=0.13, center=c, angle=0.6, tilt=0.5, color=PRED_C, width=3.5,
                              dots=False)
                nl = label(rf"step ${snaps[k]:,}$".replace(",", "{,}"), font_size=22, color=GREY_A).move_to(steps_l)
                self.play(ReplacementTransform(cur, new), ReplacementTransform(steps_l, nl), run_time=0.7 * per)
                cur, steps_l = new, nl
                self.wait(0.3 * per)
            vo.wait_until("b")
            self.play(FadeOut(recipe), FadeIn(res))
            vo.wait_until("c")
            if mpic is not None:
                self.play(FadeIn(mpic))
        self.wait(0.6)
        tk = take_away(r"distances pin down a shape, \ up to its mirror image")
        with self.voiceover(
            "Distances pin down a shape, but only up to its mirror image. Keep that in mind; AlphaFold 2's answer "
            "to it is one of its cleverest parts."
        ):
            self.play(FadeIn(tk, shift=UP * 0.1), *takeaway_anims(self, tk))
        self.wait(0.3)
        self.clear_scene()
