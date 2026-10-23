from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai20.common import (DATA, FAM, PART, bars_chart, digit_sheet, load, take_away)
from videos.ai.ai20.gendigits import BUDGET

ORDER = ["pixelcnn", "vae", "gan", "wgan", "flow"]
SHORT = {"pixelcnn": r"PixelCNN", "vae": r"VAE", "gan": r"GAN", "wgan": r"WGAN-GP", "flow": r"RealNVP"}
SPOKEN = {"pixelcnn": "the PixelCNN", "vae": "the VAE", "gan": "the GAN", "wgan": "WGAN-GP", "flow": "the flow"}


def stat(e, f, key):
    v = np.array([r[key] for r in e["table"][f]], float)
    return float(v.mean()), float(v.min()), float(v.max())


class Budget(VoiceoverScene):
    def construct(self):
        self.card()
        self.setup_()
        self.samples()
        self.scores()
        self.likelihoods()
        self.classes()

    def card(self):
        card = chapter_card(15, r"Five models, one budget", r"On equal arithmetic, which family wins what?", lit=(),
                            part=PART)
        with self.voiceover("Chapter fifteen. Five models, one budget."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def setup_(self):
        e = load("evaluate")
        head = VGroup(*[label(t, font_size=20, color=GREY_A) for t in (r"", r"parameters", r"training steps",
                                                                         r"digits seen", r"training FLOPs",
                                                                         r"passes per sample")])
        xs = [-5.4, -3.2, -1.2, 0.9, 3.1, 5.4]
        rows = VGroup()
        for i, f in enumerate(ORDER):
            r = e["table"][f][0]
            cells = [label(SHORT[f], font_size=24, color=FAM[f]),
                     MathTex(f"{int(r['params']):,}".replace(",", "{,}"), font_size=26),
                     MathTex(f"{int(r['steps']):,}".replace(",", "{,}"), font_size=26),
                     MathTex(f"{int(r['examples']) / 1e6:.2f}" + r"\text{M}", font_size=26),
                     MathTex(sci(float(r["flops"]), 2), font_size=26, color=C.BITS),
                     MathTex(f"{int(r['nfe'])}", font_size=26)]
            rows.add(VGroup(*cells))
        tab = VGroup(head, *rows)
        for k, r_ in enumerate(tab):
            for j, m in enumerate(r_):
                m.move_to([xs[j], 2.2 - 0.7 * k, 0])
        rule = Line([-6.6, 1.85, 0], [6.6, 1.85, 0], color=GREY_D, stroke_width=1.2)
        ex = [stat(e, f, "examples")[0] for f in ORDER]
        most, least = ORDER[int(np.argmax(ex))], ORDER[int(np.argmin(ex))]
        note_ = VGroup(label(rf"the budget: \ ${sci(BUDGET, 0)}$ floating-point operations of training each, \ counted "
                             r"by PyTorch's own formulas", font_size=20, color=C.BITS),
                       label(r"three seeds each; \ every model judged on $2{,}000$ samples, \ the same way",
                             font_size=20, color=GREY_A)).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Now the five image models, side by side, on equal terms. Every one got the same budget of arithmetic, "
            "six trillion floating-point operations of training, counted operation by operation, and every one was "
            "trained from three random starts. <bookmark mark='a'/> Equal arithmetic doesn't mean equal anything "
            "else. A convolution reuses its weights at every pixel, so the PixelCNN has the fewest parameters "
            f"and does the most arithmetic per digit: it saw {stat(e, 'pixelcnn', 'examples')[0] / 1e3:.0f} "
            f"thousand training digits, while {SPOKEN[most]} saw {stat(e, most, 'examples')[0] / 1e6:.1f} "
            "million. <bookmark mark='b'/> And the last column is the cost of drawing one sample: one pass for "
            "every model except the PixelCNN, which needs 196."
        ) as vo:
            self.play(FadeIn(head), Create(rule), FadeIn(note_))
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in rows], lag_ratio=0.25), run_time=2.5)
            vo.wait_until("a")
            self.play(Indicate(rows[0][1], color=FAM["pixelcnn"]), Indicate(rows[0][3], color=FAM["pixelcnn"]))
            vo.wait_until("b")
            self.play(Indicate(VGroup(*[r_[5] for r_ in rows]), color=C.BITS))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def samples(self):
        c = load("classifier")
        panels = Group()
        for f in ORDER + ["real"]:
            src = np.asarray(load(f)["s0_show"])[:16] if f != "real" else np.asarray(c["grid"])[16:32]
            sh = digit_sheet(src, 4, 4, size=0.46, gap=0.04)
            nm = label(SHORT.get(f, r"real digits"), font_size=22, color=FAM[f]).next_to(sh, UP, buff=0.12)
            panels.add(Group(sh, nm))
        panels.arrange_in_grid(2, 3, buff=(0.5, 0.45)).move_to(DOWN * 0.1)
        tg = note(r"seed $0$ of each; \ the first $16$ samples, \ not chosen").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Here is what each one draws, seed zero, the first sixteen samples, not chosen, beside real digits. "
            "<bookmark mark='a'/> Look before reading the numbers: which look sharpest, which most varied, which "
            "most like real handwriting? The measurements come next."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(p_, shift=UP * 0.1) for p_ in panels], lag_ratio=0.2), FadeIn(tg),
                      run_time=3.0)
            vo.wait_until("a")
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def scores(self):
        e, c = load("evaluate"), load("classifier")
        fid = {f: stat(e, f, "fid") for f in ORDER}
        vals = [fid[f][0] for f in ORDER]
        spread = [(fid[f][1], fid[f][2]) for f in ORDER]
        vmax = max(s[1] for s in spread) * 1.15
        ch = bars_chart(vals, [FAM[f] for f in ORDER], [SHORT[f] for f in ORDER], height=3.2, bar_w=0.62, gap=0.32,
                        vmax=vmax, spread=spread, digits=1)
        ch.move_to([-3.6, -0.2, 0])
        floor = float(c["real"]["fid"])
        fy = ch[0].get_y() + 3.2 * floor / vmax
        fl = DashedLine([ch.get_left()[0], fy, 0], [ch.get_right()[0], fy, 0], color=DATA, stroke_width=1.5)
        fll = label(r"real digits", font_size=16, color=DATA).next_to(fl, RIGHT, buff=0.08)
        fh = label(r"FID \ (lower is better; \ bar: mean, \ whisker: three seeds)", font_size=20, color=GREY_A)
        fh.next_to(ch, UP, buff=0.35)
        g = axes([0, 1], [0, 1], x_length=4.0, y_length=4.0, xlabel=r"precision", ylabel=r"recall",
                 xticks=[0, 0.5, 1], yticks=[0, 0.5, 1], center=[3.6, -0.3, 0])
        dots = VGroup()
        for f in ORDER:
            for r in e["table"][f]:
                dots.add(Dot(g.ax.c2p(r["precision"], r["recall"]), radius=0.07, color=FAM[f]))
        rd = Dot(g.ax.c2p(c["real"]["precision"], c["real"]["recall"]), radius=0.08, color=DATA)
        rl = label(r"real", font_size=16, color=DATA).next_to(rd, UR, buff=0.05)
        rank = sorted(ORDER, key=lambda f: fid[f][0])
        P = {f: stat(e, f, "precision")[0] for f in ORDER}
        R = {f: stat(e, f, "recall")[0] for f in ORDER}
        bp, br = max(ORDER, key=P.get), max(ORDER, key=R.get)
        sep = all(fid[a][2] < fid[b][1] for a, b in zip(rank, rank[1:2]))
        lead = (f"{SPOKEN[rank[0]].capitalize()} has the lowest FID, {fid[rank[0]][0]:.1f}, "
                + ("clearly ahead of the next, " if sep else "though its seeds overlap with the next, ")
                + f"{SPOKEN[rank[1]]} at {fid[rank[1]][0]:.1f}; {SPOKEN[rank[-1]]} is last at {fid[rank[-1]][0]:.1f}.")
        pr = (f"Split in two, the highest precision is {SPOKEN[bp]}'s, {P[bp]:.2f}, and the highest recall "
              f"{SPOKEN[br]}'s, {R[br]:.2f}." if bp != br else
              f"{SPOKEN[bp].capitalize()} leads on both precision, {P[bp]:.2f}, and recall, {R[bp]:.2f}.")
        with self.voiceover(
            "First, FID: the distance between our classifier's view of the generated digits and of the real ones, "
            f"two thousand of each. A perfect model would score about {floor:.2f}, the line for real digits. "
            f"<bookmark mark='a'/> {lead} <bookmark mark='b'/> {pr} Each dot is one seed: the spread between seeds "
            "is part of the result."
        ) as vo:
            self.play(FadeIn(ch[0]), FadeIn(ch.names), FadeIn(fh), Create(fl), FadeIn(fll))
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in ch.bars], lag_ratio=0.2),
                      FadeIn(VGroup(*ch[1:-3])), FadeIn(ch.vals), run_time=2.0)
            vo.wait_until("a")
            self.play(Indicate(ch.bars[ORDER.index(rank[0])], color=WHITE))
            vo.wait_until("b")
            self.play(FadeIn(g), FadeIn(rd), FadeIn(rl), LaggedStart(*[FadeIn(d_, scale=1.5) for d_ in dots],
                                                                     lag_ratio=0.05))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def likelihoods(self):
        e = load("evaluate")
        fams = ["pixelcnn", "vae", "flow"]
        st = {f: stat(e, f, "bpp") for f in fams}
        ch = bars_chart([st[f][0] for f in fams], [FAM[f] for f in fams],
                        [r"PixelCNN \\ (exact)", r"VAE \\ (a bound)", r"RealNVP \\ (a bound)"], height=3.0,
                        bar_w=0.9, gap=0.6, vmax=4.0, spread=[(st[f][1], st[f][2]) for f in fams], digits=2)
        ch.move_to([-3.2, -0.3, 0])
        hd = label(r"held-out bits per pixel \ (lower is better; \ $4$ = uniform)", font_size=20, color=GREY_A)
        hd.next_to(ch, UP, buff=0.35)
        rank = sorted(fams, key=lambda f: st[f][0])
        fid = {f: stat(e, f, "fid")[0] for f in ORDER}
        same = sorted(fams, key=lambda f: fid[f]) == rank
        msg = VGroup(label(r"the GANs: \ no likelihood at all", font_size=22, color=FAM["gan"]),
                     label(r"likelihood and sample quality: \ two different rankings" if not same else
                           r"here the two rankings agree", font_size=22, color=C.BITS))
        msg.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.4, 0.0, 0])
        with self.voiceover(
            "Second, likelihood, for the three families that have one, in bits per pixel on held-out digits: exact "
            "for the PixelCNN, an upper bound for the VAE and the flow. <bookmark mark='a'/> "
            f"{SPOKEN[rank[0]].capitalize()} is best, at {st[rank[0]][0]:.2f} bits per pixel, then "
            f"{SPOKEN[rank[1]]} at {st[rank[1]][0]:.2f} and {SPOKEN[rank[2]]} at {st[rank[2]][0]:.2f}. <bookmark "
            "mark='b'/> "
            + ("Compare the FID ranking: it is not the same. Exactly as Theis and his colleagues warned, a model "
               "can be good at probability and worse at pictures, or the reverse." if not same else
               "Here the likelihood ranking and the FID ranking agree, for these three; they need not, and on the "
               "ring they didn't.")
        ) as vo:
            self.play(FadeIn(ch[0]), FadeIn(ch.names), FadeIn(hd))
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in ch.bars], lag_ratio=0.2),
                      FadeIn(VGroup(*ch[1:-3])), FadeIn(ch.vals), run_time=2.0)
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(msg, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def classes(self):
        e = load("evaluate")
        panels = VGroup()
        shares = {}
        for f in ORDER:
            cl = np.mean([np.asarray(r["classes"], float) / max(sum(r["classes"]), 1) for r in e["table"][f]], 0)
            shares[f] = cl
            bars = VGroup(*[Rectangle(width=0.16, height=max(2.2 * v / 0.3, 0.01), stroke_width=0, fill_color=FAM[f],
                                      fill_opacity=0.85) for v in cl]).arrange(RIGHT, buff=0.05, aligned_edge=DOWN)
            base = Line(bars.get_corner(DL) + LEFT * 0.05, bars.get_corner(DR) + RIGHT * 0.05, color=GREY_C,
                        stroke_width=1)
            ref = DashedLine([bars.get_left()[0], bars.get_bottom()[1] + 2.2 * 0.1 / 0.3, 0],
                             [bars.get_right()[0], bars.get_bottom()[1] + 2.2 * 0.1 / 0.3, 0], color=DATA,
                             stroke_width=1.2)
            ticks = VGroup(*[MathTex(str(k), font_size=16, color=GREY_B).next_to(b_, DOWN, buff=0.06)
                             for k, b_ in enumerate(bars)])
            panels.add(VGroup(bars, base, ref, ticks, label(SHORT[f], font_size=20, color=FAM[f]).next_to(
                bars, UP, buff=0.5)))
        panels.arrange(RIGHT, buff=0.45).move_to(UP * 0.4)
        hd = label(r"which digits each model draws: \ the classifier's verdict on $2{,}000$ samples \ "
                   r"(dashed: one in ten)", font_size=20, color=GREY_A).to_edge(UP, buff=0.4)
        mins = {f: float(shares[f].min()) for f in ORDER}
        worst = min(ORDER, key=mins.get)
        wk = int(np.argmin(shares[worst]))
        flat = max(ORDER, key=mins.get)
        tk = take_away(r"At this scale: \ each family wins something, \ none wins everything. \ Ask what a model "
                       r"is for before asking which is best.", font_size=24)
        msg = (f"The most uneven is {SPOKEN[worst]}: its rarest digit, a {wk}, is only {100 * mins[worst]:.1f} "
               f"percent of its samples, where real data has about ten. The most even is {SPOKEN[flat]}, whose "
               f"rarest digit is still {100 * mins[flat]:.1f} percent.")
        with self.voiceover(
            "Third, a coarse but telling check: which digits does each model draw? The classifier labels two "
            "thousand samples of each, and real data has each digit about one time in ten. <bookmark mark='a'/> "
            f"{msg} Mode dropping, at the scale of whole classes, is the easiest failure to see. <bookmark "
            "mark='b'/> So, at this small scale and on one budget: every family wins something, and none wins "
            "everything. The likelihood models describe the data best; the adversarial ones draw differently "
            "from how they score; and which one is best depends on what the model is for."
        ) as vo:
            self.play(FadeIn(hd), LaggedStart(*[FadeIn(p_, shift=UP * 0.1) for p_ in panels], lag_ratio=0.2),
                      run_time=2.5)
            vo.wait_until("a")
            self.play(Indicate(panels[ORDER.index(worst)][0][wk], color=WHITE, scale_factor=1.4))
            vo.wait_until("b")
            self.play(FadeIn(tk))
        self.wait(0.3)
        self.clear_scene()
