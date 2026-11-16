from __future__ import annotations

from videos.psychology.psych37.common import *  # noqa: F403


class Mates(VoiceoverScene):
    def construct(self):
        self.card()
        self.cultures()
        self.readings()

    def card(self):
        card = chapter_card(10, r"Mate preferences across cultures", r"Do men and women want different things?",
                            lit={1989: r"Buss", 2020: r"Walter et al."}, part=PART, scale=("gene", "culture"),
                            marr=("why",))
        with self.voiceover("Chapter ten. Mate preferences across cultures."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def cultures(self):
        head = heading(r"Thirty-seven cultures, \ then forty-five countries")
        globe = VGroup(Circle(radius=1.4, color=GREY_B, stroke_width=2),
                       Ellipse(width=2.8, height=1.0, color=GREY_D, stroke_width=1),
                       Ellipse(width=1.0, height=2.8, color=GREY_D, stroke_width=1)).move_to([-4.3, 0.6, 0])
        pins = VGroup(*[Dot(globe[0].point_at_angle(a) * 0.82 + globe.get_center() * 0.18, radius=0.06,
                            color=PERSON) for a in np.linspace(0.2, 6.0, 14)])
        rows = rows_of([
            (r"Buss, \ 1989: \ 10{,}047 people in 37 cultures rated what they want in a long-term partner", WHITE),
            (r"in most, \ men gave more weight to physical attractiveness and youth, \ women to earning prospects",
             PERSON),
            (r"Walter and colleagues, \ 2020: \ 14{,}399 people in 45 countries: \ the same differences, \ again",
             GOOD),
            (r"a stated preference, \ replicated across the world; \ chapter eight showed how weakly stated "
             r"preferences predict whom people desire after they meet", YOU),
        ], 6.4, 20, 0.36).move_to([3.0, -0.2, 0])
        tag = published_tag(r"Buss (1989); \ Walter et al.\ (2020)")
        with self.voiceover(
            "Stated preferences have also been surveyed across the world. <bookmark mark='a'/> In 1989 David Buss "
            "asked ten thousand and forty-seven people in thirty-seven cultures what they want in a long-term "
            "partner. <bookmark mark='b'/> In most, men gave more weight to physical attractiveness and youth, and "
            "women to earning prospects. <bookmark mark='c'/> In 2020 Walter and colleagues asked fourteen thousand "
            "three hundred and ninety-nine people in forty-five countries, and found the same differences again. "
            "<bookmark mark='d'/> It's a stated preference, replicated across the world. And chapter eight showed "
            "how weakly stated preferences predict whom people desire after they meet."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(globe))
            vo.wait_until("a")
            self.play(FadeIn(pins), FadeIn(rows[0]))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def readings(self):
        head = heading(r"Two readings")
        left = VGroup(word_chip(r"evolutionary", color=GOOD, font_size=22, width=5.2),
                      wrapped_label(r"the sexes faced different reproductive problems, \ and evolved different "
                                    r"preferences; \ the differences should appear everywhere", 5.2, 20, WHITE)
                      ).arrange(DOWN, buff=0.3)
        right = VGroup(word_chip(r"social role", color=CROWD, font_size=22, width=5.2),
                       wrapped_label(r"the differences follow the division of labour, \ and should shrink where "
                                     r"men's and women's roles are more alike", 5.2, 20, WHITE)).arrange(DOWN, buff=0.3)
        VGroup(left, right).arrange(RIGHT, buff=0.9, aligned_edge=UP).move_to([0, 0.7, 0])
        foot = rows_of([
            (r"in the 45-country data, \ neither gender equality nor pathogen prevalence robustly predicted the size "
             r"of the differences, \ apart from the preferred age gap", PERSON),
            (r"country-level correlations with 45 points cannot settle a question about evolution, \ or about roles",
             YOU),
        ], 11.6, 20, 0.3).to_edge(DOWN, buff=0.7)
        tag = published_tag(r"Walter et al.\ (2020)")
        with self.voiceover(
            "Why? There are two readings. <bookmark mark='a'/> The evolutionary reading: the sexes faced different "
            "reproductive problems and evolved different preferences, so the differences should appear everywhere. "
            "<bookmark mark='b'/> The social-role reading: the differences follow the division of labour, and should "
            "shrink where men's and women's roles are more alike. <bookmark mark='c'/> In the forty-five-country "
            "data, neither gender equality nor how common disease was robustly predicted the size of the "
            "differences, apart from the preferred age gap. <bookmark mark='d'/> Correlations across forty-five "
            "countries can't settle a question about evolution, or about roles."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(FadeIn(right))
            vo.wait_until("c")
            self.play(FadeIn(foot[0]))
            vo.wait_until("d")
            self.play(FadeIn(foot[1]))
        self.clear_scene()
