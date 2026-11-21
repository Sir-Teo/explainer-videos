from __future__ import annotations

from videos.economics.econ51.common import *  # noqa: F403


class Operator(VoiceoverScene):
    def construct(self):
        card(self, 1, r"The Bellman operator as a contraction", r"Why does repeating the equation converge?",
             "Chapter one. The Bellman operator as a contraction.", lit={1957: r"Bellman", 1965: r"Blackwell"},
             scale=("household", "nation"), horizon=("a century",))
        self.equation()
        self.cobweb()
        self.distances()
        self.blackwell()

    def equation(self):
        eq = MathTex(r"(TV)(k) \;=\; \max_{k'}\ \Big\{\, u\big(f(k) - k'\big) \;+\; \beta\, V(k') \,\Big\}",
                     font_size=44, color=THEORY).move_to(UP * 1.6)
        parts = VGroup(
            label(r"$V$: \ a guess of the value of each capital stock", font_size=22, color=VALUE),
            label(r"$T$: \ the operator that turns one guess into a better one", font_size=22, color=WHITE),
            label(r"the answer: \ the $V$ that $T$ leaves unchanged, \ $V = TV$", font_size=22, color=POLICY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(eq, DOWN, buff=0.7)
        model = label(r"the growth model: \ $u = c^{1-\gamma}/(1-\gamma)$, \ $\gamma = 2$; \ "
                      r"$f(k) = k^{0.36} + 0.92\,k$; \ $\beta = 0.96$", font_size=19, color=GREY_A).to_edge(
            DOWN, buff=0.5)
        with self.voiceover(
            "Write the growth model as Bellman did. <bookmark mark='a'/> The value of starting a year with "
            "capital k is the best, over next year's capital, of this year's utility plus the discounted value of "
            "next year. <bookmark mark='b'/> Read the right-hand side as a machine. Put in a guess V, a value for "
            "every capital stock; <bookmark mark='c'/> the machine, the Bellman operator T, returns a new guess. "
            "<bookmark mark='d'/> The answer is the value function the machine leaves unchanged: a fixed point, V "
            "equals T of V. <bookmark mark='e'/> The model is the one of Part twenty-nine: utility with an "
            "elasticity of substitution of a half, a capital share of 0.36, eight percent depreciation, and a "
            "discount factor of 0.96."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(eq), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(parts[0], shift=RIGHT * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(parts[1], shift=RIGHT * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(parts[2], shift=RIGHT * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(model))
        self.clear_scene()

    def cobweb(self):
        b, c = 0.6, 0.8                      # a contraction on the line, drawn: x -> b x + c, fixed point 2
        ax = plane([0, 4], [0, 4], center=LEFT * 2.2 + DOWN * 0.2, x_length=5.6, y_length=5.6,
                   xticks=[0, 1, 2, 3, 4], yticks=[0, 1, 2, 3, 4], xlabel=r"a guess", ylabel=r"the operator's answer",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        diag = seg(ax, 0, 0, 4, 4, GREY_B, 1.6, dashed=True)
        line = seg(ax, 0, c, 4, b * 4 + c, VALUE, 3.0)
        fp = dot(ax, 2, 2, POLICY, 0.09)
        steps = VGroup()
        x = 3.8
        for _ in range(6):
            y = b * x + c
            steps.add(seg(ax, x, x, x, y, WHITE, 1.6), seg(ax, x, y, y, y, WHITE, 1.6))
            x = y
        side = VGroup(
            label(r"a contraction: \\ it brings any two \\ guesses closer, \\ by a factor $\beta < 1$", font_size=20,
                  color=VALUE),
            label(r"so the iterates \\ walk to the one \\ fixed point, \\ from anywhere", font_size=20,
                  color=POLICY),
            label(r"Banach's theorem \ (1922)", font_size=18, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).to_edge(RIGHT, buff=0.6)
        with self.voiceover(
            "Why should repeating the machine settle anywhere? Draw a machine on a line, a cartoon of T. <bookmark "
            "mark='a'/> The dashed diagonal is where the answer equals the guess. The purple line is the machine: "
            "it maps each guess to an answer, and it is flatter than the diagonal, so it brings any two guesses "
            "closer together. That is a contraction. <bookmark mark='b'/> Start anywhere, apply it, apply it again: "
            "the steps walk in to the one point where the line meets the diagonal. <bookmark mark='c'/> Stefan "
            "Banach proved in 1922 that a contraction on a complete space has exactly one fixed point, and that "
            "iterating from any start reaches it. The Bellman operator is such a machine, on the space of value "
            "functions."
        ) as vo:
            self.play(FadeIn(ax), Create(diag))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(s_) for s_ in steps], lag_ratio=0.5), run_time=4.0)
            self.play(FadeIn(fp, scale=1.5), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def distances(self):
        G = load("growth")
        d = np.array(G["dist"])
        n = len(d)
        ax = plane([0, n], [-7, 1], center=LEFT * 1.6 + DOWN * 0.3, x_length=8.0, y_length=4.6,
                   xticks=[0, 100, 200, 300], yticks=[-6, -4, -2, 0], xlabel=r"round of iteration",
                   ylabel=r"change from the round before, \ $\log_{10}$", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        curve = path(ax, np.arange(1, n + 1), np.log10(d), VFI, 3.0, smooth=False)
        guide = seg(ax, 1, np.log10(d[0]), n, np.log10(d[0]) + (n - 1) * np.log10(G["beta"]), GREY_B, 1.6,
                    dashed=True)
        r_last = G["ratio"][-1]
        side = VGroup(
            label(r"each round, \\ the change shrinks \\ by the factor $\beta$", font_size=20, color=WHITE),
            label(rf"measured: \ {r_last:.3f}", font_size=20, color=VFI),
            label(rf"to shrink it a million \\ times: \ $\log 10^{{-6}} / \log 0.96$ \\ $\approx 338$ rounds; \ "
                  rf"it took {G['vfi_iters']}", font_size=18, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.35)
        tag = label(r"computed: \ 300 grid points", font_size=13, color=GREY_B).to_corner(DL, buff=0.3)
        with self.voiceover(
            "On the real model, measure it. <bookmark mark='a'/> Each round, record how far the new value "
            "function is from the old, at the worst capital stock, on a log scale. <bookmark mark='b'/> After a few "
            "rounds the points fall on a straight line, and its slope is the discount factor: each round the change "
            f"shrinks by a factor of {r_last:.3f}, <bookmark mark='c'/> exactly the 0.96 the theory promises. "
            "<bookmark mark='d'/> That also says how long it will take: to shrink the change a million times needs "
            f"about three hundred and thirty-eight rounds, and it took {G['vfi_iters']}. Patience is expensive: "
            "with a discount factor of 0.99, as in quarterly models, it would take four times as many."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(curve), run_time=3.0)
            vo.wait_until("b")
            self.play(Create(guide), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def blackwell(self):
        G = load("growth")
        rows = VGroup(
            VGroup(label(r"monotonicity", font_size=26, color=VALUE),
                   MathTex(r"V \le W \;\Rightarrow\; TV \le TW", font_size=36, color=WHITE),
                   label(r"a better future never makes today worse", font_size=19, color=GREY_A),
                   label(r"checked: \ " + (r"holds" if G["monotone"] else r"fails"), font_size=19,
                         color=GAIN if G["monotone"] else LOSS)).arrange(DOWN, buff=0.18),
            VGroup(label(r"discounting", font_size=26, color=POLICY),
                   MathTex(r"T(V + a) \;=\; TV + \beta\,a", font_size=36, color=WHITE),
                   label(r"adding $a$ to every future value adds $\beta a$ today", font_size=19, color=GREY_A),
                   label(r"checked: \ error below $10^{-14}$" if G["discount_error"] < 1e-14 else
                         rf"checked: \ error {G['discount_error']:.1e}", font_size=19, color=GAIN)).arrange(
                DOWN, buff=0.18),
        ).arrange(RIGHT, buff=1.2).move_to(UP * 0.2)
        head = label(r"Blackwell's two conditions \ (1965)", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        foot = label(r"together they make $T$ a contraction with modulus $\beta$: \ the answer exists, \ is unique, \ "
                     r"and iteration finds it", font_size=21, color=WHITE).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "How do we know the Bellman operator is a contraction without proving it from scratch each time? David "
            "Blackwell gave two conditions in 1965 that are easy to check. <bookmark mark='a'/> Monotonicity: if "
            "one guess of the future is everywhere better than another, the operator's answers keep that order. "
            "A better future never makes today worse. <bookmark mark='b'/> Discounting: add the same amount to "
            "every future value, and today's value rises by only beta times that amount. <bookmark mark='c'/> "
            "Both are checked here on random guesses: the order is kept, and the discounting holds to the last "
            "digits a computer carries. <bookmark mark='d'/> Together they make T a contraction with modulus beta, "
            "so the value function exists, is unique, and iteration finds it. The rest of this part is about doing "
            "that fast, and accurately."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rows[0][:3], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(rows[1][:3], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(rows[0][3]), FadeIn(rows[1][3]))
            vo.wait_until("d")
            self.play(FadeIn(foot, shift=UP * 0.1))
        self.clear_scene()
