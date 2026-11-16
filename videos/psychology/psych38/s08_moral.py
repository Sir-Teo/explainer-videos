from __future__ import annotations

from videos.psychology.psych38.common import *  # noqa: F403


class Moral(VoiceoverScene):
    def construct(self):
        self.card()
        self.dumbfounding()
        self.dual()
        self.foundations()

    def card(self):
        card = chapter_card(7, r"Moral psychology", r"Do we reason our way to moral judgments?",
                            lit={1969: r"Kohlberg", 2001: r"Haidt; \ Greene et al.", 2009: r"Graham et al.",
                                 2020: r"Iurino \& Saucier"}, part=PART, scale=("brain", "person"),
                            marr=("what", "how"))
        with self.voiceover("Chapter seven. Moral psychology."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def dumbfounding(self):
        head = heading(r"The emotional dog")
        left = VGroup(word_chip(r"reasoning", color=WEST, font_size=20, width=2.6),
                      Arrow(UP * 0.0, DOWN * 0.8, color=GREY_B, buff=0),
                      word_chip(r"judgment", color=PERSON, font_size=20, width=2.6)).arrange(DOWN, buff=0.15)
        right = VGroup(word_chip(r"intuition", color=WORLD, font_size=20, width=2.6),
                       Arrow(UP * 0.0, DOWN * 0.8, color=GREY_B, buff=0),
                       word_chip(r"judgment", color=PERSON, font_size=20, width=2.6),
                       Arrow(UP * 0.0, DOWN * 0.8, color=GREY_B, buff=0),
                       word_chip(r"reasons, \ after", color=WEST, font_size=20, width=2.6)).arrange(DOWN, buff=0.15)
        left.move_to([-5.0, 0.2, 0])
        right.move_to([-2.0, 0.0, 0])
        lk = label(r"Kohlberg", font_size=16, color=GREY_A).next_to(left, UP, buff=0.25)
        lh = label(r"Haidt", font_size=16, color=GREY_A).next_to(right, UP, buff=0.25)
        rows = rows_of([
            (r"Kohlberg's stages (Part 31): \ moral development as better reasoning", WHITE),
            (r"Haidt, \ 2001: \ a story of adult siblings who sleep together once, \ with contraception, \ in "
             r"secret, \ and never again; \ most people say it is wrong, \ and when each reason is ruled out, \ some "
             r"still say so: \ ``I just know it's wrong''", WORLD),
            (r"the social intuitionist model: \ judgment comes first from intuition, \ and reasoning mostly "
             r"follows, \ to justify it to others", PERSON),
            (r"Royzman, \ Kim and Leeman, \ 2015: \ many people did not accept that the story was harmless, \ and "
             r"their beliefs about harm predicted who condemned it; \ true dumbfounding is rarer than it seemed", AUTH),
        ], 6.4, 19, 0.36).move_to([3.2, -0.2, 0])
        tag = published_tag(r"Haidt (2001); \ Royzman, \ Kim \& Leeman (2015)")
        with self.voiceover(
            "Where do moral judgments come from? <bookmark mark='a'/> For Lawrence Kohlberg, whose stages we met in "
            "Part 31, moral development was better reasoning. <bookmark mark='b'/> In 2001 Jonathan Haidt pressed a "
            "different case. People hear a story about adult siblings who sleep together once, with contraception, "
            "in secret, and never again. Most say it's wrong. And when each reason they offer is ruled out by the "
            "story, some still say so: I just know it's wrong. <bookmark mark='c'/> His social intuitionist model "
            "puts intuition first. The judgment comes fast, and reasoning mostly follows, to justify it to others. "
            "<bookmark mark='d'/> In 2015 Edward Royzman and colleagues found that many people didn't accept that the "
            "story was harmless, and their beliefs about harm predicted who condemned it. True dumbfounding is rarer "
            "than it seemed."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(left), FadeIn(lk))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(right), FadeIn(lh))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def dual(self):
        head = heading(r"Two processes in the scanner")
        sw = trolley_case("switch", width=3.0).move_to([-4.6, 1.2, 0])
        fb = trolley_case("footbridge", width=3.0).move_to([-1.6, 1.2, 0])
        ls = label(r"impersonal", font_size=17, color=WEST).next_to(sw, DOWN, buff=0.25)
        lf = label(r"personal", font_size=17, color=WORLD).next_to(fb, DOWN, buff=0.25)
        rows = rows_of([
            (r"Greene and colleagues, \ 2001: \ people judged personal dilemmas, \ like Footbridge, \ and "
             r"impersonal ones, \ like Switch, \ in a scanner", WHITE),
            (r"personal dilemmas engaged regions linked to emotion more; \ people who said yes to them took longer",
             WORLD),
            (r"the dual-process model: \ an alarm against harming someone up close, \ against a slower count of "
             r"lives", PERSON),
            (r"the response-time result rested on a few items and did not hold up in reanalysis; \ the "
             r"personal-force difference itself replicates, \ as chapter eight shows", AUTH),
        ], 6.4, 19, 0.36).move_to([3.2, -0.6, 0])
        tag = published_tag(r"Greene et al.\ (2001); \ McGuire et al.\ (2009)")
        with self.voiceover(
            "Joshua Greene took the trolley into the scanner. <bookmark mark='a'/> In 2001 he and colleagues had "
            "people judge personal dilemmas, like Footbridge, and impersonal ones, like Switch, while their brains "
            "were imaged. <bookmark mark='b'/> Personal dilemmas engaged regions linked to emotion more, and people "
            "who said yes to them took longer. <bookmark mark='c'/> The dual-process model: an alarm against "
            "harming someone up close, set against a slower count of lives. <bookmark mark='d'/> The response-time "
            "result rested on a few items and didn't hold up in a reanalysis. But the difference between pushing "
            "and switching replicates, as the next chapter shows."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(sw), FadeIn(fb), FadeIn(ls), FadeIn(lf))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def foundations(self):
        head = heading(r"Moral foundations")
        names = (r"care", r"fairness", r"loyalty", r"authority", r"purity")
        cols = (GOOD, WEST, WORLD, AUTH, MODEL)
        wheel = VGroup()
        for k, (n, c) in enumerate(zip(names, cols)):
            a = TAU * k / 5 + PI / 2
            wheel.add(word_chip(n, color=c, font_size=18, width=1.9).move_to([1.7 * np.cos(a), 1.5 * np.sin(a), 0]))
        wheel.move_to([-3.8, 0.0, 0])
        rows = rows_of([
            (r"moral foundations theory: \ intuitions about care, \ fairness, \ loyalty, \ authority and purity, \ "
             r"weighted differently across people and cultures", WHITE),
            (r"Graham, \ Haidt and Nosek, \ 2009: \ liberals weighted care and fairness most; \ conservatives "
             r"weighted all five more evenly", WEST),
            (r"Iurino and Saucier, \ 2020: \ the short questionnaire in 27 countries: \ the five-factor structure "
             r"did not hold up across them", AUTH),
            (r"a cross-cultural theory needs a measure that works across cultures: \ the Ledger calls the structure "
             r"contested", YOU),
        ], 6.4, 19, 0.36).move_to([3.2, -0.2, 0])
        tag = published_tag(r"Graham, \ Haidt \& Nosek (2009); \ Iurino \& Saucier (2020)")
        with self.voiceover(
            "Haidt and colleagues also proposed a map of moral intuitions. <bookmark mark='a'/> Moral foundations "
            "theory lists care, fairness, loyalty, authority and purity, weighted differently across people and "
            "cultures. <bookmark mark='b'/> In 2009 Jesse Graham, Haidt and Brian Nosek reported that liberals "
            "weighted care and fairness most, and conservatives weighted all five more evenly. "
            "<bookmark mark='c'/> But in 2020 Kathryn Iurino and Gerard Saucier tested the short questionnaire in "
            "twenty-seven countries, and the five-factor structure didn't hold up across them. "
            "<bookmark mark='d'/> A theory of cultural variation needs a measure that works across cultures. The "
            "Ledger calls the structure contested."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), LaggedStart(*[FadeIn(w, scale=1.2) for w in wheel], lag_ratio=0.25))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
