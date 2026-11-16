from __future__ import annotations

from videos.psychology.psych37.common import *  # noqa: F403


class Dating(VoiceoverScene):
    def construct(self):
        self.card()
        self.stated()
        self.variance()

    def card(self):
        card = chapter_card(8, r"What people say they want", r"Do stated preferences predict desire?",
                            lit={2008: r"Eastwick \& Finkel", 2017: r"Joel et al."}, part=PART, scale=("person",),
                            marr=("what",))
        with self.voiceover("Chapter eight. What people say they want."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def stated(self):
        head = heading(r"The ideal partner, \ and the real one")
        left = VGroup(word_chip(r"what people say", color=CROWD, font_size=22, width=5.0),
                      wrapped_label(r"asked about an ideal partner, \ men rated physical attractiveness higher than "
                                    r"women did, \ and women rated earning prospects higher than men did", 5.0, 19,
                                    WHITE)).arrange(DOWN, buff=0.3)
        right = VGroup(word_chip(r"what people do", color=PERSON, font_size=22, width=5.0),
                       wrapped_label(r"after real speed dates, \ attractiveness and earning prospects predicted "
                                     r"romantic interest about equally for men and women", 5.0, 19, WHITE)
                       ).arrange(DOWN, buff=0.3)
        VGroup(left, right).arrange(RIGHT, buff=0.9, aligned_edge=UP).move_to([0, 0.8, 0])
        rows = rows_of([
            (r"Eastwick and Finkel, \ 2008: \ the familiar sex differences in stated preferences did not show up in "
             r"whom people actually desired", WHITE),
            (r"Part 35's lesson about introspection, \ in romance: \ people's theories about what attracts them "
             r"are not a reliable account of what does", YOU),
        ], 12.0, 21, 0.3).move_to([0, -2.1, 0])
        tag = published_tag(r"Eastwick \& Finkel (2008)")
        with self.voiceover(
            "What do people say they want, and does it predict whom they want? <bookmark mark='a'/> Asked about an "
            "ideal partner, men rate physical attractiveness higher than women do, and women rate earning "
            "prospects higher than men do. <bookmark mark='b'/> In 2008 Paul Eastwick and Eli Finkel ran speed-"
            "dating events and followed up. After real dates, attractiveness and earning prospects predicted "
            "romantic interest about equally for men and women. <bookmark mark='c'/> The familiar sex differences "
            "in stated preferences didn't show up in whom people actually desired. <bookmark mark='d'/> It's Part "
            "35's lesson about introspection, in romance. People's theories about what attracts them aren't a "
            "reliable account of what does."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(FadeIn(right))
            vo.wait_until("c")
            self.play(FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def variance(self):
        head = heading(r"Three sources of desire")
        A = axes([-0.6, 2.6], [0, 30], x_length=5.4, y_length=3.4, xticks=None, yticks=[0, 10, 20, 30],
                 yfmt=lambda v: f"{v:.0f}\\%", ylabel=r"variance predicted", center=[-3.3, -0.3, 0], font_size=15)
        lo = bars(A.ax, [0, 1, 2], [4, 7, 0.3], [CROWD, PERSON, AUTH], width=0.6, opacity=0.45)
        hi = bars(A.ax, [0, 1, 2], [18, 27, 0.3], [CROWD, PERSON, AUTH], width=0.6)
        names = VGroup(*[wrapped_label(t, 1.6, 14, c).next_to(A.ax.c2p(k, 0), DOWN, buff=0.15) for k, (t, c) in
                         enumerate(((r"how much you desire people", CROWD), (r"how desired they are", PERSON),
                                    (r"your desire for this one", AUTH)))])
        rng_note = label(r"ranges reported; \ the third was not predicted", font_size=14, color=GREY_B).next_to(
            A, UP, buff=0.1)
        rows = rows_of([
            (r"Joel, \ Eastwick and Finkel, \ 2017: \ two speed-dating studies, \ over 100 self-reported traits and "
             r"preferences per person, \ fed to random forests", WHITE),
            (r"they predicted 4 to 18\% of how much a person desired partners in general, \ and 7 to 27\% of how "
             r"desired a person was by others", CROWD),
            (r"but the part that is unique to the pair, \ this person's desire for that person, \ they could not "
             r"predict at all", AUTH),
            (r"compatibility, \ if it exists, \ is not visible in questionnaires taken before two people meet", YOU),
        ], 6.0, 20, 0.36).move_to([3.4, -0.3, 0])
        tag = published_tag(r"Joel, \ Eastwick \& Finkel (2017)")
        with self.voiceover(
            "Desire has three parts. How much you desire people in general, how desired a person is by everyone, "
            "and what's unique to a particular pair. <bookmark mark='a'/> In 2017 Samantha Joel, Eastwick and "
            "Finkel fed more than a hundred self-reported traits and preferences per person, from two speed-dating "
            "studies, to machine learning. <bookmark mark='b'/> The models predicted four to eighteen percent of "
            "how much a person desired partners in general, and seven to twenty-seven percent of how desired a "
            "person was. <bookmark mark='c'/> But the part unique to the pair, this person's desire for that "
            "person, they couldn't predict at all. <bookmark mark='d'/> Compatibility, if it exists, isn't visible "
            "in questionnaires filled in before two people meet."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names), FadeIn(rng_note))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(*[GrowFromEdge(b_, DOWN) for b_ in hi[:2]], *[GrowFromEdge(b_, DOWN) for b_ in lo[:2]],
                      FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(hi[2]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
