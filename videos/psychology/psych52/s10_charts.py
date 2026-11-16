from __future__ import annotations

from videos.psychology.psych52.common import *  # noqa: F403


class Charts(VoiceoverScene):
    def construct(self):
        card_section(self, 9, r"Seeing data", r"Which chart lets a reader judge a number best?")
        self.ranking()
        self.why()
        self.preattentive()

    def ranking(self):
        d = load("charts")
        head = heading(r"Cleveland and McGill's ranking")
        A = axes([0.3, 6.7], [0, 4.5], x_length=5.6, y_length=3.0, xticks=None, yticks=[0, 1, 2, 3, 4],
                 yfmt=lambda v: f"{v:.0f}", ylabel=r"error, \ $\log_2(|\mathrm{err}| + 1/8)$", center=[-3.3, 0.3, 0],
                 font_size=12)
        cols = [GOOD, GOOD, PERSON, AUTH, AUTH, AUTH]
        b = bars(A.ax, list(range(1, 7)), d["log_err"], cols, width=0.6)
        names = VGroup(*[label(s, font_size=13, color=GREY_A).next_to(A.ax.c2p(i + 1, 0), DOWN, buff=0.12)
                         for i, s in enumerate([r"position", r"length", r"angle", r"area", r"volume", r"colour"])])
        rows = rows_of([
            (r"1984: \ William Cleveland and Robert McGill asked people what percentage one mark was of another", WHITE),
            (r"position along a common scale was judged best, \ then length, \ then angle, \ then area, \ volume and "
             r"shading", GOOD),
            (r"Heer and Bostock, \ 2010, \ repeated it online with crowd workers: \ the same order", MODEL),
            (rf"Psyche's version: \ typical errors of {d['mae'][1]:.0f} points for lengths and {d['mae'][2]:.0f} for "
             rf"angles, \ about {d['mae'][2] / d['mae'][1]:.1f} times as large", PERSON),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{work.graphical\_error}, \ illustrative noise")
        tag2 = published_tag(r"Cleveland \& McGill (1984)").to_corner(DL, buff=0.3)
        with self.voiceover(
            "Which chart lets a reader judge a number best? <bookmark mark='a'/> In 1984 William Cleveland and Robert "
            "McGill asked people what percentage one mark was of another, with the marks drawn in different ways. "
            "<bookmark mark='b'/> Position along a common scale was judged best, then length, then angle, then area, "
            "volume and shading. <bookmark mark='c'/> Jeffrey Heer and Michael Bostock repeated it online in 2010 with "
            "crowd workers, and found the same order. <bookmark mark='d'/> In Psyche's version, the typical error is "
            "about four points for lengths and seven for angles, almost twice as large."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(tag2), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), LaggedStart(*[FadeIn(x, shift=UP * 0.1) for x in b], lag_ratio=0.25))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def why(self):
        head = heading(r"Why area misleads: \ Part 11's exponents")
        sq = VGroup()
        for k, (s, x) in enumerate(((1.0, -4.8), (2.0, -2.9))):
            sq.add(Square(s * 0.9, color=PERSON, fill_opacity=0.5).move_to([x, 0.9, 0]).align_to([0, 0.3, 0], DOWN))
        bl = VGroup()
        for k, (h, x) in enumerate(((0.9, -0.9), (1.8, -0.2))):
            bl.add(Rectangle(width=0.45, height=h, color=GOOD, fill_opacity=0.6).move_to([x, 0, 0])
                   .align_to([0, 0.3, 0], DOWN))
        l1 = label(r"area twice? \ four times", font_size=16, color=PERSON).next_to(sq, DOWN, buff=0.25)
        l2 = label(r"length twice", font_size=16, color=GOOD).next_to(bl, DOWN, buff=0.25)
        rows = rows_of([
            (r"Stevens's power law (Part 11): \ perceived size grows as physical size to an exponent", WHITE),
            (r"length about 1, \ area about 0.7, \ volume about 0.6: \ a doubled area looks only about 1.6 times as "
             r"large", PERSON),
            (r"a chart that scales a symbol's side by the data quadruples its area, \ and overstates the change; \ "
             r"one that scales the area is understated", AUTH),
            (r"so: \ positions and lengths for quantities; \ area and colour for rough impressions", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        with self.voiceover(
            "Why does area mislead? <bookmark mark='a'/> Part 11's power law: perceived size grows as physical size "
            "to an exponent. <bookmark mark='b'/> For length the exponent is about one. For area it's about zero point "
            "seven, and for volume about zero point six. A doubled area looks only about one and a half times as "
            "large. <bookmark mark='c'/> So a chart that scales a symbol's side by the data quadruples its area and "
            "overstates the change, and one that scales the area understates it. <bookmark mark='d'/> Use positions "
            "and lengths for quantities, and area and colour for rough impressions."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(bl), FadeIn(l2))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(sq), FadeIn(l1))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def preattentive(self):
        chips_section(self, r"What pops out", [
            (r"pop-out", r"a single feature, \ a red mark among grey ones, \ is found in parallel (Part 18's feature "
                         r"search)", GOOD),
            (r"conjunctions", r"red and square among red circles and grey squares: \ found by serial search, \ slowly",
             AUTH),
            (r"the rule", r"highlight one thing with one feature; \ highlighting everything highlights nothing", MODEL),
            (r"colour maps", r"perceptually uniform scales, \ with equal steps in lightness; \ the rainbow scale invents "
                             r"boundaries", PERSON),
        ], "Part 18 tells chart designers what pops out. <bookmark mark='a'/> A single feature, a red mark among grey "
           "ones, is found in parallel. <bookmark mark='b'/> A conjunction, red and square among red circles and grey "
           "squares, needs serial search, and it's slow. <bookmark mark='c'/> So highlight one thing with one "
           "feature. Highlighting everything highlights nothing. <bookmark mark='d'/> And use perceptually uniform "
           "colour scales, with equal steps in lightness. The rainbow scale invents boundaries that aren't in the "
           "data.")
