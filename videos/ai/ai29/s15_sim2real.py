from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai26.common import cartpole
from videos.ai.ai29.common import AGENT, CLAIM, FAIL, GOOD, HIST, MODEL, PART, WORLD, load, node_box, spread_band

NOM = C.MODEL_Q  # trained in one simulator
RAND = C.INTERVAL  # trained in many


def heat(Z, vmax=500.0, w=3.4, h=3.4) -> ImageMobject:
    lo, hi = np.array(ManimColor("#1A2130").to_rgb()), np.array(ManimColor(GOOD).to_rgb())
    t = np.clip(np.asarray(Z) / vmax, 0, 1)[::-1]  # rows: pole length, longest at the top
    rgb = lo[None, None] * (1 - t[..., None]) + hi[None, None] * t[..., None]
    img = ImageMobject((np.concatenate([rgb, np.ones(t.shape + (1,))], -1) * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    return img.stretch_to_fit_width(w).stretch_to_fit_height(h)


class SimToReal(VoiceoverScene):
    def construct(self):
        self.card()
        self.gap()
        self.randomize()
        self.training()
        self.maps()
        self.frontier()

    def card(self):
        card = chapter_card(14, r"From simulation to reality", r"Can a robot learn in a world that isn't real?",
                            lit=(2017,), part=PART)
        with self.voiceover("Chapter fourteen. From simulation to reality."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def gap(self):
        sim = node_box(r"a simulator: \ hand-written physics", MODEL, 26, height=0.9).move_to([-3.6, 1.8, 0])
        real = node_box(r"the real robot", WORLD, 26, height=0.9).move_to([3.6, 1.8, 0])
        arr = Arrow(sim.get_right(), real.get_left(), buff=0.15, color=GREY_B)
        al = label(r"the reality gap", font_size=24, color=FAIL).next_to(arr, UP, buff=0.1)
        pros = VGroup(label(r"thousands of robots at once, \ faster than real time", font_size=26, color=GOOD),
                      label(r"no wear, \ no danger, \ resets for free", font_size=26, color=GOOD),
                      label(r"free labels: \ positions, \ contacts, \ the true state", font_size=26, color=GOOD))
        pros.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([-3.6, -0.4, 0])
        cons = VGroup(label(r"friction, \ masses, \ motor strength", font_size=26, color=FAIL),
                      label(r"delays between sensing and acting", font_size=26, color=FAIL),
                      label(r"noisy sensors, \ different lighting", font_size=26, color=FAIL))
        cons.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.6, -0.4, 0])
        hist = history_card(r"2021--22", r"Isaac Gym \ (NVIDIA); \ Rudin et al.", r"thousands of simulated legged robots "
                            r"on one GPU: \ a walking policy in minutes", width=8.0, color=HIST,
                            font_size=21).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Robots learn slowly in the real world: one robot, one attempt at a time, wearing out and falling over. "
            "So most robot learning starts in simulation. <bookmark mark='a'/> A simulator can run thousands of "
            "robots at once, faster than real time, with nothing to break and the true state always known. "
            "<bookmark mark='b'/> In 2021 and 2022 NVIDIA's Isaac Gym ran thousands of legged robots in parallel on "
            "one graphics card, and taught them to walk in minutes. <bookmark mark='c'/> The catch is the reality "
            "gap. The simulator's physics are written by people, and wrong in small ways: friction, masses, motor "
            "strength, the delay between sensing and acting, the noise in every sensor. A policy that exploits the "
            "simulator's quirks fails on the real machine."
        ) as vo:
            self.play(FadeIn(sim), FadeIn(real))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p_, shift=RIGHT * 0.1) for p_ in pros], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(hist, shift=UP * 0.15))
            vo.wait_until("c")
            self.play(GrowArrow(arr), FadeIn(al), LaggedStart(*[FadeIn(c_, shift=LEFT * 0.1) for c_ in cons],
                                                               lag_ratio=0.3))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def randomize(self):
        card = definition_card(r"Domain randomization", r"train in many simulators at once: \ $\max_\pi \ \mathbb E_{\xi "
                               r"\sim p(\xi)}\big[J(\pi;\, \xi)\big]$, \ $\xi$ the simulator's settings, \ drawn afresh "
                               r"every episode; \ if reality looks like one more draw, \ the policy works there too",
                               width=7.0, color=RAND).move_to([-2.9, 1.6, 0])
        g = np.random.default_rng(2)
        poles = VGroup(*[cartpole(0.0, g.uniform(-0.1, 0.1), scale=0.42, pole_len=1.0 + 1.6 * g.random(),
                                  color=interpolate_color(ManimColor(RAND), ManimColor(WHITE), 0.3 * k / 5))
                         for k in range(6)])
        poles.arrange_in_grid(rows=2, cols=3, buff=(0.25, 0.35))
        if poles.width > 5.6:
            poles.width = 5.6
        poles.move_to([3.8, 1.4, 0])
        cards = VGroup(
            history_card(2017, r"Tobin et al.", r"random textures, \ lights and cameras: \ an object detector trained "
                         r"only on simulated images works on real ones", width=4.2, color=HIST, font_size=21),
            history_card(2018, r"Peng et al.", r"random masses, \ friction and delays: \ a robot arm pushes a puck "
                         r"without real training", width=4.2, color=HIST, font_size=21),
            history_card(2019, r"OpenAI, \ Rubik's cube", r"randomization that widens itself as the hand masters "
                         r"each range: \ a real hand solves the cube", width=4.2, color=HIST, font_size=21),
        ).arrange(RIGHT, buff=0.25).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The fix is counterintuitive: make the simulator worse on purpose. <bookmark mark='a'/> Don't train in "
            "one simulator. Train in many, each with its own settings, drawn afresh every episode: different "
            "masses, different friction, a slower motor, a delay. <bookmark mark='b'/> A policy that works across "
            "all of them cannot rely on any one simulator's quirks, and if the real world looks like just one more "
            "draw, it works there too. <bookmark mark='c'/> Josh Tobin and colleagues did this for pictures in 2017, "
            "randomizing textures and lights, Xue Bin Peng and colleagues for physics in 2018, and OpenAI's robot "
            "hand solved a Rubik's cube in 2019 with randomization that widened itself as the hand improved."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.15))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p_) for p_ in poles], lag_ratio=0.2))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.15) for c_ in cards], lag_ratio=0.4), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def training(self):
        d = load("randomize")
        P = d["params"]
        H = np.asarray(d["nominal_hist"]), np.asarray(d["randomized_hist"])
        it = H[0][0, :, 0] + 1
        g = axes([1, P["iters"], 5], [0, 500, 100], x_length=6.4, y_length=4.0, xlabel=r"training round \ (CEM)",
                 ylabel=r"steps balanced, \ out of $500$", xticks=[1, 10, 20, 30], yticks=[0, 250, 500],
                 center=[-2.9, -0.5, 0])
        ax = g.ax
        nom_sim, nom_real = spread_band(ax, it, H[0][:, :, 2], NOM), spread_band(ax, it, H[0][:, :, 3], NOM)
        rnd_real = spread_band(ax, it, H[1][:, :, 3], RAND)
        for m in (nom_real, rnd_real):
            m[1].set_stroke(width=3.5)
        nom_sim[1].set_stroke(opacity=0.5)
        dashed = DashedVMobject(nom_sim[1].copy(), num_dashes=40)
        real = P["real"]
        nominal = d["nominal"]
        spec = VGroup(label(r"the ``real'' cart-pole", font_size=28, color=WORLD),
                      label(rf"pole ${real['l'] / nominal['l']:.1f}\times$ as long, \ ${real['mp'] / nominal['mp']:.0f}\times$ "
                            rf"as heavy", font_size=24, color=GREY_A),
                      label(rf"motor ${100 * (1 - real['F'] / nominal['F']):.0f}\%$ weaker, \ cart "
                            rf"${real['mc'] / nominal['mc']:.1f}\times$ heavier", font_size=24, color=GREY_A),
                      label(r"acts one step late, \ noisy sensors", font_size=24, color=GREY_A))
        spec.arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(UR, buff=0.35)
        leg = legend([(NOM, r"trained in Part 26's simulator"), (RAND, r"trained in randomized ones")], font_size=24)
        leg.next_to(spec, DOWN, buff=0.4).align_to(spec, LEFT)
        nn_, nr = np.asarray(d["nominal_nominal"]), np.asarray(d["nominal_real"])
        rn, rr = np.asarray(d["randomized_nominal"]), np.asarray(d["randomized_real"])
        tag = note(rf"{int(P['seeds'])} seeds each, \ band min--max; \ the same number of training episodes; \ "
                   rf"linear policies, \ cross-entropy method", font_size=17).to_edge(DOWN, buff=0.15)
        both_sim = nn_.mean() > 450 and rn.mean() > 450
        a = (f"In the simulator they were trained in, both reach {nn_.mean():.0f} and {rn.mean():.0f} steps of "
             "five hundred." if not both_sim else "In Part 26's simulator, both kinds learn to balance for the full "
             "five hundred steps.")
        if rr.mean() > 1.5 * nr.mean():
            b = (f"On the real one, the policies trained in a single simulator last {nr.mean():.0f} steps on average; "
                 f"those trained across randomized simulators, {rr.mean():.0f}.")
        else:
            b = (f"On the real one, the single-simulator policies last {nr.mean():.0f} steps and the randomized ones "
                 f"{rr.mean():.0f}: randomization did not help much here.")
        with self.voiceover(
            "Let's try it on Part 26's cart-pole. <bookmark mark='a'/> Our real cart-pole is a different machine: "
            "a longer, heavier pole, a weaker motor, a one-step delay, and noisy sensors, all inside the range we "
            "randomize over. <bookmark mark='b'/> We train simple linear policies with the cross-entropy method, "
            "eight seeds each, with the same number of training episodes, and test every round on the real machine. "
            f"<bookmark mark='c'/> {a} <bookmark mark='d'/> {b}"
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(spec))
            vo.wait_until("b")
            self.play(FadeIn(leg))
            vo.wait_until("c")
            self.play(Create(dashed), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(nom_real[0]), Create(nom_real[1]), run_time=1.5)
            self.play(FadeIn(rnd_real[0]), Create(rnd_real[1]), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def maps(self):
        d = load("randomize")
        P = d["params"]
        Ls, Fs = np.asarray(d["grid_l"]), np.asarray(d["grid_F"])
        mN, mR = np.asarray(d["nominal_map"]).mean(0), np.asarray(d["randomized_map"]).mean(0)
        imgs = Group()
        for M_, col, name in ((mN, NOM, r"trained in one simulator"), (mR, RAND, r"trained in randomized ones")):
            im = heat(M_)
            fr = SurroundingRectangle(im, color=col, buff=0.03, stroke_width=2)
            t = label(name, font_size=22, color=col).next_to(im, UP, buff=0.15)
            imgs.add(Group(im, fr, t))
        imgs.arrange(RIGHT, buff=1.4).move_to([-0.6, -0.1, 0])

        def mark(gr, l_, F_, col, txt):
            im = gr[0]
            x = im.get_left()[0] + im.width * (F_ - Fs[0]) / (Fs[-1] - Fs[0])
            y = im.get_bottom()[1] + im.height * (l_ - Ls[0]) / (Ls[-1] - Ls[0])
            return VGroup(Circle(radius=0.12, color=col, stroke_width=3).move_to([x, y, 0]),
                          label(txt, font_size=16, color=col).next_to([x, y, 0], UR, buff=0.08))

        real, nom = P["real"], d["nominal"]
        marks = VGroup(*[VGroup(mark(gr, nom["l"], nom["F"], WHITE, r"sim"), mark(gr, real["l"], real["F"], WORLD, r"real"))
                         for gr in imgs])
        xl = label(r"motor force $\to$", font_size=20, color=GREY_A).next_to(imgs[0][0], DOWN, buff=0.15)
        yl = label(r"pole length $\to$", font_size=20, color=GREY_A).rotate(PI / 2).next_to(imgs[0][0], LEFT, buff=0.15)
        xl2 = xl.copy().next_to(imgs[1][0], DOWN, buff=0.15)
        key = Group(heat(np.linspace(0, 500, 6)[None, :], w=1.6, h=0.22), label(r"$0$ \ to \ $500$ steps", font_size=22,
                                                                                  color=GREY_A))
        key.arrange(RIGHT, buff=0.15).to_corner(UR, buff=0.4)
        tag = note(r"every map: \ with the real robot's delay and sensor noise; \ mean of 8 seeds", font_size=18)
        tag.to_edge(DOWN, buff=0.2)
        frac = lambda M_: float((M_ > 400).mean())  # noqa: E731
        one_sim = ("The policies trained in one simulator balance for four hundred steps nowhere on this map, once "
                   "the delay and the noise are added." if frac(mN) == 0 else
                   f"The policies trained in one simulator balance well in only {100 * frac(mN):.0f} percent of this map.")
        with self.voiceover(
            "Here is the whole picture: how long each kind of policy balances, across pole lengths and motor "
            "strengths, every one with the real robot's delay and noise. <bookmark mark='a'/> " + one_sim + " "
            "<bookmark mark='b'/> Those trained across randomized "
            f"simulators, in {100 * frac(mR):.0f} percent, the real robot included. <bookmark mark='c'/> The price "
            "is a policy that is less tuned to any one machine; the gain is that it does not need to know which "
            "machine it is on."
        ) as vo:
            self.play(FadeIn(imgs[0]), FadeIn(xl), FadeIn(yl), FadeIn(key), FadeIn(tag), FadeIn(marks[0]))
            vo.wait_until("b")
            self.play(FadeIn(imgs[1]), FadeIn(xl2), FadeIn(marks[1]))
            vo.wait_until("c")
            self.play(Indicate(marks[1][1], color=WORLD))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def frontier(self):
        cards = VGroup(
            history_card(r"today", r"legged robots and humanoids", r"walking and running trained with reinforcement "
                         r"learning in randomized simulation, \ then run on the real robot unchanged", width=6.2,
                         color=HIST, font_size=21),
            history_card(r"Oct 2026", r"Gemini 4 Argon for Robotics \ (Google; \ a company claim)", r"from one photo of a "
                         r"real table, \ a simulated twin and $4{,}500$ simulated episodes: \ real success from $56\%$ "
                         r"to $75\%$", width=6.2, color=CLAIM, font_size=21),
            history_card(r"Oct 2026", r"Genie 4 (chapter 13)", r"learned world models offered as training grounds for "
                         r"robots: \ simulators no one wrote by hand", width=6.2, color=CLAIM, font_size=21),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).to_edge(LEFT, buff=0.4)
        d = load("randomize")
        tr_n, tr_r = np.asarray(d["nominal_trace"]), np.asarray(d["randomized_trace"])
        cps = VGroup(cartpole(float(tr_n[0, 0]), float(tr_n[0, 2]), center=[4.2, 1.5, 0], scale=0.55, color=NOM),
                     cartpole(float(tr_r[0, 0]), float(tr_r[0, 2]), center=[4.2, -1.3, 0], scale=0.55, color=RAND))
        lab = VGroup(label(r"one simulator", font_size=20, color=NOM).next_to(cps[0], UP, buff=0.2),
                     label(r"randomized", font_size=20, color=RAND).next_to(cps[1], UP, buff=0.2))
        t = ValueTracker(0)
        live = VGroup(always_redraw(lambda: cartpole(float(tr_n[min(int(t.get_value()), len(tr_n) - 1), 0]),
                                                     float(tr_n[min(int(t.get_value()), len(tr_n) - 1), 2]),
                                                     center=[4.2, 1.5, 0], scale=0.55, color=NOM)),
                      always_redraw(lambda: cartpole(float(tr_r[min(int(t.get_value()), len(tr_r) - 1), 0]),
                                                     float(tr_r[min(int(t.get_value()), len(tr_r) - 1), 2]),
                                                     center=[4.2, -1.3, 0], scale=0.55, color=RAND)))
        cnt = VGroup(label(r"step", font_size=20, color=GREY_A), Integer(0, font_size=24)).arrange(RIGHT, buff=0.12)
        cnt.to_edge(DOWN, buff=0.3).shift(RIGHT * 4.2)
        cnt[1].add_updater(lambda m: m.set_value(min(int(t.get_value()), 500)))
        tag = note(r"on the ``real'' cart-pole: \ of five episodes each, \\ the one of median length", font_size=20).next_to(cnt, UP, buff=0.15)
        fell_n, fell_r = len(tr_n) - 1, len(tr_r) - 1
        ep = (f"In a typical episode on the real cart-pole, the single-simulator policy drops the pole after {fell_n} "
              f"steps, while the randomized one is still balancing at {fell_r}." if fell_r >= 500 else
              f"In a typical episode on the real cart-pole, the single-simulator policy drops the pole after {fell_n} "
              f"steps, and the randomized one after {fell_r}.")
        with self.voiceover(
            "Domain randomization is now routine. <bookmark mark='a'/> Walking and running for legged robots and "
            "humanoids are mostly trained this way, in randomized simulation, and moved to the real machine "
            f"unchanged. <bookmark mark='b'/> {ep} <bookmark mark='c'/> The newest step closes the loop with the "
            "previous chapters: in October 2026 Google reported building a simulated twin of a real table from a "
            "single photo, and DeepMind pitched Genie 4 as a training ground for robots. Simulators that no one "
            "writes by hand, only learned."
        ) as vo:
            self.play(FadeIn(cards[0], shift=RIGHT * 0.15), FadeIn(cps), FadeIn(lab))
            vo.wait_until("b")
            self.remove(cps)
            self.add(live, cnt)
            self.play(FadeIn(tag), t.animate.set_value(min(max(fell_n, fell_r), 500)), run_time=5.0, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(cards[1], shift=RIGHT * 0.15), FadeIn(cards[2], shift=RIGHT * 0.15))
        for m in live:
            m.clear_updaters()
        cnt[1].clear_updaters()
        self.wait(0.3)
        self.clear_scene()
