from __future__ import annotations

from videos.economics.econ20.common import *  # noqa: F403


class Solow(VoiceoverScene):
    def construct(self):
        card(self, 3, r"The Solow model", r"If capital and labour can be combined in any proportion, \ where does "
             r"an economy that saves a fixed share settle?", "Chapter three. The Solow model.",
             lit={1956: r"Solow; \ Swan"}, scale=("nation",), horizon=("decades",))
        self.production()
        self.accumulation()
        self.diagram()
        self.balanced()
        self.more_saving()

    def production(self):
        s = load("solow")
        a = s["kw"]["alpha"]
        ax = plane([0, 8], [0, 2.2], center=RIGHT * 3.0 + DOWN * 0.5, x_length=6.0, y_length=4.6,
                   xticks=[0, 2, 4, 6, 8], yticks=[0, 0.5, 1, 1.5, 2], xlabel=r"capital per effective worker $k$",
                   ylabel=r"output $y$", font_size=16)
        ks = np.linspace(0, 8, 200)
        curve = path(ax, ks, ks ** a, color=OUTPUT, width=4)
        steps = VGroup()
        for k0 in (1, 3, 5):
            y0, y1 = k0 ** a, (k0 + 2) ** a
            steps.add(VGroup(seg(ax, k0, y0, k0 + 2, y0, color=GREY_B, width=2),
                             seg(ax, k0 + 2, y0, k0 + 2, y1, color=CAPITAL, width=3)))
        rows = VGroup(
            label(r"the island gets capital: \ boats, \ nets, \ a granary", font_size=23, color=CAPITAL),
            MathTex(r"Y = K^{\alpha}\,(AL)^{1-\alpha}", font_size=44),
            label(r"double $K$ and $L$: \ double $Y$ \ (constant returns)", font_size=21, color=GREY_A),
            MathTex(r"y = \frac{Y}{AL} = k^{\alpha}, \quad k = \frac{K}{AL}", font_size=40, color=OUTPUT),
            label(rf"$\alpha = 1/3$: \ each extra boat adds less \ (diminishing returns)", font_size=21,
                  color=CAPITAL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(LEFT, buff=0.5).shift(DOWN * 0.2)
        with self.voiceover(
            "Solow kept Harrod's saving and dropped the fixed ratio. <bookmark mark='a'/> The island now has "
            "capital: boats, nets, a granary, built from output that is saved instead of eaten. "
            "<bookmark mark='b'/> Output is made from capital, K, and labour, L, made more effective by technology, "
            "A, in a Cobb-Douglas production function, with capital's share alpha. <bookmark mark='c'/> Double both "
            "capital and effective labour and output doubles: constant returns. <bookmark mark='d'/> So everything "
            "can be measured per unit of effective labour: output per effective worker, y, is k to the alpha, where k "
            f"is capital per effective worker. <bookmark mark='e'/> With alpha a third, each extra boat adds less "
            "than the last: equal steps in capital buy smaller and smaller steps in output."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(ax))
            for mk, r in zip("bcd", rows[1:4]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
            self.play(Create(curve), run_time=1.5)
            vo.wait_until("e")
            self.play(FadeIn(rows[4]), LaggedStart(*[FadeIn(st) for st in steps], lag_ratio=0.5), run_time=2)
        self.clear_scene()

    def accumulation(self):
        rows = VGroup(
            MathTex(r"\dot K = sY - \delta K", font_size=46),
            MathTex(r"\frac{\dot k}{k} = \frac{\dot K}{K} - \frac{\dot A}{A} - \frac{\dot L}{L} = \frac{sY}{K} - "
                    r"\delta - g - n", font_size=42),
            MathTex(r"\dot k = s\,k^{\alpha} - (n + g + \delta)\,k", font_size=58, color=E.ACCENT),
        ).arrange(DOWN, buff=0.55).move_to(UP * 0.6)
        notes = VGroup(
            label(r"saved output becomes capital; \ a share $\delta$ wears out", font_size=21, color=SAVE),
            label(r"$k$ is a ratio: \ its growth rate is the top's less the bottom's", font_size=21, color=GREY_A),
            label(r"investment \ minus \ what keeps $k$ from shrinking: \ break-even investment", font_size=22,
                  color=BREAK),
        )
        for n_, r in zip(notes, rows):
            n_.next_to(r, DOWN, buff=0.12)
        island_ = label(r"island: \ $s = 15\%$, \ $n = 1\%$, \ $g = 2\%$, \ $\delta = 5\%$", font_size=24,
                        color=CAPITAL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Now the accumulation. <bookmark mark='a'/> Each year a share s of output is saved and becomes new "
            "capital, and a share delta of the old capital wears out. <bookmark mark='b'/> Capital per effective "
            "worker is a ratio, so its growth rate is capital's growth rate, less technology's, g, less the labour "
            "force's, n. <bookmark mark='c'/> Multiply through by k and you have the equation that runs the model: "
            "the change in capital per effective worker is investment, s times k to the alpha, less break-even "
            "investment, n plus g plus delta times k: what it takes just to equip new workers, keep up with "
            "technology and replace what wears out. <bookmark mark='d'/> The island saves fifteen percent; its "
            "people increase by one percent a year, technology by two, and five percent of its boats and nets wear "
            "out."
        ) as vo:
            self.play(Write(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            for mk, r, n_ in zip("bc", rows[1:], notes[1:]):
                vo.wait_until(mk)
                self.play(Write(r), FadeIn(n_))
            vo.wait_until("d")
            self.play(FadeIn(island_, shift=UP * 0.1))
        self.clear_scene()

    def diagram(self):
        s = load("solow")
        st = s["steady"]
        k = np.array(s["k"])
        ax = plane([0, float(k[-1])], [0, 0.65], center=LEFT * 1.3 + DOWN * 0.4, x_length=8.4, y_length=5.2,
                   xticks=[0, 2, 4, 6], yticks=[0, 0.2, 0.4, 0.6], xlabel=r"capital per effective worker $k$",
                   ylabel=r"per effective worker", font_size=16)
        inv = path(ax, k, s["sf"], color=SAVE, width=4)
        brk = path(ax, k, s["break"], color=BREAK, width=4, yr=(0, 0.65))
        li = label(r"investment $s\,k^\alpha$", font_size=19, color=SAVE).next_to(ax.ax.c2p(k[-1], s["sf"][-1]),
                                                                                  UP, buff=0.1).shift(LEFT * 0.6)
        lb = label(r"break-even $(n+g+\delta)\,k$", font_size=19, color=BREAK).next_to(
            ax.ax.c2p(7.0, 0.08 * 7.0), LEFT, buff=0.15).shift(UP * 0.25)
        star = Dot(ax.ax.c2p(st["k"], s["s"] * st["y"]), radius=0.1, color=WHITE)
        drop = DashedLine(ax.ax.c2p(st["k"], 0), ax.ax.c2p(st["k"], s["s"] * st["y"]), color=GREY_B)
        kl = MathTex(r"k^\ast", font_size=34).next_to(ax.ax.c2p(st["k"], 0), UR, buff=0.1)
        right = Arrow(ax.ax.c2p(0.6, 0.03), ax.ax.c2p(1.9, 0.03), buff=0, color=CONS, stroke_width=5)
        left = Arrow(ax.ax.c2p(6.2, 0.03), ax.ax.c2p(4.2, 0.03), buff=0, color=LABOUR, stroke_width=5)
        side = VGroup(
            MathTex(r"k^\ast = \Big(\frac{s}{n+g+\delta}\Big)^{\frac{1}{1-\alpha}}", font_size=40),
            label(rf"island: \ $k^\ast = {st['k']:.2f}$, \ $y^\ast = {st['y']:.2f}$", font_size=21, color=OUTPUT),
            label(rf"capital $=$ {st['ky']:.2f} years of output", font_size=21, color=CAPITAL),
        ).arrange(DOWN, buff=0.35).to_edge(RIGHT, buff=0.4).shift(UP * 0.8)
        with self.voiceover(
            "Here is the equation as a picture: Solow's diagram. <bookmark mark='a'/> Investment per effective worker "
            "is the saving rate times output: a curve that flattens, because of diminishing returns. "
            "<bookmark mark='b'/> Break-even investment is a straight line through the origin. "
            "<bookmark mark='c'/> Where investment is above the line, capital per effective worker grows. "
            "<bookmark mark='d'/> Where it is below, it shrinks. <bookmark mark='e'/> So from anywhere, the economy "
            "heads for the crossing, the steady state k star: the saving rate over the break-even rate, to the power "
            f"one over one minus alpha. On the island, k star is {st['k']:.2f}, and output per effective worker "
            f"{st['y']:.2f}; capital is about {st['ky']:.1f} years of output."
        ) as vo:
            self.play(FadeIn(ax))
            vo.wait_until("a")
            self.play(Create(inv), FadeIn(li))
            vo.wait_until("b")
            self.play(Create(brk), FadeIn(lb))
            vo.wait_until("c")
            self.play(GrowFromPoint(right, right.get_start()))
            vo.wait_until("d")
            self.play(GrowFromPoint(left, left.get_start()))
            vo.wait_until("e")
            self.play(FadeIn(star), Create(drop), FadeIn(kl), FadeIn(side[0]))
            self.play(FadeIn(side[1]), FadeIn(side[2]))
        self.clear_scene()

    def balanced(self):
        rows = VGroup(
            label(r"in the steady state $k$ is constant, \ so:", font_size=27, color=E.ACCENT),
            label(r"1. \ output per worker grows at $g$", font_size=24, color=OUTPUT),
            label(r"2. \ capital per worker grows at $g$ too", font_size=24, color=CAPITAL),
            label(r"3. \ the return on capital, \ $\alpha k^{\alpha-1} - \delta$, \ is constant", font_size=24,
                  color=RATE),
            label(r"4. \ capital $\div$ output, \ $k^{1-\alpha}$, \ is constant", font_size=24, color=BREAK),
            label(r"5. \ labour's share is $1-\alpha$, \ capital's $\alpha$: \ constant", font_size=24,
                  color=LABOUR),
            label(r"6. \ different growth rates? \ only on the way to a steady state, \ or with different $A$",
                  font_size=24, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(UP * 0.1)
        with self.voiceover(
            "Now look back at Kaldor's list. <bookmark mark='a'/> In the steady state capital per effective worker "
            "stands still, so per actual worker, output grows at technology's rate g. <bookmark mark='b'/> So does "
            "capital per worker. <bookmark mark='c'/> The return on capital depends only on k, so it is constant. "
            "<bookmark mark='d'/> So is the ratio of capital to output. <bookmark mark='e'/> And with Cobb-Douglas "
            "production, competitive markets pay labour a share one minus alpha of income, whatever happens. "
            "<bookmark mark='f'/> Five facts in one stroke. The sixth, different growth rates, the model can produce "
            "only in two ways: countries on their way to a steady state, or countries with different technology. "
            "Hold on to that: the rest of the part tests both."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r in zip("abcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def more_saving(self):
        s = load("solow")
        st, st2 = s["steady"], s["steady_30"]
        kk = np.linspace(0, 9, 300)
        ax2 = plane([0, 9], [0, 0.75], center=LEFT * 1.6 + DOWN * 0.4, x_length=8.0, y_length=5.0,
                    xticks=[0, 3, 6, 9], yticks=[0, 0.25, 0.5, 0.75], xlabel=r"$k$", ylabel=r"per effective worker",
                    font_size=16)
        inv1 = path(ax2, kk, 0.15 * kk ** (1 / 3), color=SAVE, width=4)
        inv2 = path(ax2, kk, 0.30 * kk ** (1 / 3), color=SAVE, width=4).set_stroke(opacity=1)
        inv1.set_stroke(opacity=0.45)
        brk = path(ax2, kk, 0.08 * kk, color=BREAK, width=4, yr=(0, 0.75))
        d1 = Dot(ax2.ax.c2p(st["k"], 0.15 * st["y"]), radius=0.09, color=GREY_B)
        d2 = Dot(ax2.ax.c2p(st2["k"], 0.30 * st2["y"]), radius=0.1, color=WHITE)
        ls = VGroup(label(r"$s = 15\%$", font_size=19, color=SAVE).next_to(ax2.ax.c2p(8, 0.15 * 8 ** (1 / 3)), DOWN,
                                                                         buff=0.12),
                    label(r"$s = 30\%$", font_size=19, color=SAVE).next_to(ax2.ax.c2p(4.5, 0.30 * 4.5 ** (1 / 3)), UP,
                                                                         buff=0.12).shift(LEFT * 0.3))
        side = VGroup(
            label(r"double the saving rate:", font_size=24, color=E.ACCENT),
            label(rf"capital: \ $\times{s['ratio_k']:.2f}$", font_size=23, color=CAPITAL),
            label(rf"output: \ $\times{s['ratio_y']:.2f}$", font_size=23, color=OUTPUT),
            MathTex(r"\frac{d\ln y^\ast}{d\ln s} = \frac{\alpha}{1-\alpha} = \frac{1}{2}", font_size=36),
            label(r"a higher level, \\ not a higher growth rate", font_size=23, color=HOLD),
        ).arrange(DOWN, buff=0.3).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "So what can saving do? <bookmark mark='a'/> Suppose the island doubles its saving rate, from fifteen "
            "to thirty percent. The investment curve doubles in height, <bookmark mark='b'/> and the steady state "
            f"moves out: capital per effective worker {s['ratio_k']:.2f} times as high, but output only "
            f"{s['ratio_y']:.2f} times. <bookmark mark='c'/> The elasticity of steady-state output with respect to "
            "saving is alpha over one minus alpha: with a capital share of a third, one half. "
            "<bookmark mark='d'/> And in the new steady state, output per worker again grows at g, two percent. "
            "Saving buys a higher level of income, not a faster rate of growth. Only technology keeps income "
            "growing. That is the uncomfortable answer."
        ) as vo:
            self.play(FadeIn(ax2), Create(inv1), Create(brk), FadeIn(d1), FadeIn(ls[0]), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(inv2), FadeIn(ls[1]))
            vo.wait_until("b")
            self.play(FadeIn(d2), FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(side[4]))
        self.clear_scene()
