from __future__ import annotations

import numpy as np

from videos.psychology.psych5.common import *  # noqa: F403


class Cable(VoiceoverScene):
    def construct(self):
        self.card()
        self.passive()
        self.travelling()
        self.speed()

    def card(self):
        card = chapter_card(7, r"Down the axon", r"How does the signal get from one end to the other?", lit=(),
                            part=PART, scale=("neuron",), marr=("how",))
        with self.voiceover(
            "Chapter seven. Down the axon."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def passive(self):
        d = load("cable")
        head = heading(r"A voltage left to itself dies within a centimetre")
        A = axes([0, 4], [0, 1.05], x_length=7.2, y_length=3.2, xticks=[0, 1, 2, 3, 4], yticks=[0, 0.5, 1.0],
                 xlabel=r"distance along the fibre (cm)", ylabel=r"share of the voltage left", center=[-2.7, -0.95, 0])
        ax = A.ax
        line = curve(ax, d["passive_x"], d["passive"], LEAK, stroke_width=4)
        lam = d["lambda_cm"]
        mark = VGroup(DashedLine(ax.c2p(lam, 0), ax.c2p(lam, np.exp(-1)), color=THRESH, stroke_width=2),
                      Dot(ax.c2p(lam, np.exp(-1)), radius=0.09, color=THRESH))
        mark_l = label(rf"$\lambda = {lam:.1f}$ cm: \ 37\% left", font_size=24, color=THRESH).next_to(
            ax.c2p(lam, np.exp(-1)), UR, buff=0.1)
        pipe = RoundedRectangle(width=7.2, height=0.5, corner_radius=0.25, color=VOLT, stroke_width=3)
        pipe.move_to([A.ax.c2p(2, 0)[0], 2.15, 0])
        leaks = VGroup(*[Arrow(pipe.get_left() + RIGHT * (0.7 + 0.8 * i) + DOWN * 0.1, pipe.get_left() + RIGHT * (0.7 + 0.8 * i)
                               + DOWN * (0.5 * np.exp(-0.3 * i) + 0.14), color=LEAK, stroke_width=3, buff=0,
                               max_tip_length_to_length_ratio=0.35) for i in range(8)])
        poke = VGroup(Arrow(pipe.get_left() + LEFT * 0.05 + UP * 0.75, pipe.get_left() + RIGHT * 0.25 + UP * 0.2,
                            color=THRESH, stroke_width=4, buff=0),
                      label(r"raise the voltage here", font_size=22, color=THRESH))
        poke[1].next_to(poke[0], RIGHT, buff=0.1).shift(UP * 0.2)
        side = VGroup(
            wrapped_label(r"Current flows along the inside, and leaks out through the membrane as it goes.", 4.6, 26,
                          WHITE),
            MathTex(r"\lambda \;=\; \sqrt{\frac{a\,R_m}{2\,R_i}}", font_size=40),
            wrapped_label(r"A wider fibre, or a tighter membrane, carries it further.", 4.6, 26, GREY_A),
            wrapped_label(r"A squid is longer than a centimetre. \ You are much longer.", 4.6, 26, P.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.75, -0.2, 0])
        keep_in_frame(side)
        tag = note(r"computed: the 1952 axon with only its leak").to_corner(DR, buff=0.2)
        with self.voiceover(
            "So far the membrane has been a single patch. An axon is a long tube of it, and the question is "
            "how an event at one end reaches the other. Try the obvious thing first. Raise the voltage at one "
            "point and let it spread along the inside like current in a cable. <bookmark mark='a'/> It "
            "doesn't get far. The inside of the fibre is salt water, a poor conductor, and the membrane "
            "leaks. Every bit of length, some of the current escapes sideways. So the voltage falls off "
            "exponentially with distance. <bookmark mark='b'/> The distance over which it falls to about a "
            f"third is called the length constant. For the squid's giant fibre it comes out near {lam:.0f} "
            "centimetre; for the fine fibres in your brain, a fraction of a millimetre. "
            "<bookmark mark='c'/> The formula says what helps: a wider fibre, because the inside conducts "
            "better, or a membrane that leaks less. <bookmark mark='d'/> But no animal can send a signal a "
            "metre this way. Nothing measurable would arrive. Passive spread is good for the short "
            "distances inside a dendrite. For the axon, something has to renew the signal on the way."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(pipe))
            self.play(GrowArrow(poke[0]), FadeIn(poke[1]))
            vo.wait_until("a")
            self.play(Create(line), LaggedStart(*[GrowArrow(a_) for a_ in leaks], lag_ratio=0.2), FadeIn(side[0]),
                      run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(mark), FadeIn(mark_l))
            vo.wait_until("c")
            self.play(Write(side[1]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3], shift=UP * 0.1))
        self.clear_scene()

    def travelling(self):
        d = load("cable")
        x, t, v = np.asarray(d["x"]), np.asarray(d["t"]), np.asarray(d["v"])
        head = heading(r"The signal renews itself at every point")
        A = axes([0, 6], [-90, 60], x_length=8.6, y_length=3.7, xticks=[0, 1, 2, 3, 4, 5, 6], yticks=[-80, -40, 0, 40],
                 xlabel=r"distance along the axon (cm)", ylabel=r"membrane potential (mV)", center=[-1.9, -0.5, 0])
        ax = A.ax
        idx = [int(np.argmin(np.abs(t - tt))) for tt in (0.6, 1.2, 1.8, 2.4)]
        waves = VGroup(*[curve(ax, x, v[i], VOLT, stroke_width=3.5) for i in idx])
        for w, op in zip(waves, (0.35, 0.5, 0.7, 1.0)):
            w.set_stroke(opacity=op)
        stamps = VGroup(*[label(rf"{t[i]:.1f} ms", font_size=20, color=GREY_A).move_to(
            ax.c2p(x[int(np.argmax(v[i]))], 52)) for i in idx])
        arrow = Arrow(ax.c2p(1.2, -84), ax.c2p(4.8, -84), color=MODEL, stroke_width=4, buff=0)
        nums = VGroup(
            big_number(rf"{d['velocity']:.1f} m/s", r"computed here, by Psyche", MODEL, font_size=46, width=3.4, cap_size=22),
            big_number(rf"{d['published']} m/s", r"computed by hand, 1952", MODEL, font_size=38, width=3.4, cap_size=22),
            big_number(rf"{d['observed']} m/s", r"measured in that axon", DATA, font_size=38, width=3.4, cap_size=22),
        ).arrange(DOWN, buff=0.3).move_to([5.2, -0.3, 0])
        keep_in_frame(nums)
        src = published_tag(archive.HODGKIN_HUXLEY_1952.cite)
        tag = psyche_tag()
        with self.voiceover(
            "Now put the four equations at every point of the tube, and connect each point to its neighbours "
            "through the salt water inside. <bookmark mark='a'/> Start a signal at the left end. The voltage "
            "there shoots up. Current spreads a little way ahead, passively, and decays as before. But it "
            "doesn't have to go far. It only has to lift the next stretch of membrane past threshold. Then "
            "that stretch fires, at full size, and lifts the stretch beyond it. <bookmark mark='b'/> So the "
            "signal moves as a wave, the same shape and the same height at every point. It isn't carried "
            "along the axon. It's rebuilt at each place by the batteries that are already there, like a row "
            "of dominoes, or a flame along a fuse. And it can't spread backwards, because the membrane "
            "behind it is refractory. <bookmark mark='c'/> That's why Helmholtz found it slow. A wave like "
            "this travels at the speed at which each patch can charge the next. And that speed is something "
            f"the model has to commit to. For this axon it comes out at {d['velocity']:.1f} metres a second. "
            f"<bookmark mark='d'/> Hodgkin and Huxley, by hand, got {d['published']}. The axon itself did "
            f"{d['observed']}. Within about a tenth, for a number nobody had fitted."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(src), FadeIn(A))
            vo.wait_until("a")
            self.play(Create(waves[0]), FadeIn(stamps[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(Create(w), FadeIn(st)) for w, st in zip(waves[1:], stamps[1:])],
                                  lag_ratio=0.8), GrowArrow(arrow), run_time=6.0)
            vo.wait_until("c")
            self.play(FadeIn(nums[0], shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(nums[1]), FadeIn(nums[2]))
        self.clear_scene()

    def speed(self):
        d = load("cable")
        lo, hi = d["helmholtz"]
        head = heading(r"Two ways to go faster")
        r, sp = np.asarray(d["radii_um"]), np.asarray(d["speeds"])
        A = axes([0, 1000], [0, 42], x_length=5.4, y_length=3.6, xticks=[0, 250, 500, 750, 1000], yticks=[0, 10, 20, 30, 40],
                 xlabel=r"radius of the axon ($\mu$m)", ylabel=r"speed (m/s)", center=[-3.6, -0.5, 0], font_size=20)
        ax = A.ax
        rr = np.linspace(20, 1000, 120)
        fit = curve(ax, rr, sp[2] * np.sqrt(rr / r[2]), LEAK, stroke_width=3)
        pts = VGroup(*[Dot(ax.c2p(a_, b_), radius=0.09, color=MODEL) for a_, b_ in zip(r, sp)])
        fit_l = label(r"speed $\propto \sqrt{\text{radius}}$", font_size=24, color=LEAK).move_to(ax.c2p(680, 20))
        # a myelinated fibre: sheath segments with gaps
        y = 1.6
        axon = Line([0.9, y, 0], [6.7, y, 0], color=VOLT, stroke_width=4)
        sheaths = VGroup(*[RoundedRectangle(width=1.1, height=0.42, corner_radius=0.2, stroke_width=0, fill_color=DATA,
                                            fill_opacity=0.85).move_to([1.6 + 1.4 * i, y, 0]) for i in range(4)])
        nodes = [np.array([0.9 + 0.0, y, 0])] + [np.array([2.3 + 1.4 * i, y, 0]) for i in range(3)] + [np.array([6.6, y, 0])]
        hop = Dot(nodes[0], radius=0.12, color=THRESH)
        my_l = VGroup(label(r"myelin: \ wrap the axon in insulation", font_size=26, color=DATA),
                      label(r"the signal is renewed only at the gaps", font_size=22, color=GREY_A)).arrange(
                          DOWN, aligned_edge=LEFT, buff=0.06).next_to(sheaths, DOWN, buff=0.3).align_to(sheaths, LEFT)
        side = VGroup(
            wrapped_label(r"The squid's way: \ a giant axon. \ Sixteen times the radius buys four times the "
                          r"speed.", 5.6, 26, MODEL),
            wrapped_label(rf"The vertebrate's way: \ insulation. \ Helmholtz's frog nerve did {lo:.0f} to {hi:.0f} "
                          r"m/s in fibres far thinner than the squid's.", 5.6, 26, DATA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.9, -1.6, 0])
        keep_in_frame(VGroup(side, my_l, sheaths, axon))
        src = historical_tag(archive.HELMHOLTZ_1850.cite)
        tag = psyche_tag()
        with self.voiceover(
            "Speed matters to an animal, and the model says what it depends on. <bookmark mark='a'/> Run the "
            "same equations on thinner and fatter axons. The speed grows as the square root of the radius. "
            "That's the squid's strategy: to make its escape signal fast it grew one enormous fibre. But the "
            "square root is a poor bargain. To double the speed you need four times the radius, which is "
            "sixteen times the volume. An animal that needs millions of fast fibres can't afford it. "
            "<bookmark mark='b'/> Vertebrates found another way. Wrap the axon in a fatty sheath, myelin, "
            "with short gaps. Under the sheath the membrane hardly leaks and stores little charge, so the "
            "voltage spreads much further and faster along the inside. The signal is renewed only at the "
            "gaps. <bookmark mark='c'/> It jumps from gap to gap. <bookmark mark='d'/> That's how the fibres "
            f"in Helmholtz's frog managed {lo:.0f} to {hi:.0f} metres a second, the same order as the squid's "
            "giant axon, in fibres a small fraction of its width. And it's why diseases that strip the "
            "myelin from nerves slow thought and movement so badly: the signal is still made, and it arrives "
            "late, or not at all."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(pts, lag_ratio=0.3), Create(fit), FadeIn(fit_l), FadeIn(side[0]), run_time=3.0)
            vo.wait_until("b")
            self.play(Create(axon), FadeIn(sheaths, lag_ratio=0.2), FadeIn(my_l), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(hop, scale=1.5))
            for p_ in nodes[1:]:
                self.play(hop.animate.move_to(p_), run_time=0.45)
            vo.wait_until("d")
            self.play(FadeIn(side[1], shift=UP * 0.1), FadeIn(src))
        self.clear_scene()
