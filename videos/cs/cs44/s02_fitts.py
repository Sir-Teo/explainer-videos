from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs44.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, axes, bar_chart, load


class Fitts(VoiceoverScene):
    def construct(self):
        self.card()
        self.tapping()
        self.channel()
        self.simulate()
        self.edges()
        self.steering()

    def card(self):
        card = chapter_card(1, r"Pointing is a channel", r"How long does it take to hit a target?",
                            lit=(1954, 1992), extra=((1954, r"Fitts: \ reciprocal tapping"),
                                                     (1988, r"Meyer et al.: \ submovements"),
                                                     (1992, r"MacKenzie: \ the Shannon form")), part=PART)
        with self.voiceover("Chapter one. Pointing is a channel."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def tapping(self):
        head = label(r"Fitts's tapping experiment, \ 1954", font_size=36).to_edge(UP, buff=0.3)
        y = 0.5

        def plates(D, W):
            left = Rectangle(width=W, height=1.6, stroke_color=DATA, fill_color=DATA, fill_opacity=0.35)
            right = left.copy()
            left.move_to([-D / 2, y, 0])
            right.move_to([D / 2, y, 0])
            bd = DoubleArrow([-D / 2, y - 1.15, 0], [D / 2, y - 1.15, 0], buff=0, color=HEAD, stroke_width=2,
                             tip_length=0.15)
            ld = label(r"$D$: \ distance between centres", font_size=19, color=HEAD).next_to(bd, DOWN, buff=0.1)
            bw = BraceBetweenPoints([D / 2 - W / 2, y + 0.85, 0], [D / 2 + W / 2, y + 0.85, 0], UP, color=LAM)
            lw = label(r"$W$: \ width", font_size=19, color=LAM).next_to(bw, UP, buff=0.08)
            return VGroup(left, right, bd, ld, bw, lw)
        p1 = plates(5.0, 1.2)
        p2 = plates(9.0, 0.45)
        stylus = Dot([-2.5, y, 0], radius=0.11, color=WHITE)
        tag = note(r"illustrative", font_size=17).to_corner(UR, buff=0.4).shift(DOWN * 0.6)
        notes = VGroup(
            wrapped_label(r"tap one plate, \ then the other, \ as fast as possible without missing", 12.4,
                          font_size=21, color=WHITE),
            wrapped_label(r"farther or narrower: \ slower; \ doubling $D$ costs about what halving $W$ costs, \ so "
                          r"only the ratio $D/W$ matters, \ and time grows with its logarithm", 12.4, font_size=21,
                          color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "In 1954 the psychologist Paul Fitts asked people to tap a metal stylus back and forth between two "
            "plates, as fast as they could without missing. <bookmark mark='a'/> Each plate has a width, and the "
            "two are a distance apart. <bookmark mark='b'/> Move the plates farther apart, or make them narrower, "
            "and the taps slow down. Doubling the distance costs about as much "
            "as halving the width: only the ratio of distance to width matters, and the time grows with its "
            "logarithm. He had been reading Shannon, and he called his paper the information capacity of the human "
            "motor system."
        ) as vo:
            self.play(FadeIn(head), FadeIn(p1[:2]), FadeIn(stylus), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(p1[2:]), FadeIn(notes[0]))
            for k in range(4):
                self.play(stylus.animate.move_to([2.5 if k % 2 == 0 else -2.5, y, 0]), run_time=0.35)
            vo.wait_until("b")
            self.play(Transform(p1, p2), stylus.animate.move_to([-4.5, y, 0]))
            for k in range(4):
                self.play(stylus.animate.move_to([4.5 if k % 2 == 0 else -4.5, y, 0]), run_time=0.7)
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def channel(self):
        head = label(r"From channel capacity to Fitts's law", font_size=36).to_edge(UP, buff=0.3)
        shannon = MathTex(r"C = B\,\log_2(1 +", r"S", r"/", r"N", r")", font_size=46)
        shannon[1].set_color(DATA)
        shannon[3].set_color(LAM)
        fitts = MathTex(r"\mathrm{ID} = \log_2(", r"D", r"/", r"W", r"+ 1)", r"\ \text{bits}", font_size=46)
        fitts[1].set_color(DATA)
        fitts[3].set_color(LAM)
        mt = MathTex(r"\mathrm{MT} =", r"a", r"+", r"b", r"\cdot \mathrm{ID}", font_size=46)
        mt[1].set_color(KERN)
        mt[3].set_color(HEAD)
        VGroup(shannon, fitts, mt).arrange(DOWN, buff=0.75).move_to([-3.0, 0.2, 0])
        a1 = Arrow(shannon.get_bottom(), fitts.get_top(), buff=0.1, color=GREY_B, stroke_width=2)
        a2 = Arrow(fitts.get_bottom(), mt.get_top(), buff=0.1, color=GREY_B, stroke_width=2)
        W = 5.4
        side = VGroup(
            wrapped_label(r"Shannon's capacity of a noisy channel \ (Part 28): \ bits per use grow with the log of "
                          r"signal over noise", W, font_size=20, color=WHITE),
            wrapped_label(r"the analogy: \ the \textbf{distance} is the signal, \ the \textbf{width} is the "
                          r"tolerated noise; \ the index of difficulty counts the bits a movement must deliver",
                          W, font_size=20, color=DATA),
            wrapped_label(r"MacKenzie's form \ (1992) \ never goes negative and fits better than Fitts's own "
                          r"$\log_2(2D/W)$", W, font_size=20, color=GREY_A),
            wrapped_label(r"$a$: \ starting and stopping; \ $b$: \ seconds per bit, \ so $1/b$ is a "
                          r"\textbf{throughput} in bits per second", W, font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([3.6, 0.1, 0])
        with self.voiceover(
            "Fitts's analogy was Shannon's channel capacity from Part 28. <bookmark mark='a'/> A channel's capacity "
            "in bits grows with the logarithm of one plus signal over noise. <bookmark mark='b'/> In pointing, the "
            "distance plays the signal and the width the noise the movement may tolerate. The index of difficulty, "
            "log of distance over width plus one, counts the bits a movement must deliver. This is Scott "
            "MacKenzie's form from 1992; it never goes negative, and it fits better than Fitts's original. "
            "<bookmark mark='c'/> Movement time is then a constant, for starting and stopping, plus a slope times "
            "the bits. The slope is seconds per bit, and its inverse is a throughput: the bandwidth of a hand."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(shannon), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(GrowArrow(a1), Write(fitts), FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(GrowArrow(a2), Write(mt), FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    def simulate(self):
        f = load("fitts")
        rows = sorted(f["rows"], key=lambda r: r["ID"])
        head = label(r"A simulated hand obeys the law", font_size=36).to_edge(UP, buff=0.3)
        # the lane: a start mark and the current target, to scale (1024 px = 6 units)
        x0, s, ly = -6.2, 6.0 / 1024, 2.25
        lane = Line([x0, ly, 0], [x0 + 6.3, ly, 0], color=GREY_D, stroke_width=2)
        start = Dot([x0, ly, 0], radius=0.07, color=WHITE)

        def target(D, W):
            return Rectangle(width=max(W * s, 0.035), height=0.45, stroke_width=0, fill_color=YES,
                             fill_opacity=0.85).move_to([x0 + D * s, ly, 0])
        tgt = target(1024, 16)
        cond = label(r"$D = 1024$, \ $W = 16$ px", font_size=18, color=GREY_A).next_to(lane, DOWN, buff=0.32)
        cond.align_to(lane, LEFT)
        hand = Dot([x0, ly, 0], radius=0.08, color=HEAD)
        hops = [0.88, 1.035, 0.997]                # one movement's submovements (illustrative)
        g = axes([0, 8, 1], [0, 1.0, 0.2], x_length=6.0, y_length=3.3, x_label=r"index of difficulty, \ bits",
                 y_label=r"mean movement time, \ s", xticks=range(0, 9, 2), yticks=[0.2, 0.4, 0.6, 0.8, 1.0],
                 fy=lambda v: f"{v:.1f}")
        g.next_to(cond, DOWN, buff=0.35).align_to(lane, LEFT).shift(RIGHT * 0.45)
        ax = g.ax
        dots = [Dot(ax.c2p(r["ID"], r["MT"]), radius=0.055, color=DATA) for r in rows]
        fit = Line(ax.c2p(0, f["a"]), ax.c2p(7.5, f["a"] + 7.5 * f["b"]), color=HEAD, stroke_width=2.5)
        W = 5.0
        side = VGroup(
            wrapped_label(r"each \textbf{submovement} aims at the centre and lands with an error proportional to "
                          r"the distance it covers; \ corrections continue until inside \ (Meyer et al., \ 1988)",
                          W, font_size=19, color=WHITE),
            wrapped_label(r"each correction shrinks the remaining distance by a constant factor, \ so the "
                          r"number of corrections grows with $\log(D/W)$", W, font_size=19, color=YES),
            wrapped_label(r"20 conditions: \ $D$ from 64 to 1024 px, \ $W$ from 8 to 64 px", W, font_size=19,
                          color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([3.95, 1.25, 0])
        fit_txt = VGroup(
            label(rf"$a = {f['a']:.3f}$ s, \ \ $b = {f['b']:.3f}$ s per bit", font_size=21, color=HEAD),
            label(rf"$R^2 = {f['r2']:.3f}$", font_size=21, color=HEAD),
            label(rf"throughput $1/b = {f['throughput_bits_per_s']:.1f}$ bits per second", font_size=21,
                  color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).next_to(side, DOWN, buff=0.4).align_to(side, LEFT)
        tag = note(r"one movement: \ illustrative", font_size=16).next_to(lane, UP, buff=0.12).align_to(lane, LEFT)
        with self.voiceover(
            "Why a logarithm? David Meyer and colleagues, in 1988, gave an answer. <bookmark mark='a'/> "
            "A movement is a series of submovements. Each aims at the centre of the target and lands with an error "
            "proportional to the distance it covered; if it misses, another follows. <bookmark mark='b'/> So each "
            "correction shrinks the remaining distance by a roughly constant factor, and the number of corrections "
            "grows with the logarithm of distance over width. <bookmark mark='c'/> We simulated that hand on twenty "
            "targets, near and far, wide and narrow. <bookmark mark='d'/> The points "
            f"fall on a line, with R squared of {f['r2']:.2f}. The slope is {f['b']:.3f} seconds per bit: a "
            f"throughput of {f['throughput_bits_per_s']:.1f} bits per second for our simulated hand. People "
            "measured with a mouse manage a few bits per second, according to Soukoreff and MacKenzie in 2004."
        ) as vo:
            self.play(FadeIn(head), Create(lane), FadeIn(start), FadeIn(tgt), FadeIn(cond), FadeIn(hand),
                      FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            for h in hops:
                self.play(hand.animate.move_to([x0 + h * 1024 * s, ly, 0]), run_time=0.5)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeOut(hand), FadeOut(tag), Create(g), FadeIn(side[2]))
            for r, d in zip(rows, dots):
                new_cond = label(rf"$D = {r['D']}$, \ $W = {r['W']}$ px", font_size=18, color=GREY_A)
                new_cond.move_to(cond, aligned_edge=LEFT)
                self.play(Transform(tgt, target(r["D"], r["W"])), Transform(cond, new_cond), FadeIn(d),
                          run_time=0.3)
            vo.wait_until("d")
            self.play(Create(fit), FadeIn(fit_txt))
        self.wait(0.4)
        self.clear_scene()

    def edges(self):
        e = load("edge")
        head = label(r"Infinitely deep targets", font_size=36).to_edge(UP, buff=0.3)
        scr = Rectangle(width=5.6, height=3.6, stroke_color=GREY_B, stroke_width=2).move_to([-3.6, -0.1, 0])
        top = scr.get_top()[1]
        bar = Rectangle(width=5.6, height=0.28, stroke_width=0, fill_color=GREY_D, fill_opacity=1).move_to(
            [scr.get_x(), top - 0.14, 0])
        t_edge = Rectangle(width=0.6, height=0.28, stroke_width=0, fill_color=YES, fill_opacity=0.9).move_to(
            [scr.get_x() + 1.2, top - 0.14, 0])
        t_mid = Rectangle(width=0.6, height=0.28, stroke_width=0, fill_color=NO, fill_opacity=0.9).move_to(
            [scr.get_x() - 1.4, 0.1, 0])
        st = Dot([scr.get_x(), -1.5, 0], radius=0.07, color=WHITE)
        p_mid = VMobject(color=NO, stroke_width=2.5).set_points_as_corners(
            [st.get_center(), t_mid.get_center() + [-0.25, 0.32, 0], t_mid.get_center() + [0.08, -0.05, 0]])
        p_edge = VMobject(color=YES, stroke_width=2.5).set_points_as_corners(
            [st.get_center(), [t_edge.get_x() + 0.1, top, 0]])
        sc_tag = note(r"schematic", font_size=16).next_to(scr, DOWN, buff=0.12).align_to(scr, LEFT)
        bc = bar_chart([e["normal"], e["edge"]], [r"in the middle", r"at the edge"], [NO, YES], height=2.4,
                       bar_w=1.0, gap=1.0, fmt_=lambda v: f"{v:.2f} s", font_size=20)
        bc.move_to([3.1, 0.6, 0])
        cap = label(r"mean time, \ same target, \ simulated", font_size=18, color=GREY_A).next_to(bc, UP, buff=0.25)
        notes = VGroup(
            wrapped_label(r"the pointer stops at the edge: \ overshoot is impossible, \ so the target is infinitely "
                          r"deep along the movement", 6.0, font_size=19, color=YES),
            wrapped_label(r"Macintosh \ (1984): \ one menu bar at the top of the screen; \ corners are edges twice "
                          r"over", 6.0, font_size=19, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(bc, DOWN, buff=0.45).set_x(3.6)
        with self.voiceover(
            "Designers exploit a loophole. <bookmark mark='a'/> A pointer cannot leave the screen. "
            "Aim at a target on the edge and overshoot is impossible: the pointer stops there, as if the target were "
            "infinitely deep. <bookmark mark='b'/> In our simulation the same target takes "
            f"{e['normal']:.2f} seconds in the middle and {e['edge']:.2f} at the edge: the hand can fling, "
            "and need not correct. <bookmark mark='c'/> That is why the Macintosh, in 1984, put a "
            "single menu bar at the very top of the screen, and why the corners, edges twice over, are the "
            "fastest places of all to reach."
        ) as vo:
            self.play(FadeIn(head), Create(scr), FadeIn(bar), FadeIn(t_edge), FadeIn(t_mid), FadeIn(st),
                      FadeIn(sc_tag))
            vo.wait_until("a")
            self.play(Create(p_mid), Create(p_edge), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(cap), FadeIn(bc))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def steering(self):
        head = label(r"The steering law: \ tunnels", font_size=36).to_edge(UP, buff=0.3)
        # a cascading menu: the pointer must stay inside the item while it travels to the submenu
        items = VGroup(*[Rectangle(width=3.8, height=0.5, stroke_color=GREY_C, stroke_width=1.2, fill_color=BG,
                                   fill_opacity=1) for _ in range(5)]).arrange(DOWN, buff=0).move_to([-4.3, 0.3, 0])
        names = VGroup(*[label(t, font_size=20, color=GREY_A).move_to(items[k]).align_to(items[k], LEFT).shift(
            RIGHT * 0.15) for k, t in enumerate((r"Open recent $\blacktriangleright$", r"New", r"Save", r"Export",
                                                 r"Print"))])
        items[0].set_fill(DATA, opacity=0.3)
        sub = VGroup(*[Rectangle(width=2.4, height=0.5, stroke_color=GREY_C, stroke_width=1.2, fill_color=BG,
                                 fill_opacity=1) for _ in range(4)]).arrange(DOWN, buff=0)
        sub.next_to(items[0], RIGHT, buff=0).align_to(items[0], UP)
        subn = VGroup(*[label(t, font_size=20, color=GREY_A).move_to(sub[k]).align_to(sub[k], LEFT).shift(
            RIGHT * 0.15) for k, t in enumerate((r"notes.txt", r"plan.md", r"talk.pdf", r"job.py"))])
        y1 = items[0].get_y()
        xl, xr = items[0].get_left()[0], items[0].get_right()[0]
        path = VMobject(color=HEAD, stroke_width=3).set_points_smoothly(
            [[xl + 2.05, y1 - 0.07, 0], [xl + 2.6, y1 + 0.08, 0], [xl + 3.2, y1 - 0.06, 0], [xr - 0.05, y1, 0],
             [xr + 0.1, sub[1].get_y(), 0]])
        tun = BraceBetweenPoints([xl + 2.05, items[0].get_top()[1], 0], items[0].get_corner(UR), UP, color=LAM)
        tl = label(r"$A$", font_size=20, color=LAM).next_to(tun, UP, buff=0.05)
        wb = BraceBetweenPoints(items[0].get_corner(DL), items[0].get_corner(UL), LEFT, color=LAM)
        wl = label(r"$W$", font_size=20, color=LAM).next_to(wb, LEFT, buff=0.05)
        law = MathTex(r"T = a + b\,\frac{A}{W}", font_size=44, color=HEAD)
        gen = MathTex(r"T = a + b \int_C \frac{ds}{W(s)}", font_size=36, color=GREY_A)
        W = 5.4
        side = VGroup(
            law, gen,
            wrapped_label(r"Accot and Zhai \ (1997): \ for a path through a tunnel, \ time grows \textit{linearly} "
                          r"with length over width, \ not logarithmically", W, font_size=20, color=WHITE),
            wrapped_label(r"a long, \ narrow menu item is a tunnel: \ slip out, \ and the submenu closes", W,
                          font_size=20, color=NO),
            wrapped_label(r"remedies: \ wider items, \ shallower menus, \ and submenus that forgive a diagonal "
                          r"path towards them", W, font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.7, 0.0, 0])
        tag = note(r"schematic", font_size=16).next_to(items, DOWN, buff=0.2).align_to(items, LEFT)
        with self.voiceover(
            "Some movements must stay inside a path. <bookmark mark='a'/> To reach a submenu, the pointer travels "
            "along the parent item, and if it slips out on the way the submenu closes. <bookmark mark='b'/> Johnny "
            "Accot and Shumin Zhai showed in 1997 that steering through a tunnel takes time proportional to its "
            "length over its width, summed along the path. That is linear, not logarithmic, so tunnels cost far "
            "more than targets. <bookmark mark='c'/> Nested menus are tunnels in series. The remedies are wider "
            "items, shallower menus, and submenus that forgive a diagonal path towards them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(items), FadeIn(names), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(sub), FadeIn(subn), FadeIn(tun), FadeIn(tl), FadeIn(wb), FadeIn(wl))
            self.play(Create(path), run_time=1.5)
            vo.wait_until("b")
            self.play(Write(law), FadeIn(gen), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]), FadeIn(side[4]))
        self.wait(0.4)
        self.clear_scene()


_ = (KERN, LAM)
