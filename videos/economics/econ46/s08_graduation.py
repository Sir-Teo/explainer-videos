from __future__ import annotations

from videos.economics.econ46.common import *  # noqa: F403


class Graduation(VoiceoverScene):
    def construct(self):
        card(self, 7, r"The graduation programme", r"Can one big push lift the very poorest for good?",
             "Chapter seven. The graduation programme.", lit={2015: r"Banerjee et al.", 2022: r"Balboni et al."},
             scale=("household",), horizon=("a decade",))
        self.package()
        self.six()
        self.island()

    def package(self):
        cards = point_cards([
            (r"an asset", r"goats, \ cows, \\ a small shop: \\ a way to earn", POOR),
            (r"training", r"how to keep it \\ alive and earning", SCHOOL),
            (r"support", r"cash or food \\ for the first \\ months", CASH),
            (r"savings", r"an account, \\ and the habit", CREDIT),
            (r"coaching", r"weekly visits \\ for a year \\ or two", HEALTH),
        ], width=13.0, cols=5, font_size=18).move_to(DOWN * 0.2)
        head = label(r"BRAC's package for the ultra-poor", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        foot = label(r"designed in Bangladesh for people too poor to borrow: \ a big push, \ once",
                     font_size=20, color=GREY_A).to_edge(DOWN, buff=0.7)
        tag = published_tag(tables.GRADUATION_2015.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Microcredit did little for the poorest, who had no business to lend to. In Bangladesh the charity BRAC "
            "designed something else for them. <bookmark mark='a'/> A productive asset, goats or a cow or the stock "
            "for a small shop. <bookmark mark='b'/> Training in how to keep it alive and earning. <bookmark "
            "mark='c'/> Cash or food for the first months, so the asset is not sold or eaten. <bookmark mark='d'/> "
            "A savings account. <bookmark mark='e'/> And a coach who visits every week, for a year or two. "
            "<bookmark mark='f'/> It is expensive, and it is meant to happen once: a big push, aimed at exactly the "
            "threshold of chapter three. The name is graduation: from aid, into a livelihood."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cards.cards[0], shift=UP * 0.1))
            vo.wait_until("a")
            self.play(Circumscribe(cards.cards[0], color=WHITE, buff=0.05))
            for mk, c in zip("bcde", cards.cards[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
            vo.wait_until("f")
            self.play(FadeIn(foot))
        self.clear_scene()

    def six(self):
        T = tables.GRADUATION_2015.data
        sites = (("Ethiopia", True), ("Ghana", True), ("Honduras", False), ("India", True), ("Pakistan", True),
                 ("Peru", True))
        tiles = VGroup()
        for nm, up in sites:
            box = RoundedRectangle(width=1.9, height=1.3, corner_radius=0.1, stroke_color=GAIN if up else LOSS,
                                   stroke_width=2.4, fill_color=GAIN if up else LOSS, fill_opacity=0.12)
            t = VGroup(label(nm, font_size=21, color=WHITE),
                       label(r"consumption up" if up else r"no gain", font_size=15, color=GAIN if up else LOSS)
                       ).arrange(DOWN, buff=0.12).move_to(box)
            tiles.add(VGroup(box, t))
        tiles.arrange(RIGHT, buff=0.25).move_to(UP * 0.5)
        rows = VGroup(
            label(rf"six randomized trials, \ about {T['people']:,} people".replace(",", "{,}"), font_size=22,
                  color=TRIAL),
            label(rf"a year after the programme ended: \ consumption higher in {T['consumption_up']} of 6",
                  font_size=22,
                  color=GAIN),
            label(rf"benefits greater than costs in {T['benefits_exceed']} of 6", font_size=22, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(DOWN, buff=0.7)
        head = label(r"Banerjee et al., \ \emph{Science}, \ 2015", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.GRADUATION_2015.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Would it work outside Bangladesh? <bookmark mark='a'/> Abhijit Banerjee, Esther Duflo, Dean Karlan, "
            "Christopher Udry and their coauthors ran the same programme as six randomized trials, in Ethiopia, "
            f"Ghana, Honduras, India, Pakistan and Peru, with about {T['people']:,} people. <bookmark mark='b'/> A "
            f"year after the programme ended, consumption was higher in {T['consumption_up']} of the six sites. "
            "Honduras was the exception. <bookmark mark='c'/> And in "
            f"{T['benefits_exceed']} of the six, the benefits were larger than the costs. A programme designed in "
            "one country, run by different organizations on three continents, mostly worked. That is unusual, and "
            "it is the strongest evidence that, for the very poorest, a large push can do what small help cannot."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), LaggedStart(*[FadeIn(t[0]) for t in tiles], lag_ratio=0.1),
                      run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), LaggedStart(*[FadeIn(t[1][0]) for t in tiles], lag_ratio=0.15))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), LaggedStart(*[FadeIn(t[1][1]) for t in tiles], lag_ratio=0.15))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def island(self):
        G = load("grad")
        after, end = np.array(G["after"]), np.array(G["end"])
        th = G["threshold"]
        ax = plane([5, 40], [-15, 25], center=LEFT * 1.9 + DOWN * 0.35, x_length=8.0, y_length=4.8,
                   xticks=[5, 10, 15, 20, 25, 30, 35, 40], yticks=[-15, -10, -5, 0, 5, 10, 15, 20, 25],
                   xlabel=r"capital just after the transfer", ylabel=r"change in capital over twelve years",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:+.0f}".replace("-", "{-}"), font_size=13)
        zero = DashedLine(ax.ax.c2p(5, 0), ax.ax.c2p(40, 0), color=GREY_B, stroke_width=1.6)
        tl = vline(ax, th, -15, 25, WHITE)
        tlab = label(rf"the threshold, \ {th:.1f}", font_size=15, color=WHITE).next_to(ax.ax.c2p(th, 25), RIGHT,
                                                                                      buff=0.1).shift(DOWN * 0.2)
        d = end - after
        sel = (after >= 5) & (after <= 40) & (d >= -15) & (d <= 25)
        pts = VGroup(*[dot(ax, a, b, ESCAPE if a > th else TRAP, 0.035) for a, b in zip(after[sel], d[sel])])
        med = path(ax, G["mids"], G["gain"], E.ACCENT, 3.4)
        side = VGroup(
            label(r"the Island's households, \\ each given 10", font_size=18, color=WHITE),
            label(r"left of the line: \\ they lose ground", font_size=18, color=TRAP),
            label(r"right of it: \\ they climb, \ slowly \\ at first", font_size=18, color=ESCAPE),
            label(r"gold: \ the median \\ change, \ by capital", font_size=18, color=E.ACCENT),
            label(rf"{100 * G['share_crossed']:.0f}\% pushed across", font_size=18, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "This is how Balboni and her coauthors found their threshold, and it can be done on the Island. "
            "<bookmark mark='a'/> Give every household a transfer of ten. Across, each household's capital just "
            "after the transfer; up the side, how much it changed over the next twelve years. <bookmark mark='b'/> "
            "Households that end up below the threshold lose ground: the transfer is slowly eaten. <bookmark "
            "mark='c'/> Those above it climb, slowly at first, toward the high steady state. <bookmark mark='d'/> The "
            "median change, in gold, crosses zero "
            "near the threshold. In Bangladesh, with real households and real cows, the curve had the same shape. "
            f"<bookmark mark='e'/> Here, {100 * G['share_crossed']:.0f} percent were pushed across. A larger "
            "transfer would push more, which is why the size of the push, not only whether there is one, is the "
            "policy question."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(zero), Create(tl), FadeIn(tlab), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(side[0]), LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.002), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(med), FadeIn(side[3]), run_time=1.5)
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()
