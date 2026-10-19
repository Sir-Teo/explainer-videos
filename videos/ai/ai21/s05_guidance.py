from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai21.common import DATA, FM_C, NOISE, SCORE, cloud, load


def guidance_arrows(w: float = 3.0) -> VGroup:
    """Classifier-free guidance at one point: the direction told nothing, the direction told the letter, and the
    difference between them stretched by w."""
    o = np.array([0.0, 0.0, 0.0])
    vu, vc = np.array([2.0, 0.3, 0.0]), np.array([1.9, 1.0, 0.0])
    vg = vu + w * (vc - vu)
    dot = Dot(o, radius=0.07, color=WHITE)
    au = Arrow(o, vu, buff=0, color=GREY_B, stroke_width=5, max_tip_length_to_length_ratio=0.12)
    ac = Arrow(o, vc, buff=0, color=FM_C, stroke_width=5, max_tip_length_to_length_ratio=0.12)
    ag = Arrow(o, vg, buff=0, color=C.BITS, stroke_width=5, max_tip_length_to_length_ratio=0.1)
    diff = DashedLine(vu, vg, color=C.BITS, stroke_width=2, dash_length=0.08)
    lu = label(r"told nothing \ ($\varnothing$): \ unconditional", font_size=22, color=GREY_B).next_to(au.get_end(), RIGHT, buff=0.15)
    lc = label(r"told ``A'': \ conditional", font_size=22, color=FM_C).next_to(ac.get_end(), RIGHT, buff=0.15)
    lg = label(rf"$w = {w:g}$: \ the difference, \ stretched", font_size=22, color=C.BITS).next_to(ag.get_end(), RIGHT, buff=0.15)
    return VGroup(diff, au, ac, ag, dot, lu, lc, lg)


