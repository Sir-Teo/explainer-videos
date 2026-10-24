from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai25.common import (AUG, KIND_COLOR, KIND_NAME, PART, PLAIN, STRUCT, SYM, load, node_box, points2d,
                                   take_away, takeaway_anims)


def mean_band(d, kind, sizes, metric="acc"):
    vals = np.array([[d[f"{kind}_{n}_s{s}"][metric] for s in d["seeds"]] for n in sizes])
    return vals.mean(1), vals.min(1), vals.max(1)


class Sets(VoiceoverScene):
    def construct(self):
        self.card()
        self.orders()
        self.theorem()
        self.architecture()
        self.training()
        self.experiment()

    def card(self):
        card = chapter_card(3, r"Functions of sets", r"How do you build a function that ignores order?", lit=(),
                            part=PART)
        with self.voiceover("Chapter three. Functions of sets."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def orders(self):
        d = load("deepsets")
        P = np.asarray(d["examples"])[0]
        perm = np.asarray(d["demo_perm"])
        c = np.array([-4.3, 0.3, 0])
        S = 1.3
        dots = points2d(P, S, c, SYM, 0.07)
        nums = VGroup(*[label(str(i + 1), font_size=15, color=GREY_A).next_to(dots[i], UR, buff=0.02)
                        for i in range(len(P))])
        nums_p = VGroup(*[label(str(int(np.flatnonzero(perm == i)[0]) + 1), font_size=15, color=GREY_A)
                          .next_to(dots[i], UR, buff=0.02) for i in range(len(P))])
        pl = label(r"one set of $16$ points", font_size=24, color=SYM).next_to(dots, UP, buff=0.5)

        def vec(order):
            v = P[order].reshape(-1)
            cells = VGroup()
            for k, val in enumerate(v[:12]):
                cells.add(MathTex(f"{val:+.2f}", font_size=20, color=GREY_A))
            cells.add(MathTex(r"\vdots", font_size=22, color=GREY_B))
            return cells.arrange(DOWN, buff=0.07)

        v1 = vec(np.arange(len(P))).move_to([-1.3, 0.0, 0])
        v2 = vec(perm).move_to([-1.3, 0.0, 0])
        vl = label(r"what an MLP sees: \ $32$ numbers", font_size=20, color=PLAIN).next_to(v1, UP, buff=0.2)
        names = [r"ring", r"disc", r"segment", r"two blobs"]

        def bars(prob, col, x):
            g = VGroup()
            for k, p in enumerate(prob):
                b = Rectangle(width=max(2.4 * p, 0.02), height=0.28, stroke_width=0, fill_color=col, fill_opacity=0.85)
                b.move_to([x + b.width / 2, 1.4 - 0.42 * k, 0])
                g.add(VGroup(b, label(names[k], font_size=18, color=GREY_B).next_to([x, 1.4 - 0.42 * k, 0], LEFT,
                                                                                    buff=0.12)))
            return g

        mlp1 = bars(np.asarray(d["demo_mlp_prob"]), PLAIN, 2.6)
        mlp2 = bars(np.asarray(d["demo_mlp_prob_perm"]), PLAIN, 2.6)
        ds1 = bars(np.asarray(d["demo_ds_prob"]), STRUCT, 2.6).shift(DOWN * 2.4)
        ds2 = bars(np.asarray(d["demo_ds_prob_perm"]), STRUCT, 2.6).shift(DOWN * 2.4)
        h1 = label(KIND_NAME["mlp"], font_size=22, color=PLAIN).move_to([3.4, 2.05, 0])
        h2 = label(KIND_NAME["deepsets"], font_size=22, color=STRUCT).move_to([3.4, -0.35, 0])
        pm, pm2 = np.asarray(d["demo_mlp_prob"]), np.asarray(d["demo_mlp_prob_perm"])
        same_cls = int(pm.argmax()) == int(pm2.argmax())
        mlp_line = (f"its belief that this is a ring goes from {100 * pm[0]:.0f} to {100 * pm2[0]:.0f} percent" if
                    same_cls else f"it changes its mind: from {names[int(pm.argmax())]} to "
                                  f"{names[int(pm2.argmax())]}")
        tag = note(r"computed: \ networks trained here on $8{,}192$ sets", font_size=20).to_corner(DR, buff=0.25)
        with self.voiceover(
            "Sixteen points in the plane, from one of four shapes: a ring, a disc, a segment, or two blobs. Say which. "
            "<bookmark mark='a'/> A plain network needs a list, so we number the points and feed it thirty-two coordinates. "
            "<bookmark mark='b'/> But the numbering is arbitrary: renumber, and the picture is the same while the list is "
            f"not. <bookmark mark='c'/> A plain network trained on eight thousand sets sees a new input: {mlp_line}. "
            "<bookmark mark='d'/> Deep Sets, built for sets, gives exactly the same answer, as it must."
        ) as vo:
            self.play(FadeIn(dots), FadeIn(pl))
            vo.wait_until("a")
            self.play(FadeIn(nums), FadeIn(v1), FadeIn(vl), FadeIn(tag))
            vo.wait_until("b")
            self.play(ReplacementTransform(nums, nums_p), ReplacementTransform(v1, v2), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(h1), FadeIn(mlp1))
            self.play(ReplacementTransform(mlp1, mlp2), run_time=1.2)
            vo.wait_until("d")
            self.play(FadeIn(h2), FadeIn(ds1))
            self.play(ReplacementTransform(ds1, ds2), run_time=1.2)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def theorem(self):
        th = theorem_card(r"Deep Sets", r"a function of finite subsets of a countable set is invariant to the order "
                          r"of its elements \ \textbf{if and only if} \ it can be written $f(X) = \rho\big(\sum_{x \in X}"
                          r" \phi(x)\big)$", who=r"Zaheer, Kottur, Ravanbakhsh, P\'oczos, Salakhutdinov \& Smola (2017)",
                          width=11.8, color=STRUCT).to_edge(UP, buff=0.3)
        rows = [
            cmath(r"\rho\Big(\sum_{x \in X} \phi(x)\Big)", r"\;\Leftarrow\;", r"\text{any order gives the same sum}",
                  font_size=32),
            cmath(r"\phi(x) = 4^{-c(x)}", r",\quad", r"c(x) \in \{1, 2, 3, \dots\}", font_size=32),
            cmath(r"\sum_{x \in X} 4^{-c(x)}", r"=", r"0.d_1 d_2 d_3 \ldots \ (\text{base } 4)", font_size=32),
            cmath(r"f", r"=", r"f \circ \Big(\sum \phi\Big)^{-1} \circ \sum \phi", font_size=32),
        ]
        whys = [why(r"the easy direction"), why(r"number the elements of the universe"),
                why(r"$d_k = 1$ iff element $k$ is in $X$: \ no carries"),
                why(r"one-to-one: \ invert it, \ then apply $f$")]
        for r_ in rows:
            r_.scale(30 / 32)
        step = ladder(self, rows, whys, keep=4, top=1.15, x=-1.6, align_index=1, buff=0.3, edge=6.9)
        cont = label(r"real numbers: \ the power sums $\sum_i x_i^k$, \ $k = 1, \dots, n$, \ pin down $n$ numbers "
                     r"(Newton); \ fewer won't do \ (Wagstaff et al.\ 2019)", font_size=22, color=GREY_A)
        cont.to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The theorem behind Deep Sets, from Manzil Zaheer and colleagues in 2017: a function of sets ignores order "
            "exactly when it is a sum of one function phi over the elements, followed by another function rho. <bookmark "
            "mark='a'/> One direction is easy: a sum is the same in any order. <bookmark mark='b'/> For the other, number "
            "every possible element, and let phi of x be four to the minus its number. <bookmark mark='c'/> In base four, "
            "the sum has a one in place k exactly when element k is in the set: no carries, so different sets give different "
            "sums. <bookmark mark='d'/> So any function of the set is a function of the sum: undo the sum, then apply f. "
            "<bookmark mark='e'/> For sets of real numbers, power sums play this role, by Newton's identities."
        ) as vo:
            self.play(FadeIn(th, shift=UP * 0.1))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            vo.wait_until("e")
            self.play(FadeIn(cont))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def architecture(self):
        d = load("deepsets")
        P = np.asarray(d["examples"])[1]
        c = np.array([-5.3, 0.4, 0])
        dots = points2d(P[:6], 1.1, c, SYM, 0.07)
        phis = VGroup(*[node_box(r"$\phi$", STRUCT, font_size=24, height=0.42, pad=0.15) for _ in range(6)])
        phis.arrange(DOWN, buff=0.12).move_to([-2.9, 0.4, 0])
        arrs = VGroup(*[Arrow(dt.get_center(), ph.get_left(), buff=0.12, color=GREY_C, stroke_width=1.6,
                              max_tip_length_to_length_ratio=0.12) for dt, ph in zip(dots, phis)])
        sigma = MathTex(r"\sum", font_size=60, color=STRUCT).move_to([-0.9, 0.4, 0])
        arrs2 = VGroup(*[Arrow(ph.get_right(), sigma.get_left(), buff=0.1, color=GREY_C, stroke_width=1.6,
                               max_tip_length_to_length_ratio=0.12) for ph in phis])
        rho = node_box(r"$\rho$", STRUCT, font_size=30).move_to([0.8, 0.4, 0])
        out = label(r"ring? \ disc? \ segment? \ two blobs?", font_size=22, color=GREY_A).next_to(rho, RIGHT, buff=0.4)
        a1 = Arrow(sigma.get_right(), rho.get_left(), buff=0.1, color=GREY_C, stroke_width=2)
        a2 = Arrow(rho.get_right(), out.get_left(), buff=0.1, color=GREY_C, stroke_width=2)
        same = label(r"the same $\phi$ for every point: \ sharing weights, \ as a convolution shares them across "
                     r"positions", font_size=22, color=STRUCT).to_edge(DOWN, buff=1.5)
        rel = VGroup(
            label(r"PointNet (Qi et al.\ 2017): \ the same with a maximum in place of the sum", font_size=22,
                  color=GREY_A),
            label(r"attention without positions (Part 13): \ each element's output turns with the order "
                  r"\ (equivariant)", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "As a network, this is simple. <bookmark mark='a'/> The same small network phi reads every point, <bookmark "
            "mark='b'/> the results are summed, <bookmark mark='c'/> and a second network rho reads the sum. <bookmark "
            "mark='d'/> phi's weights are shared by every point, as a convolution shares its weights across positions. "
            "<bookmark mark='e'/> PointNet, the same year, used a maximum instead of the sum. And a transformer without "
            "positions treats its tokens as a set: reorder the inputs, and the outputs reorder with them."
        ) as vo:
            self.play(FadeIn(dots))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(p_)) for a, p_ in zip(arrs, phis)],
                                  lag_ratio=0.15), run_time=1.6)
            vo.wait_until("b")
            self.play(*[GrowArrow(a) for a in arrs2], FadeIn(sigma))
            vo.wait_until("c")
            self.play(GrowArrow(a1), FadeIn(rho), GrowArrow(a2), FadeIn(out))
            vo.wait_until("d")
            self.play(FadeIn(same))
            vo.wait_until("e")
            self.play(FadeIn(rel))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def training(self):
        c = load("setcurves")
        n = int(c["n"])
        kinds = ("deepsets", "mlp_aug", "mlp")
        cur = {k: np.asarray(c[k]) for k in kinds}
        last = int(cur["deepsets"][-1, 0])
        g = axes([0, last], [0, 1.0], x_length=7.2, y_length=4.2, xlabel=r"training step",
                 ylabel=r"held-out accuracy", xticks=[0, last // 2, last], yticks=[0.25, 0.5, 0.75, 1.0],
                 xfmt=lambda v: f"{v:,.0f}".replace(",", "{,}"), center=[-2.2, -0.35, 0])
        head = label(rf"one training run of each, \ on ${n}$ training sets", font_size=30).to_edge(UP, buff=0.4)
        chance = DashedLine(g.ax.c2p(0, 0.25), g.ax.c2p(last, 0.25), color=GREY_D)
        chl = label(r"chance", font_size=18, color=GREY_C).next_to(chance, UP, buff=0.05).align_to(chance, RIGHT)
        lines = {k: curve(g.ax, cur[k][:, 0], cur[k][:, 1], KIND_COLOR[k], 3.5) for k in kinds}

        def first(k, thr=0.8):
            i = np.flatnonzero(cur[k][:, 1] >= thr)
            return int(cur[k][i[0], 0]) if len(i) else None

        fin = {k: 100 * float(cur[k][-1, 1]) for k in kinds}
        side = VGroup()
        for k, nm in zip(kinds, (KIND_NAME["deepsets"], r"MLP, \ reordered copies", KIND_NAME["mlp"])):
            f80 = first(k)
            row = VGroup(label(nm, font_size=22, color=KIND_COLOR[k]),
                         label(rf"ends at ${fin[k]:.0f}\%$", font_size=22, color=GREY_A),
                         label(rf"passes $80\%$ at step ${f80:,}$".replace(",", "{,}") if f80 is not None else
                               r"never reaches $80\%$", font_size=20, color=GREY_B))
            side.add(row.arrange(DOWN, aligned_edge=LEFT, buff=0.1))
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([4.6, -0.2, 0])
        tag = note(r"computed: \ seed $0$, \ $1{,}000$ held-out sets, \ accuracy every $200$ steps", font_size=18)
        tag.to_corner(DR, buff=0.2)
        d80, a80, m80 = first("deepsets"), first("mlp_aug"), first("mlp")
        e_ds, e_ml, e_au = fin["deepsets"], fin["mlp"], fin["mlp_aug"]
        ds_txt = (f"Deep Sets passes eighty percent after {d80:,} steps and ends at {e_ds:.0f} percent"
                  if d80 is not None else f"Deep Sets never passes eighty percent; it ends at {e_ds:.0f} percent")
        if m80 is None:
            mlp_txt = f"never gets to eighty percent; it ends at {e_ml:.0f} percent"
        else:
            mlp_txt = f"passes eighty percent only at step {m80:,}, and ends at {e_ml:.0f} percent"
        if a80 is None:
            aug_txt = f"never gets to eighty percent either; it ends at {e_au:.0f}"
        elif d80 is not None and a80 > d80:
            aug_txt = f"gets there too, but later, at step {a80:,}, and ends at {e_au:.0f}"
        else:
            aug_txt = f"gets there at step {a80:,} and ends at {e_au:.0f}"
        with self.voiceover(
            f"Before the full comparison, watch one training run of each, on {n} training sets, the held-out accuracy "
            f"checked every two hundred steps. <bookmark mark='a'/> {ds_txt}. <bookmark mark='b'/> The plain MLP "
            f"{mlp_txt}. <bookmark mark='c'/> The MLP shown reordered copies {aug_txt}."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), Create(chance), FadeIn(chl), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(lines["deepsets"]), run_time=2.5)
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(lines["mlp"]), run_time=2.5)
            self.play(FadeIn(side[2]))
            vo.wait_until("c")
            self.play(Create(lines["mlp_aug"]), run_time=2.5)
            self.play(FadeIn(side[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def experiment(self):
        d = load("deepsets")
        sizes = list(d["sizes"])
        lx = np.log10(sizes)
        g = axes([lx[0], lx[-1]], [0.2, 1.0], x_length=6.2, y_length=3.8, xlabel=r"training sets",
                 ylabel=r"test accuracy", xticks=list(lx), yticks=[0.25, 0.5, 0.75, 1.0],
                 xfmt=lambda v: f"{10 ** v:,.0f}".replace(",", "{,}"), center=[-2.6, -0.3, 0])
        chance = DashedLine(g.ax.c2p(lx[0], 0.25), g.ax.c2p(lx[-1], 0.25), color=GREY_D)
        chl = label(r"chance", font_size=18, color=GREY_C).next_to(chance, UP, buff=0.05).align_to(chance, RIGHT)
        objs = {}
        for kind in ("mlp", "mlp_aug", "deepsets"):
            m, lo, hi = mean_band(d, kind, sizes)
            col = KIND_COLOR[kind]
            objs[kind] = VGroup(band(g.ax, lx, lo, hi, col, 0.22), curve(g.ax, lx, m, col, 3.5),
                                VGroup(*[Dot(g.ax.c2p(a, b), radius=0.05, color=col) for a, b in zip(lx, m)]))
        lg = legend([(STRUCT, KIND_NAME["deepsets"]), (AUG, r"MLP, \ shown reordered copies"),
                     (PLAIN, KIND_NAME["mlp"])], font_size=20).move_to([4.5, -1.1, 0])
        flips = VGroup(label(r"answers that change \ when the same set is reordered:", font_size=22, color=GREY_A))
        n_big = sizes[-1]
        for kind in ("mlp", "mlp_aug", "deepsets"):
            f_ = np.mean([d[f"{kind}_{n_big}_s{s}"]["flip"] for s in d["seeds"]])
            flips.add(label(rf"{KIND_NAME[kind]}: \ ${100 * f_:.0f}\%$", font_size=24, color=KIND_COLOR[kind]))
        flips.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([4.4, 1.3, 0])
        params = {k: d[f"{k}_{n_big}_s0"]["params"] for k in ("mlp", "deepsets")}
        tag = note(rf"computed: \ three seeds each \ (band: \ min--max), \ ${d['steps']:,}$ steps each; \ "
                   rf"MLP ${params['mlp']:,}$ weights, \ Deep Sets ${params['deepsets']:,}$".replace(",", "{,}")
                   .replace("{{,}}", "{,}"), font_size=18).to_corner(DR, buff=0.2)
        a_ds = mean_band(d, "deepsets", sizes)[0]
        a_ml = mean_band(d, "mlp", sizes)[0]
        a_au = mean_band(d, "mlp_aug", sizes)[0]
        n0 = sizes[0]
        f_ml = np.mean([d[f"mlp_{n_big}_s{s}"]["flip"] for s in d["seeds"]])
        f_au = np.mean([d[f"mlp_aug_{n_big}_s{s}"]["flip"] for s in d["seeds"]])
        # how many sets does each need to reach Deep Sets' accuracy on the fewest?
        target = a_ds[0]
        reach = [n for n, a in zip(sizes, a_au) if a >= target]
        reach_txt = (f"The MLP with reordered copies needs {reach[0]:,} sets to match that" if reach else
                     f"The MLP with reordered copies never matches that, even with {n_big:,} sets")
        if a_ds[-1] - a_au[-1] >= 0.03:
            last = "Even at the largest size Deep Sets stays ahead"
        elif a_au[-1] - a_ds[-1] >= 0.005:
            last = "At the largest size the copies have caught up and passed it"
        else:
            last = "At the largest size the copies have nearly caught up"
        reach_m = [n for n, a in zip(sizes, a_ml) if a >= target]
        mlp_vs = (f"and even with {n_big:,} sets it stays below what Deep Sets reached with {n0}" if not reach_m else
                  f"and it needs {reach_m[0]:,} sets to reach what Deep Sets did with {n0}")
        with self.voiceover(
            f"Now train them on {n0} up to {n_big:,} sets, three seeds each, the same number of steps. <bookmark mark='a'/> "
            f"With only {n0} sets, Deep Sets is right {100 * a_ds[0]:.0f} percent of the time. <bookmark mark='b'/> The "
            f"plain MLP is at {100 * a_ml[0]:.0f} percent, {mlp_vs}: it must learn from examples that sixteen factorial "
            f"orderings are one thing. <bookmark mark='c'/> Reordered copies help a lot: {100 * a_au[0]:.0f} percent at {n0} "
            f"sets. {reach_txt}. {last}: Deep Sets {100 * a_ds[-1]:.0f} percent, the copies {100 * a_au[-1]:.0f}. <bookmark "
            "mark='d'/> But copies teach the symmetry only approximately: reorder the same test sets, and the plain MLP "
            f"changes its answer on {100 * f_ml:.0f} percent of them, the one trained on copies on {100 * f_au:.0f} percent, "
            "Deep Sets on none."
        ) as vo:
            self.play(FadeIn(g), Create(chance), FadeIn(chl), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(objs["deepsets"]), FadeIn(lg[0]))
            vo.wait_until("b")
            self.play(FadeIn(objs["mlp"]), FadeIn(lg[2]))
            vo.wait_until("c")
            self.play(FadeIn(objs["mlp_aug"]), FadeIn(lg[1]))
            vo.wait_until("d")
            self.play(FadeIn(flips[0]), LaggedStart(*[FadeIn(f_) for f_ in flips[1:]], lag_ratio=0.4))
        self.wait(0.6)
        tk = take_away(r"order-free by construction: \ less to learn, \ and never fooled by a renumbering")
        with self.voiceover(
            "So building the symmetry in did two things: it saved data, and it made the answer exactly order-free, on every "
            "input. Graphs are next: sets with connections."
        ):
            self.play(FadeIn(tk, shift=UP * 0.1), *takeaway_anims(self, tk))
        self.wait(0.3)
        self.clear_scene()
