from __future__ import annotations

from videos.economics.econ8.common import *  # noqa: F403

RTS_COLOR = {"decreasing (0.75)": CAP, "constant (1.0)": OUT, "increasing (1.2)": LAB}


class Scale(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Returns to scale", r"What happens when a firm doubles everything?", "Chapter three. Returns "
             r"to scale.", lit={1949: r"Chenery's pipelines"}, scale=("firm", "market"))
        self.doubling()
        self.pipeline()
        self.limits()

    def doubling(self):
        s = load("scale")
        ts = np.array(s["ts"])
        ax = plane([1, 4], [0, 60], center=LEFT * 3.6 + DOWN * 0.3, x_length=5.6, y_length=5.0,
                   xticks=[1, 2, 3, 4], yticks=[0, 20, 40, 60], xlabel=r"inputs, \ as a multiple of (4, 4)",
                   ylabel=r"boats a month", font_size=17, xfmt=lambda v: rf"\times {v:.0f}")
        curves, labs = VGroup(), VGroup()
        for k, vals in s["rows"].items():
            col = RTS_COLOR[k]
            curves.add(VMobject(stroke_color=col, stroke_width=3.5).set_points_smoothly(
                [ax.ax.c2p(t, v) for t, v in zip(np.linspace(1, 4, 4), vals)]))
            labs.add(label(rf"{k}: \ $\times${vals[1] / vals[0]:.2f} when doubled", font_size=20, color=col))
        labs.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        rule = VGroup(
            MathTex(r"q(tK, tL) = t^{\,a+b}\, q(K, L)", font_size=38),
            label(r"$a + b < 1$: \ decreasing; \ $= 1$: \ constant; \\ $a + b > 1$: \ increasing", font_size=22,
                  color=GREY_A),
            label(r"the yard: \ $0.25 + 0.5 = 0.75$, \ decreasing", font_size=23, color=CAP),
            label(r"not diminishing returns: \ here \emph{everything} grows", font_size=22, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        side = VGroup(labs, rule).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        if side.width > 6.2:
            side.scale_to_fit_width(6.2)
        side.to_edge(RIGHT, buff=0.35).shift(DOWN * 0.2)
        with self.voiceover(
            "Diminishing returns hold one input fixed. Returns to scale ask what happens when the firm grows in every "
            "dimension at once. <bookmark mark='a'/> Multiply every input by t. If output rises by t to the power "
            "of the sum of the exponents, the technology has decreasing, constant or increasing returns as that sum "
            "is below, equal to or above one. <bookmark mark='b'/> Crusoe's yard has decreasing returns: double its "
            "slipways and its shipwrights and output rises by a factor of one point six eight. "
            "<bookmark mark='c'/> With constant returns it would double; with increasing returns, here one point two, "
            "it would rise two point three times. <bookmark mark='d'/> Don't confuse this with diminishing returns: "
            "that was about adding workers to fixed slipways. This is about the whole yard."
        ) as vo:
            self.play(FadeIn(ax))
            vo.wait_until("a")
            self.play(FadeIn(rule[0]), FadeIn(rule[1]))
            vo.wait_until("b")
            self.play(Create(curves[0]), FadeIn(labs[0]), FadeIn(rule[2]))
            vo.wait_until("c")
            self.play(Create(curves[1]), FadeIn(labs[1]), Create(curves[2]), FadeIn(labs[2]))
            vo.wait_until("d")
            self.play(FadeIn(rule[3]))
        self.clear_scene()

    def pipeline(self):
        s = load("scale")
        small = Circle(radius=0.55, stroke_color=CAP, stroke_width=6, fill_color=LAB, fill_opacity=0.35)
        large = Circle(radius=1.1, stroke_color=CAP, stroke_width=6, fill_color=LAB, fill_opacity=0.35)
        pipes = VGroup(small, large).arrange(RIGHT, buff=1.2).to_edge(LEFT, buff=1.0).shift(UP * 1.3)
        cap_l = VGroup(label(r"diameter $d$", font_size=21).next_to(small, DOWN, buff=0.2),
                       label(r"diameter $2d$", font_size=21).next_to(large, DOWN, buff=0.2))
        facts = VGroup(
            label(r"steel: \ the circumference, \ $\propto d$", font_size=25, color=CAP),
            label(r"capacity: \ the cross-section, \ $\propto d^{2}$", font_size=25, color=LAB),
            label(r"double the diameter: \ twice the steel, \\ four times the capacity", font_size=25),
            label(r"cost $\propto$ capacity$^{1/2}$: \ increasing returns, \\ from geometry", font_size=25,
                  color=OUT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.5).shift(UP * 1.0)
        ax = plane([0, 100], [0, 100], center=LEFT * 3.4 + DOWN * 2.1, x_length=4.6, y_length=2.4,
                   xticks=[0, 50, 100], yticks=[0, 50, 100], xlabel=r"capacity", ylabel=r"cost", font_size=14)
        cap = np.array(s["cap"])
        lin = path(ax, cap, cap, color=GREY_B, width=2)
        six = path(ax, cap, 100 * (cap / 100) ** 0.6, color=OUT, width=3)
        foot = VGroup(
            label(r"chemical engineers' six-tenths rule: \\ plant cost $\propto$ capacity$^{0.6}$ (Williams, 1947)",
                  font_size=21, color=OUT),
            label(r"Chenery (1949): \ production functions \\ built from engineering, \ gas pipelines first",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(ax, RIGHT, buff=0.6).shift(UP * 0.1)
        tag = illustrative_tag(r"geometry; \ the rule as engineers state it", corner=DR, font_size=14)
        with self.voiceover(
            "Where do increasing returns come from? Often from geometry. <bookmark mark='a'/> Take a pipeline. The "
            "steel it needs goes with the pipe's circumference, proportional to its diameter. <bookmark mark='b'/> "
            "What it can carry goes with its cross-section, proportional to the diameter squared. "
            "<bookmark mark='c'/> Double the diameter and you use twice the steel to carry four times as much: cost "
            "rises with the square root of capacity. <bookmark mark='d'/> Tanks, boilers and reactors work the same "
            "way, surface against volume, and chemical engineers have a rule of thumb for it, the six-tenths rule, "
            "published in 1947: a plant's cost rises with its capacity to the power nought point six. In 1949 Hollis "
            "Chenery built economic production functions directly from such engineering relations, starting with "
            "natural gas pipelines."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(pipes[0]), FadeIn(cap_l[0]))
            vo.wait_until("a")
            self.play(FadeIn(facts[0]), Indicate(small, color=CAP))
            vo.wait_until("b")
            self.play(FadeIn(facts[1]), FadeIn(pipes[1]), FadeIn(cap_l[1]))
            vo.wait_until("c")
            self.play(FadeIn(facts[2]), FadeIn(facts[3]))
            vo.wait_until("d")
            self.play(FadeIn(ax), Create(lin), Create(six), FadeIn(foot))
        self.clear_scene()

    def limits(self):
        rows = VGroup(
            label(r"if bigger is cheaper, \ why isn't every industry one firm?", font_size=32, color=E.ACCENT),
            label(r"some inputs don't scale: \ management, \ attention, \ the founder's time", font_size=27),
            label(r"transport and demand: \ a boatyard serves one coast", font_size=27),
            label(r"returns can be increasing for a plant \\ and decreasing for a firm that runs many", font_size=27),
            label(r"Coase's answer, \ chapter 10: \ organizing inside a firm has costs too, \\ and they rise with its "
                  r"size", font_size=25, color=FIRM),
        ).arrange(DOWN, buff=0.4)
        with self.voiceover(
            "That raises an obvious question. <bookmark mark='a'/> If bigger is cheaper, why isn't every industry a "
            "single firm? <bookmark mark='b'/> Partly because some inputs don't scale: management, attention, the "
            "founder's own time. <bookmark mark='c'/> Partly because of transport costs and the size of the market: a "
            "boatyard serves one stretch of coast. <bookmark mark='d'/> A plant can have increasing returns while a "
            "firm running many plants has decreasing ones. <bookmark mark='e'/> Coase's answer, in chapter ten, is "
            "that organizing things inside a firm has costs too, and they rise as the firm grows."
        ) as vo:
            self.play(FadeIn(rows[0], shift=UP * 0.1))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
