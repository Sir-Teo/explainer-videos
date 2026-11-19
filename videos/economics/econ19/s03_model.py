from __future__ import annotations

from videos.economics.econ19.common import *  # noqa: F403


class Model(VoiceoverScene):
    def construct(self):
        card(self, 2, r"The Malthusian model", r"If more people means less land each, \ and more income means more "
             r"children, \ where does the economy settle?", "Chapter two. The Malthusian model.",
             lit={1798: r"Malthus", 1817: r"Ricardo's rent"}, scale=("household", "nation"), horizon=("a century",))
        self.derive()
        self.trap()
        self.run()

    def derive(self):
        m = load("malthus")
        v = load("vital")
        beta = m["beta"]
        left = plane([0.2, 2.6], [0, 2.4], center=LEFT * 3.5 + DOWN * 0.6, x_length=5.4, y_length=4.2,
                     xticks=[0.5, 1, 1.5, 2, 2.5], yticks=[0, 0.5, 1, 1.5, 2], xlabel=r"population $L$",
                     ylabel=r"income per head $y$", font_size=17)
        Ls = np.linspace(0.25, 2.6, 120)
        curve = path(left, Ls, ml.income(Ls, 1.0, beta=beta), color=GDP, width=4, yr=(0, 2.4))
        eq = MathTex(r"y = A\,\Big(\frac{X}{L}\Big)^{\beta}", font_size=34, color=GDP).next_to(left, UP, buff=0.15)
        right = plane([0.6, 1.6], [20, 50], center=RIGHT * 3.4 + DOWN * 0.6, x_length=5.2, y_length=4.2,
                      xticks=[0.6, 0.8, 1.0, 1.2, 1.4, 1.6], yticks=[20, 30, 40, 50],
                      xlabel=r"income per head $y$", ylabel=r"per 1{,}000 a year", font_size=17)
        bl = path(right, v["y"], v["births"], color=BIRTH, width=4)
        dl = path(right, v["y"], v["deaths"], color=DEATH, width=4)
        lb = VGroup(label(r"births", font_size=19, color=BIRTH).next_to(right.ax.c2p(1.55, v["births"][-6]), UP,
                                                                         buff=0.1),
                    label(r"deaths", font_size=19, color=DEATH).next_to(right.ax.c2p(1.55, v["deaths"][-6]), DOWN,
                                                                        buff=0.1))
        sub = VGroup(DashedLine(right.ax.c2p(1.0, 20), right.ax.c2p(1.0, 50), color=E.ACCENT, stroke_width=2),
                     label(r"subsistence $\bar y$", font_size=18, color=E.ACCENT).next_to(right.ax.c2p(1.0, 50), UP,
                                                                                            buff=0.06))
        tag = published_tag(r"Malthus (1798); \ Ricardo, \emph{Principles} (1817), ch.\ 2", corner=DR, font_size=13)
        with self.voiceover(
            "The model has two parts. <bookmark mark='a'/> The first is diminishing returns. Land is fixed. Put more "
            "people to work on it, and each produces less: income per head, y, equals technology A times land per "
            f"person to a power beta, here {beta:g}. <bookmark mark='b'/> So the more people, the lower the income "
            "of each: the curve slopes down. <bookmark mark='c'/> The second part is people. When income per head is "
            "high, people marry earlier, more children survive, and fewer people die: births rise with income and "
            "deaths fall. <bookmark mark='d'/> At one income they balance. Call it subsistence: not starvation, but "
            "the standard of living at which the population just replaces itself."
        ) as vo:
            self.play(FadeIn(left), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(eq))
            vo.wait_until("b")
            self.play(Create(curve), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(right), Create(bl), Create(dl), FadeIn(lb), run_time=2)
            vo.wait_until("d")
            self.play(Create(sub[0]), FadeIn(sub[1]))
        self.clear_scene()

    def trap(self):
        m = load("malthus")
        beta = m["beta"]
        ax = plane([0.2, 2.6], [0, 2.4], center=LEFT * 1.6 + DOWN * 0.5, x_length=7.4, y_length=4.8,
                   xticks=[0.5, 1, 1.5, 2, 2.5], yticks=[0, 0.5, 1, 1.5, 2], xlabel=r"population $L$",
                   ylabel=r"income per head $y$", font_size=17)
        Ls = np.linspace(0.25, 2.6, 120)
        c1 = path(ax, Ls, ml.income(Ls, 1.0, beta=beta), color=GDP, width=4, yr=(0, 2.4))
        sub = VGroup(DashedLine(ax.ax.c2p(0.2, 1.0), ax.ax.c2p(2.6, 1.0), color=E.ACCENT, stroke_width=2),
                     label(r"subsistence", font_size=18, color=E.ACCENT).next_to(ax.ax.c2p(2.6, 1.0), RIGHT, buff=0.1))
        star = Dot(ax.ax.c2p(1.0, 1.0), radius=0.1, color=WHITE)
        hi = Dot(ax.ax.c2p(0.55, float(ml.income(0.55, beta=beta))), radius=0.09, color=BIRTH)
        lo = Dot(ax.ax.c2p(1.8, float(ml.income(1.8, beta=beta))), radius=0.09, color=DEATH)
        a_hi = Arrow(hi.get_center(), ax.ax.c2p(0.95, float(ml.income(0.95, beta=beta))), buff=0.15, color=BIRTH)
        a_lo = Arrow(lo.get_center(), ax.ax.c2p(1.08, float(ml.income(1.08, beta=beta))), buff=0.15, color=DEATH)
        A2 = 1.0 + m["invention"][1]
        c2 = path(ax, Ls, ml.income(Ls, A2, beta=beta), color=TECH, width=4, yr=(0, 2.4))
        star2 = Dot(ax.ax.c2p(m["L_star_after"], 1.0), radius=0.1, color=TECH)
        rows = VGroup(
            label(r"above subsistence: \ births exceed deaths, \ $L$ grows, \ $y$ falls", font_size=20, color=BIRTH),
            label(r"below: \ deaths exceed births, \ $L$ shrinks, \ $y$ rises", font_size=20, color=DEATH),
            label(r"a stable point: \ the Malthusian trap", font_size=22, color=E.ACCENT),
            label(rf"better technology: \ the curve shifts up, \ but the economy settles at the same $y$ with "
                  rf"{m['L_star_after']:.2f} \ times the people", font_size=20, color=TECH),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.3).shift(UP * 1.2)
        for r in rows:
            if r.width > 4.6:
                r.width = 4.6
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.3).shift(UP * 1.3)
        with self.voiceover(
            "Put the two parts together. <bookmark mark='a'/> If income is above subsistence, births exceed "
            "deaths, the population grows, and with less land each, income falls. <bookmark mark='b'/> If income is "
            "below, deaths exceed births, the population shrinks, and income rises. <bookmark mark='c'/> Either way "
            "the economy returns to the point where income is at subsistence. It is a stable point: the Malthusian "
            "trap. <bookmark mark='d'/> Now invent a better plough, raising A by half. The curve shifts up, and for "
            "a while everyone is richer. But the population grows until income is back at subsistence, with "
            f"{m['L_star_after']:.2f} times as many people. Technology buys people, not income."
        ) as vo:
            self.play(FadeIn(ax), Create(c1), Create(sub[0]), FadeIn(sub[1]), FadeIn(star))
            vo.wait_until("a")
            self.play(FadeIn(hi), GrowArrow(a_hi), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(lo), GrowArrow(a_lo), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Indicate(star, color=E.ACCENT, scale_factor=1.6))
            vo.wait_until("d")
            self.play(Create(c2), FadeIn(rows[3]), run_time=1.5)
            self.play(FadeIn(star2), star.animate.set_opacity(0.4))
        self.clear_scene()

    def run(self):
        m = load("malthus")
        t, y, L = np.array(m["year"], float), np.array(m["y"]), np.array(m["L"])
        top = plane([0, 400], [0.8, 1.7], center=UP * 1.35 + LEFT * 0.6, x_length=10.6, y_length=2.3,
                    xticks=[0, 100, 200, 300, 400], yticks=[1.0, 1.25, 1.5], ylabel=r"income per head",
                    font_size=16)
        bot = plane([0, 400], [0, 2.2], center=DOWN * 1.85 + LEFT * 0.6, x_length=10.6, y_length=2.3,
                    xticks=[0, 100, 200, 300, 400], yticks=[0, 1, 2], xlabel=r"year on the island",
                    ylabel=r"population", font_size=16)
        cy = path(top, t, y, color=GDP, width=3.5, smooth=False)
        cL = path(bot, t, L, color=POP, width=3.5, smooth=False)
        pl, inv = m["plague"], m["invention"]
        marks = VGroup(
            label(rf"year {pl[0]}: \ a plague kills {100 * pl[1]:.0f}\%", font_size=18, color=DEATH).move_to(
                top.ax.c2p(pl[0] + 45, 1.62)),
            label(rf"year {inv[0]}: \ a better plough, \ $A$ \ $+{100 * inv[1]:.0f}\%$", font_size=18,
                  color=TECH).move_to(top.ax.c2p(inv[0] + 70, 1.62)),
        )
        lines = VGroup(*[DashedLine(top.ax.c2p(x, 0.8), top.ax.c2p(x, 1.55), color=c, stroke_width=1.5)
                         for x, c in ((pl[0], DEATH), (inv[0], TECH))])
        tag = agora_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Agora runs it. The island starts in its trap: income at subsistence, the population steady. "
            f"<bookmark mark='a'/> In year {pl[0]} a plague kills {100 * pl[1]:.0f} percent of the islanders. The "
            f"survivors have more land each, and income per head jumps by {100 * (m['jump_y'] - 1):.0f} percent. "
            "<bookmark mark='b'/> Then, slowly, the population recovers, and income falls back: half the gap closes "
            f"in about {m['half_life']:.0f} years. <bookmark mark='c'/> In year {inv[0]} a better plough raises "
            f"output by half. Income jumps by {100 * (m['jump_y_invention'] - 1):.0f} percent, and again drifts back, "
            "while the population climbs towards almost twice its old size. <bookmark mark='d'/> In this world "
            "nothing that happens to technology or to death can raise living standards for good. Only fewer births "
            "could, which is why, in later editions, Malthus urged what he called moral restraint: marrying later."
        ) as vo:
            self.play(FadeIn(top), FadeIn(bot), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(marks[0]), Create(lines[0]))
            vo.wait_until("b")
            self.play(Create(cy), Create(cL), run_time=6, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(marks[1]), Create(lines[1]))
            vo.wait_until("d")
            self.play(Indicate(marks[1], color=WHITE, scale_factor=1.05))
        self.clear_scene()
