from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai21.common import AUTO_C, CFG_C, CLS_C, FM_C, PART, Panel, legend, load, take_away

GX = (-3.0, 3.0)
GY = (-1.6, 1.6)
MNAME = {"cfg": r"classifier-free", "cls": r"classifier guidance", "auto": r"autoguidance"}
MSPOKEN = {"cfg": "classifier-free guidance", "cls": "classifier guidance", "auto": "autoguidance"}
MCOL = {"cfg": CFG_C, "cls": CLS_C, "auto": AUTO_C}


def guidance_arrows(w: float = 3.0) -> VGroup:
    """Classifier-free guidance at one point: the direction told nothing, the direction told the letter, and the
    difference between them stretched by w."""
    o = np.array([0.0, 0.0, 0.0])
    vu, vc = np.array([2.0, 0.3, 0.0]), np.array([1.9, 1.0, 0.0])
    vg = vu + w * (vc - vu)
    dot = Dot(o, radius=0.07, color=WHITE)
    au = Arrow(o, vu, buff=0, color=GREY_B, stroke_width=5, max_tip_length_to_length_ratio=0.12)
    ac = Arrow(o, vc, buff=0, color=FM_C, stroke_width=5, max_tip_length_to_length_ratio=0.12)
    ag = Arrow(o, vg, buff=0, color=CFG_C, stroke_width=5, max_tip_length_to_length_ratio=0.1)
    diff = DashedLine(vu, vg, color=CFG_C, stroke_width=2, dash_length=0.08)
    lu = label(r"told nothing \ ($\varnothing$)", font_size=22, color=GREY_B).next_to(au.get_end(), RIGHT, buff=0.15)
    lc = label(r"told ``A''", font_size=22, color=FM_C).next_to(ac.get_end(), RIGHT, buff=0.15)
    lg = label(rf"$w = {w:g}$: \ the difference, \ stretched", font_size=22, color=CFG_C).next_to(ag.get_end(), RIGHT, buff=0.15)
    return VGroup(diff, au, ac, ag, dot, lu, lc, lg)


