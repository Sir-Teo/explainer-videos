from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import sim
from videos.quant.quant5.common import BM, DRIFT, ITO, JUMP, PART, STRAT, load, pause


class Signatures(VoiceoverScene, ThreeDScene):
    def construct(self):
        hx = load("helix")
        sr = load("sig_regression")
        self.card()
        self.helix(hx)
        self.chen()
        self.lab(sr)
        self.replay(sr)

    def card(self):
        c = chapter_card(16, r"Rough paths and signatures", r"What does an integral need to know about a path?",
                         part=PART)
        with self.voiceover("Chapter sixteen. Rough paths, and signatures."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def helix(self, hx):
        ax = ThreeDAxes(x_range=[-1, 1, 0.5], y_range=[-1, 1, 0.5], z_range=[0, 1.3, 0.5], x_length=5.0, y_length=5.0,
                        z_length=4.0, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False, "stroke_width": 2})
        ax.shift(LEFT * 1.6 + DOWN * 0.4)
        ns = ["2", "4", "8"]
        cols = {"2": ITO, "4": STRAT, "8": JUMP}
        floors, sols = {}, {}
        for k in ns:
            d = hx[k]
            n = int(k)
            t = np.asarray(d["t"])
            X1, X2 = np.cos(n ** 2 * t) / n, np.sin(n ** 2 * t) / n
            floors[k] = VMobject(stroke_color=cols[k], stroke_width=2.5).set_points_as_corners(
                [ax.c2p(a, b, 0) for a, b in zip(X1, X2)])
            sols[k] = VMobject(stroke_color=cols[k], stroke_width=3).set_points_as_corners(
                [ax.c2p(a, b, c) for a, b, c in zip(d["Y1"], d["Y2"], d["Y3"])])
        eq = VGroup(MathTex(r"X^{(n)}_t = \tfrac1n\big(\cos n^2 t,\ \sin n^2 t\big)", font_size=28),
                    MathTex(r"dY^1 = dX^1,\ \ dY^2 = dX^2,\ \ dY^3 = Y^1\,dX^2 - Y^2\,dX^1", font_size=26),
                    MathTex(r"\|X^{(n)}\|_\infty = \tfrac1n \to 0, \qquad Y^3_1 \to 1", font_size=28, color=JUMP)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UR, buff=0.3)
        tab = VGroup(*[MathTex(rf"n = {k}:\ \sup|X| = {hx[k]['sup']:.3f},\ \ Y^3_1 = {hx[k]['Y3_end']:.3f}", font_size=24,
                               color=cols[k]) for k in ns]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        tab.next_to(eq, DOWN, buff=0.35).align_to(eq, LEFT)
        rows = VGroup(MathTex(r"A_t = \tfrac12\int_0^t \big(X^1 dX^2 - X^2 dX^1\big) = \tfrac12 \cdot \tfrac{1}{n^2} \cdot n^2 t "
                              r"= \tfrac{t}{2}", font_size=26, color=ITO),
                      label(r"a circle of radius $r$ at angular speed $\omega$ sweeps area at rate $\tfrac12 r^2\omega$; "
                            r"$Y^3 = 2A$", font_size=18, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        rows.to_corner(DR, buff=0.35)
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=0.9)
        self.add_fixed_in_frame_mobjects(eq, tab, rows)
        self.remove(eq, tab, rows)
        with self.voiceover(
            "Why does integration need more than the path? Terry Lyons's example: a path running in tiny fast "
            "circles, radius one over n, n squared radians a unit of time. Seen from above, it shrinks to a point as "
            "n grows. <bookmark mark='a'/> Feed it to a simple equation whose third coordinate integrates Y one d X "
            "two minus Y two d X one. <bookmark mark='b'/> Turn the camera to the side: the solutions are helices "
            "whose shadows shrink while their height still climbs to about one. <bookmark mark='c'/> The height is "
            "twice the Lévy area the path sweeps, and a small circle swept fast accrues area at a constant rate. So "
            "the solution map is not continuous in the path alone. Lyons proved in 1998 that it is continuous in the "
            "path together with its area: that pair is a rough path."
        ) as vo:
            self.play(Create(ax), FadeIn(eq[0]))
            for k in ns:
                self.play(Create(floors[k]), run_time=1.2)
            vo.wait_until("a")
            self.play(FadeIn(eq[1]))
            vo.wait_until("b")
            self.move_camera(phi=70 * DEGREES, theta=-50 * DEGREES, run_time=2.5)
            for k in ns:
                self.play(Create(sols[k]), run_time=1.5)
            self.play(FadeIn(tab), FadeIn(eq[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows))
            self.move_camera(theta=-20 * DEGREES, run_time=max(vo.remaining(0.5) - 0.5, 2))
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0,
                         added_anims=[FadeOut(VGroup(ax, *floors.values(), *sols.values())), FadeOut(eq), FadeOut(tab),
                                      FadeOut(rows)], run_time=1.5)
        self.clear_scene()

    def chen(self):
        a = np.array([[0, 0], [1, 0], [1, 1]], float)
        b = np.array([[0, 0], [0, 1], [1, 1]], float)
        sa, sb = sim.signature2(a), sim.signature2(b)
        plane = NumberPlane(x_range=[-0.5, 1.5, 0.5], y_range=[-0.5, 1.5, 0.5], x_length=3.4, y_length=3.4,
                            background_line_style={"stroke_color": GREY_D, "stroke_width": 1}).to_corner(UL, buff=0.4)
        pa = VMobject(stroke_color=BM, stroke_width=5).set_points_as_corners([plane.c2p(*p) for p in a])
        pb = VMobject(stroke_color=STRAT, stroke_width=5).set_points_as_corners([plane.c2p(*p) for p in b])
        area = VGroup(Polygon(*[plane.c2p(*p) for p in [(0, 0), (1, 0), (1, 1)]], stroke_width=0, fill_color=BM,
                              fill_opacity=0.35),
                      Polygon(*[plane.c2p(*p) for p in [(0, 0), (0, 1), (1, 1)]], stroke_width=0, fill_color=STRAT,
                              fill_opacity=0.35))
        pc, ans = pause(r"Right-then-up and up-then-right: same increments. Which level of the signature first tells "
                        r"them apart?", rf"Level 2: L\'evy areas ${sa['levy_area'][0, 1]:+.1f}$ and "
                        rf"${sb['levy_area'][0, 1]:+.1f}$.", width=5.4, font_size=19)
        VGroup(pc, ans).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(plane, DOWN, buff=0.3).align_to(plane, LEFT)
        rows = [cmath(r"S(X)^{i_1 \dots i_k}_{s,t}", r"=", r"\int_{s < u_1 < \dots < u_k < t} dX^{i_1}_{u_1} \cdots dX^{i_k}_{u_k}",
                      font_size=28),
                cmath(r"S(X * Y)", r"=", r"S(X) \otimes S(Y), \qquad S(\text{segment } \Delta) = \Big(1, \Delta, "
                      r"\tfrac{\Delta^{\otimes 2}}{2!}, \tfrac{\Delta^{\otimes 3}}{3!}, \dots\Big)", font_size=28,
                      colors={r"S(X) \otimes S(Y)": ITO}),
                cmath(r"\big\|S^k(X)\big\|", r"\le", r"\frac{L^k}{k!}", font_size=30),
                cmath(r"\langle \ell_1, S\rangle\,\langle \ell_2, S\rangle", r"=", r"\langle \ell_1 \sqcup\!\sqcup\, \ell_2, S\rangle",
                      font_size=30)]
        whys = [why(r"the signature: every iterated integral; level 1 is the increment, the antisymmetric part of "
                    r"level 2 the L\'evy area", 18),
                why(r"Chen (1957): concatenating paths multiplies signatures; a straight segment's is the tensor "
                    r"exponential", 18),
                why(r"the simplex has volume $1/k!$: truncation error decays factorially", 18),
                why(r"the shuffle product: linear functionals form an algebra; with time added, Stone--Weierstrass "
                    r"gives universal approximation on compact sets", 18)]
        step = ladder(self, rows, whys, keep=4, top=3.3, x=2.3, buff=0.5, edge=6.95)
        with self.voiceover(
            "A pause. Right then up, or up then right: same start, same end, same increments. Which statistic tells "
            "them apart? <bookmark mark='a'/> The signed area to the chord: plus a half and minus a half. Kuo-Tsai "
            "Chen showed in 1957 that a path is captured by all its iterated integrals, its signature; level one is "
            "the increment, level two contains the area. <bookmark mark='b'/> Chen's identity: joining paths "
            "multiplies signatures, and a straight segment's signature is the tensor exponential of its increment. "
            "<bookmark mark='c'/> The levels shrink factorially. <bookmark mark='d'/> And products of linear "
            "functions of the signature are again linear, so by Stone-Weierstrass, linear functions of the signature "
            "approximate any continuous function of the path."
        ) as vo:
            self.play(FadeIn(plane), Create(pa), Create(pb), FadeIn(pc), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(area), FadeIn(ans))
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.wait(0.4)
        self.clear_scene()

    def lab(self, sr):
        card = lab_card(r"the signature, by Chen's identity", [
            "def signature(path, depth):                 # Chen, segment by segment",
            "    X = np.asarray(path, float)",
            "    S = [np.ones(())] + [np.zeros((X.shape[1],) * k) for k in range(1, depth + 1)]",
            "    for dx in np.diff(X, axis=0):",
            "        seg = [np.ones(())]                          # exp of a straight segment",
            "        for k in range(1, depth + 1):",
            "            seg.append(np.multiply.outer(seg[-1], dx) / k)",
            "        S = [sum(np.multiply.outer(S[i], seg[k - i]) for i in range(k + 1))",
            "             for k in range(depth + 1)]              # S <- S (x) seg",
            "    return S",
        ], source="explainer/quant/house/sim.py", width=9.4, font_size=16).to_edge(UP, buff=0.4)
        sq = np.array([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]], float)
        S = sim.signature(sq, 2)
        outs = [f"S = signature(unit square, 2):  level 1 = {S[1].round(3).tolist()},  area = {(S[2][0, 1] - S[2][1, 0]) / 2:.3f}",
                f"signature_batch: {sr['N']:,} paths, depth 5 -> {sr['n_feats'][-1]} features (time + 2 assets)"]
        with self.voiceover(
            "Here is the House's signature, exactly as the identity reads. Start with the signature of nothing: one, "
            "then zeros. For each straight segment, build its tensor exponential level by level, each level the "
            "previous one times the increment, divided by k, and multiply it into the running signature with Chen's "
            "product. <bookmark mark='a'/> Run it on the unit square traversed once: the increments are zero, and the "
            "area is one. <bookmark mark='b'/> A batched version computes it for twenty thousand paths at once, three "
            "hundred and sixty-three numbers per path at depth five, which the experiment needs."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            lab_run(self, card, outs[:1], font_size=16)
            vo.wait_until("b")
            self.play(FadeIn(Text(outs[1], font="DejaVu Sans Mono", font_size=16).scale(card.text_scale)
                             .next_to(card.out, DOWN, buff=0.12).align_to(card.out, LEFT)))
        self.wait(0.4)
        self.clear_scene()

    def replay(self, sr):
        tg = sr["targets"]
        r2 = np.asarray(tg["asian"]["r2"])
        depths = np.arange(1, 6)

        def frame(i):
            k = str(min(i + 1, 5))
            d = sr["scatter"][k]
            pr, tr = np.asarray(d["pred"]), np.asarray(d["true"])
            hi = float(np.percentile(tr, 99)) * 1.1
            a = axes([0, hi], [0, hi], x_length=4.0, y_length=4.0, xlabel=r"true Asian payoff", ylabel=r"predicted",
                     xticks=[0], yticks=[0], font_size=14)
            dots = VGroup(*[Dot(a.ax.c2p(min(x, hi), np.clip(y, 0, hi)), radius=0.025, color=ITO, fill_opacity=0.7)
                            for x, y in zip(tr, pr)])
            diag = DashedLine(a.ax.c2p(0, 0), a.ax.c2p(hi, hi), color=GREY_B, stroke_width=1.5)
            t = MathTex(rf"\text{{depth }} {k}:\ {sr['n_feats'][int(k) - 1]} \text{{ features}}", font_size=24,
                        color=ITO).next_to(a, UP, buff=0.1)
            return VGroup(a, diag, dots, t)
        rp = TrainingReplay(depths, r2, frame, checkpoints=[1, 2, 3, 4, 5], ylabel=r"hold-out $R^2$, Asian call",
                            xlabel=r"signature depth", color=ITO, left=LEFT * 3.6 + DOWN * 0.3, right=RIGHT * 3.0 + DOWN * 0.3)
        base = tg["asian"]["base"]
        bl = VGroup(*[DashedLine(rp.ax.c2p(1, v), rp.ax.c2p(5, v), color=c, stroke_width=1.8)
                      for v, c in ((base["last"], GREY_B), (base["path"], DRIFT)) if rp.lo < v < rp.hi])
        best = int(np.argmax(r2.mean(0))) + 1
        rm = r2.mean(0)
        tab = VGroup(
            label(rf"average (exactly level 2): $R^2$ = {tg['average']['r2_mean'][1]:.4f} at depth 2", font_size=18,
                  color=GREY_A),
            label(rf"L\'evy area (level 2): $R^2$ = {tg['area']['r2_mean'][1]:.4f} at depth 2, "
                  rf"{tg['area']['base']['path']:.3f} from the raw path", font_size=18, color=GREY_A),
            label(rf"Asian call: best {rm[best - 1]:.3f} at depth {best}; raw path {base['path']:.3f}; last value "
                  rf"{base['last']:.3f}", font_size=18, color=ITO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).to_edge(DOWN, buff=0.15)
        over = rm[-1] < rm[best - 1] - 0.005
        verdict = (f"It peaks at depth {best}, {rm[best - 1]:.3f}, and slips at depth five, {rm[-1]:.3f}: "
                   f"{sr['n_feats'][-1]} features begin to overfit twelve thousand training paths."
                   if over else f"It climbs to {rm[-1]:.3f} at depth five.")
        with self.voiceover(
            "Now learn with it: twenty thousand paths of two correlated assets plus time, and linear regressions on "
            "the truncated signature, scored on unseen paths over five splits. <bookmark mark='a'/> Two checks: the "
            "average price is exactly linear in level two, and so is the area between the assets; at depth two both "
            f"reach an R squared of {tg['average']['r2_mean'][1]:.3f}, while all sixty-five raw prices explain "
            f"{100 * tg['area']['base']['path']:.1f} percent of the area. <bookmark mark='b'/> Then an Asian call, "
            "which is linear in nothing. Scrub through the depths: the predictions tighten onto the diagonal. "
            f"{verdict} The raw path manages {base['path']:.3f}. <bookmark mark='c'/> Signatures return in the next "
            "two chapters, and in Parts fourteen, seventeen and forty-two."
            " Next: how desks build, test and run these models."
        ) as vo:
            self.play(FadeIn(rp), FadeIn(bl))
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(tab[1]))
            vo.wait_until("b")
            rp.play(self, run_time=6)
            self.play(FadeIn(tab[2]))
            vo.wait_until("c")
        self.wait(0.4)
        self.clear_scene()