class Guidance(VoiceoverScene):
    def construct(self):
        self.card()
        self.condition()
        self.guide()

    def card(self):
        card = chapter_card(4, r"Guidance", r"How do you ask for something specific?", part=21)
        with self.voiceover("Chapter four. Guidance."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def condition(self):
        g = load("guidance")
        S = 0.75
        A, I_ = cloud(np.asarray(g["A"])[:500], C.TRUE_P, radius=0.02, scale=S), cloud(np.asarray(g["I"])[:500], C.SURPRISE,
                                                                                        radius=0.02, scale=S)
        la = label(r"``A''", font_size=30, color=C.TRUE_P).next_to(A, UP, buff=0.3)
        li = label(r"``I''", font_size=30, color=C.SURPRISE).next_to(I_, UP, buff=0.3)
        colors = {r"c": C.BITS, r"\varnothing": GREY_B}
        f = cmath(r"v_\theta(x, t,", r"c", r")", r"\quad\text{or}\quad", r"v_\theta(x, t,", r"\varnothing", r")", colors=colors,
                  font_size=38).to_edge(DOWN, buff=1.0)
        fl = label(r"told the letter, \ or (one time in five) \ told nothing", font_size=24, color=GREY_A).next_to(f, DOWN, buff=0.15)
        cl = VGroup(label(r"conditional", font_size=22, color=C.BITS).next_to(f[0:3], UP, buff=0.12),
                    label(r"unconditional", font_size=22, color=GREY_B).next_to(f[4:], UP, buff=0.12))
        cite_ = cite(r"J.~Ho \& T.~Salimans, \textit{Classifier-Free Diffusion Guidance} (2022)", corner=DR)
        with self.voiceover(
            "So far the model draws whatever it likes. To ask for something, tell it what you want: a caption, or "
            "here, which letter. <bookmark mark='a'/> We trained a flow model on two letters, A and I, telling it "
            "which letter each training point came from, except one time in five, when it's told nothing. <bookmark mark='b'/> Told the letter, the model is called conditional; told "
            "nothing, unconditional. So one network learns both: the letter it's asked for, and letters in general."
        ) as vo:
            self.play(FadeIn(A), FadeIn(I_), FadeIn(la), FadeIn(li), FadeIn(cite_))
            vo.wait_until("a")
            self.play(Write(f), FadeIn(fl))
            vo.wait_until("b")
            self.play(FadeIn(cl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def guide(self):
        g = load("guidance")
        ws = [float(w) for w in g["ws"]]
        Xs = {w: np.asarray(g[f"w{w:g}"])[:500] for w in ws}
        allx = np.concatenate(list(Xs.values()))
        S = min(1.95 / np.percentile(np.abs(allx[:, 0]), 99.5), 1.35 / np.percentile(np.abs(allx[:, 1]), 99.5))
        panels = VGroup()
        for i, w in enumerate(ws):
            c = np.array([-4.45 + 4.45 * i, -0.3])  # one fixed origin per panel, so a sample's move is its own
            pts = cloud(Xs[w], FM_C, radius=0.018, scale=S, shift=c)
            frame = Rectangle(width=4.2, height=3.0, stroke_color=GREY_D, stroke_width=1.2).move_to([c[0], c[1], 0])
            t = label(rf"$w = {w:g}$", font_size=28, color=C.BITS).next_to(frame, UP, buff=0.15)
            on = float(g[f"onA{w:g}"])
            sp = float(g[f"spread{w:g}"])
            st = label(rf"${100 * on:.0f}\%$ on the A; \ spread ${sp:.2f}$", font_size=20, color=GREY_A).next_to(frame, DOWN, buff=0.1)
            panels.add(VGroup(frame, pts, t, st))
        sub = label(r"the same $500$ starting points in every panel", font_size=20, color=GREY_B)
        sub.next_to(panels, UP, buff=0.3)
        colors = {r"w": C.BITS, r"v_\theta(x,t,c)": FM_C, r"v_\theta(x,t,\varnothing)": GREY_B}
        f = cmath(r"v", "=", r"v_\theta(x,t,\varnothing)", "+", r"w", r"\,\big(", r"v_\theta(x,t,c)", "-",
                  r"v_\theta(x,t,\varnothing)", r"\big)", colors=colors, font_size=34).to_edge(UP, buff=0.4)
        on0, on1, on4 = (float(g[f"onA{w:g}"]) for w in ws)
        sp1, sp4 = float(g["spread1"]), float(g["spread4"])
        tail = label(r"stronger guidance: \ more on target, \ less variety", font_size=26, color=C.BITS).to_edge(DOWN, buff=0.4)
        arrows = guidance_arrows(3.0).move_to(DOWN * 0.3)
        with self.voiceover(
            "Now ask for an A, and mix the two answers. At any point, the unconditional model points one way, the "
            "conditional one another. Start from the unconditional direction, and push along the difference, "
            "towards the conditional one and past it, by a weight w. <bookmark mark='a'/> With w equal to zero, the request is ignored: "
            f"{100 * on0:.0f} percent of samples land on the A. <bookmark mark='b'/> With w equal to one, the "
            f"plain conditional model: {100 * on1:.0f} percent. <bookmark mark='c'/> Push past it, to w equal to four, "
            f"and you overshoot on purpose: {100 * on4:.0f} percent, and the samples crowd towards the most A-like "
            f"part of the A, their spread shrinking from {sp1:.2f} to {sp4:.2f}. Every image model turns this knob: "
            "more faithful to the prompt, less varied."
        ) as vo:
            self.play(Write(f))
            self.play(FadeIn(arrows[4]), GrowArrow(arrows[1]), FadeIn(arrows[5]))
            self.play(GrowArrow(arrows[2]), FadeIn(arrows[6]))
            self.play(Create(arrows[0]), GrowArrow(arrows[3]), FadeIn(arrows[7]))
            vo.wait_until("a")
            self.play(FadeOut(arrows))
            self.play(FadeIn(panels[0]), FadeIn(sub))
            # the same starting noise at every w: each sample slides from where it landed to where it lands now
            vo.wait_until("b")
            self.play(FadeIn(VGroup(panels[1][0], panels[1][2], panels[1][3])), TransformFromCopy(panels[0][1], panels[1][1]),
                      run_time=1.6)
            vo.wait_until("c")
            self.play(FadeIn(VGroup(panels[2][0], panels[2][2], panels[2][3])), TransformFromCopy(panels[1][1], panels[2][1]),
                      FadeIn(tail), run_time=1.6)
        self.wait(0.3)
        self.clear_scene()
