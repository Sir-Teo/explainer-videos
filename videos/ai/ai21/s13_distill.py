from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai21.common import (CD_C, DATA, DMD_C, FM_C, HIST, NOISE, PART, PROG_C, Panel, bars_chart, distill_picture,
                                   load, take_away)


class Distill(VoiceoverScene):
    def construct(self):
        self.card()
        self.progressive()
        self.consistency()
        self.dmd()
        self.compare()

    def card(self):
        card = chapter_card(12, r"Distillation", r"Can a student do in one step what a teacher does in fifty?", part=PART)
        with self.voiceover("Chapter twelve. Distillation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def progressive(self):
        d = load("distill")
        rounds = [int(r) for r in d["rounds"]]
        SW = np.asarray(d["prog_sw"])  # seed, round
        snaps = np.asarray(d["prog_snaps"])
        pn = Panel(5.4, center=[-3.6, -0.4, 0])
        pts = pn.dots(snaps[0], PROG_C, radius=0.022)
        cnt = label(rf"teacher: \ ${rounds[0]}$ steps", font_size=26, color=FM_C).next_to(pn, UP, buff=0.12)
        hi = float(SW.max()) * 1.15
        g = axes([0, len(rounds) - 1], [0, hi], x_length=4.6, y_length=2.8, xlabel=r"steps after each round",
                 ylabel=r"distance from the data", xticks=[], yticks=[0, round(hi / 2, 2)], center=[3.4, 0.5, 0])
        g.add(*[MathTex(str(r), font_size=20, color=GREY_B).next_to(g.ax.c2p(i, 0), DOWN, buff=0.12) for i, r in enumerate(rounds)])
        xs = np.arange(len(rounds))
        bd = band(g.ax, xs, SW.min(0), SW.max(0), PROG_C, 0.2)
        cv = curve(g.ax, xs, SW.mean(0), PROG_C, 3)
        dots = VGroup(*[Dot(g.ax.c2p(i, v), radius=0.05, color=PROG_C) for i, v in enumerate(SW.mean(0))])
        gl = gloss(r"distillation", r"a slow teacher's results become the targets \\ a fast student learns to hit",
                   distill_picture(), width=4.6, color=PROG_C).to_corner(DR, buff=0.3)
        dp = gl[1][-1]
        for m_ in (dp[1], dp[2], dp[3][1]):
            m_.set_opacity(0)
        per = int(d["per_round"])
        t64, s1 = float(SW[:, 0].mean()), float(SW[:, -1].mean())
        rise = s1 / max(t64, 1e-9)
        nh, n0 = len(rounds) - 1, rounds[0]
        verdict = (f"After {nh} halvings the one-step student lands {s1:.3f} from the data, against the teacher's "
                   f"{t64:.3f} with {n0} steps." if rise < 1.5 else
                   f"After {nh} halvings the one-step student lands {s1:.3f} from the data, against the teacher's "
                   f"{t64:.3f} with {n0} steps: each halving loses a little.")
        with self.voiceover(
            "Solvers can only do so much: a curved path needs steps. Distillation changes the network instead. "
            "<bookmark mark='a'/> A slow teacher's results become the targets that a fast student learns to hit. "
            "<bookmark mark='b'/> Tim Salimans and Jonathan Ho's progressive distillation, in 2022: a student "
            "learns to do two of the teacher's steps in one; then it becomes the teacher, and the steps halve again. "
            "They went from thousands of steps to four, with an FID of 3.0 on CIFAR-10. <bookmark mark='c'/> Ours "
            f"starts from our flow-matching teacher at {rounds[0]} steps and halves {len(rounds) - 1} times, "
            f"{per:,} training steps a round. {verdict}"
        ) as vo:
            self.play(FadeIn(pn), FadeIn(pts), FadeIn(cnt))
            vo.wait_until("a")
            self.play(FadeIn(gl, shift=UP * 0.2))
            self.play(LaggedStart(*[x.animate.set_opacity(1) for x in dp[1]], lag_ratio=0.1), run_time=1.0)
            self.play(dp[2].animate.set_opacity(1), dp[3][1].animate.set_opacity(1))
            vo.wait_until("b")
            self.play(FadeOut(gl))
            self.play(FadeIn(g), FadeIn(bd), FadeIn(dots[0]))
            vo.wait_until("c")
            for i in range(1, len(rounds)):
                c2 = label(rf"student: \ ${rounds[i]}$ step" + ("s" if rounds[i] > 1 else ""), font_size=26,
                           color=PROG_C).move_to(cnt)
                self.play(*pn.move(pts, snaps[i]), Transform(cnt, c2), FadeIn(dots[i]),
                          Create(Line(g.ax.c2p(i - 1, SW.mean(0)[i - 1]), g.ax.c2p(i, SW.mean(0)[i]), color=PROG_C,
                                      stroke_width=3)), run_time=0.8)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def consistency(self):
        d = load("distill")
        snaps = np.asarray(d["cd_snaps"])
        at = [int(a) for a in d["cd_snap_at"]]
        sw = np.asarray(d["cd_sw"])
        # one ODE path, and points on it all mapped to the same end
        path = VMobject(color=FM_C, stroke_width=3).set_points_smoothly(
            [np.array([-6.2 + 1.1 * k, -1.0 + 0.9 * math.sin(0.7 * k), 0]) for k in range(6)])
        ps = [path.point_from_proportion(u) for u in (0.0, 0.3, 0.55, 0.8)]
        end = path.get_end()
        jumps = VGroup(*[CurvedArrow(p_ + UP * 0.05, end + UP * 0.12, angle=-0.6, color=CD_C, stroke_width=2.5,
                                     tip_length=0.15) for p_ in ps])
        dots = VGroup(*[Dot(p_, radius=0.07, color=WHITE) for p_ in ps], Dot(end, radius=0.09, color=DATA))
        pl = label(r"every point of one path \ $\mapsto$ \ the same end", font_size=20, color=CD_C).next_to(path, DOWN, buff=0.4)
        tag = note(r"schematic").next_to(pl, DOWN, buff=0.1)
        rows = [
            cmath(r"f_\theta(x_\tau, \tau)", r"=", r"x_\tau + (1 - \tau)\, F_\theta(x_\tau, \tau)", font_size=30),
            cmath(r"\mathcal L", r"=", r"\big\| f_\theta(x_\tau, \tau) - \operatorname{sg} f_\theta(x_{\tau+\Delta},\ \tau + \Delta) \big\|^2",
                  font_size=30),
        ]
        whys = [why(r"$f(x, 1) = x$: \ at the data end, \ nothing to do"),
                why(r"$x_{\tau + \Delta}$: \ one teacher step along the ODE")]
        step = ladder(self, rows, whys, keep=2, top=3.1, x=-0.2, buff=0.6, edge=6.85)
        pn = Panel(3.6, center=[4.6, -1.3, 0])
        pts = pn.dots(snaps[0], CD_C, radius=0.02)
        cnt = label(rf"step ${at[0]:,}$".replace(",", "{,}"), font_size=22, color=CD_C).next_to(pn, UP, buff=0.1)
        card = history_card(2024, r"Lu \& Song: \ continuous-time consistency (sCM)", r"$1.5$ billion parameters, \ two "
                            r"steps: \ FID $1.88$ on ImageNet $512^2$", color=HIST, width=5.2, font_size=18)
        card.move_to([-3.4, -2.6, 0])
        cite_ = cite(r"Y.~Song, P.~Dhariwal, M.~Chen \& I.~Sutskever, \textit{Consistency Models} (2023)", corner=UR, font_size=18)
        sw_s = f"{sw.mean():.3f}"
        with self.voiceover(
            "Consistency models, from Yang Song, Prafulla Dhariwal, Mark Chen and Ilya Sutskever in 2023, skip the "
            "rounds. <bookmark mark='a'/> Teach a network to send every point on an ODE path straight to the path's "
            "end. Then any point, including pure noise, is one jump from a sample. <bookmark mark='b'/> Build in the "
            "boundary: at the data end, the jump is nothing. <bookmark mark='c'/> And train self-consistency: a "
            "point's jump must match the jump from one teacher step further along, with that target held fixed. "
            f"<bookmark mark='d'/> Ours, distilled from the same teacher, one jump from the same noise during "
            f"training: it ends {sw_s} from the data, on average over {len(sw)} seeds. <bookmark mark='e'/> In 2024 "
            "Cheng Lu and Yang Song made the continuous-time version stable at scale: two steps, an FID of 1.88 on "
            "ImageNet at 512 pixels."
        ) as vo:
            self.play(FadeIn(cite_), Create(path), FadeIn(dots), FadeIn(pl), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(j) for j in jumps], lag_ratio=0.2))
            vo.wait_until("b")
            step(0)
            vo.wait_until("c")
            step(1)
            vo.wait_until("d")
            self.play(FadeIn(pn), FadeIn(pts), FadeIn(cnt))
            for k in range(1, len(snaps)):
                c2 = label(rf"step ${at[k]:,}$".replace(",", "{,}"), font_size=22, color=CD_C).move_to(cnt)
                self.play(*pn.move(pts, snaps[k]), Transform(cnt, c2), run_time=0.7)
            vo.wait_until("e")
            self.play(FadeIn(card, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dmd(self):
        d = load("distill")
        snaps = np.asarray(d["dmd_snaps"])
        at = [int(a) for a in d["dmd_snap_at"]]
        sw = np.asarray(d["dmd_sw"])
        rows = [
            cmath(r"\min_\theta", r"\;", r"\mathbb E_t\, \mathrm{KL}\big(p_{\text{fake}, t} \,\|\, p_{\text{real}, t}\big),"
                  r"\qquad x = G_\theta(z)", font_size=30),
            cmath(r"\nabla_\theta \mathrm{KL}", r"=", r"\mathbb E_z\Big[\big(\nabla \log p_{\text{fake}}(x) - \nabla \log "
                  r"p_{\text{real}}(x)\big)\; \frac{\partial x}{\partial \theta}\Big]", font_size=30),
            cmath(r"\nabla \log p", r"\approx", r"\text{a diffusion model's score: \ the teacher (real), \ a second "
                  r"model of } G\text{'s samples (fake)}", font_size=26),
        ]
        whys = [why(r"match distributions, \ not paths"), why(r"through the sample; \ $\mathbb E[\partial_\theta \log p] = 0$"),
                why(r"two scores")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-2.6, buff=0.55, edge=6.85)
        pn = Panel(3.8, center=[-4.4, -1.6, 0])
        pts = pn.dots(snaps[0], DMD_C, radius=0.02)
        cnt = label(rf"generator step ${at[0]:,}$".replace(",", "{,}"), font_size=20, color=DMD_C).next_to(pn, UP, buff=0.1)
        pub = VGroup(history_card(2024, r"Yin et al.: \ DMD", r"one step: \ FID $2.62$ on ImageNet $64^2$; \ $20$ "
                                  r"images a second", color=HIST, width=4.4, font_size=17),
                     history_card(2024, r"Yin et al.: \ DMD2", r"plus a GAN loss on real images: \ FID $1.28$ (Part 20)",
                                  color=HIST, width=4.4, font_size=17)).arrange(DOWN, buff=0.15).move_to([3.9, -1.9, 0])
        with self.voiceover(
            "A third way matches distributions rather than paths. Tianwei Yin and colleagues' distribution matching "
            "distillation trains a one-step generator so that, blurred to every noise level, its samples look like "
            "the teacher's. <bookmark mark='a'/> The gradient of that KL divergence, taken through each sample, is "
            "the difference of two scores: the generator's own distribution's, minus the real one's. "
            "<bookmark mark='b'/> The real score is the teacher. The fake score comes from a second diffusion model, "
            "trained all along on the generator's latest samples. <bookmark mark='c'/> Ours: the generator starts as "
            f"the teacher's single blurry step and is pushed, sample by sample, onto the letters: {sw.mean():.3f} from "
            f"the data at the end, over {len(sw)} seeds. <bookmark mark='d'/> At scale, one step, an FID of 2.62 on "
            "small ImageNet images; with a GAN loss added, DMD2 reached 1.28."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            self.play(FadeIn(pn), FadeIn(pts), FadeIn(cnt))
            for k in range(1, len(snaps)):
                c2 = label(rf"generator step ${at[k]:,}$".replace(",", "{,}"), font_size=20, color=DMD_C).move_to(cnt)
                self.play(*pn.move(pts, snaps[k]), Transform(cnt, c2), run_time=0.7)
            vo.wait_until("d")
            self.play(FadeIn(pub))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def compare(self):
        d, f = load("distill"), load("flow")
        teacher1 = np.asarray(f["fm_sw"])[:, 0]
        prog = np.asarray(d["prog_sw"])
        vals = {"t1": teacher1, "prog": prog[:, -1], "cd": np.asarray(d["cd_sw"]), "dmd": np.asarray(d["dmd_sw"]),
                "t64": prog[:, 0]}
        keys = ["t1", "prog", "cd", "dmd", "t64"]
        cols = {"t1": GREY_B, "prog": PROG_C, "cd": CD_C, "dmd": DMD_C, "t64": FM_C}
        names = {"t1": r"teacher, \ $1$ step", "prog": r"progressive", "cd": r"consistency", "dmd": r"DMD",
                 "t64": r"teacher, \ $64$ steps"}
        ch = bars_chart([vals[k].mean() for k in keys], [cols[k] for k in keys], [names[k] for k in keys], height=3.2,
                        bar_w=0.9, gap=0.7, spread=[(vals[k].min(), vals[k].max()) for k in keys], digits=3, font_size=20)
        ch.move_to([-2.2, -0.2, 0])
        head = label(rf"one step from noise \ (distance from the data; \ floor ${float(d['floor']):.3f}$; \ "
                     rf"${len(vals['cd'])}$ seeds)", font_size=24, color=GREY_A).to_edge(UP, buff=0.5)
        S = Group()
        for i, (k, key) in enumerate((("prog", "prog_one"), ("cd", "cd_one"), ("dmd", "dmd_one"))):
            pn = Panel(2.6, center=[4.8, 1.6 - 2.0 * i, 0])
            S.add(Group(pn, pn.scatter(np.asarray(d[key]), cols[k], radius_px=1.3, res=240)))
        budget = VGroup(label(rf"budgets: \ progressive ${len(d['rounds']) - 1} \times {int(d['per_round']):,}$ steps; \ "
                              rf"consistency ${int(d['steps']):,}$; \ DMD ${int(d['steps']) // 2:,}$ generator steps".replace(",", "{,}"),
                              font_size=18, color=GREY_A)).to_edge(DOWN, buff=0.3)
        best = min(["prog", "cd", "dmd"], key=lambda k: vals[k].mean())
        spoken = {"prog": "progressive distillation", "cd": "consistency distillation", "dmd": "distribution matching"}
        gap = vals[best].mean() / max(vals["t64"].mean(), 1e-9)
        n0 = int(d["rounds"][0])
        pc = 100 * (gap - 1)
        verdict = (f"The best student here is {spoken[best]}, at {vals[best].mean():.3f}, within {pc:.0f} percent of "
                   f"the teacher's {n0} steps." if gap < 2 else
                   f"The best student here is {spoken[best]}, at {vals[best].mean():.3f}, still {gap:.1f} times the "
                   f"teacher's distance with {n0} steps.")
        with self.voiceover(
            "Side by side, one step from the same noise. The teacher's own single step is a blur, "
            f"{vals['t1'].mean():.3f} from the data. <bookmark mark='a'/> {verdict} <bookmark mark='b'/> The "
            "budgets differ, as they do in practice, and on images the ranking depends on scale and care. Today's "
            "fastest image models are distilled this way; FLUX one's quickest version, for one, by an adversarial "
            "form of distillation, in one to four steps. All of them need a teacher. Can a model be one-step from "
            "scratch?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(ch.bars[0]), FadeIn(ch.vals[0]), FadeIn(ch.names[0]), FadeIn(ch[0]))
            vo.wait_until("a")
            self.play(FadeIn(ch), LaggedStart(*[FadeIn(s_) for s_ in S], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(budget))
        self.wait(0.3)
        self.clear_scene()
