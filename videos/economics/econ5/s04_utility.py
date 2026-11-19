from __future__ import annotations

from videos.economics.econ5.common import *  # noqa: F403


class Utility(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Utility as a label", r"If utility cannot be measured, what is the number for?",
             "Chapter three. Utility as a label.")
        self.labels()
        self.lexicographic()
        self.mrs()

    def labels(self):
        ax = goods_axes(center=LEFT * 2.9 + DOWN * 0.2, top=10, ticks=(0, 2, 4, 6, 8, 10))
        a = ax.ax
        cd = cs.Preference("cobb-douglas", a=0.5)
        xs = np.linspace(0.3, 10, 300)
        levels = (2.0, 4.0, 6.0)
        curves = VGroup(*[curve(ax, xs, cd.indifference(lv, xs), color=IC, top=10) for lv in levels])
        tags = {}
        for name, f in (("u", lambda v: v * v), ("v", lambda v: 2 * np.log(v)), ("w", lambda v: v ** 6)):
            g = VGroup()
            for lv, c_ in zip(levels, curves):
                x_at = 9.0
                y_at = float(cd.indifference(lv, [x_at])[0])
                val = f(lv)
                txt = f"{val:.0f}" if abs(val) >= 10 or name != "v" else f"{val:.2f}"
                g.add(label(txt, font_size=22, color=E.ACCENT).next_to(a.c2p(x_at, y_at), UR, buff=0.05))
            tags[name] = g
        forms = VGroup(
            MathTex(r"u = x\,y", font_size=36),
            MathTex(r"v = \log x + \log y", font_size=36),
            MathTex(r"w = (x\,y)^3", font_size=36),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        rows = VGroup(
            label(r"Debreu (1954): \ a complete, transitive, \\ continuous ranking has a utility function",
                  font_size=23, color=E.ACCENT),
            forms,
            label(r"three functions, \ one map of curves: \\ the same tastes", font_size=24, color=IC),
            label(r"only the order of the numbers means anything", font_size=24, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.5)
        tag = published_tag(r"G.\ Debreu, in Thrall, Coombs and Davis, eds., \emph{Decision Processes} (1954)",
                            corner=DR, font_size=13)
        with self.voiceover(
            "If tastes are only a ranking, what is utility? <bookmark mark='a'/> In 1954 Gérard Debreu proved that "
            "a complete, transitive and continuous ranking can always be described by a number: a utility function "
            "that gives better bundles bigger numbers. <bookmark mark='b'/> Here is one person's map of indifference "
            "curves, labelled by the product of fish and coconuts: four, sixteen, thirty-six. "
            "<bookmark mark='c'/> Label them instead with logarithms, and the numbers change. "
            "<bookmark mark='d'/> Or cube the product, and they change again. <bookmark mark='e'/> But the curves "
            "don't move, and the person chooses exactly the same things. The number is a label. Only its order "
            "means anything: bigger is better, and nothing else. Economists call such utility ordinal."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(Indicate(rows[0], color=E.ACCENT, scale_factor=1.02))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(c_) for c_ in curves], lag_ratio=0.3), FadeIn(tags["u"]), FadeIn(forms[0]))
            vo.wait_until("c")
            self.play(ReplacementTransform(tags["u"], tags["v"]), FadeIn(forms[1]))
            vo.wait_until("d")
            self.play(ReplacementTransform(tags["v"], tags["w"]), FadeIn(forms[2]))
            vo.wait_until("e")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]))
        self.clear_scene()

    def lexicographic(self):
        ax = goods_axes(center=LEFT * 2.9 + DOWN * 0.2, top=10, ticks=(0, 2, 4, 6, 8, 10))
        a = ax.ax
        cols = VGroup()
        for x in (2, 4, 6, 8):
            cols.add(VGroup(*[Dot(a.c2p(x, y), radius=0.05, color=interpolate_color(ManimColor(GREY_D),
                                                                                     ManimColor(E.ACCENT), y / 10))
                              for y in np.linspace(0.3, 9.7, 30)]))
        arrows = VGroup(*[Arrow(a.c2p(x, 9.7), a.c2p(x + 2, 0.3), buff=0.1, color=GREY_C, stroke_width=1.5,
                                max_tip_length_to_length_ratio=0.06) for x in (2, 4, 6)])
        rows = VGroup(
            label(r"the dictionary order: \\ more fish is always better; \\ coconuts only break ties", font_size=24),
            label(r"complete \ and \ transitive", font_size=24, color=PASS),
            label(r"but no two bundles are equally good: \\ no indifference curves at all", font_size=24),
            label(r"every number for $(4, y)$ must sit above \\ every number for $(2, y')$: \ there are not "
                  r"\\ enough numbers for every fish count", font_size=22, color=VIOL),
            label(r"continuity fails: \ no utility function exists", font_size=24, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.45)
        with self.voiceover(
            "Continuity isn't a technicality. Here's a ranking that lacks it. <bookmark mark='a'/> Someone ranks "
            "bundles the way a dictionary ranks words: more fish is always better, however many coconuts it costs, "
            "and coconuts only break ties. <bookmark mark='b'/> That's complete, and transitive. "
            "<bookmark mark='c'/> But no two different bundles are ever equally good, so there are no indifference "
            "curves, only points. <bookmark mark='d'/> Try to number them. Every bundle with four fish needs a "
            "bigger number than every bundle with two, so each count of fish needs its own stretch of numbers, and "
            "the fish counts between two and four need theirs too. There aren't enough numbers to go round. "
            "<bookmark mark='e'/> The lexicographic order has no utility function. Continuity is what rules it "
            "out."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c_) for c_ in cols], lag_ratio=0.3), run_time=1.6)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), LaggedStart(*[GrowArrow(x) for x in arrows], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def mrs(self):
        eqs = VGroup(
            MathTex(r"\text{MRS} = \frac{\partial u/\partial x}{\partial u/\partial y}", font_size=44),
            MathTex(r"u = xy:\quad \frac{y}{x}", font_size=40, color=IC),
            MathTex(r"w = (xy)^3:\quad \frac{3x^2y^3}{3x^3y^2} = \frac{y}{x}", font_size=40, color=IC),
            MathTex(r"\text{at } (4, 2):\ \ \text{give up } \tfrac{1}{2}\ \text{coconut for one more fish}",
                    font_size=36, color=E.ACCENT),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.5)
        rows = VGroup(
            label(r"marginal utilities change with the label; \ their ratio does not", font_size=26, color=WHITE),
            label(r"the ratio is what choices reveal: \ the rate at which a person will trade", font_size=26,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.55)
        with self.voiceover(
            "What survives the relabelling? <bookmark mark='a'/> The marginal rate of substitution: how many "
            "coconuts a person would give up for one more fish, the ratio of the two marginal utilities. "
            "<bookmark mark='b'/> With the product as utility, it's y over x. <bookmark mark='c'/> Cube the product, "
            "and each marginal utility changes, but the threes and the extra powers cancel in the ratio: still y "
            "over x. <bookmark mark='d'/> At four fish and two coconuts, this person would trade half a coconut for "
            "one more fish. <bookmark mark='e'/> That rate of trade is something a choice can reveal. The size of a "
            "marginal utility, by itself, is not."
        ) as vo:
            self.play(Write(eqs[0]))
            for mk, e_ in zip("bcd", eqs[1:]):
                vo.wait_until(mk)
                self.play(Write(e_))
            vo.wait_until("e")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
        self.clear_scene()
