from __future__ import annotations

from videos.psychology.psych38.common import *  # noqa: F403


def muller_lyer(length: float = 3.0, out: bool = True, color=WHITE) -> VGroup:
    """A Müller-Lyer line with fins pointing out (looks longer) or in (looks shorter)."""
    a, b = np.array([-length / 2, 0, 0]), np.array([length / 2, 0, 0])
    f = 0.42
    s = -1 if out else 1
    fins = VGroup()
    for end, d in ((a, -1), (b, 1)):
        for v in (1, -1):
            tip = end + np.array([s * d * f * 0.8, v * f * 0.6, 0])
            fins.add(Line(end, tip, color=color, stroke_width=4))
    return VGroup(Line(a, b, color=color, stroke_width=4), fins)


class Illusion(VoiceoverScene):
    def construct(self):
        self.card()
        self.lines()
        self.why()

    def card(self):
        card = chapter_card(2, r"Even an illusion varies", r"Does culture reach down into perception?",
                            lit={1966: r"Segall et al.", 2015: r"Gandhi et al."}, part=PART,
                            scale=("circuit", "culture"), marr=("what",))
        with self.voiceover("Chapter two. Even an illusion varies."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def lines(self):
        head = heading(r"Two equal lines")
        top = muller_lyer(3.2, out=True, color=WEST).move_to([-3.6, 1.3, 0])
        bot = muller_lyer(3.2, out=False, color=WORLD).move_to([-3.6, -0.2, 0])
        ruler = VGroup(DashedLine([-5.2, 1.9, 0], [-5.2, -0.8, 0], color=GREY_B),
                       DashedLine([-2.0, 1.9, 0], [-2.0, -0.8, 0], color=GREY_B))
        A = axes([-0.6, 3.6], [0, 1.0], x_length=5.0, y_length=1.9, xticks=None, yticks=None,
                 ylabel=r"illusion size", center=[-3.6, -2.4, 0], font_size=14)
        heights = [0.9, 0.7, 0.45, 0.2]
        cols = [WEST, WEST, WORLD, WORLD]
        b = bars(A.ax, [0, 1, 2, 3], heights, cols, width=0.55)
        note = label(r"the pattern reported, \ drawn schematically", font_size=13, color=GREY_B).next_to(A, RIGHT,
                                                                                                    buff=0.2)
        rows = rows_of([
            (r"the Müller-Lyer illusion: \ the lines are the same length; \ the one with fins pointing out looks "
             r"longer", WHITE),
            (r"Segall, \ Campbell and Herskovits, \ 1966: \ fieldworkers tested children and adults in more than a "
             r"dozen societies, \ asking which of two lines looked longer", WEST),
            (r"American and European samples showed the largest illusion; \ some groups, \ such as San foragers in "
             r"the Kalahari, \ showed little", WORLD),
            (r"their explanation: \ eyes raised among rectangular buildings learn to read corners as depth", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.2, 0])
        tag = historical_tag(r"Segall, \ Campbell \& Herskovits (1966)")
        with self.voiceover(
            "If anything should be the same everywhere, it's how two lines look. <bookmark mark='a'/> In the "
            "Müller-Lyer illusion, the two lines are the same length. The one with fins pointing out looks longer. "
            "<bookmark mark='b'/> In 1966 Marshall Segall, Donald Campbell and Melville Herskovits's "
            "fieldworkers tested children and adults in more than a dozen societies, asking which of two lines looked longer. "
            "<bookmark mark='c'/> American and European samples showed the largest illusion. Some groups, like San "
            "foragers in the Kalahari, showed little. <bookmark mark='d'/> Their explanation was the carpentered "
            "world: eyes raised among rectangular buildings learn to read corners as depth."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(top), FadeIn(bot))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Create(ruler))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(A), FadeIn(note), *[GrowFromEdge(x, DOWN) for x in b[:2]])
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), *[GrowFromEdge(x, DOWN) for x in b[2:]])
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def why(self):
        head = heading(r"Why it varies is still argued")
        cols = VGroup()
        for title, body, c in (
                (r"carpentered world", r"the illusion is learned from rectangular environments", WEST),
                (r"newly sighted children", r"Gandhi and colleagues, \ 2015: \ children who gained sight through "
                                            r"cataract surgery, \ tested within 48 hours, \ already saw the "
                                            r"illusion", GOOD),
                (r"method", r"Amir and Firestone, \ 2025: \ the old procedures and samples differ in ways that could "
                            r"produce the differences; \ many animals see the illusion too", AUTH)):
            cols.add(VGroup(word_chip(title, color=c, font_size=19, width=3.8), wrapped_label(body, 3.8, 18, WHITE))
                     .arrange(DOWN, buff=0.3))
        cols.arrange(RIGHT, buff=0.45, aligned_edge=UP).move_to([0, 0.6, 0])
        foot = rows_of([
            (r"Part 14 entered this in the Ledger as contested: \ the illusion is real; \ whether its size depends "
             r"on the environment is not settled", YOU),
            (r"the lesson stands: \ even a basic perceptual effect was measured mostly in one kind of society", WORLD),
        ], 12.0, 20, 0.3).to_edge(DOWN, buff=0.8)
        tag = published_tag(r"Gandhi et al.\ (2015); \ Amir \& Firestone (2025)")
        with self.voiceover(
            "Why it varies is still argued. <bookmark mark='a'/> The carpentered-world account says the illusion is "
            "learned. <bookmark mark='b'/> But in 2015 Tapan Gandhi and colleagues tested children who had just "
            "gained their sight through cataract surgery, within forty-eight hours. They already saw the illusion. "
            "<bookmark mark='c'/> And in 2025 a review by Amir and Firestone argued that the old procedures and "
            "samples differ in ways that could produce the differences, and noted that many animals see the "
            "illusion too. <bookmark mark='d'/> Part 14 entered this in the Ledger as contested. The illusion is "
            "real. Whether its size depends on the environment is not settled. <bookmark mark='e'/> The lesson "
            "stands either way: even a basic perceptual effect had been measured mostly in one kind of society."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, c in zip("abc", cols):
                vo.wait_until(m)
                self.play(FadeIn(c, shift=UP * 0.15))
            for m, r in zip("de", foot):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
