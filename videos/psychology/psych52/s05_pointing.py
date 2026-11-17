from __future__ import annotations

from videos.psychology.psych52.common import *  # noqa: F403


class Pointing(VoiceoverScene):
    def construct(self):
        card_section(self, 4, r"Pointing, \ measured", r"How many bits per second does a hand deliver?")
        self.law()
        self.effective()
        self.steering()

    def law(self):
        d = load("pointing")
        head = heading(r"Sixteen conditions, \ one line")
        A = axes([0.5, 6.5], [0, 1.0], x_length=5.6, y_length=3.2, xticks=[1, 2, 3, 4, 5, 6], yticks=[0, 0.5, 1.0],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}", xlabel=r"index of difficulty (bits)",
                 ylabel=r"movement time (s)", center=[-3.3, 0.3, 0], font_size=12)
        pts = scatter(A.ax, d["ID"], d["MT"], MODEL, radius=0.07)
        xs = np.array([0.8, 6.3])
        line = Line(A.ax.c2p(xs[0], d["a"] + d["b"] * xs[0]), A.ax.c2p(xs[1], d["a"] + d["b"] * xs[1]), color=PERSON,
                    stroke_width=4)
        rows = rows_of([
            (r"Psyche points at targets 64 to 512 pixels away and 8 to 64 wide: \ 24 movements in each of 16 "
             r"conditions", WHITE),
            (r"the index of difficulty, \ $\log_2(D/W + 1)$, \ collapses all sixteen onto one line", MODEL),
            (rf"MT = {d['a']:.2f} + {d['b']:.2f} ID seconds, \ $r$ = {d['r']:.3f}: \ Fitts (1954), \ in MacKenzie's "
             rf"Shannon form", PERSON),
            (r"distance and size trade exactly: \ double both and nothing changes", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{work.fitts\_effective}, \ 384 simulated movements")
        with self.voiceover(
            "Part 51 met Fitts's law. Here it's measured the way designers measure it. <bookmark mark='a'/> Psyche "
            "points at targets from sixty-four to five hundred and twelve pixels away, and from eight to sixty-four "
            "wide: twenty-four movements in each of sixteen conditions. <bookmark mark='b'/> The index of difficulty, "
            "the log of distance over width plus one, collapses all sixteen onto one line. <bookmark mark='c'/> About "
            "two tenths of a second plus two tenths per bit, with a correlation near one. <bookmark mark='d'/> "
            "Distance and size trade exactly. Double both, and nothing changes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(pts))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Create(line))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def effective(self):
        d = load("pointing")
        rows_section(self, r"Throughput, \ from where the clicks land", [
            (r"people trade speed for accuracy: \ one person aims carefully, \ another sprays", WHITE),
            (r"so measure the width they actually used: \ $W_e = 4.133 \times$ the SD of the endpoints, \ which "
             r"covers 96\% of a normal spread", MODEL),
            (rf"throughput = $ID_e$ / MT, \ in bits per second: \ here {d['TP_mean']:.1f}, \ within the range reported "
             rf"for a mouse", PERSON),
            (r"ISO 9241-9 uses it to compare devices: \ a mouse, \ a touchpad, \ a joystick, \ an eye tracker", GOOD),
            (r"one number per device and person, \ comparable across studies: \ the reason Fitts's law is still used",
             YOU),
        ], "One complication: people trade speed for accuracy. <bookmark mark='a'/> One person aims carefully, "
           "another sprays. <bookmark mark='b'/> So measure the width they actually used: four point one three times "
           "the spread of their endpoints, which covers ninety-six percent of a normal distribution. "
           "<bookmark mark='c'/> Throughput is the effective index of difficulty divided by movement time, in bits per "
           "second. Here, about three point eight, within the range reported for a mouse. <bookmark mark='d'/> The "
           "international standard uses it to compare devices: a mouse, a touchpad, a joystick, an eye tracker. "
           "<bookmark mark='e'/> One number per device and person, comparable across studies. That's why Fitts's law "
           "is still in use seventy years on.", tag=psyche_tag(r"\texttt{work.fitts\_effective}"))

    def steering(self):
        d = load("steering")
        head = heading(r"Steering through a tunnel")
        A = axes([0, 850], [0, 7], x_length=5.6, y_length=3.0, xticks=[100, 200, 400, 800], yticks=[0, 2, 4, 6],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f} s", xlabel=r"tunnel length (pixels)",
                 ylabel=r"time", center=[-3.3, 0.3, 0], font_size=12)
        cols = [AUTH, PERSON, GOOD]
        cs = VGroup(*[curve(A.ax, d["L"], d["t"][i], cols[i], stroke_width=4) for i in range(3)])
        key = VGroup(*[label(rf"width {int(w)}", font_size=13, color=c) for w, c in zip(d["W"], cols)])
        key.arrange(RIGHT, buff=0.4).next_to(A, UP, buff=0.2)
        rows = rows_of([
            (r"Accot and Zhai, \ 1997: \ moving along a path of length $A$ and width $W$ takes $a + b\,A/W$", WHITE),
            (r"not a logarithm but a ratio: \ every step of the path must be kept inside the walls", MODEL),
            (r"cascading menus are tunnels: \ a narrow, \ long path to a submenu is slow and error-prone", AUTH),
            (r"the fixes: \ wider paths, \ forgiving delays before a submenu closes, \ or no cascades at all", GOOD),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{work.steering\_time}, \ illustrative constants")
        with self.voiceover(
            "Some movements aren't to a target but along a path. <bookmark mark='a'/> Johnny Accot and Shumin Zhai "
            "found in 1997 that steering through a tunnel of length A and width W takes a constant plus b times A "
            "over W. <bookmark mark='b'/> Not a logarithm but a ratio, because every step of the path must stay "
            "inside the walls. <bookmark mark='c'/> Cascading menus are tunnels. A narrow, long path to a submenu is "
            "slow and error-prone. <bookmark mark='d'/> The fixes are wider paths, a forgiving delay before a submenu "
            "closes, or no cascades at all."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), LaggedStart(*[Create(c) for c in cs], lag_ratio=0.3))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
