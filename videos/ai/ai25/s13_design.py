from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai25.common import (AUG, CHAIN_GRAD, HIST, MSA_C, PAIR_C, PART, PLAIN, PRED_C, STRUCT, SYM, TRUE_C,
                                   chain2d_mob, chain3d, load, node_box, take_away, takeaway_anims)
from videos.ai.ai25.s12_af3 import chain_sheet


class Design(VoiceoverScene):
    def construct(self):
        self.card()
        self.inverse()
        self.mpnn()
        self.rfdiffusion()
        self.replay()
        self.frontier()

    def card(self):
        card = chapter_card(12, r"Designing proteins", r"Can we write the sequence for a shape we want?", lit=(),
                            part=PART)
        with self.voiceover("Chapter twelve. Designing proteins."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def inverse(self):
        f = load("fold")
        X = np.asarray(f["X"])
        seq = node_box(r"sequence", MSA_C, font_size=28, height=0.9).move_to([-4.6, 0.8, 0])
        fold = chain3d(X, scale=0.1, center=[2.0, 0.8, 0], angle=0.6, tilt=0.5, gradient=CHAIN_GRAD, width=3,
                       dots=False)
        a1 = CurvedArrow(seq.get_right() + UP * 0.25, fold.get_left() + UP * 0.6, angle=-0.5, color=PAIR_C,
                         stroke_width=3)
        a2 = CurvedArrow(fold.get_left() + DOWN * 0.6, seq.get_right() + DOWN * 0.25, angle=-0.5, color=STRUCT,
                         stroke_width=3)
        l1 = label(r"prediction: \ AlphaFold", font_size=24, color=PAIR_C).next_to(a1, UP, buff=0.1)
        l2 = label(r"design: \ the inverse problem", font_size=24, color=STRUCT).next_to(a2, DOWN, buff=0.1)
        top7 = history_card(2003, r"Top7 \ (Kuhlman, \ Baker et al.)", r"a fold never seen in nature, \ designed "
                            r"with the Rosetta energy function, \ made, \ and its crystal structure matched the design",
                            width=6.0, color=HIST).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Structure prediction goes from a sequence to a shape. <bookmark mark='a'/> Design goes the other way: from a "
            "shape you want, a binder for a virus, a scaffold for a catalyst, to a sequence that folds into it. <bookmark "
            "mark='b'/> This was David Baker's life's work, the other half of the 2024 Nobel. In 2003 his group designed "
            "Top7, a fold never seen in nature, with the Rosetta energy function, and it folded as designed. For two decades "
            "such designs took experts, and most attempts failed."
        ) as vo:
            self.play(FadeIn(seq), FadeIn(fold), Create(a1), FadeIn(l1))
            vo.wait_until("a")
            self.play(Create(a2), FadeIn(l2))
            vo.wait_until("b")
            self.play(FadeIn(top7, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mpnn(self):
        f = load("fold")
        X = np.asarray(f["X"])
        c = np.array([-3.6, -0.2, 0])
        g = chain3d(X, scale=0.13, center=c, angle=0.6, tilt=0.5, color=GREY_B, width=2.5, dots=True, dot_r=0.04)
        D = np.sqrt(((X[:, None] - X[None]) ** 2).sum(-1))
        k = 6
        edges = VGroup()
        for i in range(len(X)):
            for j in np.argsort(D[i])[1:k + 1]:
                if j > i + 1:
                    edges.add(Line(g.pts[i], g.pts[j], color=SYM, stroke_width=0.8, stroke_opacity=0.5))
        aa = "MKVLEELAKRLEEAGKKAIEEALKLAKEGDLEKAKKLLEEAKKLAEEAGL"
        order = np.random.default_rng(2).permutation(len(X))
        letters = VGroup(*[data_text(aa[i % len(aa)], font="DejaVu Sans Mono", font_size=14, color=MSA_C)
                           .move_to(g.pts[i] + np.array([0.12, 0.12, 0])) for i in range(len(X))])
        facts = VGroup(
            label(r"ProteinMPNN \ (Dauparas et al., \ 2022)", font_size=26, color=STRUCT),
            label(r"the backbone as a graph: \ each residue joined \\ to its nearest neighbours in space", font_size=22),
            label(r"message passing over distances \ (invariant, \ chapter 7)", font_size=22),
            label(r"then the amino acids, \ one at a time, \ in a random order", font_size=22),
            label(r"native sequence recovered: \ $52.4\%$, \ against $32.9\%$ for Rosetta", font_size=24,
                  color=PAIR_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        facts.move_to([0, 0.3, 0]).align_to(np.array([-0.4, 0, 0]), LEFT)
        cite_ = cite(r"Dauparas et al., \textit{Science} (2022)", corner=DR)
        with self.voiceover(
            "Deep learning changed both halves of design, starting with the sequence. <bookmark mark='a'/> In 2022 Justus "
            "Dauparas and colleagues in Baker's lab built ProteinMPNN: it reads a backbone as a graph, each residue joined to "
            "its nearest neighbours in space, <bookmark mark='b'/> passes messages built from distances, so the backbone's "
            "orientation can't matter, <bookmark mark='c'/> and writes the amino acids one at a time, in random order, each "
            "conditioned on those already written. <bookmark mark='d'/> On natural backbones it recovers 52.4 percent of the "
            "native amino acids, against 32.9 for Rosetta."
        ) as vo:
            self.play(FadeIn(g), FadeIn(facts[0]), FadeIn(cite_))
            vo.wait_until("a")
            self.play(Create(edges, lag_ratio=0.01), FadeIn(facts[1]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(facts[2]))
            vo.wait_until("c")
            self.play(FadeIn(facts[3]),
                      LaggedStart(*[FadeIn(letters[i], scale=1.5) for i in order], lag_ratio=0.04), run_time=3.0)
            vo.wait_until("d")
            self.play(FadeIn(facts[4]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rfdiffusion(self):
        steps = [(r"RFdiffusion: \\ a backbone from noise", STRUCT), (r"ProteinMPNN: \\ $8$ sequences each", MSA_C),
                 (r"AlphaFold 2 check: \\ does it fold back?", PAIR_C), (r"the lab", HIST)]
        boxes = VGroup(*[node_box(t, c, font_size=22, height=1.1) for t, c in steps]).arrange(RIGHT, buff=0.6)
        boxes.move_to(UP * 1.9)
        arr = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.08, color=GREY_B, stroke_width=2.5)
                       for a, b in zip(boxes, boxes[1:])])
        crit = label(r"kept if: \ predicted aligned error $< 5$, \ within $2$\,\AA\ of the design", font_size=20,
                     color=PAIR_C).next_to(boxes[2], DOWN, buff=0.2)
        how = VGroup(
            label(r"RoseTTAFold, \ fine-tuned to remove noise from residue frames", font_size=22),
            label(r"positions: \ Gaussian noise; \ orientations: \ random turns on $SO(3)$; \ $200$ steps",
                  font_size=22),
            label(r"conditioned on a motif to hold, \ a target to bind, \ a symmetry to obey", font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([-2.0, -0.7, 0])
        res = VGroup(
            label(r"binders: \ $19\%$ worked in the lab, \ about $100\times$ the Rosetta-based rate", font_size=22,
                  color=STRUCT),
            label(r"an influenza binder's cryo-EM structure: \ $0.63$\,\AA\ from its design", font_size=22,
                  color=STRUCT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.4)
        cite_ = cite(r"Watson et al., \textit{Nature} (2023)", corner=DR)
        # illustrative: a backbone emerging from noise (our bundle, not RFdiffusion's output)
        X = np.asarray(load("fold")["X"])
        noisy = X + np.random.default_rng(3).normal(0, 6.0, X.shape)
        kw = dict(scale=0.11, center=[4.3, -0.6, 0], angle=0.6, tilt=0.5, width=2.5, dots=False)
        c_noisy = chain3d(noisy, color=GREY_B, **kw)
        c_clean = chain3d(X, gradient=CHAIN_GRAD, **kw)
        il = note(r"illustrative: \ from noise to a backbone", font_size=20).next_to(c_clean, DOWN, buff=0.25)
        with self.voiceover(
            "Then the backbone. In 2023 Joseph Watson and colleagues published RFdiffusion. <bookmark mark='a'/> They "
            "fine-tuned RoseTTAFold, a structure predictor, to remove noise from residue frames: noise on positions, random "
            "turns on orientations, two hundred steps from noise to a backbone, optionally holding a motif in place, binding "
            "a target, or obeying a symmetry. <bookmark mark='b'/> The pipeline became: diffuse a backbone; let ProteinMPNN "
            "write eight sequences for it; <bookmark mark='c'/> keep those that AlphaFold 2 folds back onto the design, "
            "within two ångströms and confidently; <bookmark mark='d'/> only then go to the lab. <bookmark mark='e'/> For "
            "binders, nineteen percent of designs worked, about a hundred times the earlier Rosetta-based rate, and one "
            "influenza binder's measured structure sat 0.63 ångströms from its design."
        ) as vo:
            self.play(FadeIn(how[0]), FadeIn(cite_), FadeIn(c_noisy), FadeIn(il))
            self.play(Transform(c_noisy, c_clean), run_time=4.0)
            vo.wait_until("a")
            self.play(FadeIn(how[1]), FadeIn(how[2]))
            vo.wait_until("b")
            self.play(FadeIn(boxes[0]), GrowArrow(arr[0]), FadeIn(boxes[1]))
            vo.wait_until("c")
            self.play(GrowArrow(arr[1]), FadeIn(boxes[2]), FadeIn(crit))
            vo.wait_until("d")
            self.play(GrowArrow(arr[2]), FadeIn(boxes[3]))
            vo.wait_until("e")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def replay(self):
        dd = load("diffusion")
        frames = dd["egnn_s0"]["frames"]
        snaps = list(dd["snaps"])
        curve_ = np.asarray(dd["egnn_s0"]["curve"])
        sheets = [chain_sheet(np.clip(np.asarray(fr)[:8], -3.0, 3.0), 4, scale=0.3, gap=1.25, color=STRUCT)
                  .move_to([2.9, 0.4, 0]) for fr in frames]
        g = axes([0, curve_[-1, 0]], [0.0, float(np.ceil(curve_[:, 1].max() * 10) / 10)], x_length=4.6, y_length=3.0,
                 xlabel=r"training step", ylabel=r"denoising loss", xticks=[0, curve_[-1, 0]], yticks=[0.0],
                 xfmt=lambda v: f"{v:,.0f}".replace(",", "{,}"), center=[-3.6, 0.2, 0])
        cv = curve(g.ax, curve_[:, 0], curve_[:, 1], STRUCT, 3)
        dot = Dot(g.ax.c2p(curve_[0, 0], curve_[0, 1]), color=STRUCT)
        cnt = label(r"before training", font_size=22, color=GREY_A).next_to(sheets[0], UP, buff=0.2)
        sl = label(r"the same eight noise seeds, \ sampled at each checkpoint", font_size=20, color=GREY_B)
        sl.next_to(sheets[0], DOWN, buff=0.25)
        nn_s = np.mean([dd[f"egnn_s{s}"]["nn_median"] for s in (0, 1)])
        nn_h = dd["nn_heldout_median"]
        tag = note(r"computed: \ chapter 11's equivariant denoiser, \ seed $0$", font_size=20).to_corner(DR,
                                                                                                    buff=0.2)
        if nn_s < 0.7 * nn_h:
            novel = "closer to training chains than genuinely new chains are, a sign of some copying"
        elif nn_s <= 1.5 * nn_h:
            novel = "about as far from their nearest training chain as genuinely new chains are"
        else:
            novel = "farther than genuinely new chains are: not copies, but not quite the real thing either"
        clash_s = float(np.mean([dd[f"egnn_s{s}"]["clash"] for s in (0, 1)]))
        if clash_s < 0.15:
            last_stage = "then compact folds like the training set's"
        else:
            last_stage = (f"then compact folds, though {100 * clash_s:.0f} percent of the final samples still have two "
                          "atoms too close, which the training chains never do")
        with self.voiceover(
            "Our toy denoiser from the last chapter shows the idea in miniature. Here is its training: the loss, "
            "and samples drawn from the same eight noise seeds at each checkpoint. <bookmark mark='a'/> At first, "
            f"tangles; then chains with nearly the right bond lengths; {last_stage}. <bookmark mark='b'/> Are they "
            f"new? The median sample sits {nn_s:.2f} from its nearest training chain, against {nn_h:.2f} for real "
            f"chains it never saw: {novel}."
        ) as vo:
            self.play(FadeIn(g), FadeIn(dot), FadeIn(sheets[0]), FadeIn(cnt), FadeIn(sl), FadeIn(tag))
            vo.wait_until("a")
            per = max(0.5, vo.until("b") / max(1, len(frames) - 1))
            cur = sheets[0]
            for k in range(1, len(frames)):
                new = label(rf"after ${snaps[k]:,}$ steps".replace(",", "{,}"), font_size=22,
                            color=GREY_A).move_to(cnt)
                idx = min(int(np.searchsorted(curve_[:, 0], snaps[k])), len(curve_) - 1)
                self.play(FadeOut(cur), FadeIn(sheets[k]), ReplacementTransform(cnt, new),
                          dot.animate.move_to(g.ax.c2p(curve_[idx, 0], curve_[idx, 1])), run_time=0.7 * per)
                cur, cnt = sheets[k], new
                self.wait(0.3 * per)
            self.play(Create(cv))
            vo.wait_until("b")
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def frontier(self):
        cards = VGroup(
            history_card(2024, r"AlphaProteo \ (Google DeepMind)", r"binders for targets such as VEGF-A and SARS-CoV-2's "
                         r"spike", width=4.2, color=HIST),
            history_card(2024, r"BindCraft \ (Pacesa et al.)", r"binders designed by backpropagating through "
                         r"AlphaFold 2", width=4.2, color=HIST),
            history_card(2024, r"ESM3 \ (EvolutionaryScale)", r"a language model of sequence, structure and "
                         r"function; \ a new fluorescent protein", width=4.2, color=HIST),
            history_card(2025, r"RFdiffusion3 \ (Baker lab)", r"every atom designed, \ DNA binders and enzymes; \ "
                         r"open, \ ten times faster than RFdiffusion2", width=4.2, color=HIST),
            history_card(2025, r"BoltzGen", r"an open model for designing binders", width=4.2,
                         color=HIST),
            history_card(2024, r"Responsible AI x Biodesign", r"a community statement: \ screening of DNA "
                         r"synthesis, \ sharing with care", width=4.2, color=PLAIN),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.25, 0.3)).move_to(DOWN * 0.15)
        head = label(r"Design since RFdiffusion", font_size=34).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Since then the field has moved fast. <bookmark mark='a'/> In 2024 Google DeepMind's AlphaProteo designed "
            "binders for medically important targets, <bookmark mark='b'/> BindCraft designed binders by gradient descent "
            "through AlphaFold 2 itself, <bookmark mark='c'/> and EvolutionaryScale's ESM3, a language model over sequence, "
            "structure and function, wrote a new fluorescent protein far from any natural one. <bookmark mark='d'/> In 2025 "
            "RFdiffusion3 designed at the level of single atoms, <bookmark mark='e'/> and BoltzGen appeared as an open "
            "alternative. <bookmark mark='f'/> Tools this capable could be misused; in 2024 many researchers signed "
            "commitments on responsible biodesign, including screening DNA synthesis."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate("abcdef"):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.1), run_time=0.8)
        self.wait(0.6)
        tk = take_away(r"design: \ diffuse a backbone, \ write its sequence, \ check that it folds back, \ then make "
                       r"it")
        with self.voiceover(
            "Design, in one line: diffuse a backbone, write a sequence for it, check that the sequence folds back, "
            "and only then make it. Now from molecules to the whole planet."
        ):
            self.play(FadeOut(cards), FadeIn(tk, shift=UP * 0.1), *takeaway_anims(self, tk))
        self.wait(0.3)
        self.clear_scene()
