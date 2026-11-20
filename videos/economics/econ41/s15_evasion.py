from __future__ import annotations

from videos.economics.econ41.common import *  # noqa: F403


class Evasion(VoiceoverScene):
    def construct(self):
        card(self, 13, r"Evasion", r"Why do most people pay what they owe?",
             "Chapter thirteen. Evasion.", lit={1972: r"Allingham and Sandmo", 2011: r"Kleven et al."},
             scale=("person", "nation"), horizon=("a year",))
        self.model()
        self.denmark()

    def model(self):
        Ev = load("evasion")
        ax = plane([0, 0.6], [0, 1.05], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.4, y_length=4.6,
                   xticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6], yticks=[0, 0.25, 0.5, 0.75, 1.0],
                   xlabel=r"probability of an audit", ylabel=r"share of income declared",
                   xfmt=lambda v: f"{100 * v:.0f}\\%", yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        ln = path(ax, Ev["p"], Ev["declared"], WORKER, 3.4, smooth=False)
        real = vline(ax, 0.01, 0, 1.05, LOSS)
        rl = label(r"real audit rates: \\ around 1\% or less", font_size=16, color=LOSS).next_to(
            ax.ax.c2p(0.01, 1.0), RIGHT, buff=0.12)
        side = VGroup(
            label(rf"the Island: \ a {100 * Ev['t']:.0f}\% tax, \\ a fine equal to \\ the evaded tax, \\ risk aversion "
                  rf"{Ev['rho']:g}", font_size=17, color=GREY_A),
            label(rf"below {100 * Ev['first']:.0f}\% audits: \\ declare nothing", font_size=19, color=LOSS),
            label(rf"declare everything \\ only at {100 * Ev['full']:.0f}\%", font_size=19, color=WORKER),
            label(r"yet most people \\ pay: \ why?", font_size=20, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "In 1972 Michael Allingham and Agnar Sandmo treated evasion as a gamble. Declare less, and you save the "
            "tax on what you hide; get caught, and you pay it back with a fine. <bookmark mark='a'/> On the Island, "
            f"with a {100 * Ev['t']:.0f} percent tax and a fine equal to the evaded tax, a cautious taxpayer "
            f"declares nothing at all unless the chance of an audit exceeds {100 * Ev['first']:.0f} percent, "
            f"<bookmark mark='b'/> and declares everything only when it reaches {100 * Ev['full']:.0f} percent. "
            "<bookmark mark='c'/> Real audit rates are around one percent or less. <bookmark mark='d'/> By this "
            "model almost everyone should cheat. Most people do not. Why?"
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), Create(ln), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
            vo.wait_until("c")
            self.play(Create(real), FadeIn(rl))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def denmark(self):
        D = tables.EVASION.data
        rows = [(r"income reported \\ by third parties", D["third_party"], WORKER),
                (r"self-reported \\ income", D["self"], LOSS)]
        bars = VGroup()
        for k, (nm, v, col) in enumerate(rows):
            y = 0.7 - 1.5 * k
            w = max(v * 0.15, 0.04)
            r = Rectangle(width=w, height=0.7, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                np.array([-0.6 + w / 2, y, 0]))
            bars.add(VGroup(label(nm, font_size=21, color=WHITE).next_to(np.array([-0.75, y, 0]), LEFT, buff=0.15), r,
                            label(f"{v:g}\\%", font_size=24, color=col).next_to(r, RIGHT, buff=0.15)))
        head = label(r"Denmark, \ 2007--08: \ the share of income evaded", font_size=26, color=E.ACCENT).to_edge(
            UP, buff=0.5)
        sub = label(rf"about {D['n']:,} taxpayers, \ half audited thoroughly at random", font_size=19,
                    color=GREY_A).next_to(head, DOWN, buff=0.2)
        foot = label(r"what works is not fear but information: \ third-party reporting", font_size=21,
                     color=GAIN).to_edge(DOWN, buff=0.8)
        tag = published_tag(tables.EVASION.tag, corner=DR, font_size=10)
        with self.voiceover(
            "In 2007 and 2008 the Danish tax authority, working with Henrik Kleven, Emmanuel Saez and coauthors, "
            f"audited half of about {D['n']:,} randomly chosen taxpayers thoroughly. <bookmark mark='a'/> On income "
            "that employers, banks and others report directly to the tax authority, evasion was "
            f"{D['third_party']} percent. <bookmark mark='b'/> On income that taxpayers report themselves, "
            f"{D['self']} percent. <bookmark mark='c'/> People are not so much unwilling to cheat as unable: when a "
            "third party reports the income, there is nothing to hide. That is why wage earners comply, why the "
            "self-employed are where evasion lives, and why the most effective enforcement is information, not "
            "fines."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub), FadeIn(tag), *[FadeIn(b_[0]) for b_ in bars])
            for mk, b_ in zip("ab", bars):
                vo.wait_until(mk)
                self.play(GrowFromEdge(b_[1], LEFT), FadeIn(b_[2]))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()
