from __future__ import annotations

from videos.economics.econ63.common import *  # noqa: F403

SQ = [np.array([-0.6, 0.6, 0]), np.array([0.6, 0.6, 0]), np.array([0.6, -0.6, 0]), np.array([-0.6, -0.6, 0])]


def four(edges, color=LINK, center=ORIGIN, hub=None):
    pts = [p + center for p in SQ]
    if hub is not None:
        pts = [center + np.array([0, 0, 0])] + [center + 0.85 * np.array([np.cos(a), np.sin(a), 0])
                                               for a in (PI / 2, PI / 2 + 2 * PI / 3, PI / 2 + 4 * PI / 3)]
    lines = VGroup(*[Line(pts[i], pts[j], stroke_width=2.4, color=color) for i, j in edges])
    dots = VGroup(*[Dot(p, radius=0.09, color=SEED if (hub is not None and k == 0) else PEOPLE)
                    for k, p in enumerate(pts)])
    return VGroup(lines, dots)


class Formation(VoiceoverScene):
    def construct(self):
        card(self, 12, r"Network formation", r"If people choose their own links, \ do they build the network a "
             r"planner would choose?", "Chapter twelve. Network formation.", lit={1996: r"Jackson and Wolinsky"},
             scale=("person", "firm"), horizon=("a year",))
        self.rules()
        self.costs()

    def rules(self):
        comp = four([(0, 1), (1, 2), (2, 3), (3, 0), (0, 2), (1, 3)], center=LEFT * 4.4 + DOWN * 0.4)
        star = four([(0, 1), (0, 2), (0, 3)], center=DOWN * 0.4, hub=True)
        empty = four([], center=RIGHT * 4.4 + DOWN * 0.4)
        names = VGroup(label(r"complete: \ 6 links", font_size=20, color=LINK).next_to(comp, DOWN, buff=0.35),
                       label(r"star: \ 3 links", font_size=20, color=SEED).next_to(star, DOWN, buff=0.35),
                       label(r"empty", font_size=20, color=GREY_B).next_to(empty, DOWN, buff=0.35))
        rule = VGroup(
            label(r"each player gains $\delta^{d}$ from every player $d$ links away, \ and pays $c$ for each of its "
                  r"own links", font_size=22, color=WHITE),
            label(r"$\delta = 0.6$: \ a friend is worth 0.6, \ a friend of a friend 0.36", font_size=20,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.25)
        head = label(r"suppliers, \ counterparties, \ friends: \ links chosen one pair at a time", font_size=28,
                     color=E.ACCENT)
        VGroup(head, rule).arrange(DOWN, buff=0.4).to_edge(UP, buff=0.45)
        tag = published_tag(r"Jackson and Wolinsky, \ Journal of Economic Theory 71(1) (1996)", corner=DL,
                            font_size=12)
        with self.voiceover(
            "So far the network was given. But firms choose their suppliers, banks their counterparties, people "
            "their friends. Matthew Jackson and Asher Wolinsky asked whether the network they build is the one a "
            "planner would build. <bookmark mark='a'/> Their connections model: each player gains something from "
            "every other player it is connected to, directly or indirectly, delta for a direct link, delta squared "
            "at two steps, and so on; and each pays a cost c for every link of its own. <bookmark mark='b'/> With "
            "delta at 0.6, a friend is worth 0.6, a friend of a friend 0.36. <bookmark mark='c'/> With four "
            "players, three shapes matter: everyone linked to everyone, a star, and no links at all."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(head, shift=DOWN * 0.1))
            vo.wait_until("a")
            self.play(FadeIn(rule[0]))
            vo.wait_until("b")
            self.play(FadeIn(rule[1]))
            vo.wait_until("c")
            self.play(FadeIn(comp), FadeIn(star), FadeIn(empty), FadeIn(names))
        self.clear_scene()

    def costs(self):
        F = load("formation")
        rows = F["rows"]
        c = np.array([r["c"] for r in rows])
        ax = plane([0, 1.2], [-1, 6], center=UP * 0.8 + LEFT * 0.7, x_length=7.4, y_length=3.8,
                   xticks=[0, 0.24, 0.6, 0.96, 1.2], yticks=[0, 2, 4, 6], xlabel=r"cost of a link, \ $c$",
                   ylabel=r"total payoff of all four", xfmt=lambda v: f"{v:.2f}", yfmt=lambda v: f"{v:.0f}",
                   font_size=14)
        lc = path(ax, c, [r["complete_value"] for r in rows], LINK, 3.2, yr=(-1, 6), smooth=False)
        ls = path(ax, c, [r["star_value"] for r in rows], SEED, 3.2, yr=(-1, 6), smooth=False)
        le = path(ax, c, [0.0 for _ in rows], GREY_B, 3.2, smooth=False)

        def strip(flags, y, color):
            g = VGroup()
            for r, f in zip(rows, flags):
                if f:
                    p0, p1 = ax.ax.c2p(r["c"] - 0.0125, y - 0.25), ax.ax.c2p(r["c"] + 0.0125, y + 0.25)
                    g.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], fill_color=color, fill_opacity=0.8,
                                    stroke_width=0).move_to((p0 + p1) / 2))
            return g
        y0 = -3.6
        eff = VGroup(strip([r["efficient_links"] == 6 for r in rows], y0, LINK),
                     strip([r["efficient_links"] == 3 for r in rows], y0, SEED),
                     strip([r["efficient_links"] == 0 for r in rows], y0, GREY_B))
        stab = VGroup(strip([r["complete_stable"] for r in rows], y0 - 0.8, LINK),
                      strip([r["star_stable"] for r in rows], y0 - 0.8, SEED))
        el = label(r"efficient", font_size=17, color=WHITE).next_to(ax.ax.c2p(0, y0), LEFT, buff=0.2)
        sl = label(r"pairwise stable", font_size=17, color=WHITE).next_to(ax.ax.c2p(0, y0 - 0.8), LEFT, buff=0.2)
        gap = shade(ax, [(0.6, 0.96)], y0 - 1.2, 6, SHOCK, 0.12)
        side = VGroup(
            label(r"cheap links: \ everyone links, \ efficiently", font_size=18, color=LINK),
            label(r"dearer: \ the star is best \\ and stable while $c < \delta$", font_size=18, color=SEED),
            label(r"$\delta < c < \delta + \delta^2$: \\ the star is best, \\ but the hub cuts its links", font_size=18,
                  color=SHOCK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = island_tag(r"computed: \ every network of four players; \ agora.network.formation", corner=DL,
                         font_size=12)
        with self.voiceover(
            "Now vary the cost of a link and ask two questions. Which network gives the most in total? And which "
            "would survive, if any two players could add a link they both want, and anyone could cut one of their "
            "own? <bookmark mark='a'/> When links are cheap, below delta minus delta squared, everyone linked to "
            "everyone is best, and nobody wants to cut a link. <bookmark mark='b'/> When links cost more, the star "
            "is best: everyone reaches everyone in two steps with only three links. And while the cost is below "
            "delta, it is stable too. <bookmark mark='c'/> But between delta and delta plus delta squared, the "
            "star is still the best network, and it does not survive. The hub pays for three links whose benefit "
            "goes mostly to the others: each leaf reaches the other two through the hub. So the hub cuts them. "
            "<bookmark mark='d'/> The efficient network exists, and nobody wants to be its centre. That is the "
            "tension in every network built by choice, from supply chains to friendships: links create value for "
            "people who do not pay for them, and the fix is to pay the centre."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(lc), Create(ls), Create(le), FadeIn(el), FadeIn(sl))
            vo.wait_until("a")
            self.play(FadeIn(eff[0]), FadeIn(stab[0]), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(eff[1]), FadeIn(stab[1]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(gap), FadeIn(side[2]), FadeIn(eff[2]))
            vo.wait_until("d")
            self.play(Indicate(gap, color=SHOCK, scale_factor=1.0))
        self.clear_scene()
