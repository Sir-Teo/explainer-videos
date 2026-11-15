from __future__ import annotations

from videos.psychology.psych30.common import *  # noqa: F403


class Minds(VoiceoverScene):
    def construct(self):
        self.card()
        self.maxi()
        self.implicit()
        self.imitation()

    def card(self):
        card = chapter_card(9, r"Other minds", r"When do children know that others can be wrong?",
                            lit={1977: r"Meltzoff \& Moore", 1983: r"Wimmer \& Perner", 2001: r"Wellman et al.",
                                 2005: r"Onishi \& Baillargeon", 2018: r"Kulke et al."},
                            part=PART, scale=("person",), marr=("what",))
        with self.voiceover("Chapter nine. Other minds."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def maxi(self):
        head = heading(r"False belief at four")
        blue = cup(LOOK).move_to([-4.6, -0.6, 0])
        green = cup(NUM).move_to([-2.4, -0.6, 0])
        bl = label(r"where Maxi left it", font_size=16, color=LOOK).next_to(blue, DOWN, buff=0.15)
        gl = label(r"where it is now", font_size=16, color=NUM).next_to(green, DOWN, buff=0.15)
        q = label(r"where will Maxi look?", font_size=22, color=YOU).move_to([-3.5, 1.2, 0])
        rows = rows_of([
            (r"Heinz Wimmer and Josef Perner, \ 1983: \ Maxi puts his chocolate in a cupboard and goes out; \ his "
             r"mother moves it; \ where will Maxi look?", WHITE),
            (r"most three-year-olds say: \ where it is now; \ most children by about four to five say: \ where he "
             r"left it", MIND),
            (r"Henry Wellman, \ David Cross and Julanne Watson, \ 2001: \ a meta-analysis of 178 studies; \ the "
             r"shift is consistent across countries and versions of the task, \ with age the main predictor", NUM),
            (r"a theory of mind: \ knowing that others act on what they believe, \ even when it is false", GOOD),
        ], 5.6, 21, 0.32).move_to([3.4, -0.1, 0])
        tag = published_tag(r"Wimmer \& Perner (1983); \ Wellman, \ Cross \& Watson (2001)")
        with self.voiceover(
            "Infants live among other minds. When do they understand them? <bookmark mark='a'/> In 1983 Heinz "
            "Wimmer and Josef Perner told children a story. Maxi puts his chocolate in a cupboard and goes out to "
            "play. While he's away, his mother moves it. Where will Maxi look for it? <bookmark mark='b'/> Most "
            "three-year-olds say: where it is now. By about four or five, most children say: where he left it. "
            "<bookmark mark='c'/> In 2001 Henry Wellman, David Cross and Julanne Watson pooled a hundred and "
            "seventy-eight studies. The shift is consistent across countries and versions of the task, and age is "
            "the main predictor. <bookmark mark='d'/> This is a theory of mind: knowing that other people act on "
            "what they believe, even when it's false."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(blue), FadeIn(green), FadeIn(bl), FadeIn(gl), FadeIn(q))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def implicit(self):
        head = heading(r"False belief at fifteen months?")
        rows = rows_of([
            (r"Kristine Onishi and Ren\'ee Baillargeon, \ 2005: \ an actor hides a toy in a green box; \ while she "
             r"cannot see, \ it moves to the yellow one", WHITE),
            (r"15-month-olds looked longer when she searched the yellow box, \ where the toy really was: \ as if "
             r"they expected her to act on her false belief", MIND),
            (r"anticipatory looking studies, \ where infants look ahead to where an agent will search, \ seemed to "
             r"agree", MIND),
            (r"Louisa Kulke, \ Hannes Rakoczy and colleagues, \ 2018: \ a preregistered replication of four such "
             r"tasks; \ one replicated, \ and not once its confounds were removed", LOST),
            (r"other replications of looking-time versions also failed; \ multi-laboratory tests are under way; "
             r"\ the claim is contested", GREY_A),
        ], 12.2, 25, 0.38).move_to([0, -0.2, 0])
        tag = published_tag(r"Onishi \& Baillargeon (2005); \ Kulke et al.\ (2018)")
        with self.voiceover(
            "Then the instrument of this part seemed to move the age far down. <bookmark mark='a'/> In 2005 "
            "Kristine Onishi and Renée Baillargeon had an actor hide a toy in a green box. While she couldn't see, "
            "it moved to the yellow one. <bookmark mark='b'/> Fifteen-month-olds looked longer when she searched "
            "the yellow box, where the toy really was, as if they expected her to act on her false belief. "
            "<bookmark mark='c'/> Studies of anticipatory looking, where infants look ahead to where an agent will "
            "search, seemed to agree. <bookmark mark='d'/> In 2018 Louisa Kulke, Hannes Rakoczy and colleagues ran a "
            "preregistered replication of four such tasks. One replicated, and not once its confounds were removed. "
            "<bookmark mark='e'/> Other replications of looking-time versions also failed, and multi-laboratory "
            "tests are under way. The claim is contested."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def imitation(self):
        head = heading(r"Do newborns imitate?")
        rows = rows_of([
            (r"Andrew Meltzoff and Keith Moore, \ 1977: \ infants 12 to 21 days old seemed to copy an adult's "
             r"tongue protrusion, \ mouth opening and lip protrusion", WHITE),
            (r"if so, \ a link between seeing and doing, \ self and other, \ from birth", MIND),
            (r"Janine Oostenbroek and colleagues, \ 2016: \ 106 infants at 1, \ 3, \ 6 and 9 weeks, \ 11 gestures "
             r"each; \ infants produced gestures as often after control models as after matching ones", LOST),
            (r"Meltzoff's reanalysis found tongue protrusion matched; \ tongue protrusion is also what infants do "
             r"when aroused by anything interesting; \ contested", GREY_A),
        ], 12.2, 25, 0.4).move_to([0, -0.2, 0])
        tag = published_tag(r"Meltzoff \& Moore (1977); \ Oostenbroek et al.\ (2016)")
        with self.voiceover(
            "One more claim about other people starts at birth. <bookmark mark='a'/> In 1977 Andrew Meltzoff and "
            "Keith Moore reported that infants between twelve and twenty-one days old copied an adult's tongue "
            "protrusion, mouth opening and lip protrusion. <bookmark mark='b'/> If so, there's a link between "
            "seeing and doing, between self and other, from birth. <bookmark mark='c'/> In 2016 Janine Oostenbroek "
            "and colleagues followed a hundred and six infants at one, three, six and nine weeks, with eleven "
            "gestures each. Infants produced each gesture as often after control models as after matching ones. "
            "<bookmark mark='d'/> Meltzoff's reanalysis of their data found tongue protrusion matched. But tongue "
            "protrusion is also what infants do when aroused by anything interesting. Contested."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
