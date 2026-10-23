from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai25.common import (AUG, HIST, KIND_COLOR, MSA_C, PAIR_C, PART, PLAIN, PRED_C, STRUCT, SYM, TRUE_C,
                                   chain2d_mob, load, node_box, take_away)


def chain_sheet(S, cols, scale=0.32, gap=1.35, color=STRUCT, width=2.2, dot_r=0.035):
    g = VGroup()
    for k, P in enumerate(np.asarray(S)):
        r, c = divmod(k, cols)
        g.add(chain2d_mob(P, scale=scale, center=[c * gap, -r * gap, 0], color=color, width=width, dot_r=dot_r))
    return g


class AF3(VoiceoverScene):
    def construct(self):
        self.card()
        self.overview()
        self.diffusion()
        self.experiment()
        self.ecosystem()

    def card(self):
        card = chapter_card(11, r"AlphaFold 3: \ diffusion over atoms", r"Do you need equivariance at all?",
                            lit=(), part=PART)
        with self.voiceover("Chapter eleven. AlphaFold 3: diffusion over atoms."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def overview(self):
        ins = VGroup(*[node_box(t, c, font_size=20) for t, c in (
            (r"proteins", PAIR_C), (r"DNA, \ RNA", MSA_C), (r"small molecules", PRED_C), (r"ions, \ modified residues",
                                                                                          GREY_A))])
        ins.arrange(DOWN, buff=0.18).move_to([-5.4, 0.3, 0])
        b = [node_box(r"MSA module \ $\times 4$", MSA_C, font_size=22, height=0.9),
             node_box(r"Pairformer \ $\times 48$", PAIR_C, font_size=24, height=1.0),
             node_box(r"diffusion module: \ every atom's coordinates", STRUCT, font_size=22, height=1.0)]
        b[0].move_to([-2.3, 0.3, 0])
        b[1].move_to([0.6, 0.3, 0])
        b[2].move_to([4.3, 0.3, 0])
        arr = VGroup(Arrow(ins.get_right(), b[0].get_left(), buff=0.1, color=GREY_B, stroke_width=2.5),
                     Arrow(b[0].get_right(), b[1].get_left(), buff=0.1, color=GREY_B, stroke_width=2.5),
                     Arrow(b[1].get_right(), b[2].get_left(), buff=0.1, color=GREY_B, stroke_width=2.5))
        notes = VGroup(
            label(r"the Evoformer's pair stack, \ with the alignment cut down to four blocks", font_size=21,
                  color=PAIR_C),
            label(r"no frames, \ no torsion angles: \ atoms, \ denoised", font_size=21, color=STRUCT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.6)
        sch = note(r"schematic, \ after Abramson et al.\ (2024)", font_size=20).to_corner(UR, buff=0.25)
        with self.voiceover(
            "In May 2024 Google DeepMind and Isomorphic Labs published AlphaFold 3. <bookmark mark='a'/> It takes "
            "almost anything found in a cell's structures: protein chains, DNA and RNA, small drug-like molecules, "
            "ions, chemically modified residues, and predicts how they sit together. <bookmark mark='b'/> The "
            "alignment gets just four blocks of processing, <bookmark mark='c'/> and the trunk is the Pairformer, the "
            "Evoformer's pair stack, forty-eight blocks, with its triangle updates intact. <bookmark mark='d'/> The "
            "big change is the end. The structure module, with its frames and invariant attention, is gone. In its "
            "place, a diffusion model that writes down every atom's coordinates directly."
        ) as vo:
            self.play(FadeIn(sch))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(i_) for i_ in ins], lag_ratio=0.2), run_time=1.5)
            vo.wait_until("b")
            self.play(GrowArrow(arr[0]), FadeIn(b[0]))
            vo.wait_until("c")
            self.play(GrowArrow(arr[1]), FadeIn(b[1]), FadeIn(notes[0]))
            vo.wait_until("d")
            self.play(GrowArrow(arr[2]), FadeIn(b[2]), FadeIn(notes[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def diffusion(self):
        dd = load("diffusion")
        path = dd["egnn_s0"]["path"]
        ts = sorted((int(t) for t in path), reverse=True)
        strip = VGroup()
        for t in ts:
            P = np.asarray(path[str(t)])[0]
            P = np.clip(P, -3.2, 3.2)
            m = chain2d_mob(P, scale=0.32, color=STRUCT if t == 0 else interpolate_color(ManimColor(GREY_C),
                                                                                         ManimColor(STRUCT),
                                                                                         1 - t / ts[0]),
                            width=2.2, dot_r=0.04)
            strip.add(VGroup(m, MathTex(rf"t = {t}", font_size=20, color=GREY_B).next_to(m, DOWN, buff=0.12)))
        strip.arrange(RIGHT, buff=0.25).move_to([0, 1.5, 0])
        if strip.width > 13.2:
            strip.width = 13.2
        sl = label(r"one of our samples, \ from noise to a chain \ (computed)", font_size=20, color=GREY_A)
        sl.next_to(strip, UP, buff=0.15)
        quote = label(r"``no invariance or equivariance with respect to global rotations and translation of the "
                      r"molecule are required in the architecture''", font_size=22, color=PAIR_C)
        quote.width = min(quote.width, 12.6)
        quote.move_to([0, -0.6, 0])
        qc = note(r"Abramson et al., \textit{Nature} (2024)", font_size=20).next_to(quote, DOWN, buff=0.12)
        how = VGroup(
            label(r"instead: \ every training structure centred, \ randomly turned and shifted", font_size=22,
                  color=AUG),
            label(r"generative models can invent structure: \ trained also on AlphaFold-Multimer's predictions "
                  r"(cross-distillation)", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.4)
        head = label(r"diffusion over coordinates \ (Part 21)", font_size=32, color=STRUCT).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Diffusion is Part 21's idea, applied to atoms. <bookmark mark='a'/> Add noise to a structure's "
            "coordinates, at every level from a whisper to pure noise, and train a network to remove it. Then start "
            "from pure noise and remove it step by step. Here is a sample from a small model of ours, from noise to "
            "a chain. <bookmark mark='b'/> And here is the surprise. After four chapters of building symmetry in, the "
            "AlphaFold 3 paper says plainly that no invariance or equivariance to rotations and translations is "
            "required in the architecture. <bookmark mark='c'/> Instead, every training structure is centred and "
            "turned at random: augmentation, the cheap route of chapter two. <bookmark mark='d'/> Generative models "
            "can also invent structure where there is none, in floppy regions; AlphaFold 3 was trained on "
            "AlphaFold-Multimer's predictions too, which taught it to leave those regions as loose extended chains."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(sl), LaggedStart(*[FadeIn(s_) for s_ in strip], lag_ratio=0.3), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(quote), FadeIn(qc))
            vo.wait_until("c")
            self.play(FadeIn(how[0]))
            vo.wait_until("d")
            self.play(FadeIn(how[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def experiment(self):
        dd = load("diffusion")
        data = np.asarray(dd["data"])
        kinds = ["egnn", "mlp"]
        names = {"egnn": r"E(2)-equivariant denoiser", "mlp": r"plain MLP, \ randomly turned data"}
        cols = {"egnn": STRUCT, "mlp": AUG}
        real = chain_sheet(data[:6], 3, color=TRUE_C).move_to([-4.6, 1.4, 0])
        rl = label(r"training chains", font_size=22, color=TRUE_C).next_to(real, UP, buff=0.15)
        sheets = {k: chain_sheet(np.asarray(dd[f"{k}_s0"]["samples"])[:6], 3, color=cols[k]) for k in kinds}
        sheets["egnn"].move_to([-0.2, 1.4, 0])
        sheets["mlp"].move_to([4.4, 1.4, 0])
        sls = {k: label(names[k], font_size=20, color=cols[k]).next_to(sheets[k], UP, buff=0.15) for k in kinds}
        stats = {k: dict(bond=np.mean([dd[f"{k}_s{s}"]["bond_mad"] for s in (0, 1)]),
                         clash=np.mean([dd[f"{k}_s{s}"]["clash"] for s in (0, 1)]),
                         nn=np.mean([dd[f"{k}_s{s}"]["nn_median"] for s in (0, 1)]),
                         params=dd[f"{k}_s0"]["params"]) for k in kinds}
        hdr = [r"", r"bond length off by", r"two atoms clash", r"nearest training chain"]
        xs = [-4.4, -0.9, 2.2, 5.0]
        y0 = -1.15
        head = VGroup(*[label(h, font_size=20, color=GREY_A).move_to([x, y0, 0]) for h, x in zip(hdr, xs) if h])
        rows = VGroup()
        ref = (dd["ref_bond_mad"], dd["ref_clash"], dd["nn_heldout_median"])
        for i, (nm, vals, col) in enumerate([(r"real chains", ref, TRUE_C)] +
                                             [(names[k], (stats[k]["bond"], stats[k]["clash"], stats[k]["nn"]),
                                               cols[k]) for k in kinds]):
            y = y0 - 0.5 * (i + 1)
            r_ = VGroup(label(nm, font_size=20, color=col).move_to([xs[0], y, 0]))
            r_.add(MathTex(f"{vals[0]:.3f}", font_size=26, color=col).move_to([xs[1], y, 0]))
            r_.add(MathTex(f"{100 * vals[1]:.1f}\\%", font_size=26, color=col).move_to([xs[2], y, 0]))
            r_.add(MathTex(f"{vals[2]:.2f}", font_size=26, color=col).move_to([xs[3], y, 0]))
            rows.add(r_)
        tag = note(rf"computed: \ $4{{,}}000$ compact chains of $12$ atoms; \ same steps, \ two seeds each; \ "
                   rf"${stats['egnn']['params']:,}$ and ${stats['mlp']['params']:,}$ weights".replace(",", "{,}")
                   .replace("{{,}}", "{,}"), font_size=18).to_corner(DR, buff=0.15)
        e, m = stats["egnn"], stats["mlp"]
        better = (e["bond"] < m["bond"]) + (e["clash"] < m["clash"])
        if better == 2:
            verdict = "The equivariant denoiser draws better chains on both counts"
        elif better == 0:
            verdict = "The plain network, trained on turned copies, does as well or better on both counts"
        else:
            verdict = "Each wins on one count"
        nn_line = ("and neither simply copies its training chains" if min(e["nn"], m["nn"]) > 0.5 * ref[2] else
                   "though the samples sit closer to training chains than real new chains do")
        with self.voiceover(
            "So is equivariance worth it, for a generator? We can test the question on a toy. Four thousand compact "
            "chains of twelve atoms in the plane, with bonds of length one. <bookmark mark='a'/> Two denoisers, "
            "trained the same number of steps: one equivariant to rotations, like EGNN, and a plain MLP that sees "
            "every chain turned at random, as AlphaFold 3's network does. <bookmark mark='b'/> Their samples. "
            f"<bookmark mark='c'/> Bonds: the equivariant model's are off by {e['bond']:.3f} on average, the plain "
            f"one's by {m['bond']:.3f}. Clashes, two atoms on top of each other: {100 * e['clash']:.1f} percent of "
            f"chains against {100 * m['clash']:.1f}. {verdict}, {nn_line}. <bookmark mark='d'/> At AlphaFold 3's "
            "scale, trained on the whole Protein Data Bank with a large network, DeepMind chose the plain network fed "
            "with turned copies: data and compute standing in for built-in symmetry."
        ) as vo:
            self.play(FadeIn(real), FadeIn(rl), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(sls["egnn"]), FadeIn(sls["mlp"]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c_) for c_ in sheets["egnn"]], lag_ratio=0.15),
                      LaggedStart(*[FadeIn(c_) for c_ in sheets["mlp"]], lag_ratio=0.15), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(head), FadeIn(rows))
            vo.wait_until("d")
            self.play(Indicate(rows[2], color=AUG, scale_factor=1.03))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ecosystem(self):
        res = VGroup(
            label(r"protein--ligand poses (PoseBusters): \ ``50\% more accurate than the best traditional methods''",
                  font_size=22, color=PRED_C),
            label(r"also better than AlphaFold-Multimer on protein complexes and antibodies", font_size=22,
                  color=PAIR_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(UP, buff=0.45)
        rc = note(r"Google DeepMind \& Isomorphic Labs (May 2024); \ Abramson et al.\ (2024)", font_size=18)
        rc.next_to(res, DOWN, buff=0.12).align_to(res, LEFT)
        cards = VGroup(
            history_card(2024, r"AlphaFold Server; \ code for academics", r"free web server for non-commercial use; "
                         r"\ code and weights for academic use in November", width=4.3, color=HIST),
            history_card(2024, r"open reproductions", r"Chai-1, \ Boltz-1, \ Protenix: \ the recipe, \ rebuilt in "
                         r"the open", width=4.3, color=HIST),
            history_card(2025, r"Boltz-2; \ OpenFold3", r"binding strength predicted too \ (Boltz-2); \ a "
                         r"consortium's fully open model \ (preview, October)", width=4.3, color=HIST),
            history_card(2026, r"IsoDDE \ (Isomorphic Labs)", r"proprietary; \ on new antibody--antigen pairs, \ "
                         r"$2.3\times$ AlphaFold 3's rate of high-accuracy predictions \ (their report, February)",
                         width=4.3, color=HIST),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.25)).next_to(rc, DOWN, buff=0.35)
        if cards.height > 4.6:
            cards.height = 4.6
        cards.set_x(0)
        with self.voiceover(
            "On drug-like molecules bound to proteins, DeepMind reported AlphaFold 3 fifty percent more accurate "
            "than the best traditional docking methods, and better than its predecessor on protein complexes and "
            "antibodies. <bookmark mark='a'/> It came as a free server for non-commercial use, and in November 2024 "
            "as code and weights for academics. <bookmark mark='b'/> Within months, open reproductions appeared: "
            "Chai-1, Boltz-1, Protenix. <bookmark mark='c'/> In 2025 Boltz-2 added a prediction of how strongly a "
            "molecule binds, and the OpenFold consortium previewed a fully open model. <bookmark mark='d'/> And in "
            "February 2026 Isomorphic Labs reported a proprietary successor that, on new antibody–antigen pairs, "
            "makes high-accuracy predictions 2.3 times as often as AlphaFold 3, by their own benchmark."
        ) as vo:
            self.play(FadeIn(res), FadeIn(rc))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.1))
        self.wait(0.6)
        tk = take_away(r"AlphaFold 3: \ the pair stack kept, \ the geometry handed to diffusion, \ the symmetry "
                       r"learned from turned copies")
        with self.voiceover(
            "AlphaFold 3 kept the pair stack, handed the geometry to diffusion, and let the network learn the "
            "symmetry from turned copies. Prediction runs backwards, too: from a shape you want, to a protein that "
            "folds into it."
        ):
            self.play(FadeOut(cards), FadeIn(tk, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
