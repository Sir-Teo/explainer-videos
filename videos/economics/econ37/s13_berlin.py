from __future__ import annotations

from videos.economics.econ37.common import *  # noqa: F403

EAST = "#E8A0B4"
WEST = "#7EC8F5"


class Berlin(VoiceoverScene):
    def construct(self):
        card(self, 11, r"The Berlin Wall as an experiment", r"How strong are the forces that hold a city together?",
             "Chapter eleven. The Berlin Wall as an experiment.",
             lit={1961: r"the Wall", 1989: r"the Wall falls", 2015: r"Ahlfeldt, \ Redding, \ Sturm and Wolf"},
             scale=("firm", "city"), horizon=("a century",))
        self.history()
        self.jobs()
        self.prices()

    def history(self):
        R = load("berlin")["arsw"]
        cards = point_cards([
            (r"1936", r"one city; \\ its business centre \\ in Mitte", WHITE),
            (r"1961", r"the Wall: \ West Berlin \\ cut off from \\ the old centre", RENT),
            (r"1989", r"the Wall falls; \\ the city is \\ joined again", GAIN),
            (r"the data", rf"land values for \\ thousands of blocks \\ in {R['years'][0]}, {R['years'][1]} \\ and "
                          rf"{R['years'][2]}", CITY),
        ], width=12.8, cols=4, font_size=20).move_to(DOWN * 0.1)
        head = label(r"a city cut in two, \ and rejoined", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.ARSW_2015.tag, corner=DR, font_size=12)
        with self.voiceover(
            "Agglomeration is hard to measure because places that are productive attract people, and people make "
            "places productive. Berlin offers an experiment no one would design. <bookmark mark='a'/> Before the "
            "war it was one city, its business centre in the district of Mitte. <bookmark mark='b'/> In 1961 the "
            "Wall cut West Berlin off from that centre, which lay in the East. <bookmark mark='c'/> In 1989 it fell, "
            "and the city was joined again. <bookmark mark='d'/> Gabriel Ahlfeldt, Stephen Redding, Daniel Sturm "
            "and Nikolaus Wolf collected land values and employment for thousands of city blocks in 1936, 1986 and "
            "2006, and asked what the division and the reunion did to each."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cards.cards[0], shift=UP * 0.1))
            vo.wait_until("a")
            self.play(Indicate(cards.cards[0], color=WHITE, scale_factor=1.03))
            for mk, c in zip("bcd", cards.cards[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def jobs(self):
        B = load("berlin")
        xa, HM = np.array(B["x_all"]), np.array(B["HM"])
        xw, HMd = np.array(B["x"]), np.array(B["HM_div"])
        top = max(HM.max(), HMd.max()) * 1.1
        ax = plane([-6.2, 6.2], [0, top], center=DOWN * 0.3, x_length=11.4, y_length=4.4,
                   xticks=[-6, -4, -2, 0, 2, 4, 6], yticks=[], xlabel=r"kilometres along the line city",
                   ylabel=r"where people work", xfmt=lambda v: f"{v:.0f}", font_size=14)
        before = VGroup(*[Rectangle(width=0.17, height=max(h / top * 4.4, 0.002), stroke_width=0,
                                    fill_color=EAST if x >= 0 else WEST, fill_opacity=0.75).move_to(
            ax.ax.c2p(x, h / 2)) for x, h in zip(xa, HM)])
        after = VGroup(*[Rectangle(width=0.17, height=max(h / top * 4.4, 0.002), stroke_width=0, fill_color=GOLD,
                                   fill_opacity=0.9).move_to(ax.ax.c2p(x, h / 2)) for x, h in zip(xw, HMd)])
        wall = Line(ax.ax.c2p(0, 0), ax.ax.c2p(0, top), color=RENT, stroke_width=6)
        wl = label(r"the Wall", font_size=18, color=RENT).next_to(wall, UP, buff=0.1)
        l_old = label(r"the old centre", font_size=17, color=EAST).next_to(ax.ax.c2p(1.5, HM.max()), UP, buff=0.1)
        l_new = label(r"the West's own centre", font_size=17, color=GOLD).next_to(
            ax.ax.c2p(-3.5, HMd.max()), UP, buff=0.1)
        foot = label(rf"before the Wall {100 * B['jobs_east']:.0f}\% of jobs lay east of the line", font_size=18,
                     color=GREY_A).to_edge(DOWN, buff=0.35)
        tag = published_tag(r"a line city with Ahlfeldt et al.'s parameters, \ solved by Agora", corner=DR,
                            font_size=12)
        with self.voiceover(
            "Their model is a city of many blocks in which people choose where to live and where to work, commute "
            "between them, and make each other more productive when they work close together. Agora solves a small "
            "version: sixty blocks on a line. <bookmark mark='a'/> Joined, most jobs crowd around the old centre, "
            f"just east of where the Wall will run: {100 * B['jobs_east']:.0f} percent of them. "
            "<bookmark mark='b'/> Now build the Wall. The western half must employ its own people, and a new centre "
            "grows in the West, around what had been a secondary district, as the area by the Zoo station did in "
            "West Berlin."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(before, lag_ratio=0.02), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(l_old), FadeIn(foot))
            vo.wait_until("b")
            self.play(Create(wall), FadeIn(wl))
            self.play(before.animate.set_opacity(0.15), FadeIn(after, lag_ratio=0.02), FadeIn(l_new), run_time=2.0)
        self.clear_scene()

    def prices(self):
        B = load("berlin")
        R = B["arsw"]
        x, div = np.array(B["x"]), np.array(B["division"])
        ax = plane([-6.2, 0.2], [-0.35, 0.35], center=LEFT * 2.0 + DOWN * 0.4, x_length=7.6, y_length=4.6,
                   xticks=[-6, -4, -2, 0], yticks=[-0.3, -0.15, 0, 0.15, 0.3],
                   xlabel=r"position in the West \ (the Wall at 0)", ylabel=r"change in floor prices \ (log, "
                   r"relative)", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:+.2f}", font_size=14)
        zero = seg(ax, -6.2, 0, 0.2, 0, GREY_B, 1.5)
        d_line = path(ax, x, div, RENT, 3.4)
        r_line = path(ax, x, -div, GAIN, 3.4)
        wall = Line(ax.ax.c2p(0, -0.35), ax.ax.c2p(0, 0.35), color=RENT, stroke_width=5)
        k_near = int(np.argmax(x))
        side = VGroup(
            label(rf"division: \ near the Wall {100 * div[k_near]:+.0f}\%", font_size=19, color=RENT),
            label(r"reunification: \ the reverse", font_size=19, color=GAIN),
            label(r"Ahlfeldt et al.:", font_size=19, color=E.ACCENT),
            label(rf"productivity rises {R['lambda']:.2f} \\ per log point of nearby \\ employment, \ fading "
                  rf"fast \\ with distance \ ($\delta$ = {R['delta']:.2f})", font_size=17, color=WHITE),
            label(rf"residents value \\ nearby residents too \\ ({R['eta']:.2f})", font_size=17, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.4)
        tag = published_tag(tables.ARSW_2015.tag + r"; \ the line city", corner=DR, font_size=12)
        with self.voiceover(
            "And prices. <bookmark mark='a'/> On the line city, division lowers floor prices most in the western "
            f"blocks next to the Wall, about {abs(100 * div[k_near]):.0f} percent relative to the West's average, "
            "and raises them around the new western centre. <bookmark mark='b'/> Reunification runs the film "
            "backwards. <bookmark mark='c'/> That is the pattern the authors found in Berlin's land values. Fitting "
            "their model to it, they estimated that a block's productivity rises with the employment nearby, "
            f"with an elasticity of {R['lambda']:.2f}, and that the effect fades within a few minutes' travel. "
            f"<bookmark mark='d'/> Residents, too, value nearby residents, with an elasticity of {R['eta']:.2f}. "
            "Agglomeration is strong, but intensely local: it lives in the blocks around you."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(wall), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(d_line), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(r_line), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(side[4]))
        self.clear_scene()
