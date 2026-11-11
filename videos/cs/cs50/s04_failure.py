from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs50.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, axes, load, trace


def node(text, col, w=2.5, h=0.9, size=19):
    box = RoundedRectangle(width=w, height=h, corner_radius=0.14, stroke_color=col, stroke_width=2.2, fill_color=BG,
                           fill_opacity=1)
    t = wrapped_label(text, w - 0.25, font_size=size, color=col).move_to(box)
    return VGroup(box, t)


class Failure(VoiceoverScene):
    def construct(self):
        self.card()
        self.models()
        self.cascade()
        self.metastable()
        self.loop()

    def card(self):
        card = chapter_card(3, r"How systems fail", r"Why can an overload outlast its cause?", lit=(1983, 2021),
                            extra=((1983, r"Schlichting and Schneider: \ fail-stop"),
                                   (2021, r"Bronson et al.: \ metastable failures")), part=PART)
        with self.voiceover("Chapter three. How systems fail, and why some failures outlast their causes."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def models(self):
        head = label(r"From fail-stop to gray", font_size=36).to_edge(UP, buff=0.3)
        c = np.array([-3.2, -0.35, 0])
        specs = [(r"fail-stop", YES, 1.9, 0.75), (r"crash", DATA, 3.1, 1.75), (r"omission", LAM, 4.3, 2.75),
                 (r"timing", KERN, 5.5, 3.75), (r"arbitrary \ (Byzantine)", NO, 6.6, 4.75)]
        rings = VGroup()
        for name, col, w, h in specs:
            r = RoundedRectangle(width=w, height=h, corner_radius=0.2, stroke_color=col, stroke_width=2.4).move_to(c)
            t = label(name, font_size=18, color=col)
            if h < 1:
                t.move_to(r)
            else:
                t.next_to(r.get_top(), DOWN, buff=0.1)
            rings.add(VGroup(r, t))
        gray = DashedVMobject(Ellipse(width=1.9, height=0.95, color=GREY_A, stroke_width=2.5), num_dashes=26).move_to(
            c + np.array([1.9, -1.15, 0]))
        gray_t = label(r"gray", font_size=19, color=GREY_A).move_to(gray)
        notes = VGroup(
            wrapped_label(r"\textbf{fail-stop}: \ halts, \ and others can tell that it has \ (Schlichting and "
                          r"Schneider, \ 1983)", 5.4, font_size=19, color=YES),
            wrapped_label(r"\textbf{omission}: \ some messages or requests just vanish", 5.4, font_size=19, color=LAM),
            wrapped_label(r"\textbf{timing}: \ answers, \ but too late: \ a slow disk, \ a long pause", 5.4,
                          font_size=19, color=KERN),
            wrapped_label(r"\textbf{arbitrary}: \ anything at all, \ even wrong answers", 5.4, font_size=19, color=NO),
            wrapped_label(r"\textbf{gray failure}: \ partial, \ and seen differently by the health check and by the "
                          r"users \ (Huang et al., \ 2017; \ chapter 15)", 5.4, font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.85, -0.35, 0])
        with self.voiceover(
            "Failures come in kinds, and each kind contains the ones before it. <bookmark mark='a'/> The kindest is "
            "fail-stop: a machine halts, and everyone else can tell that it has. Fault-tolerant protocols love it. "
            "<bookmark mark='b'/> A plain crash halts without announcing it. Omission loses some messages and not "
            "others. <bookmark mark='c'/> A timing failure answers, but too late: a slow disk, a long pause. "
            "<bookmark mark='d'/> And an arbitrary failure may do anything at all, even send wrong answers. "
            "<bookmark mark='e'/> The failures that hurt most in practice are gray: partial, intermittent, and seen "
            "differently by the health check, which reports all is well, and by the users, who are timing out. "
            "Chapter fifteen returns to them."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(rings[0][0]), FadeIn(rings[0][1]), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Create(rings[1][0]), FadeIn(rings[1][1]))
            self.play(Create(rings[2][0]), FadeIn(rings[2][1]), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(Create(rings[3][0]), FadeIn(rings[3][1]), FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(Create(rings[4][0]), FadeIn(rings[4][1]), FadeIn(notes[3]))
            vo.wait_until("e")
            self.play(Create(gray), FadeIn(gray_t), FadeIn(notes[4]))
        self.wait(0.4)
        self.clear_scene()

    def cascade(self):
        head = label(r"A cascading failure", font_size=36).to_edge(UP, buff=0.3)
        n, u0 = 5, 0.72
        BH, BW = 2.2, 1.5
        yb = -0.9
        servers = VGroup()
        bars = []
        for k in range(n):
            x = -5.0 + k * 2.5
            box = Rectangle(width=BW, height=BH, stroke_color=GREY_B, stroke_width=2).move_to([x, yb + BH / 2, 0])
            bar = Rectangle(width=BW - 0.5, height=BH * u0, stroke_width=0, fill_color=YES, fill_opacity=0.8)
            bar.move_to([x, yb + BH * u0 / 2, 0])
            name = label(rf"server {k + 1}", font_size=18, color=GREY_A).next_to(box, DOWN, buff=0.12)
            servers.add(VGroup(box, name))
            bars.append(bar)
        bars = VGroup(*bars)

        def util_labels(u, alive):
            return VGroup(*[label(rf"{100 * u:.0f}\%" if a else r"down", font_size=19,
                                  color=(YES if u <= 0.8 else (HEAD if u <= 1.0 else NO)) if a else NO).next_to(
                servers[k][1], DOWN, buff=0.1) for k, a in enumerate(alive)])

        def new_bar(k, u):
            col = YES if u <= 0.8 else (HEAD if u <= 1.0 else NO)
            x = servers[k][0].get_x()
            return Rectangle(width=BW - 0.5, height=BH * u, stroke_width=0, fill_color=col, fill_opacity=0.8).move_to(
                [x, yb + BH * u / 2, 0])
        lab0 = util_labels(u0, [True] * n)
        cap_l = label(r"box = capacity", font_size=17, color=GREY_B).next_to(servers, UP, buff=0.95).align_to(
            servers, LEFT)
        eq = MathTex(r"u_{\text{each}} = u_0\,\frac{n}{n - k}", font_size=34, color=HEAD).next_to(servers, UP, buff=0.8)
        eq.align_to(servers, RIGHT)
        u1, u2 = u0 * n / (n - 1), u0 * n / (n - 2)
        cross = VGroup()
        for k in (0, 1):
            b = servers[k][0]
            cross.add(VGroup(Line(b.get_corner(UL), b.get_corner(DR), color=NO, stroke_width=4),
                             Line(b.get_corner(UR), b.get_corner(DL), color=NO, stroke_width=4)))
        lab1 = util_labels(u1, [False] + [True] * 4)
        lab2 = util_labels(u2, [False, False] + [True] * 3)
        lab3 = util_labels(u2, [False] * 5)
        ill = note(r"illustrative: \ five servers sharing a load that fills 72\% of each", font_size=16).to_edge(
            DOWN, buff=0.25)
        foot = wrapped_label(r"the survivors inherit the work; \ remedies: \ headroom \ (N + k, \ chapter 6), \ and "
                             r"refusing excess load instead of falling over \ (chapter 5)", 12.0, font_size=19,
                             color=WHITE).next_to(ill, UP, buff=0.15)
        with self.voiceover(
            "Failures spread. <bookmark mark='a'/> Five servers share a load that keeps each one seventy-two percent "
            "busy. <bookmark mark='b'/> One fails, and the balancer moves its share to the other four: each is now at "
            "ninety percent. The load each survivor carries is the original times n over n minus k. "
            "<bookmark mark='c'/> A second one fails, perhaps because ninety percent made it slow enough to fail its "
            "health check, and the remaining three are asked for a hundred and twenty percent. "
            "<bookmark mark='d'/> They cannot give it. Queues grow, they too look dead, and the cascade takes the "
            "rest. <bookmark mark='e'/> The remedies come later in this part: headroom, so that losing machines does "
            "not overload the rest, and servers that refuse excess work instead of falling over under it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(servers), FadeIn(cap_l), FadeIn(ill))
            vo.wait_until("a")
            self.play(*[GrowFromEdge(b, DOWN) for b in bars], FadeIn(lab0))
            vo.wait_until("b")
            self.play(Create(cross[0]), bars[0].animate.stretch_to_fit_height(0.01).align_to(bars[1], DOWN),
                      *[Transform(bars[k], new_bar(k, u1)) for k in range(1, n)], Transform(lab0, lab1))
            self.play(Write(eq))
            vo.wait_until("c")
            self.play(Create(cross[1]), bars[1].animate.stretch_to_fit_height(0.01).align_to(bars[2], DOWN),
                      *[Transform(bars[k], new_bar(k, u2)) for k in range(2, n)], Transform(lab0, lab2))
            vo.wait_until("d")
            self.play(*[servers[k][0].animate.set_stroke(NO) for k in range(2, n)],
                      *[bars[k].animate.set_fill(NO, 0.3) for k in range(2, n)], Transform(lab0, lab3))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def metastable(self):
        o = load("overload")
        none, rt = o["none"], o["retries"]
        t0, t1, frac = rt["trigger"]
        cap, base = rt["capacity"], rt["base"]
        T = len(rt["offered"])
        late = sum(rt["offered"][60:]) / len(rt["offered"][60:])
        head = label(r"A metastable failure, \ simulated", font_size=36).to_edge(UP, buff=0.3)
        g = axes([0, T, 20], [0, 400, 100], x_length=9.6, y_length=4.3, x_label=r"seconds",
                 xticks=range(0, T + 1, 20), yticks=(0, 100, 200, 300, 400), font=16)
        g.next_to(head, DOWN, buff=0.4).to_edge(LEFT, buff=0.9)
        ax = g.ax
        ylab = label(r"requests a second", font_size=17, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        band = Rectangle(width=ax.c2p(t1, 0)[0] - ax.c2p(t0, 0)[0], height=ax.c2p(0, 400)[1] - ax.c2p(0, 0)[1],
                         stroke_width=0, fill_color=NO, fill_opacity=0.12).move_to(
            (ax.c2p(t0, 0) + ax.c2p(t1, 400)) / 2)
        band_l = label(r"trigger: \ capacity halved", font_size=16, color=NO).next_to(band, UP, buff=0.05)
        cap_pts = [(0, cap), (t0, cap), (t0, cap * frac), (t1, cap * frac), (t1, cap), (T, cap)]
        cap_line = DashedVMobject(trace(ax, cap_pts, WHITE, width=2), num_dashes=60)

        def series(v):
            return [(s + 0.5, x) for s, x in enumerate(v)]
        good0 = trace(ax, series(none["goodput"]), YES, width=2.5)
        off1 = trace(ax, series(rt["offered"]), NO, width=2.5)
        good1 = trace(ax, series(rt["goodput"]), HEAD, width=3.5)
        right = ax.get_right()[0] + 0.2
        keys = VGroup(
            label(r"capacity", font_size=17, color=WHITE).move_to([right, ax.c2p(0, cap)[1] + 0.16, 0],
                                                                  aligned_edge=LEFT),
            label(rf"users send {base:.0f}/s", font_size=17, color=GREY_B),
        )
        keys[1].next_to(keys[0], DOWN, buff=0.08).align_to(keys[0], LEFT)
        k0 = wrapped_label(rf"no retries: \ answered requests recover {none['recovered_s']:.0f} s after the "
                           r"trigger", 2.3, font_size=17, color=YES)
        k1 = wrapped_label(rf"three immediate retries: \ about {late:.0f} sent a second", 2.3, font_size=17, color=NO)
        k2 = wrapped_label(r"answered in time: \ zero, \ for the rest of the run", 2.3, font_size=17, color=HEAD)
        k0.move_to([right, ax.c2p(0, 25)[1], 0], aligned_edge=LEFT)
        k1.move_to([right, ax.c2p(0, 330)[1], 0], aligned_edge=LEFT)
        k2.move_to([right, ax.c2p(0, 200)[1], 0], aligned_edge=LEFT)
        with self.voiceover(
            "Now the strangest failure of all. <bookmark mark='a'/> In this simulation a server answers a hundred "
            "requests a second, and users send eighty: comfortable. Clients give up on a request after one second. "
            "<bookmark mark='b'/> At thirty seconds comes a trigger: for ten seconds, capacity halves, as when a "
            "replica is lost or a long pause stalls the server. <bookmark mark='c'/> Without retries, a queue builds, "
            "requests time out, and eleven seconds after the trigger ends the server has caught up. "
            "<bookmark mark='d'/> Now let each client retry a timed-out request up to three times, immediately. The "
            f"same ten seconds tip it over. The load sent climbs to about {late:.0f} requests a second, four times "
            "what the users want, <bookmark mark='e'/> and the number answered in time falls to zero, and stays "
            "there, eighty seconds after the trigger has gone. Nothing is broken any more. The system is simply stuck."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(ylab))
            vo.wait_until("a")
            self.play(Create(cap_line), FadeIn(keys))
            vo.wait_until("b")
            self.play(FadeIn(band), FadeIn(band_l))
            vo.wait_until("c")
            self.play(Create(good0), run_time=2.5)
            self.play(FadeIn(k0))
            vo.wait_until("d")
            self.play(good0.animate.set_stroke(opacity=0.3), k0.animate.set_opacity(0.4))
            self.play(Create(off1), run_time=2.5)
            self.play(FadeIn(k1))
            vo.wait_until("e")
            self.play(Create(good1), run_time=2.0)
            self.play(FadeIn(k2))
        self.wait(0.4)
        self.clear_scene()

    def loop(self):
        head = label(r"Stuck in the bad state", font_size=36).to_edge(UP, buff=0.3)
        st = node(r"stable", YES, w=2.2, h=0.8).move_to([-4.7, 1.5, 0])
        vu = node(r"vulnerable", HEAD, w=2.2, h=0.8).move_to([-4.7, -0.4, 0])
        me = node(r"metastable", NO, w=2.2, h=0.8).move_to([-4.7, -2.3, 0])
        a1 = CurvedArrow(st.get_left() + DOWN * 0.15, vu.get_left() + UP * 0.15, angle=PI / 2.2, color=GREY_B,
                         stroke_width=2.5)
        a2 = CurvedArrow(vu.get_right() + UP * 0.15, st.get_right() + DOWN * 0.15, angle=PI / 2.2, color=GREY_B,
                         stroke_width=2.5)
        a3 = Arrow(vu.get_bottom(), me.get_top(), buff=0.06, color=NO, stroke_width=3)
        l1 = label(r"load rises", font_size=16, color=GREY_B).next_to(a1, LEFT, buff=0.08)
        l2 = label(r"falls", font_size=16, color=GREY_B).next_to(a2, RIGHT, buff=0.08)
        l3 = label(r"trigger", font_size=17, color=NO).next_to(a3, RIGHT, buff=0.1)
        self_loop = CurvedArrow(me.get_right() + UP * 0.2, me.get_right() + DOWN * 0.2, angle=-PI * 1.4, color=NO,
                                stroke_width=2.5)
        l4 = label(r"sustains itself", font_size=16, color=NO).next_to(self_loop, RIGHT, buff=0.08)
        states = VGroup(st, vu, me, a1, a2, a3, l1, l2, l3)
        # the loop
        C, R = np.array([2.4, -0.3, 0]), 2.0
        texts = (r"queue is long", r"requests wait past their timeout", r"clients retry", r"load exceeds capacity")
        angs = (PI / 2, 0, -PI / 2, PI)
        boxes = VGroup(*[node(t, NO if k == 3 else KERN, w=2.6, h=0.95, size=18).move_to(
            C + R * np.array([np.cos(a), np.sin(a), 0]) * np.array([1.35, 1.0, 0])) for k, (t, a) in
            enumerate(zip(texts, angs))])
        arrows = VGroup(*[CurvedArrow(boxes[k].get_center() + 0.2 * (boxes[(k + 1) % 4].get_center()
                                                                     - boxes[k].get_center()),
                                      boxes[(k + 1) % 4].get_center() + 0.2 * (boxes[k].get_center()
                                                                               - boxes[(k + 1) % 4].get_center()),
                                      angle=-PI / 5, color=GREY_B, stroke_width=2.5) for k in range(4)])
        for k, a in enumerate(arrows):
            a.set_z_index(-1)
        path = ParametricFunction(lambda u: C + np.array([1.35 * R * np.cos(PI / 4 - u), R * np.sin(PI / 4 - u), 0]),
                                  t_range=[0, TAU])
        token = Dot(radius=0.11, color=HEAD).move_to(path.get_start()).set_z_index(3)
        waste = wrapped_label(r"the server is fully busy, \ with requests whose clients have already given up", 2.6,
                              font_size=18, color=GREY_A).move_to(C)
        foot = wrapped_label(r"Bronson et al. \ (2021): \ a trigger, \ then a \textit{sustaining effect}; \ removing "
                             r"the trigger does not help, \ only cutting the load does; \ Huang et al. \ (2022) found "
                             r"this pattern in the incident reports of many large services", 12.6, font_size=18,
                             color=WHITE).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "Nathan Bronson and colleagues named this a metastable failure, in 2021. <bookmark mark='a'/> A system "
            "is stable at low load. At high load it becomes vulnerable: still working, but a trigger can push it "
            "into a bad state, <bookmark mark='b'/> and the bad state sustains itself. <bookmark mark='c'/> Here is "
            "the loop. The queue is long, so requests wait past their timeout. Their clients retry, so there is more "
            "load than capacity, so the queue stays long. <bookmark mark='d'/> Meanwhile the server is fully busy, "
            "with work for clients who have already given up. Removing the trigger does nothing, because the loop no "
            "longer needs it; only cutting the load breaks it. <bookmark mark='e'/> Huang and colleagues, in 2022, "
            "found this pattern in the incident reports of many large services. The next chapter is about retrying "
            "without feeding the loop."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(states))
            vo.wait_until("b")
            self.play(Create(self_loop), FadeIn(l4))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.3), Create(arrows))
            self.play(FadeIn(token))
            self.play(MoveAlongPath(token, path), run_time=3.0, rate_func=linear)
            vo.wait_until("d")
            self.play(FadeIn(waste), MoveAlongPath(token, path), run_time=3.0, rate_func=linear)
            self.play(MoveAlongPath(token, path), run_time=3.0, rate_func=linear)
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()


_ = (DATA, LAM)
