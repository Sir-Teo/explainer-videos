from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai21.common import DATA, DDIM_C, DDPM_C, NOISE, PART, SCORE, Panel, load, take_away

SDE_C, ODE_C = DDPM_C, DDIM_C


class SDE(VoiceoverScene):
    def construct(self):
        self.card()
        self.forward()
        self.reverse()
        self.flow()
        self.compare()

    def card(self):
        card = chapter_card(5, r"Running time backwards", r"Is there one equation behind every sampler?", part=PART)
        with self.voiceover("Chapter five. Running time backwards."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def forward(self):
        s = load("sde")
        ts = [float(t) for t in s["snap_t"]]
        snaps = np.asarray(s["ode_snaps"])  # the marginals, from noise (t = 1) to data
        pn = Panel(6.0, center=[-3.4, -0.4, 0], xlim=(-3.2, 3.4), ylim=(-3.0, 2.6))
        dots = pn.dots(snaps[-1], DATA, radius=0.02)
        tl = label(rf"$t = {ts[-1]:g}$", font_size=26, color=GREY_A).next_to(pn, UP, buff=0.12)
        d = definition_card(r"the forward SDE", VGroup(
            MathTex(r"dx = -\tfrac12 \beta(t)\, x\, dt + \sqrt{\beta(t)}\; dW", font_size=34),
            label(r"a shrink, \ and Brownian kicks \ (Part 5's Ornstein--Uhlenbeck)", font_size=22, color=GREY_A),
            label(r"the thousand-step chain, \ as the steps shrink to nothing", font_size=22, color=GREY_A),
            label(r"here $\beta(t)$ rises from $0.1$ to $20$ as $t$ goes from $0$ to $1$", font_size=22, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.18), width=6.2).move_to([3.5, 0.3, 0])
        cite_ = cite(r"Y.~Song, J.~Sohl-Dickstein, D.~Kingma, A.~Kumar, S.~Ermon \& B.~Poole, \textit{Score-Based "
                     r"Generative Modeling through SDEs} (2021)", corner=DR, font_size=18)
        with self.voiceover(
            "In 2021 Yang Song and colleagues let the number of steps go to infinity. <bookmark mark='a'/> The chain of "
            "small shrinks and small kicks becomes a stochastic differential equation: a drift towards the origin, "
            "and Brownian motion, Part 5's Ornstein-Uhlenbeck process with a rate that rises over time. "
            "<bookmark mark='b'/> Run it, and the letters dissolve into a bell of noise."
        ) as vo:
            self.play(FadeIn(pn), FadeIn(dots), FadeIn(tl), FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(d, shift=UP * 0.2))
            vo.wait_until("b")
            for k in range(len(ts) - 2, -1, -1):
                t2 = label(rf"$t = {ts[k]:g}$", font_size=26, color=GREY_A).move_to(tl)
                col = interpolate_color(ManimColor(DATA), ManimColor(NOISE), 1 - k / (len(ts) - 1))
                self.play(*pn.move(dots, snaps[k], color=col), Transform(tl, t2), run_time=0.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def reverse(self):
        s = load("sde")
        P = np.asarray(s["sde_paths"])
        snaps = np.asarray(s["sde_snaps"])
        pn = Panel(6.0, center=[-3.4, -0.4, 0], xlim=(-3.2, 3.4), ylim=(-3.0, 2.6))
        dots = pn.dots(snaps[0], NOISE, radius=0.02)
        card = theorem_card(r"time reversed", VGroup(
            MathTex(r"dx = \big[-\tfrac12 \beta(t)\, x - \beta(t)\,", r"\nabla \log p_t(x)", r"\big]\, dt + \sqrt{\beta(t)}\; "
                    r"d\bar W", font_size=30),
            label(r"run from $t = 1$ down to $0$, \ $d\bar W$: \ Brownian motion in reversed time", font_size=20,
                  color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.15), who=r"Anderson (1982)", width=6.6)
        card.body[0][1].set_color(SCORE)
        card.move_to([3.4, 0.9, 0])
        note_ = label(r"the score: \ the one thing that must be learned", font_size=24, color=SCORE).next_to(card, DOWN, buff=0.3)
        trails = pn.paths(P, SDE_C, stroke_width=1.3, opacity=0.7)
        with self.voiceover(
            "In 1982 Brian Anderson showed that such a diffusion has a reverse in time that is also a diffusion: "
            "the same shrink and kicks, plus a push up the score of the noised data at that moment. "
            "<bookmark mark='a'/> The score is the only thing in it we don't know, and the last three chapters "
            "showed how a network learns it. <bookmark mark='b'/> Here it is run with the exact score of our "
            "letters: noise flows back into the letters, each point jittering all the way."
        ) as vo:
            self.play(FadeIn(pn), FadeIn(dots), FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(note_))
            vo.wait_until("b")
            for k in range(1, len(snaps)):
                col = interpolate_color(ManimColor(NOISE), ManimColor(DATA), k / (len(snaps) - 1))
                self.play(*pn.move(dots, snaps[k], color=col), run_time=0.45)
            self.play(Create(trails), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def flow(self):
        rows = [
            cmath(r"\partial_t p", r"=", r"-\nabla \cdot \big(f\, p\big) + \tfrac12\, g^2\, \Delta p", font_size=34),
            cmath(r"\Delta p", r"=", r"\nabla \cdot \big(\nabla p\big) = \nabla \cdot \big(p\, \nabla \log p\big)", font_size=34),
            cmath(r"\partial_t p", r"=", r"-\nabla \cdot \Big( \big[f - \tfrac12\, g^2\, \nabla \log p\big]\; p \Big)",
                  font_size=34),
            cmath(r"\frac{dx}{dt}", r"=", r"f(x, t) - \tfrac12\, g(t)^2\,", r"\nabla \log p_t(x)",
                  colors={r"\nabla \log p_t(x)": SCORE}, font_size=34),
        ]
        whys = [why(r"Fokker--Planck \ (Part 5), \ drift $f$, \ noise $g$"), why(r"$\nabla p = p\, \nabla \log p$"),
                why(r"one divergence: \ a continuity equation"), why(r"particles moving with that velocity: \ no noise")]
        step = ladder(self, rows, whys, keep=4, top=2.6, x=-2.2, buff=0.55, edge=6.85)
        box = theorem_card(r"the probability-flow ODE", label(r"a deterministic flow whose particles have the same "
                                                              r"density $p_t$ at every time as the SDE's", font_size=24),
                           width=8.4).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "There is a second way back, with no randomness at all. Start from Part 5's Fokker-Planck equation for "
            "the density: the drift moves it, the noise spreads it. <bookmark mark='a'/> The spreading term can be "
            "rewritten, because the gradient of p is p times the gradient of log p. <bookmark mark='b'/> Now both "
            "terms are a divergence of something times p: a continuity equation, the law of a fluid whose particles "
            "move with a velocity field. <bookmark mark='c'/> So particles that simply follow this velocity, with no "
            "noise at all, have exactly the same density at every moment as the noisy ones. <bookmark mark='d'/> "
            "Song and colleagues called it the probability-flow ODE: one more use for the same score."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            self.play(FadeIn(box, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def compare(self):
        s = load("sde")
        ts = [float(t) for t in s["snap_t"]]
        panels = []
        for i, kind in enumerate(("sde", "ode")):
            pn = Panel(4.4, center=[-4.5 + 4.65 * i, 0.75, 0], xlim=(-3.2, 3.4), ylim=(-3.0, 2.6))
            P = np.asarray(s[f"{kind}_paths"])
            col = SDE_C if kind == "sde" else ODE_C
            panels.append(VGroup(pn, pn.paths(P, col, stroke_width=1.4, opacity=0.8),
                                 pn.dots(P[0], NOISE, radius=0.03), pn.dots(P[-1], DATA, radius=0.03),
                                 label(r"reverse SDE" if kind == "sde" else r"probability-flow ODE", font_size=22,
                                       color=col).next_to(pn, UP, buff=0.1)))
        sub = label(r"the same $40$ starting points", font_size=20, color=GREY_B).next_to(VGroup(*panels), DOWN, buff=0.12)
        top = 1.15 * max(float(np.max(s["sde_sw"])), float(np.max(s["ode_sw"])), float(np.max(s["floor_sw"])))
        ys = next(v for v in (0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0) if v >= top / 3)
        g = axes([0, 1], [0, top], x_length=3.4, y_length=2.6, xlabel=r"time $t$", ylabel=r"distance from $p_t$",
                 xticks=[0, 0.5, 1], yticks=[round(ys * k, 3) for k in range(int(top / ys) + 1)], center=[5.0, 0.55, 0])
        tt = np.array(ts)
        cs = curve(g.ax, tt, np.asarray(s["sde_sw"]), SDE_C, 3)
        co = curve(g.ax, tt, np.asarray(s["ode_sw"]), ODE_C, 3)
        cf = DashedLine(g.ax.c2p(0, float(np.mean(s["floor_sw"]))), g.ax.c2p(1, float(np.mean(s["floor_sw"]))),
                        color=GREY_B, stroke_width=1.5)
        fl = label(r"fresh samples of $p_t$", font_size=16, color=GREY_B).next_to(cf, UP, buff=0.04)
        floor = np.asarray(s["floor_sw"])
        sde_sw, ode_sw = np.asarray(s["sde_sw"]), np.asarray(s["ode_sw"])
        ode_ok = bool(np.all(ode_sw < 1.3 * floor + 0.01))
        sde_ok = bool(np.all(sde_sw < 1.3 * floor + 0.01))
        end_s, end_o = float(sde_sw[-1]), float(ode_sw[-1])
        n_sde = int(s["n_sde"])
        if ode_ok and sde_ok:
            verdict = "Both stay as close to the true marginals as fresh samples of them, at every time we measured."
        elif ode_ok:
            verdict = (f"The ODE stays as close to the true marginals as fresh samples of them, all the way down; the "
                       f"SDE, with {n_sde:,} random steps, drifts a little at the end, {end_s:.3f} against the ODE's "
                       f"{end_o:.3f}: random steps need to be smaller.")
        else:
            verdict = f"Both stay near the true marginals; at the end the SDE is {end_s:.3f} away, the ODE {end_o:.3f}."
        rt = float(s["roundtrip_err"])
        dec = max(1, int(math.floor(-math.log10(max(rt, 1e-300)))))
        stats = VGroup(label(rf"path length: \ SDE ${float(s['sde_len']):.1f}$, \ ODE ${float(s['ode_len']):.1f}$",
                             font_size=20, color=GREY_A),
                       label(rf"the ODE there and back: \ off by ${sci(rt, 1)}$", font_size=20, color=ODE_C),
                       label(r"Song et al.\ (2021), CIFAR-10: \ FID $2.20$", font_size=20, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).to_edge(DOWN, buff=0.35).shift(RIGHT * 2.6)
        with self.voiceover(
            "Here are both, run with the exact score from the same forty starting points. <bookmark mark='a'/> The "
            f"SDE's paths wander: on average each is {float(s['sde_len']):.1f} long. The ODE's glide, "
            f"{float(s['ode_len']):.1f}. They end at different places. <bookmark mark='b'/> But measure the whole "
            f"clouds against fresh samples of the true density, at every time. {verdict} <bookmark mark='c'/> And "
            f"the ODE can be run both ways: from data to noise and back, the points return to where they started to "
            f"{dec} decimal places: "
            "an invertible map, Part 20's continuous normalizing flow, with an exact likelihood. One learned score, "
            "two ways back; the next chapters are about solving them in as few steps as possible."
        ) as vo:
            self.play(*[FadeIn(VGroup(p[0], p[2], p[4])) for p in panels], FadeIn(sub))
            vo.wait_until("a")
            self.play(*[Create(p[1]) for p in panels], run_time=2.0)
            self.play(*[FadeIn(p[3]) for p in panels])
            vo.wait_until("b")
            self.play(FadeIn(g), Create(cf), FadeIn(fl), Create(cs), Create(co))
            vo.wait_until("c")
            self.play(FadeIn(stats))
        self.wait(0.3)
        self.clear_scene()
