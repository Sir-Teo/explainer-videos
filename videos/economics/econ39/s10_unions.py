from __future__ import annotations

from videos.economics.econ39.common import *  # noqa: F403


class Unions(VoiceoverScene):
    def construct(self):
        card(self, 8, r"Unions", r"What do unions do to pay?", "Chapter eight. Unions.",
             lit={1984: r"Freeman and Medoff", 1998: r"Vella and Verbeek"}, scale=("firm", "nation"),
             horizon=("a decade",))
        self.decline()
        self.premium()
        self.compression()

    def decline(self):
        U = load("unions")
        B = U["bls"]
        rows = [(r"all wage and salary workers, \ 1983", B["y1983"], UNION),
                (r"all wage and salary workers, \ 2024", B["y2024"], UNION),
                (r"the public sector, \ 2024", B["public"], GREY_B),
                (r"the private sector, \ 2024", B["private"], GREY_B)]
        bars = VGroup()
        for k, (nm, v, col) in enumerate(rows):
            y = 1.5 - 1.0 * k
            r = Rectangle(width=v * 0.2, height=0.5, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                np.array([-0.6 + v * 0.1, y, 0]))
            bars.add(VGroup(label(nm, font_size=19, color=WHITE).next_to(np.array([-0.7, y, 0]), LEFT, buff=0.1),
                            r, label(f"{v}\\%", font_size=19, color=WHITE).next_to(r, RIGHT, buff=0.12)))
        head = label(r"union members, \ percent of employees", font_size=26, color=E.ACCENT).to_edge(UP, buff=0.7)
        tag = published_tag(tables.UNIONS.tag, corner=DR, font_size=12)
        with self.voiceover(
            "Unions bargain for a whole workplace at once, and they have been shrinking. <bookmark mark='a'/> In "
            f"1983, the first year of comparable figures, {B['y1983']} percent of American employees belonged to "
            f"a union. <bookmark mark='b'/> By 2024, {B['y2024']} percent. <bookmark mark='c'/> What remains is "
            f"mostly in government, where {B['public']} percent belong; <bookmark mark='d'/> in private firms, "
            f"{B['private']} percent. What did their decline do to the wage structure?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, b_ in zip("abcd", bars):
                vo.wait_until(mk)
                self.play(FadeIn(b_, shift=RIGHT * 0.1))
        self.clear_scene()

    def premium(self):
        U = load("unions")
        rows = [(r"raw difference", U["raw"], None, GREY_B),
                (r"least squares, \ with controls", U["pooled"], U["pooled_se"], UNION),
                (r"the same men, \ in and out of unions", U["fe"], U["fe_se"], GAIN)]
        bars = VGroup()
        for k, (nm, v, se, col) in enumerate(rows):
            y = 0.9 - 1.1 * k
            r = Rectangle(width=v * 20, height=0.5, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                np.array([-0.4 + v * 10, y, 0]))
            xend = -0.4 + (v + 1.96 * (se or 0)) * 20 if se else -0.4 + v * 20
            g = VGroup(label(nm, font_size=19, color=col).next_to(np.array([-0.5, y, 0]), LEFT, buff=0.1), r,
                       label(f"{v:.3f}", font_size=19, color=WHITE).next_to(np.array([xend, y, 0]), RIGHT, buff=0.2))
            if se:
                g.add(Line(np.array([-0.4 + (v - 1.96 * se) * 20, y, 0]), np.array([-0.4 + (v + 1.96 * se) * 20, y, 0]),
                           color=WHITE, stroke_width=2))
            bars.add(g)
        head = label(rf"the union wage premium: \ {U['n_men']} young men, \ 1980--87", font_size=24,
                     color=E.ACCENT).to_edge(UP, buff=0.7)
        foot = label(r"log points; \ the line is a 95\% interval", font_size=17, color=GREY_A).to_edge(DOWN,
                                                                                                 buff=0.6)
        tag = data_tag(r"Vella and Verbeek's panel, \ via Wooldridge's data; \ recomputed", corner=DR, font_size=12)
        with self.voiceover(
            "First, the premium. Here are 545 young American men followed from 1980 to 1987, about a quarter of them "
            "in a union in any year. <bookmark mark='a'/> Union members earned about "
            f"{say_pct(np.expm1(U['raw']), 0)} more. <bookmark mark='b'/> Controlling for schooling, experience, "
            f"marriage and race leaves the gap at {U['pooled']:.2f} log points. <bookmark mark='c'/> But union jobs "
            "may go to different kinds of men. So compare each man with himself, in the years he was in a union "
            f"and the years he was not. The premium falls to {U['fe']:.2f}, with a standard error of "
            f"{U['fe_se']:.2f}: still about eight percent, but less than half the cross-sectional gap. Much of the "
            "raw gap was who joins, not what the union does."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(foot))
            for mk, b_ in zip("abc", bars):
                vo.wait_until(mk)
                self.play(FadeIn(b_, shift=RIGHT * 0.1))
        self.clear_scene()

    def compression(self):
        U = load("unions")
        g = np.array(U["grid"])
        ax = plane([0, 3.6], [0, 1.2], center=LEFT * 2.2 + DOWN * 0.4, x_length=7.4, y_length=4.6,
                   xticks=[0, 1, 2, 3], yticks=[0, 0.5, 1.0], xlabel=r"log hourly wage, \ 1985",
                   ylabel=r"density", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}", font_size=14)
        du = path(ax, g, U["dens"]["union"], UNION, 3.2)
        dn = path(ax, g, U["dens"]["non"], GREY_B, 3.0)
        c78, c85 = U["cps"]["78"], U["cps"]["85"]
        side = VGroup(
            label(rf"union: \ spread (s.d.) {c85['sd_union']:.2f}", font_size=19, color=UNION),
            label(rf"non-union: \ spread {c85['sd_non']:.2f}", font_size=19, color=GREY_B),
            label(r"unions compress pay: \\ standard rates, \ seniority \\ scales, \ smaller gaps \\ by schooling",
                  font_size=17, color=WHITE),
            label(r"as unions shrank, \\ that compression faded", font_size=17, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        tag = data_tag(r"Current Population Survey, \ 1978 and 1985, \ via Wooldridge's data", corner=DR,
                       font_size=12)
        with self.voiceover(
            "Unions also change the shape of pay. In a 1985 sample from the Current Population Survey, "
            "<bookmark mark='a'/> the log wages of non-union workers spread widely, <bookmark mark='b'/> while "
            "union members' are bunched together: a standard deviation of "
            f"{c85['sd_union']:.2f} against {c85['sd_non']:.2f}. <bookmark mark='c'/> Contracts set standard rates "
            "for jobs and seniority scales, and narrow the gaps by schooling and skill. In these data the union "
            f"premium was about {c85['premium']:.2f} log points in both 1978 and 1985, while the union share of the "
            f"sample fell from {100 * c78['share']:.0f} to {100 * c85['share']:.0f} percent. <bookmark mark='d'/> "
            "With fewer workers covered, less of the labour market is compressed: studies attribute a real part "
            "of the rise in men's wage inequality since the 1970s to the decline of unions."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(dn), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(du), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
