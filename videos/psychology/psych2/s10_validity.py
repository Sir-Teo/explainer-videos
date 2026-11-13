from __future__ import annotations

from videos.psychology.psych2.common import *  # noqa: F403

V_COLOR = ("#7EC8F5", P.ACCENT, "#B48EF0", "#7BD88F")


def tile(num: str, title: str, question: str, where: str, color, width=6.6) -> VGroup:
    head = VGroup(label(num, font_size=44, color=color), label(title, font_size=34, color=color))
    head.arrange(RIGHT, buff=0.3, aligned_edge=DOWN)
    q = wrapped_label(question, width - 0.8, 28, WHITE)
    w = wrapped_label(where, width - 0.8, 22, GREY_B)
    inner = VGroup(head, q, w).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    box = RoundedRectangle(width=width, height=inner.height + 0.5, corner_radius=0.14, stroke_color=color,
                           stroke_width=2, fill_color=CARD_FILL, fill_opacity=0.95)
    inner.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.35)
    return VGroup(box, inner)


class Validity(VoiceoverScene):
    def construct(self):
        self.card()
        self.four()
        self.weird()
        self.quasi()

    def card(self):
        card = chapter_card(9, r"Four ways to be wrong", r"A study found an effect. \ What exactly has it shown?",
                            lit={1963: r"Campbell \& Stanley", 2010: r"the WEIRD problem"}, part=PART,
                            scale=("group", "culture"), marr=("what",))
        with self.voiceover(
            "Chapter nine. Four ways to be wrong."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def four(self):
        head = heading(r"A study says: \ ``the game speeds reactions''. \ Four questions.", font_size=32)
        tiles = VGroup(
            tile(r"1", r"statistical conclusion", r"Is there a difference at all, or is it the luck of the draw?",
                 r"chapter 5, and Part 4", V_COLOR[0]),
            tile(r"2", r"internal", r"Was it the game that made the difference, in this study?",
                 r"chapters 3 to 7: \ controls, shuffles, blinds", V_COLOR[1]),
            tile(r"3", r"construct", r"Was it ``the game'', and was it ``reaction speed''?",
                 r"what was really changed, and what was really measured: \ Part 3", V_COLOR[2]),
            tile(r"4", r"external", r"Would it hold for other people, other places, other times?",
                 r"who was studied, and who was not", V_COLOR[3]),
        ).arrange_in_grid(2, 2, buff=(0.3, 0.28)).next_to(head, DOWN, buff=0.35)
        if tiles.get_bottom()[1] < -3.8:
            tiles.scale_to_fit_height(tiles.height + tiles.get_bottom()[1] + 3.8).next_to(head, DOWN, buff=0.35)
        src = note(r"Shadish, Cook \& Campbell (2002)").to_corner(DL, buff=0.3)
        with self.voiceover(
            "Suppose a study has done everything in the last six chapters, and reports that the game speeds "
            "reactions. There are still four separate ways it could be wrong, and it helps to keep them apart. "
            "They come from Campbell again, with Thomas Cook and William Shadish. <bookmark mark='a'/> One. Is "
            "there a difference at all, or just the luck of the draw? That's statistical conclusion validity, "
            "and it's Part 4's subject. <bookmark mark='b'/> Two. Granted a difference, was it the game that "
            "made it, in this study? Internal validity. Everything so far today has been about this one. "
            "<bookmark mark='c'/> Three. Was it really the game, and not, say, the attention the players got? "
            "And was it really reaction speed that improved, or just skill at one particular test? Construct "
            "validity: whether the labels fit the things. <bookmark mark='d'/> And four. Would it hold for "
            "people who weren't in the study, somewhere else, ten years from now? External validity. A study "
            "can be perfect on one of these and fail another, and arguments about a finding go better when "
            "people say which one they're arguing about."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            ghosts = tiles.copy().set_opacity(0.22)
            self.play(LaggedStart(*[FadeIn(g_, shift=UP * 0.1) for g_ in ghosts], lag_ratio=0.3), run_time=4.0)
            for mark, g_, t in zip("abcd", ghosts, tiles):
                vo.wait_until(mark)
                self.play(FadeOut(g_), FadeIn(t))
        self.clear_scene()

    def weird(self):
        head = heading(r"External validity: \ who was in the room?")
        n = 100
        west = 96
        us = 68
        cols = [P.ACCENT] * us + ["#7EC8F5"] * (west - us) + [GREY_C] * (n - west)
        crowd = people_row(n, cols, height=0.42, buff=0.1, per_row=20).move_to([-2.9, -0.15, 0])
        cap = label(r"of every 100 samples in six leading psychology journals, 2003 to 2007:", font_size=26)
        cap.next_to(crowd, UP, buff=0.35).align_to(crowd, LEFT)
        facts = VGroup(
            label(rf"{us} from the United States", font_size=30, color=P.ACCENT),
            label(rf"{west} from Western industrial", font_size=30, color="#7EC8F5"),
            label(r"countries, which hold about", font_size=26, color=GREY_A),
            label(r"12\% of the world's people", font_size=26, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([4.6, 0.3, 0])
        keep_in_frame(facts, 0.3)
        word = VGroup(label(r"WEIRD:", font_size=34, color=P.ACCENT),
                      label(r"Western, Educated, Industrialized, Rich, Democratic", font_size=30))
        word.arrange(RIGHT, buff=0.3).to_edge(DOWN, buff=0.8)
        src = published_tag(r"Arnett (2008); \ Henrich, Heine \& Norenzayan (2010)")
        with self.voiceover(
            "External validity has a famous number attached. In 2008 Jeffrey Arnett counted where the "
            "participants came from in six leading psychology journals. <bookmark mark='a'/> Of every hundred "
            f"samples, {us} were from the United States. <bookmark mark='b'/> {west} were from Western "
            "industrial countries, which hold about an eighth of the world's people. And within those, a great "
            "many were university students. <bookmark mark='c'/> Two years later Joseph Henrich and his colleagues "
            "gave the population a name: Western, educated, industrialized, rich and democratic. Weird. Their "
            "point was sharper than under-sampling. On several measures where other societies have been "
            "tested, these participants sit at the far end of the range. This series will say who was studied, "
            "and Part 38 asks which findings travel."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap), FadeIn(src))
            grey = crowd.copy()
            for p_ in grey:
                p_.set_color(GREY_D)
            self.play(FadeIn(grey, lag_ratio=0.01), run_time=1.5)
            vo.wait_until("a")
            self.play(*[grey[i].animate.set_color(P.ACCENT) for i in range(us)], FadeIn(facts[0]))
            vo.wait_until("b")
            self.play(*[grey[i].animate.set_color("#7EC8F5") for i in range(us, west)], FadeIn(facts[1]),
                      FadeIn(facts[2]), FadeIn(facts[3]))
            vo.wait_until("c")
            self.play(FadeIn(word, shift=UP * 0.15))
        self.clear_scene()

    def sketch(self, kind) -> VGroup:
        A = axes([0, 10], [0, 10], x_length=3.8, y_length=2.5, center=ORIGIN)
        ax = A.ax
        g = VGroup(A)
        if kind == "rd":  # a jump at a cutoff
            g.add(Line(ax.c2p(0.5, 2.5), ax.c2p(5, 4.5), color=CTRL, stroke_width=4),
                  Line(ax.c2p(5, 6.5), ax.c2p(9.5, 8.5), color=TREAT, stroke_width=4),
                  DashedLine(ax.c2p(5, 0), ax.c2p(5, 9.5), color=GREY_B, stroke_width=2))
        elif kind == "did":  # two groups before and after
            g.add(Line(ax.c2p(1, 3), ax.c2p(5, 4), color=CTRL, stroke_width=4),
                  Line(ax.c2p(5, 4), ax.c2p(9, 5), color=CTRL, stroke_width=4),
                  Line(ax.c2p(1, 5), ax.c2p(5, 6), color=TREAT, stroke_width=4),
                  Line(ax.c2p(5, 6), ax.c2p(9, 9), color=TREAT, stroke_width=4),
                  DashedLine(ax.c2p(5, 6), ax.c2p(9, 7), color=TREAT, stroke_width=2),
                  DashedLine(ax.c2p(5, 0), ax.c2p(5, 9.5), color=GREY_B, stroke_width=2))
        else:  # a lottery
            for k in range(8):
                g.add(card(RED_CARD if k % 3 == 0 else BLACK_CARD, 0.3, 0.44).move_to(ax.c2p(1.2 + 1.1 * k, 5)))
        return g

    def quasi(self):
        head = heading(r"When you cannot shuffle")
        items = VGroup()
        for kind, name, text in (
            ("lottery", r"a natural experiment", r"the world did the shuffling: \ a lottery, a draft number, a "
                                                 r"birthday"),
            ("rd", r"a cutoff", r"people just above and just below a threshold are alike, except for what the "
                                r"threshold gave them"),
            ("did", r"before and after, twice", r"compare the change in the treated group with the change in an "
                                                r"untreated one"),
        ):
            pic = self.sketch(kind)
            t = VGroup(label(name, font_size=32, color=P.ACCENT), wrapped_label(text, 4.1, 25, WHITE))
            t.arrange(DOWN, buff=0.12)
            items.add(VGroup(pic, t).arrange(DOWN, buff=0.3))
        items.arrange(RIGHT, buff=0.45, aligned_edge=UP)
        if items.width > 13.4:
            items.width = 13.4
        items.move_to([0, -0.2, 0])
        cannot = VGroup(label(r"You cannot assign people to", font_size=34, color=GREY_A),
                        VGroup(*[label(t, font_size=44, color=WHITE) for t in (r"a childhood", r"a stroke",
                                                                              r"an earthquake")])
                        .arrange(RIGHT, buff=0.9)).arrange(DOWN, buff=0.4).move_to([0, 0.2, 0])
        foot = label(r"each replaces the shuffle with an assumption, and says which one: \ \emph{Statistics, Built}, "
                     r"Parts 35 to 37", font_size=26, color=GREY_A).to_edge(DOWN, buff=0.7)
        sch = schematic_tag(UR)
        with self.voiceover(
            "And sometimes you can't randomize at all. You can't assign people to a childhood, or a stroke, or "
            "an earthquake. Then the craft is to find a comparison that comes close. <bookmark mark='a'/> "
            "Sometimes the world has shuffled for you: a lottery, a draft number, the month you were born. "
            "<bookmark mark='b'/> Sometimes there's a cutoff, a pass mark or an age limit, and the people just "
            "either side of it are alike in everything except what the cutoff gave them. <bookmark mark='c'/> "
            "And sometimes you can compare two changes: how much the treated group changed, against how much a "
            "similar untreated group changed over the same period. <bookmark mark='d'/> Each of these stands "
            "in for the shuffle with an assumption, and the honest ones say which. The Statistics series spends "
            "three parts on them. For today the point is the ranking: a design is as good as its answer to the "
            "question, what else could explain this?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(sch), FadeIn(cannot[0]))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in cannot[1]], lag_ratio=0.5), run_time=3.0)
            vo.wait_until("a")
            self.play(FadeOut(cannot))
            self.play(FadeIn(items[0], shift=UP * 0.15))
            for mark, it in zip("bc", items[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(it, shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(foot, shift=UP * 0.15))
        self.clear_scene()