class Guidance(VoiceoverScene):
    def construct(self):
        self.card()
        self.condition()
        self.bayes()
        self.cfg()
        self.sweep()
        self.auto()

    def card(self):
        card = chapter_card(14, r"Guidance", r"How do you ask for something specific?", part=PART)
        with self.voiceover("Chapter fourteen. Guidance."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def condition(self):
        g = load("guidance")
        pn = Panel(7.6, center=[0, 1.0, 0], xlim=GX, ylim=GY)
        Ad, Id = np.asarray(g["A"])[:500], np.asarray(g["I"])[:500]
        A, I_ = pn.dots(Ad, C.TRUE_P, radius=0.024), pn.dots(Id, C.SURPRISE, radius=0.024)
        la = label(r"``A''", font_size=30, color=C.TRUE_P).next_to(pn.p(float(Ad[:, 0].mean()), GY[1]), UP, buff=0.1)
        li = label(r"``I''", font_size=30, color=C.SURPRISE).next_to(pn.p(float(Id[:, 0].mean()), GY[1]), UP, buff=0.1)
        colors = {r"c": C.BITS, r"\varnothing": GREY_B}
        f = cmath(r"v_\theta(x, \tau,", r"c", r")", r"\quad\text{or}\quad", r"v_\theta(x, \tau,", r"\varnothing", r")",
                  colors=colors, font_size=36).move_to([0, -1.95, 0])
        fl = label(r"told the letter, \ or (one time in five) \ told nothing", font_size=22, color=GREY_A).next_to(f, DOWN, buff=0.12)
        snaps = np.asarray(g["snaps"])
        steps = [int(s) for s in g["snap_steps"]]
        pr = Panel(5.6, center=[3.7, 0.3, 0], xlim=GX, ylim=GY)
        rd = pr.dots(snaps[0], FM_C, radius=0.018)
        rl = label(rf"asked for ``A'', \ training step ${steps[0]}$", font_size=20, color=FM_C).next_to(pr, UP, buff=0.1)
        cite_ = cite(r"J.~Ho \& T.~Salimans, \textit{Classifier-Free Diffusion Guidance} (2022)", corner=DR)
        with self.voiceover(
            "So far the model draws whatever it likes. To ask for something, tell it what you want: a caption, or "
            "here, which letter. <bookmark mark='a'/> We trained a flow model on two letters, A and I, telling it "
            "which letter each example came from, except one time in five, when it is told nothing. "
            "<bookmark mark='b'/> One network learns both: the letter it is asked for, and letters in general. "
            "<bookmark mark='c'/> Here it is learning, asked for an A at each checkpoint."
        ) as vo:
            self.play(FadeIn(pn), FadeIn(A), FadeIn(I_), FadeIn(la), FadeIn(li), FadeIn(cite_))
            vo.wait_until("a")
            self.play(Write(f), FadeIn(fl))
            vo.wait_until("b")
            vo.wait_until("c")
            left = VGroup(pn, A, I_, la, li, f, fl)
            self.play(left.animate.scale(0.66).move_to([-3.55, 0.1, 0]), run_time=1.0)
            self.play(FadeIn(pr), FadeIn(rd), FadeIn(rl))
            for k in range(1, len(snaps)):
                r2 = label(rf"asked for ``A'', \ training step ${steps[k]:,}$".replace(",", "{,}"), font_size=20,
                           color=FM_C).move_to(rl)
                self.play(*pr.move(rd, snaps[k]), Transform(rl, r2), run_time=0.7)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bayes(self):
        rows = [
            cmath(r"p(x \mid y)", r"=", r"p(y \mid x)\; p(x)\, /\, p(y)", font_size=36),
            cmath(r"\nabla \log p(x \mid y)", r"=", r"\nabla \log p(x) + \nabla \log p(y \mid x)", font_size=36),
            cmath(r"\nabla \log p(x) + w\, \nabla \log p(y \mid x)", r"=", r"\nabla \log \big[\, p(x)\; p(y \mid x)^{w} \,\big]",
                  font_size=34),
        ]
        whys = [why(r"Bayes"), why(r"$p(y)$ doesn't depend on $x$: \ it vanishes"),
                why(r"a guidance weight $w$: \ a sharpened classifier")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-1.0, buff=0.65, edge=6.85)
        card = history_card(2021, r"Dhariwal \& Nichol: \ classifier guidance", r"a classifier trained on noisy images, "
                            r"its gradient added to the score: \ ImageNet $256^2$, \ FID $4.59$", color=C.HUMAN, width=7.6,
                            font_size=20).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The first way to ask came from Bayes' rule. <bookmark mark='a'/> Take logs and gradients, and the "
            "score of the images that fit a label is the ordinary score plus the gradient of a classifier's log "
            "probability: the evidence, p of y, doesn't depend on x, so it disappears. <bookmark mark='b'/> Multiply "
            "the classifier's push by a weight w above one, and you sample from a sharpened version, the data "
            "reweighted towards what the classifier is surest of. <bookmark mark='c'/> Prafulla Dhariwal and Alex "
            "Nichol did this in 2021, with a classifier trained on noisy images, and beat GANs on ImageNet."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            self.play(FadeIn(card, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cfg(self):
        colors = {r"w": CFG_C, r"v_\theta(x, \tau, c)": FM_C, r"v_\theta(x, \tau, \varnothing)": GREY_B}
        rows = [
            cmath(r"\nabla \log p(y \mid x)", r"=", r"\nabla \log p(x \mid y) - \nabla \log p(x)", font_size=34),
            cmath(r"v", r"=", r"v_\theta(x, \tau, \varnothing)", r"+", r"w", r"\,\big(", r"v_\theta(x, \tau, c)", r"-",
                  r"v_\theta(x, \tau, \varnothing)", r"\big)", colors=colors, font_size=34),
        ]
        whys = [why(r"Bayes again: \ the classifier is implicit"), why(r"in velocities: \ push along the difference")]
        step = ladder(self, rows, whys, keep=2, top=3.0, x=-1.6, buff=0.55, edge=6.85)
        arrows = guidance_arrows(3.0).scale(0.9).move_to([-0.6, -1.5, 0])
        with self.voiceover(
            "Classifier guidance needs a second network. In 2022 Jonathan Ho and Tim Salimans noticed that the model "
            "told the label and the model told nothing already contain a classifier: <bookmark mark='a'/> the "
            "gradient of log p of y given x is their difference. <bookmark mark='b'/> So start from the unconditional "
            "direction and push along the difference, towards the conditional one and past it, by a weight w. "
            "<bookmark mark='c'/> One network, two evaluations per step, no classifier. This is classifier-free "
            "guidance, and it became the standard way for text-to-image models to follow their prompts."
        ) as vo:
            step(0)
            vo.wait_until("a")
            vo.wait_until("b")
            step(1)
            self.play(FadeIn(arrows[4]), GrowArrow(arrows[1]), FadeIn(arrows[5]))
            self.play(GrowArrow(arrows[2]), FadeIn(arrows[6]))
            vo.wait_until("c")
            self.play(Create(arrows[0]), GrowArrow(arrows[3]), FadeIn(arrows[7]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sweep(self):
        g = load("guidance")
        ws = [float(w) for w in g["w"]]
        X = np.asarray(g["cfg_x"])
        show = [0.0, 1.0, 4.0]
        panels = Group()
        for i, w in enumerate(show):
            j = ws.index(w)
            pn = Panel(4.1, center=[-4.45 + 4.45 * i, 1.2, 0], xlim=GX, ylim=GY)
            on, sp = np.asarray(g["cfg_onA"])[:, j], np.asarray(g["cfg_spread"])[:, j]
            panels.add(Group(pn, pn.scatter(X[j], CFG_C, radius_px=1.5, res=300),
                             label(rf"$w = {w:g}$", font_size=26, color=CFG_C).next_to(pn, UP, buff=0.1),
                             label(rf"${100 * on.mean():.0f}\%$ on the A; \ spread ${sp.mean():.2f}$", font_size=19,
                                   color=GREY_A).next_to(pn, DOWN, buff=0.08)))
        sub = label(r"the same $1{,}000$ starting points in every panel", font_size=18, color=GREY_B).next_to(panels, UP, buff=0.12)
        on = {w: float(np.asarray(g["cfg_onA"])[:, ws.index(w)].mean()) for w in show}
        sp = {w: float(np.asarray(g["cfg_spread"])[:, ws.index(w)].mean()) for w in show}
        prec = np.asarray(g["cfg_prec"]).mean(0)
        rec = np.asarray(g["cfg_rec"]).mean(0)
        gg = axes([0, max(ws)], [0, 1.05], x_length=6.0, y_length=2.2, xlabel=r"guidance weight $w$",
                  ylabel=r"precision \ and \ recall against the real A", xticks=[0, 1, 2, 4, 6], yticks=[0, 0.5, 1],
                  center=[-1.6, -2.35, 0], font_size=18)
        cp = curve(gg.ax, ws, prec, CFG_C, 3)
        cr = VMobject(color=CFG_C, stroke_width=3).set_points_as_corners([gg.ax.c2p(a, b) for a, b in zip(ws, rec)])
        cr = DashedVMobject(cr, num_dashes=40)
        lg = VGroup(label(r"solid: \ precision, \ samples that look real", font_size=18, color=CFG_C),
                    label(r"dashed: \ recall, \ real points the samples cover", font_size=18, color=CFG_C)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).next_to(gg, RIGHT, buff=0.4)
        jr = int(np.argmax(prec))
        r_drop = next((w for w, r in zip(ws, rec) if r < 0.5 * rec[0]), None)
        drop_note = (f"Recall, how much of the real A the samples cover, halves by w equal to {r_drop:g}: more "
                     "faithful, less varied." if r_drop is not None else "Recall stays high across the sweep.")
        with self.voiceover(
            f"Ask for an A, from the same starting noise, at three weights. <bookmark mark='a'/> At w equal to zero "
            f"the request is ignored: {100 * on[0.0]:.0f} percent of the samples land on the A. <bookmark mark='b'/> "
            f"At one, the plain conditional model: {100 * on[1.0]:.0f} percent. <bookmark mark='c'/> At four you "
            f"overshoot on purpose: {100 * on[4.0]:.0f} percent, crowded towards the most A-like strokes, the spread "
            f"shrinking from {sp[1.0]:.2f} to {sp[4.0]:.2f}. <bookmark mark='d'/> Across the whole sweep, with "
            f"{len(np.asarray(g['cfg_prec']))} seeds: precision, the share of samples that look like real A's, peaks "
            f"at w equal to {ws[jr]:g}. {drop_note}"
        ) as vo:
            self.play(FadeIn(panels[0]), FadeIn(sub))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(panels[1]))
            vo.wait_until("c")
            self.play(FadeIn(panels[2]))
            vo.wait_until("d")
            self.play(FadeIn(gg), Create(cp), Create(cr), FadeIn(lg))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def auto(self):
        g = load("guidance")
        ms = ["cfg", "cls", "auto"]
        wk = {"cfg": "w", "cls": "cls_w", "auto": "auto_w"}
        P = {m: np.asarray(g[f"{m}_prec"]).mean(0) for m in ms}
        R = {m: np.asarray(g[f"{m}_rec"]).mean(0) for m in ms}
        W = {m: [float(w) for w in g[wk[m]]] for m in ms}
        ax = axes([0, 1.05], [0, 1.05], x_length=4.8, y_length=4.8, xlabel=r"recall: \ variety", ylabel=r"precision: \ fidelity",
                  xticks=[0, 0.5, 1], yticks=[0, 0.5, 1], center=[-3.2, -0.3, 0])
        curves = VGroup()
        for m in ms:
            pts = [ax.ax.c2p(r, p) for r, p in zip(R[m], P[m])]
            c_ = VGroup(VMobject(color=MCOL[m], stroke_width=3).set_points_as_corners(pts),
                        *[Dot(q, radius=0.05, color=MCOL[m]) for q in pts])
            curves.add(c_)
        real = Dot(ax.ax.c2p(float(g["real_rec"]), float(g["real_prec"])), radius=0.09, color=WHITE)
        rl = label(r"real vs real", font_size=18, color=WHITE).next_to(real, RIGHT, buff=0.1)
        lg = legend([(MCOL[m], MNAME[m]) for m in ms], font_size=20).move_to([3.6, 2.4, 0])
        rows = [
            cmath(r"v", r"=", r"v_{\text{weak}}(x, \tau, c) + w\,\big(v_\theta(x, \tau, c) - v_{\text{weak}}(x, \tau, c)\big)",
                  font_size=28),
        ]
        rows[0].move_to([3.3, 1.2, 0])
        if rows[0].width > 6.6:
            rows[0].width = 6.6
        wl = label(r"guide with a smaller, \ less-trained version of the same model", font_size=20, color=AUTO_C).next_to(rows[0], DOWN, buff=0.12)
        card = history_card(2024, r"Karras et al.: \ autoguidance", r"ImageNet: \ FID $1.01$ at $64^2$, \ $1.25$ at "
                            r"$512^2$", color=C.HUMAN, width=5.4, font_size=19).move_to([3.5, -1.0, 0])
        f1 = {m: float(np.max(2 * P[m] * R[m] / np.maximum(P[m] + R[m], 1e-9))) for m in ms}
        best = max(ms, key=lambda m: f1[m])
        wbest = {m: W[m][int(np.argmax(2 * P[m] * R[m] / np.maximum(P[m] + R[m], 1e-9)))] for m in ms}
        verdict = (f"On our letters the best balance of fidelity and variety is autoguidance's, at w equal to "
                   f"{wbest['auto']:g}." if best == "auto" else
                   f"On our letters the best balance of fidelity and variety is {MSPOKEN[best]}'s, at w equal to "
                   f"{wbest[best]:g}; autoguidance's best comes close.")
        if abs(f1["cfg"] - f1["cls"]) < 0.05:
            cls_note = "Classifier-free guidance and classifier guidance trace similar curves."
        elif f1["cfg"] > f1["cls"]:
            cls_note = "Classifier-free guidance reaches a better balance than classifier guidance with our small noisy classifier."
        else:
            cls_note = "Classifier guidance, with our small noisy classifier, reaches a better balance than classifier-free guidance."
        ta = take_away(r"Guidance trades variety for fidelity; \ which push you add decides the rate of exchange.")
        with self.voiceover(
            "Guidance trades variety for fidelity. Plot every weight on a plane: recall across, precision up. "
            "<bookmark mark='a'/> " + cls_note + " "
            "<bookmark mark='b'/> In 2024 Tero Karras and colleagues asked why push away from the unconditional "
            "model at all. Its fault is that it is worse: so guide instead with a smaller, less-trained version of "
            "the same conditional model. <bookmark mark='d'/> The push then corrects the model's own errors, "
            "without dragging it towards a different distribution. <bookmark mark='e'/> They set records on "
            "ImageNet: an FID of 1.01 at 64 pixels and 1.25 at 512. <bookmark mark='c'/> Our weak model is narrower "
            f"and trained an eighth as long. {verdict}"
        ) as vo:
            self.play(FadeIn(ax), FadeIn(real), FadeIn(rl), FadeIn(lg))
            vo.wait_until("a")
            self.play(Create(curves[0]), Create(curves[1]), run_time=1.6)
            vo.wait_until("b")
            self.play(Write(rows[0]), FadeIn(wl))
            vo.wait_until("d")
            self.play(Create(curves[2]), run_time=1.4)
            vo.wait_until("e")
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(Indicate(curves[ms.index(best)], color=WHITE, scale_factor=1.05))
            self.play(FadeIn(ta, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()
