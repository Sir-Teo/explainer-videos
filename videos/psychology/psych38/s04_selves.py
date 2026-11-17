from __future__ import annotations

from videos.psychology.psych38.common import *  # noqa: F403


def self_map(interdependent: bool, color) -> VGroup:
    """Markus and Kitayama's diagram: the self as a circle among others; in the interdependent self the
    boundaries overlap."""
    me = Circle(radius=0.55, color=color, stroke_width=4).move_to(ORIGIN)
    dot = Dot(radius=0.06, color=color)
    others = VGroup()
    r = 0.9 if interdependent else 1.45
    for k in range(5):
        a = TAU * k / 5 + PI / 2
        c = Circle(radius=0.42, color=GREY_B, stroke_width=2).move_to([r * np.cos(a), r * np.sin(a), 0])
        others.add(VGroup(c, Dot(c.get_center() + 0.12 * RIGHT, radius=0.04, color=GREY_B)))
    if interdependent:
        for k in range(5):
            a = TAU * k / 5 + PI / 2
            others.add(Dot([0.35 * np.cos(a), 0.35 * np.sin(a), 0], radius=0.05, color=GREY_B))
    return VGroup(others, me, dot)


class Selves(VoiceoverScene):
    def construct(self):
        self.card()
        self.selves()
        self.attention()
        self.measures()

    def card(self):
        card = chapter_card(3, r"Independent and interdependent selves", r"Do cultures make different selves?",
                            lit={1980: r"Hofstede", 1991: r"Markus \& Kitayama", 2001: r"Masuda \& Nisbett",
                                 2002: r"Oyserman et al."}, part=PART, scale=("person", "culture"), marr=("what",))
        with self.voiceover("Chapter three. Independent and interdependent selves."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def selves(self):
        head = heading(r"Two construals of the self")
        ind = self_map(False, WEST).move_to([-4.6, 0.7, 0])
        dep = self_map(True, WORLD).move_to([-1.5, 0.7, 0])
        li = label(r"independent", font_size=20, color=WEST).next_to(ind, DOWN, buff=0.25)
        ld = label(r"interdependent", font_size=20, color=WORLD).next_to(dep, DOWN, buff=0.25)
        note = wrapped_label(r"after Markus and Kitayama's figure: \ the dots inside a circle are what defines "
                             r"that self", 5.6, 14, GREY_B).move_to([-3.05, -1.9, 0])
        rows = rows_of([
            (r"Markus and Kitayama, \ 1991: \ two construals of the self", WHITE),
            (r"independent: \ a self defined by its own attributes, \ abilities and preferences, \ bounded and "
             r"stable across settings; \ common in North America and Western Europe", WEST),
            (r"interdependent: \ a self defined by relationships and roles, \ shifting with the setting; \ common "
             r"in East Asia and much of the world", WORLD),
            (r"the claim: \ the construal shapes thinking, \ emotion and motivation", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.2, 0])
        tag = historical_tag(r"Markus \& Kitayama (1991)")
        with self.voiceover(
            "The most influential theory of cultural difference is about the self. <bookmark mark='a'/> In 1991 "
            "Hazel Markus and Shinobu Kitayama described two ways of construing it. <bookmark mark='b'/> The "
            "independent self is defined by its own attributes, abilities and preferences: bounded, and stable "
            "across settings. They saw it as common in North America and Western Europe. <bookmark mark='c'/> The "
            "interdependent self is defined by relationships and roles, and shifts with the setting. They saw it as "
            "common in East Asia, and in much of the world. <bookmark mark='d'/> Their claim was that the construal "
            "shapes thinking, emotion and motivation."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(note))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(ind), FadeIn(li))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(dep), FadeIn(ld))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def attention(self):
        head = heading(r"What is in the picture?")
        water = Rectangle(width=5.2, height=3.0, stroke_color=GREY_D, fill_color="#0E2233", fill_opacity=1)
        water.move_to([-3.6, 0.4, 0])
        weeds = VGroup(*[Line([-5.7 + 0.45 * k, -1.1, 0], [-5.6 + 0.45 * k, -0.4 + 0.25 * np.sin(k), 0],
                              color=GOOD, stroke_width=3) for k in range(11)])
        rocks = VGroup(*[Ellipse(width=0.6, height=0.3, color=GREY_B, fill_opacity=0.5).move_to([x, -0.95, 0])
                         for x in (-4.9, -3.3, -2.0)])

        def fish(c, s=1.0):
            body = Ellipse(width=0.9 * s, height=0.42 * s, color=c, fill_opacity=0.9, stroke_width=0)
            tail = Polygon([-0.45 * s, 0, 0], [-0.75 * s, 0.2 * s, 0], [-0.75 * s, -0.2 * s, 0], color=c,
                           fill_opacity=0.9, stroke_width=0)
            return VGroup(body, tail)

        big = fish(PERSON, 1.4).move_to([-3.4, 0.9, 0])
        small = VGroup(fish(GREY_A, 0.7).move_to([-5.1, 1.4, 0]), fish(GREY_A, 0.7).move_to([-2.0, 0.2, 0]),
                       fish(GREY_A, 0.6).move_to([-4.6, 0.0, 0]))
        rows = rows_of([
            (r"Masuda and Nisbett, \ 2001: \ Japanese and American students watched animated underwater scenes and "
             r"described them", WHITE),
            (r"Americans began more often with the large focal fish", WEST),
            (r"Japanese students said more about the background, \ the water, \ rocks and plants, \ and the "
             r"relations between things; \ they also recognized a fish less well on a new background", WORLD),
            (r"Nisbett's summary: \ analytic attention to objects, \ holistic attention to fields", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.2, 0])
        tag = published_tag(r"Masuda \& Nisbett (2001)")
        with self.voiceover(
            "The idea reached perception too. <bookmark mark='a'/> In 2001 Takahiko Masuda and Richard Nisbett "
            "showed Japanese and American students animated underwater scenes and asked them to describe what they "
            "saw. <bookmark mark='b'/> Americans more often began with the big fish in the middle. "
            "<bookmark mark='c'/> Japanese students said more about the background, the water, the rocks and the "
            "plants, and about relations between things. They also recognized a fish less well when it appeared on "
            "a new background. <bookmark mark='d'/> Nisbett summed it up as analytic attention to objects, against "
            "holistic attention to the whole field."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(water), FadeIn(weeds), FadeIn(rocks), FadeIn(small),
                      FadeIn(big))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Indicate(big, color=WEST, scale_factor=1.15))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Indicate(VGroup(weeds, rocks), color=WORLD, scale_factor=1.05))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def measures(self):
        head = heading(r"How good are the measures?")
        rows = rows_of([
            (r"Hofstede, \ 1980: \ surveys of employees of one company, \ IBM, \ in dozens of countries, \ "
             r"summarized as national scores on dimensions such as individualism", WHITE),
            (r"Oyserman, \ Coon and Kemmelmeier, \ 2002: \ a meta-analysis of individualism and collectivism "
             r"questionnaires", WEST),
            (r"European Americans did score higher on individualism and lower on collectivism than others, \ but "
             r"the differences were smaller and less consistent than the theory implied, \ and varied with the "
             r"scale used", WORLD),
            (r"Part 3's lesson: \ a difference on a questionnaire is only as good as the questionnaire's meaning "
             r"in each place; \ the next chapters show how that can fail", YOU),
        ], 12.4, 21, 0.42).move_to([0, -0.3, 0])
        tag = published_tag(r"Hofstede (1980); \ Oyserman, \ Coon \& Kemmelmeier (2002)")
        with self.voiceover(
            "How good are the measures behind these contrasts? <bookmark mark='a'/> Geert Hofstede's famous "
            "dimensions came from surveys of the employees of one company, IBM, in dozens of countries, summed up "
            "as national scores on dimensions such as individualism. <bookmark mark='b'/> In 2002 Daphna Oyserman "
            "and colleagues meta-analysed the individualism and collectivism questionnaires. "
            "<bookmark mark='c'/> European Americans did score higher on individualism and lower on collectivism "
            "than others. But the differences were smaller and less consistent than the theory implied, and they "
            "depended on which scale was used. <bookmark mark='d'/> It's Part 3's lesson. A difference on a "
            "questionnaire is only as good as the questionnaire's meaning in each place, and the next chapters show "
            "how that can fail."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
