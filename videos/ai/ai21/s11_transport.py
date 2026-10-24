from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai21.common import (DATA, FM_C, NOISE, OT_C, PART, SCORE, Panel, load, panel_arrows, take_away)

TRIG_C = C.BITS


class Transport(VoiceoverScene):
    def construct(self):
        self.card()
        self.monge()
        self.matching()
        self.check()
        self.interpolants()

    def card(self):
        card = chapter_card(10, r"Optimal transport and flow matching", r"What is the cheapest way to carry noise into data?",
                            part=PART)
        with self.voiceover("Chapter ten. Optimal transport and flow matching."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def monge(self):
        tr = load("transport")
        Z, X = np.asarray(tr["ot_z"])[:200], np.asarray(tr["ot_x"])[:200]
        pn = Panel(6.6, center=[0, -0.6, 0], xlim=(-3.4, 3.4), ylim=(-3.0, 2.6))  # slides left for the card
        dz, dx = pn.dots(Z, NOISE, radius=0.03), pn.dots(X, DATA, radius=0.03)
        lines = VGroup(*[Line(a, b, stroke_width=1.0, color=OT_C, stroke_opacity=0.5) for a, b in zip(pn.pts(Z), pn.pts(X))])
        movers = pn.dots(Z, OT_C, radius=0.03)
        card = theorem_card(r"Benamou--Brenier", VGroup(
            MathTex(r"W_2^2(p_0, p_1) = \min_{p,\, v} \int_0^1\!\!\int \|v(x, \tau)\|^2\, p(x, \tau)\, dx\, d\tau", font_size=28),
            MathTex(r"\text{subject to}\quad \partial_\tau p + \nabla \cdot (p\, v) = 0", font_size=28),
            label(r"the best flow: \ every particle in a straight line, \ at constant speed", font_size=22, color=OT_C)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15), who=r"Monge (1781), \ Kantorovich (1942), \ Benamou \& Brenier (2000)",
            width=6.2).move_to([3.5, 0.6, 0])
        cost = float(tr["cost_ot"])
        cl = label(rf"the optimal pairing of ${int(tr['n']):,}$ points: \ cost ${cost:.3f}$".replace(",", "{,}"), font_size=20,
                   color=OT_C).next_to(pn, DOWN, buff=0.12)
        with self.voiceover(
            "Step back to an older question. In 1781 Gaspard Monge asked how to move a pile of earth into a hole "
            "with the least work. <bookmark mark='a'/> Pair every bit of noise with a bit of data so that the "
            "average squared distance moved is as small as possible: Leonid Kantorovich's 1942 version, and its "
            "minimum is the Wasserstein distance of Part 20. <bookmark mark='b'/> In 2000 Jean-David Benamou and Yann "
            "Brenier wrote the same problem as a flow: of every velocity field that carries one density into the "
            "other, find the one with the least kinetic energy. <bookmark mark='c'/> The answer moves every particle "
            "in a straight line at constant speed, and the lines never cross."
        ) as vo:
            self.play(FadeIn(pn), FadeIn(dz), FadeIn(dx))
            vo.wait_until("a")
            self.play(Create(lines), FadeIn(cl), run_time=2.0)
            vo.wait_until("b")
            self.play(VGroup(pn, dz, dx, lines, cl).animate.shift(LEFT * 3.1), run_time=0.8)
            movers.shift(LEFT * 3.1)
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("c")
            self.add(movers)
            self.play(*pn.move(movers, X), run_time=2.5, rate_func=linear)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def matching(self):
        tr = load("transport")
        Z, X = np.asarray(tr["cond_z"]), np.asarray(tr["cond_x"])
        pn = Panel(5.4, center=[-4.0, 1.1, 0], xlim=(-3.4, 3.4), ylim=(-3.0, 2.6))
        lines = VGroup(*[DashedLine(a, b, stroke_width=1.4, color=GREY_B, dash_length=0.06) for a, b in zip(pn.pts(Z), pn.pts(X))])
        dz, dx = pn.dots(Z, NOISE, radius=0.04), pn.dots(X, DATA, radius=0.04)
        pl = label(r"independent pairs: \ straight, \ crossing", font_size=20, color=GREY_A).next_to(pn, DOWN, buff=0.1)
        colors = {r"z": NOISE, r"x_1": DATA, r"v": FM_C}
        defs = VGroup(cmath(r"x_\tau = (1 - \tau)\,", r"z", r"+ \tau\,", r"x_1", colors=colors, font_size=30),
                      cmath(r"\text{each pair's velocity: }\ ", r"x_1", r"-", r"z", colors=colors, font_size=30)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2).move_to([2.6, 2.5, 0])
        rows = [
            cmath(r"\partial_\tau p_\tau(x)", r"=", r"\mathbb E_{z, x_1}\big[\partial_\tau\, p_\tau(x \mid z, x_1)\big]", font_size=28),
            cmath(r"\partial_\tau p_\tau(x)", r"=", r"-\nabla \cdot \mathbb E_{z, x_1}\big[(x_1 - z)\; p_\tau(x \mid z, x_1)\big]",
                  font_size=28),
            cmath(r"\partial_\tau p_\tau(x)", r"=", r"-\nabla \cdot \big(p_\tau(x)\; v(x, \tau)\big), \quad v(x, \tau) = "
                  r"\mathbb E[x_1 - z \mid x_\tau = x]", font_size=28),
        ]
        whys = [why(r"the marginal: \ an average over pairs"), why(r"each pair moves at its own velocity"),
                why(r"Bayes: \ average the velocity at $x$")]
        step = ladder(self, rows, whys, keep=2, top=0.1, x=-0.8, buff=0.35, edge=6.85)
        small = VGroup(pn, lines, dz, dx).copy()
        small.scale(3.4 / 5.4).move_to([-5.1, 1.9, 0])
        loss = label(r"and the regression $\big\| v_\theta(x_\tau, \tau) - (x_1 - z) \big\|^2$ has the same minimizer \ "
                     r"(the trick of chapter four)", font_size=22, color=FM_C).to_edge(DOWN, buff=0.3)
        cite_ = cite(r"Lipman et al.; \ Liu, Gong \& Liu; \ Albergo \& Vanden-Eijnden \ (all 2023)", corner=UR, font_size=18)
        with self.voiceover(
            "Flow matching borrows the straight lines without solving the transport problem. Three groups proposed "
            "it at once, in 2023: Yaron Lipman and colleagues at Meta, Xingchao Liu and colleagues in Texas, and "
            "Michael Albergo and Eric Vanden-Eijnden in New York. <bookmark mark='a'/> Pair noise and data at random, "
            "join each pair with a straight line, and the pair's velocity is simply data minus noise. "
            "<bookmark mark='b'/> But these lines cross, and a flow can't: at a crossing a particle would need two "
            "velocities. The theorem that saves it: the density at time tau is an average over pairs, "
            "<bookmark mark='c'/> each moving at its own velocity, <bookmark mark='d'/> so it obeys the continuity "
            "equation with the average velocity at each point: the expected data-minus-noise, given that a line "
            "passes through x. <bookmark mark='e'/> And regressing on the pairs' velocities learns exactly that "
            "average, the same trick as denoising score matching."
        ) as vo:
            self.play(FadeIn(cite_), FadeIn(pn), FadeIn(dz), FadeIn(dx))
            vo.wait_until("a")
            self.play(Create(lines), FadeIn(defs), FadeIn(pl))
            vo.wait_until("b")
            self.play(Transform(VGroup(pn, lines, dz, dx), small), FadeOut(pl), run_time=1.0)
            step(0)
            vo.wait_until("c")
            step(1)
            vo.wait_until("d")
            step(2)
            vo.wait_until("e")
            self.play(FadeIn(loss))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def check(self):
        tr = load("transport")
        G = np.asarray(tr["grid"])
        taus = [float(t) for t in tr["field_taus"]]
        P = np.asarray(tr["fm_paths"])
        pn = Panel(6.4, center=[-3.2, 0.1, 0], xlim=(-3.4, 3.4), ylim=(-3.0, 2.6))
        fields = [panel_arrows(pn, G, np.asarray(tr[f"field{t:g}"]), color=FM_C, max_len=0.3, stroke_width=1.8) for t in taus]
        tl = [label(rf"$\tau = {t:g}$", font_size=24, color=FM_C).next_to(pn, UP, buff=0.1) for t in taus]
        dots = pn.dots(P[0][:200], NOISE, radius=0.025)
        trails = pn.paths(P[:, :200:4], FM_C, stroke_width=1.2, opacity=0.6)
        rows = tr["marginal_rows"]
        ok = all(r["sw_flow"] <= r["sw_floor_hi"] for r in rows)
        tab = VGroup(label(r"particles following $v$ \ against the interpolation itself", font_size=20, color=GREY_A),
                     label(rf"(fresh samples, \ ${int(tr['n']):,}$ points: \ lowest to highest of $8$)".replace(",", "{,}"),
                           font_size=18, color=GREY_B),
                     *[label(rf"$\tau = {r['tau']:g}$: \ ${r['sw_flow']:.3f}$ \ (${r['sw_floor_lo']:.3f}$ to "
                             rf"${r['sw_floor_hi']:.3f}$)", font_size=20) for r in rows]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).move_to([3.7, 1.6, 0])
        ci, cf, co = (float(tr[k]) for k in ("cost_indep", "cost_fm", "cost_ot"))
        act = float(tr["action_fm"])
        st = float(tr["straight_fm"])
        costs = VGroup(label(r"average squared distance moved:", font_size=20, color=GREY_A),
                       label(rf"random pairs: \ ${ci:.2f}$", font_size=20, color=GREY_B),
                       label(rf"the flow's map: \ ${cf:.3f}$ \ (its kinetic energy: ${act:.2f}$)", font_size=20, color=FM_C),
                       label(rf"the optimal pairing: \ ${co:.3f}$", font_size=20, color=OT_C),
                       label(rf"straightness of the flow's paths: \ ${st:.2f}$ \ ($1$: straight)", font_size=20, color=FM_C)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).move_to([3.7, -1.6, 0])
        verdict = ("At every time we checked, they are as close to it as fresh samples are: the theorem holds."
                   if ok else "At every time we checked, they are close to it, nearly as close as fresh samples.")
        near = cf - co < 0.25 * (ci - co)
        cost_note = (f"the flow's own map moves points {cf:.3f} on average, close to the optimal {co:.3f} and far below "
                     f"random pairing's {ci:.2f}. " if near else
                     f"the flow's map moves points {cf:.3f} on average, between the optimal {co:.3f} and random "
                     f"pairing's {ci:.2f}. ")
        with self.voiceover(
            "On our letters this average velocity is known exactly. Here it is at four moments: early on, everything "
            "heads for the middle; late, each point heads for its nearest stroke. <bookmark mark='a'/> Follow it "
            "from noise, and compare the particles with the straight-line interpolation of random pairs at the same "
            f"time. {verdict} <bookmark mark='b'/> But look at the paths: they bend, with a straightness of {st:.2f}. "
            "<bookmark mark='c'/> And the cost: " + cost_note + f"Its kinetic energy, {act:.2f}, is far above its "
            "cost: the paths are curved and the speed uneven. Flow matching is not optimal transport; it is a good "
            "start."
        ) as vo:
            self.play(FadeIn(pn), FadeIn(fields[0]), FadeIn(tl[0]))
            for k in range(1, len(taus)):
                self.play(ReplacementTransform(fields[k - 1], fields[k]), ReplacementTransform(tl[k - 1], tl[k]), run_time=1.0)
            vo.wait_until("a")
            self.play(fields[-1].animate.set_opacity(0.2), FadeIn(dots), FadeOut(tl[-1]))
            self.play(*pn.move(dots, P[-1][:200]), Create(trails), run_time=3.0)
            self.play(FadeIn(tab))
            vo.wait_until("b")
            self.play(Indicate(trails, color=WHITE))
            vo.wait_until("c")
            self.play(FadeIn(costs))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def interpolants(self):
        tr = load("transport")
        panels = VGroup()
        for i, (k, col, nm) in enumerate((("fm", FM_C, r"straight line: \ $x_\tau = (1-\tau)\, z + \tau\, x_1$"),
                                          ("trig", TRIG_C, r"diffusion: \ $x_\tau = \cos(\tfrac{\pi\tau}{2})\, z + "
                                                           r"\sin(\tfrac{\pi\tau}{2})\, x_1$"))):
            pn = Panel(5.2, center=[-3.4 + 6.8 * i, -0.55, 0], xlim=(-3.4, 3.4), ylim=(-3.0, 2.6))
            P = np.asarray(tr[f"{k}_paths"])
            panels.add(VGroup(pn, pn.paths(P[:, ::3], col, stroke_width=1.3, opacity=0.7),
                              label(nm, font_size=20, color=col).next_to(pn, UP, buff=0.12),
                              label(rf"straightness ${float(tr[f'straight_{k}']):.2f}$", font_size=20, color=col).next_to(pn, DOWN, buff=0.1)))
        d = definition_card(r"stochastic interpolants", MathTex(r"x_\tau = \alpha(\tau)\, z + \beta(\tau)\, x_1 \;\big(+\, "
                                                               r"\gamma(\tau)\, n\big)", font_size=28), width=6.0)
        d.to_edge(UP, buff=0.25)
        sf, st = float(tr["straight_fm"]), float(tr["straight_trig"])
        verdict = ("Measured on our letters, the diffusion path's flow is, if anything, the straighter: "
                   f"{st:.2f} against {sf:.2f}." if st > sf else
                   f"Measured on our letters, the straight line's flow is straighter: {sf:.2f} against {st:.2f}.")
        ta = take_away(r"The bends come from averaging over random pairings. \ To straighten the flow, \ change the pairing.")
        with self.voiceover(
            "Albergo and Vanden-Eijnden's framing makes the family clear: a stochastic interpolant mixes noise and "
            "data with any two coefficient curves, plus optional noise. <bookmark mark='a'/> Flow matching's "
            "straight line is one choice; a diffusion model's quarter circle, cosine and sine, is another, and the same "
            "average-velocity argument turns either into a flow. <bookmark mark='b'/> " + verdict + " Straight "
            "lines between pairs do not make straight flows. <bookmark mark='c'/> The bends come from averaging over "
            "random pairings; to straighten the flow, change the pairing. That is the next chapter."
        ) as vo:
            self.play(FadeIn(d, shift=DOWN * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(panels[0][0], panels[0][2], panels[1][0], panels[1][2])),
                      Create(panels[0][1]), Create(panels[1][1]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(panels[0][3]), FadeIn(panels[1][3]))
            vo.wait_until("c")
            ta.to_edge(UP, buff=0.3)
            self.play(FadeOut(d), FadeIn(ta, shift=DOWN * 0.2))
        self.wait(0.3)
        self.clear_scene()
