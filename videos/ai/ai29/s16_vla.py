from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai29.common import AGENT, EXPERT, FAIL, GOOD, HIST, PART, REWARD, load

REG, FLOW = C.MODEL_Q, C.INTERVAL


class VLA(VoiceoverScene):
    def construct(self):
        self.card()
        self.history()
        self.pipeline()
        self.exact()
        self.modes()
        self.chunks()

    def card(self):
        card = chapter_card(15, r"Vision-language-action models", r"How does a language model move a robot arm?",
                            lit=(2026,), part=PART)
        with self.voiceover("Chapter fifteen. Vision-language-action models."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def pipeline(self):
        cam = VGroup(*[Square(0.3, stroke_color=C.BITS, stroke_width=1.2, fill_color=C.BITS, fill_opacity=0.25) for _ in range(9)])
        cam.arrange_in_grid(rows=3, cols=3, buff=0.04).move_to([-5.2, 1.0, 0])
        cl = label(r"camera images", font_size=20, color=C.BITS).next_to(cam, DOWN, buff=0.12)
        txt = VGroup(*[Square(0.3, stroke_color=C.TRUE_P, stroke_width=1.2, fill_color=C.TRUE_P, fill_opacity=0.25) for _ in range(5)])
        txt.arrange(RIGHT, buff=0.04).move_to([-5.0, -1.0, 0])
        tl = label(r"``fold the towel''", font_size=20, color=C.TRUE_P).next_to(txt, DOWN, buff=0.12)
        vlm = RoundedRectangle(width=3.0, height=2.4, corner_radius=0.2, stroke_color=WHITE, stroke_width=2.5).move_to([-0.8, 0, 0])
        vl = label(r"a vision-language model \\ (pretrained on the web)", font_size=22, color=WHITE).move_to(vlm)
        act = RoundedRectangle(width=2.4, height=1.4, corner_radius=0.2, stroke_color=C.INTERVAL, stroke_width=2.5).move_to([3.0, 0, 0])
        al = label(r"an action expert: \\ flow matching \\ (Part 21)", font_size=22, color=C.INTERVAL).move_to(act)
        arm = VGroup(Line([5.0, -1.2, 0], [5.4, 0.2, 0], color=GREY_A, stroke_width=6), Line([5.4, 0.2, 0], [6.2, 0.6, 0], color=GREY_A,
                                                                                                  stroke_width=6),
                     Dot([5.4, 0.2, 0], radius=0.08, color=GREY_B), Dot([6.2, 0.6, 0], radius=0.1, color=C.INTERVAL))
        arrows = VGroup(Arrow(cam.get_right(), vlm.get_left() + UP * 0.5, buff=0.1, color=GREY_B),
                        Arrow(txt.get_right(), vlm.get_left() + DOWN * 0.5, buff=0.1, color=GREY_B),
                        Arrow(vlm.get_right(), act.get_left(), buff=0.1, color=GREY_B),
                        Arrow(act.get_right(), arm[0].get_start() + UP * 0.6 + LEFT * 0.2, buff=0.1, color=GREY_B))
        # RT-2's way: actions written as tokens, like words
        toks = VGroup(*[VGroup(RoundedRectangle(width=0.62, height=0.42, corner_radius=0.06, stroke_color=GREY_B, stroke_width=1.5),
                               Text(v, font="DejaVu Sans Mono", font_size=16, color=GREY_A)) for v in ("132", "87", "201", "64")])
        for t_ in toks:
            t_[1].move_to(t_[0])
        toks.arrange(RIGHT, buff=0.08).move_to([3.0, 0, 0])
        tkl = label(r"actions as tokens, \ like words \ (RT-2)", font_size=20, color=GREY_B).next_to(toks, DOWN, buff=0.2)
        ta = Arrow(vlm.get_right(), toks.get_left(), buff=0.1, color=GREY_B)
        # pi-zero's way: flow matching turns noise into a smooth stretch of motion
        xs = np.linspace(1.9, 4.1, 24)
        g = np.random.default_rng(18)
        y0 = -1.85 + 0.45 * g.standard_normal(len(xs))
        y1 = -1.85 + 0.35 * np.sin((xs - 1.9) * 2.6)
        noisy = VGroup(*[Dot([x, y, 0], radius=0.045, color=C.INTERVAL) for x, y in zip(xs, y0)])
        smooth = VGroup(*[Dot([x, y, 0], radius=0.045, color=C.INTERVAL) for x, y in zip(xs, y1)])
        path = VMobject(color=C.INTERVAL, stroke_width=3).set_points_smoothly([[x, y, 0] for x, y in zip(xs, y1)])
        fml = label(r"noise $\to$ a smooth motion", font_size=20, color=C.INTERVAL).next_to(smooth, DOWN, buff=0.35)
        cite_ = cite(r"A.~Brohan et al., \textit{RT-2} (2023); \ K.~Black et al., \textit{$\pi_0$} (2024)", corner=DR)
        tag = note(r"schematic").to_corner(DL, buff=0.3)
        ae = gloss(r"action expert", r"a small extra network on the vision-language model, \\ whose only job is smooth arm motion \\ "
                   r"(not Part 16's mixture-of-experts experts)", corner=UR, width=5.6, color=C.INTERVAL)
        with self.voiceover(
            "Here is what is inside a vision-language-action model. It starts from a model that already "
            "reads images and text, trained on the web. <bookmark mark='a'/> Give it camera images and an "
            "instruction, and add a way to output motion. <bookmark mark='r'/> RT-2, in 2023, wrote actions as "
            "tokens, like words. <bookmark mark='b'/> Pi-zero, in 2024, added an action expert: a small extra network "
            "attached to the vision-language model, whose only job is to output smooth arm motions. It's not one of "
            "part sixteen's mixture-of-experts experts. It generates those motions by flow matching, part twenty-one's "
            "machinery, now drawing trajectories instead of pictures."
        ) as vo:
            self.play(Create(vlm), FadeIn(vl), FadeIn(tag), FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(cam, shift=RIGHT * 0.2), FadeIn(cl), FadeIn(txt, shift=RIGHT * 0.2), FadeIn(tl))
            self.play(GrowArrow(arrows[0]), GrowArrow(arrows[1]), Indicate(vlm, color=WHITE, scale_factor=1.03))
            vo.wait_until("r")
            self.play(GrowArrow(ta), LaggedStart(*[FadeIn(t_, shift=RIGHT * 0.15) for t_ in toks], lag_ratio=0.2), FadeIn(tkl))
            vo.wait_until("b")
            self.play(FadeOut(VGroup(toks, tkl, ta)), GrowArrow(arrows[2]), Create(act), FadeIn(al))
            self.play(FadeIn(ae))
            self.play(FadeIn(noisy, lag_ratio=0.05), FadeIn(fml))
            self.play(Transform(noisy, smooth), run_time=1.5)
            self.play(Create(path), GrowArrow(arrows[3]), FadeIn(arm))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def chunks(self):
        ax = Axes(x_range=[0, 50, 10], y_range=[-1.2, 1.2, 1], x_length=10.0, y_length=2.2, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to(DOWN * 2.0)

        def f(t):
            return 0.8 * np.sin(t / 7) * np.cos(t / 13)

        segs = VGroup(*[VMobject(color=C.INTERVAL, stroke_width=4).set_points_smoothly(
            [ax.c2p(t, f(t)) for t in np.linspace(10 * i, 10 * (i + 1), 60)]) for i in range(5)])
        bands = VGroup(*[Rectangle(width=10.0 / 5 * 0.98, height=2.2, stroke_color=GREY_D, stroke_width=1, fill_color=C.INTERVAL,
                                   fill_opacity=0.05).move_to(ax.c2p(5 + 10 * i, 0)) for i in range(5)])
        bl = VGroup(*[label(rf"chunk {i + 1}", font_size=20, color=GREY_B).next_to(b, UP, buff=0.08) for i, b in enumerate(bands)])
        head = label(r"action chunks: \ the model plans a short stretch of motion at once, \\ then looks again", font_size=26)
        head.to_edge(UP, buff=0.3)
        xn = label(r"time $\to$ \ (the elbow's angle)", font_size=22, color=GREY_A).next_to(ax, DOWN, buff=0.12)
        tag = note(r"illustrative trajectory").to_corner(DR, buff=0.3)
        # a two-link arm whose elbow follows the planned trajectory
        tt = ValueTracker(0.0)
        base = np.array([-0.8, -0.2, 0])

        def arm():
            t = tt.get_value()
            a1 = 1.15 + 0.35 * f(t)
            a2 = a1 - 1.1 + 1.1 * f(t)
            p1 = base + 1.5 * np.array([np.cos(a1), np.sin(a1), 0])
            p2 = p1 + 1.3 * np.array([np.cos(a2), np.sin(a2), 0])
            return VGroup(Line(base, p1, color=GREY_A, stroke_width=8), Line(p1, p2, color=GREY_A, stroke_width=7),
                          Dot(base, radius=0.1, color=GREY_B), Dot(p1, radius=0.08, color=C.INTERVAL), Dot(p2, radius=0.11, color=WHITE))

        plinth = Rectangle(width=1.2, height=0.2, stroke_width=0, fill_color=GREY_D, fill_opacity=1).next_to(base, DOWN, buff=0.08)
        live = always_redraw(arm)
        cursor = always_redraw(lambda: Line(ax.c2p(tt.get_value(), -1.2), ax.c2p(tt.get_value(), 1.2), color=WHITE, stroke_width=2))
        dot = always_redraw(lambda: Dot(ax.c2p(tt.get_value(), f(tt.get_value())), radius=0.07, color=WHITE))
        look = label(r"look", font_size=24, color=C.BITS).move_to([3.2, 0.6, 0])
        plan = label(r"plan a chunk", font_size=24, color=C.INTERVAL).move_to([3.2, 0.6, 0])
        act = label(r"act", font_size=24, color=WHITE).move_to([3.2, 0.6, 0])

        def chunk(i):
            self.play(FadeIn(look, scale=1.2), bands[i].animate.set_fill(opacity=0.18), run_time=0.3)
            self.play(FadeOut(look), FadeIn(plan), Create(segs[i]), run_time=0.5)
            self.play(FadeOut(plan), FadeIn(act), tt.animate.set_value(10 * (i + 1)), run_time=1.0, rate_func=linear)
            self.play(FadeOut(act), bands[i].animate.set_fill(opacity=0.05), run_time=0.2)

        with self.voiceover(
            "And it doesn't act one tiny step at a time. It plans a chunk of motion, a second or so, then looks at "
            "the world again and plans the next: <bookmark mark='a'/> the belief and the world model of the earlier "
            "chapters, folded into one network that sees, thinks and moves."
        ) as vo:
            still = arm()  # fade in a still copy; the live arm (rebuilt every frame) can't be faded in
            self.play(FadeIn(head), Create(ax), FadeIn(xn), FadeIn(tag), FadeIn(bands), FadeIn(bl), FadeIn(plinth), FadeIn(still))
            self.remove(still)
            self.add(live, cursor, dot)
            for i in range(3):
                chunk(i)
            vo.wait_until("a")
            for i in range(3, 5):
                chunk(i)
        live.clear_updaters()
        cursor.clear_updaters()
        dot.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def exact(self):
        """pi-zero's flow-matched chunks, exactly."""
        H = 50
        t = np.linspace(0, 1, H)
        a = 0.6 * np.sin(2.2 * t + 0.3) + 0.25 * t ** 2 + 0.08 * np.sin(9 * t)  # an illustrative joint angle over one chunk
        colors = {r"A": C.INTERVAL, r"\varepsilon": C.TRUE_P, r"v_\theta": C.BITS}
        f1 = cmath(r"A", r"= (a_t, \ldots, a_{t+H-1}), \quad", r"A", r"^{\tau} = (1 - \tau)\,", r"\varepsilon", r"+ \tau\,", r"A",
                   colors=colors, font_size=32)
        f2 = cmath(r"\mathcal{L} = \big\|", r"v_\theta", r"(", r"A", r"^{\tau}, o_t) - (", r"A", r"-", r"\varepsilon", r")\big\|^2",
                   colors=colors, font_size=32)
        f3 = cmath(r"A", r"^{\tau + \delta} = ", r"A", r"^{\tau} + \delta\, ", r"v_\theta", r"(", r"A", r"^{\tau}, o_t), \quad "
                   r"\delta = 0.1", colors=colors, font_size=32)
        top = VGroup(f1, f2, f3).arrange(DOWN, buff=0.3, aligned_edge=LEFT).to_corner(UL, buff=0.5)
        why1 = why(r"a straight line from noise to the chunk").next_to(f1, RIGHT, buff=0.4)
        why2 = why(r"learn the line's velocity, \ given what the robot sees").next_to(f2, RIGHT, buff=0.4)
        why3 = why(r"to act: \ $10$ Euler steps from noise").next_to(f3, RIGHT, buff=0.4)
        for w_ in (why1, why2, why3):
            keep_in_frame(w_)
        tl = label(r"$\pi_0$: \ a chunk of $H = 50$ actions \ ($1$ s at $50$ Hz), \ flow matching as in Part 21", font_size=20,
                   color=C.INTERVAL).next_to(top, DOWN, buff=0.25).align_to(top, LEFT)
        eps = np.clip(np.random.default_rng(3).normal(0, 0.45, H), -1, 1)
        px = CornerAxes(x_range=[0, H, 10], y_range=[-1, 1, 0.5], x_length=6.0, y_length=2.2, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([0, -2.1, 0])
        tau = ValueTracker(0.0)

        def mix():
            v = (1 - tau.get_value()) * eps + tau.get_value() * a
            return VGroup(VMobject(color=C.INTERVAL, stroke_width=2, stroke_opacity=0.5).set_points_as_corners(
                [px.c2p(i, x) for i, x in enumerate(v)]), *[Dot(px.c2p(i, x), radius=0.03, color=C.INTERVAL) for i, x in enumerate(v)])

        path = always_redraw(mix)
        pl = always_redraw(lambda: MathTex(rf"A^{{\tau}}, \ \tau = {tau.get_value():.2f}", font_size=26, color=C.INTERVAL)
                           .next_to(px, LEFT, buff=0.3))
        tag = note(r"illustrative chunk").to_corner(DR, buff=0.3)
        cite_ = cite(r"K.~Black et al., \textit{$\pi_0$} (2024)", corner=DL)
        with self.voiceover(
            "Here is pi zero's action expert, exactly. <bookmark mark='a'/> A chunk is the next fifty actions, one "
            "second of motion. Training draws a straight line from pure noise to the true chunk, <bookmark mark='b'/> "
            "and teaches the network the velocity along that line, given what the robot sees: part twenty-one's "
            "flow matching. <bookmark mark='c'/> To act, it starts from noise and takes ten small steps along the "
            "learned velocity, and the noise becomes a motion."
        ) as vo:
            self.play(FadeIn(cite_), FadeIn(tag), Create(px), Write(f1), FadeIn(why1), run_time=1.5)
            self.add(path, pl)
            vo.wait_until("a")
            self.play(FadeIn(tl))
            vo.wait_until("b")
            self.play(Write(f2), FadeIn(why2))
            vo.wait_until("c")
            self.play(Write(f3), FadeIn(why3))
            self.play(tau.animate.set_value(1.0), run_time=4.0, rate_func=smooth)
        path.clear_updaters()
        pl.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def history(self):
        cards = VGroup(
            history_card(r"Dec 2022", r"RT-1 \ (Google)", r"a transformer from camera images and an instruction to arm "
                         r"actions: \ $130{,}000$ demonstrations, \ $700$ tasks, \ $13$ robots, \ $17$ months", width=6.4,
                         color=HIST, font_size=24),
            history_card(r"Jul 2023", r"RT-2 \ (Google DeepMind)", r"a web-trained vision-language model fine-tuned to "
                         r"write actions as tokens: \ on unseen objects and scenes, \ $62\%$ success against RT-1's $32\%$",
                         width=6.4, color=HIST, font_size=24),
            history_card(r"Oct 2023", r"Open X-Embodiment \ ($21$ institutions)", r"over a million robot trajectories, \ "
                         r"$22$ kinds of robot, \ pooled", width=6.4, color=HIST, font_size=24),
            history_card(r"Jun 2024", r"OpenVLA \ (Kim, Pertsch et al.)", r"open weights, \ $7$ billion parameters, \ "
                         r"$970{,}000$ trajectories: \ $16.5$ points more success than the $55$-billion RT-2-X, \ "
                         r"across $29$ tasks", width=6.4, color=HIST, font_size=24),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.3))
        if cards.width > 13.2:
            cards.width = 13.2
        cards.move_to(DOWN * 0.3)
        head = label(r"Robots learn from the web, \ and from each other", font_size=34).to_edge(UP, buff=0.35)
        with self.voiceover(
            "In chapter one we left robot learning at Google's RT-1, a transformer trained on a hundred and thirty "
            "thousand demonstrations. <bookmark mark='a'/> The next step was to borrow a mind. RT-2, in 2023, took a "
            "vision-language model trained on the web and fine-tuned it to write the robot's actions as if they "
            "were words. On objects and scenes it had never seen, it succeeded sixty-two percent of the time, "
            "against RT-1's thirty-two: knowledge from the web, turned into motion. <bookmark mark='b'/> Then "
            "twenty-one labs pooled over a million trajectories from twenty-two kinds of robot, the Open "
            "X-Embodiment dataset. <bookmark mark='c'/> On it, OpenVLA, with open weights and seven billion "
            "parameters, beat the fifty-five-billion-parameter RT-2-X by sixteen and a half points across "
            "twenty-nine tasks."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cards[0], shift=UP * 0.15))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k + 1], shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def modes(self):
        from videos.ai.ai29.envs import GOAL, OBST

        d = load("detour")
        demos = np.asarray(d["demos"])
        R = 1.75

        def panel(cx, title, col):
            box = RoundedRectangle(width=4.2, height=3.1, corner_radius=0.1, stroke_color=GREY_D, stroke_width=1.5).move_to([cx, -0.4, 0])
            ob = Circle(radius=OBST[2] * R, stroke_width=0, fill_color=FAIL, fill_opacity=0.5).move_to(box.get_center() + R * np.array([OBST[0], OBST[1], 0]))
            gl = Star(n=5, outer_radius=0.13, color=REWARD, fill_opacity=1).move_to(box.get_center() + R * np.array([GOAL[0], GOAL[1], 0]))
            t = label(title, font_size=22, color=col).next_to(box, UP, buff=0.12)
            return VGroup(box, ob, gl, t)

        def path(ctr, pts, col, w=2, op=0.8):
            lim = 1.45 / R  # keep every path inside its panel
            P = [ctr + R * np.array([float(np.clip(x, -1.1, 1.1)), float(np.clip(y, -lim, lim)), 0]) for x, y in pts]
            return VMobject(stroke_color=col, stroke_width=w, stroke_opacity=op).set_points_as_corners(P)

        pans = VGroup(panel(-4.5, r"the demonstrations", EXPERT), panel(0, r"regression \ (mean squared error)", REG),
                      panel(4.5, r"flow matching", FLOW))
        ctrs = [p_[0].get_center() for p_ in pans]
        dem = VGroup(*[path(ctrs[0], dd, EXPERT, 1.5, 0.6) for dd in demos[:24]])
        last = str(max(int(k) for k in d["regress_snaps"]))
        reg = VGroup(*[path(ctrs[1], p_, REG) for p_ in d["regress_snaps"][last]["paths"]])
        flo = VGroup(*[path(ctrs[2], p_, FLOW) for p_ in d["flow_snaps"][last]["paths"]])
        hr, hf = np.asarray(d["regress_hit"]), np.asarray(d["flow_hit"])
        rr, rf = np.asarray(d["regress_reached"]), np.asarray(d["flow_reached"])
        stats = VGroup(
            label(rf"hits the obstacle: \ ${100 * hr.mean():.0f}\%$ \ (seeds ${100 * hr.min():.0f}$--${100 * hr.max():.0f}\%$)",
                  font_size=19, color=REG).next_to(pans[1], DOWN, buff=0.25),
            label(rf"hits the obstacle: \ ${100 * hf.mean():.0f}\%$ \ (seeds ${100 * hf.min():.0f}$--${100 * hf.max():.0f}\%$)",
                  font_size=19, color=FLOW).next_to(pans[2], DOWN, buff=0.25))
        tag = note(rf"computed: \ {int(d['params']['demos'])} demonstrations, \ chunks of {int(d['params']['chunk'])} moves, "
                   rf"\ {int(d['params']['seeds'])} seeds each, \ {int(d['n_starts'])} starts per seed", font_size=17)
        tag.to_edge(DOWN, buff=0.15)
        head = label(r"Why the action expert is generative", font_size=32).to_edge(UP, buff=0.35)
        above, below = float(np.mean(d["flow_above"])), float(np.mean(d["flow_below"]))
        if hr.mean() > hf.mean() + 0.2:
            v = (f"Trained to minimize squared error, the policy learns the average of the two ways round, and the "
                 f"average goes straight through the obstacle: it hits it {100 * hr.mean():.0f} percent of the time. "
                 f"<bookmark mark='c'/> The flow-matching policy samples one way or the other, above "
                 f"{100 * above:.0f} percent of the time and below {100 * below:.0f}, and hits it "
                 f"{100 * hf.mean():.0f} percent of the time.")
        else:
            v = (f"Here the regression policy hits the obstacle {100 * hr.mean():.0f} percent of the time, and the flow "
                 f"policy {100 * hf.mean():.0f}: <bookmark mark='c'/> a smaller difference than the theory suggests.")
        with self.voiceover(
            "Why go to the trouble of a generative model for actions? Because people demonstrate in more than one "
            "way. <bookmark mark='a'/> Here, demonstrations pass an obstacle above or below, half and half. "
            "<bookmark mark='b'/> " + v + " Real demonstrations are full of such choices: which hand, which "
            "grasp, which way round."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pans), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(p_) for p_ in dem], lag_ratio=0.05), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(p_) for p_ in reg], lag_ratio=0.1), run_time=2.0)
            self.play(FadeIn(stats[0]))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(p_) for p_ in flo], lag_ratio=0.1), run_time=2.0)
            self.play(FadeIn(stats[1]))
        self.wait(0.3)
        self.clear_scene()
