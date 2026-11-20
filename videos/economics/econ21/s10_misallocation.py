from __future__ import annotations

from videos.economics.econ21.common import *  # noqa: F403


class Misallocation(VoiceoverScene):
    def construct(self):
        card(self, 8, r"Misallocation: \ the same inputs, \ less output", r"How much output is lost when capital and "
             r"workers sit in the wrong firms?", "Chapter eight. Misallocation: the same inputs, less output.",
             lit={2009: r"Hsieh and Klenow", 2021: r"Bils, Klenow and Ruane"}, scale=("firm", "nation"),
             horizon=("a year",))
        self.idea()
        self.plants()
        self.dial()

    def idea(self):
        rows = VGroup(
            label(r"in an efficient economy, \ a worker or a machine earns the same extra revenue in every firm",
                  font_size=23, color=GREY_A),
            label(r"if not, \ moving it from a low-return firm to a high-return one raises output for free", font_size=23,
                  color=CONS),
            MathTex(r"\text{TFPR}_i = P_i \times \text{TFPQ}_i \;\propto\; \text{MRPK}_i^{\alpha}\,"
                    r"\text{MRPL}_i^{1-\alpha}", font_size=40),
            label(r"revenue productivity should be equal across firms: \ its spread measures the wedges", font_size=22,
                  color=WEDGE),
            MathTex(r"\ln\frac{\text{TFP}_{\text{efficient}}}{\text{TFP}} \approx \frac{\sigma}{2}\,"
                    r"\operatorname{var}(\ln \text{TFPR})", font_size=42, color=E.ACCENT),
            label(r"(lognormal, \ $\sigma$ the elasticity of substitution between varieties)", font_size=18,
                  color=GREY_B),
        ).arrange(DOWN, buff=0.35).move_to(UP * 0.1)
        tag = published_tag(r"Hsieh and Klenow, QJE 124(4) (2009): \ 1403--1448", corner=DR, font_size=12)
        with self.voiceover(
            "Part nine proved that competitive markets put every resource where it earns the most. "
            "<bookmark mark='a'/> In an efficient economy, an extra worker or an extra machine adds the same revenue "
            "in every firm. <bookmark mark='b'/> If it does not, moving it from a firm where it adds little to one "
            "where it adds a lot raises output with no new inputs at all. <bookmark mark='c'/> Chang-Tai Hsieh and "
            "Peter Klenow turned that into a measure. A firm's revenue productivity, its price times its physical "
            "productivity, is proportional to the marginal revenue products of its capital and labour. "
            "<bookmark mark='d'/> With no distortions it would be the same in every firm. Its spread measures the "
            "wedges: taxes, subsidies, credit and connections that favour some firms over others. "
            "<bookmark mark='e'/> If it is lognormal, the output lost is about sigma over two times its variance."
        ) as vo:
            self.play(FadeIn(tag))
            for mk, r in zip("abcde", rows[:5]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
            self.play(FadeIn(rows[5]))
        self.clear_scene()

    def plants(self):
        p = load("plants")
        lo, hi = p["economies"][p["lo"]], p["economies"][p["hi"]]
        bins = np.linspace(-2.2, 2.2, 45)

        def hist(ax, vals, col):
            h, e = np.histogram(vals, bins=bins, density=True)
            g = VGroup()
            for k, v in enumerate(h):
                x0, x1 = e[k], e[k + 1]
                top = ax.ax.c2p(x0, v)[1]
                base = ax.ax.c2p(x0, 0)[1]
                g.add(Rectangle(width=ax.ax.c2p(x1, 0)[0] - ax.ax.c2p(x0, 0)[0], height=max(top - base, 0.001),
                                stroke_width=0, fill_color=col, fill_opacity=0.7).move_to(
                    [(ax.ax.c2p(x0, 0)[0] + ax.ax.c2p(x1, 0)[0]) / 2, base, 0], aligned_edge=DOWN))
            return g
        a1 = plane([-2.2, 2.2], [0, 1.3], center=LEFT * 3.4 + DOWN * 0.6, x_length=5.6, y_length=3.6,
                   xticks=[-2, -1, 0, 1, 2], yticks=[0, 0.5, 1.0], xlabel=r"log TFPR, \ relative to the mean",
                   xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", font_size=14)
        a2 = plane([-2.2, 2.2], [0, 1.3], center=RIGHT * 3.0 + DOWN * 0.6, x_length=5.6, y_length=3.6,
                   xticks=[-2, -1, 0, 1, 2], yticks=[0, 0.5, 1.0], xlabel=r"log TFPR, \ relative to the mean",
                   xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", font_size=14)
        h1 = hist(a1, lo["log_tfpr"], CONS)
        h2 = hist(a2, hi["log_tfpr"], WEDGE)
        t1 = VGroup(label(rf"island A: \ sd {lo['sd_log_tfpr']:.2f}", font_size=21, color=CONS),
                    label(rf"output lost: \ {pc(lo['gain'], 0)} \ (formula {pc(lo['lognormal'], 0)})", font_size=19,
                          color=GREY_A)).arrange(DOWN, buff=0.1).next_to(a1, UP, buff=0.25)
        t2 = VGroup(label(rf"island B: \ sd {hi['sd_log_tfpr']:.2f}", font_size=21, color=WEDGE),
                    label(rf"output lost: \ {pc(hi['gain'], 0)} \ (formula {pc(hi['lognormal'], 0)})", font_size=19,
                          color=GREY_A)).arrange(DOWN, buff=0.1).next_to(a2, UP, buff=0.25)
        head = label(rf"{commas(p['n'])} plants, \ the same physical productivities, \ two sets of wedges; \ "
                     rf"$\sigma = {p['sigma']:g}$", font_size=21, color=GREY_A).to_edge(UP, buff=0.3)
        tag = agora_tag(corner=DR, font_size=14)
        with self.voiceover(
            f"Agora runs it on the island's factories: {p['n']:,} plants with the same physical productivities in two "
            "economies. Only the wedges differ. <bookmark mark='a'/> In economy A, revenue productivity has a "
            f"standard deviation of about {lo['sd_log_tfpr']:.2f} in logs. Moving labour until revenue products are "
            f"equal would raise output by {100 * lo['gain']:.0f} percent; the formula says "
            f"{100 * lo['lognormal']:.0f}. <bookmark mark='b'/> In economy B the wedges are larger, a standard "
            f"deviation of {hi['sd_log_tfpr']:.2f}, and the loss is {100 * hi['gain']:.0f} percent. Because the "
            "loss grows with the variance of the wedges, a spread less than twice as wide brings a loss more than four "
            "times as large. "
            "<bookmark mark='c'/> Same people, same plants, same technology: very different output."
        ) as vo:
            self.play(FadeIn(head), FadeIn(a1), FadeIn(a2), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(r, DOWN) for r in h1], lag_ratio=0.02), FadeIn(t1), run_time=2)
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(r, DOWN) for r in h2], lag_ratio=0.02), FadeIn(t2), run_time=2)
            vo.wait_until("c")
            self.play(Indicate(t2[1]))
        self.clear_scene()

    def dial(self):
        dial = dials.DIALS["misallocation"]
        rows = VGroup(
            label(r"the misallocation dial \ (opened in Part 9)", font_size=27, color=E.ACCENT),
            *[label(rf"{tex_safe(e.who)} ({e.year}): \ {tex_safe(e.sample)}: \ {e.value:g}\%", font_size=19,
                    color=GREY_A) for e in dial.estimates],
            wrapped_label(tex_safe(dial.meaning), 12.4, 18, HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(UP * 0.1)
        for r in rows[1:-1]:
            if r.width > 12.8:
                r.width = 12.8
        tag = published_tag(r"Hsieh and Klenow (2009), \ table 6; \ Bils, Klenow and Ruane (2021)", corner=DR,
                            font_size=12)
        with self.voiceover(
            "Hsieh and Klenow measured it in the real thing, census data on manufacturing plants. "
            "<bookmark mark='a'/> If China's plants in 2005 had been allocated as efficiently as America's were in "
            "1997, its manufacturing productivity would have been about thirty percent higher; India's, in 1994, "
            "nearly sixty. <bookmark mark='b'/> But measurement error also spreads revenue productivity out, and "
            "Mark Bils, Peter Klenow and Cian Ruane's correction cuts the potential gains substantially, in "
            "America most of all. That is why the dial reads contested. Misallocation is part of the residual, "
            "but how large a part is still argued."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[1:-1]], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(rows[-1]))
        self.clear_scene()
