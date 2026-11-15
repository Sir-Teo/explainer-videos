from __future__ import annotations

from videos.psychology.psych32.common import *  # noqa: F403


class Harm(VoiceoverScene):
    def construct(self):
        self.card()
        self.timeline()
        self.buck()
        self.burt()
        self.gould()

    def card(self):
        card = chapter_card(11, r"The history of harm", r"What was done with the number?",
                            lit={1913: r"Goddard", 1917: r"Army tests", 1927: r"\emph{Buck v. Bell}"}, part=PART,
                            scale=("society",), marr=("what",))
        with self.voiceover("Chapter eleven. The history of harm."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def timeline(self):
        head = heading(r"Within twenty years")
        line = Line([-6.0, 1.9, 0], [6.0, 1.9, 0], color=GREY_B, stroke_width=3)
        events = [(1908, r"Goddard brings Binet's test to America"), (1913, r"Ellis Island"),
                  (1917, r"the Army tests"), (1924, r"the Immigration Act"), (1927, r"\emph{Buck v. Bell}")]
        marks = VGroup()
        for yr, t in events:
            x = -6.0 + 12.0 * (yr - 1905) / 25
            marks.add(VGroup(Dot([x, 1.9, 0], radius=0.08, color=HARM), label(str(yr), font_size=18, color=HARM)
                             .move_to([x, 2.25, 0]), wrapped_label(t, 2.0, 15, GREY_A).move_to([x, 1.35, 0])))
        rows = rows_of([
            (r"Henry Goddard translated Binet's scale and used it to label people ``feeble-minded''; \ at Ellis "
             r"Island he tested small, \ selected groups of immigrants and reported most of them feeble-minded, \ a "
             r"study later thoroughly discredited", WHITE),
            (r"in 1917 Robert Yerkes's committee built the Army Alpha, \ written, \ and Army Beta, \ pictorial, \ and "
             r"tested well over a million recruits; \ the results were read as showing many recruits, \ and many "
             r"immigrants, \ to be of low intelligence", G),
            (r"how much the tests shaped the 1924 Immigration Act is disputed: \ Snyderman and Herrnstein, \ 1983, \ "
             r"found Congress took little notice; \ others disagree", VERB),
        ], 12.4, 21, 0.32).move_to([0, -1.2, 0])
        tag = historical_tag(r"Snyderman \& Herrnstein (1983)")
        with self.voiceover(
            "Binet warned against reading his scale as a fixed quantity. In America, it was read exactly that way. "
            "<bookmark mark='a'/> Henry Goddard translated Binet's scale and used it to label people feeble-minded. "
            "At Ellis Island he tested small, selected groups of arriving immigrants and reported most of them "
            "feeble-minded, a study since thoroughly discredited. <bookmark mark='b'/> In 1917 a committee led by "
            "Robert Yerkes built the Army Alpha, a written test, and the Army Beta, a pictorial one for those who "
            "couldn't read English, and tested well over a million recruits. The results were read as showing that "
            "many recruits, and many immigrants, were of low intelligence. <bookmark mark='c'/> How much the tests "
            "shaped the restrictive Immigration Act of 1924 is disputed. In 1983 Mark Snyderman and Richard "
            "Herrnstein found that Congress took little notice of them; other historians disagree."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), Create(line), LaggedStart(*[FadeIn(m) for m in marks],
                                                                           lag_ratio=0.3))
            for m, r in zip("abc", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def buck(self):
        head = heading(r"\emph{Buck v. Bell}, \ 1927")
        quote = wrapped_label(r"``Three generations of imbeciles are enough.''", 10.0, 36, HARM).move_to([0, 1.6, 0])
        who = label(r"Justice Oliver Wendell Holmes, \ for the majority", font_size=22, color=GREY_A)
        who.next_to(quote, DOWN, buff=0.25)
        rows = rows_of([
            (r"Virginia's 1924 law allowed the sterilization of people in state institutions judged "
             r"``feeble-minded''; \ Carrie Buck was the test case", WHITE),
            (r"the Supreme Court upheld it, \ eight votes to one", HARM),
            (r"tens of thousands of Americans were sterilized under such laws; \ the Court has never expressly "
             r"overruled the decision, \ though \emph{Skinner v. Oklahoma}, \ 1942, \ undercut it", G),
            (r"a mental test was part of the evidence: \ a number, \ treated as a fact about a person's worth", YOU),
        ], 12.4, 23, 0.38).move_to([0, -1.3, 0])
        with self.voiceover(
            "The worst use came in court. <bookmark mark='a'/> Virginia's 1924 law allowed the sterilization of "
            "people in state institutions who were judged feeble-minded. Carrie Buck was the test case. "
            "<bookmark mark='b'/> In 1927 the Supreme Court upheld the law, eight votes to one, and Justice Oliver "
            "Wendell Holmes wrote: three generations of imbeciles are enough. <bookmark mark='c'/> Tens of thousands "
            "of Americans were sterilized under laws like it. The Court has never expressly overruled the decision, "
            "though in 1942 Skinner versus Oklahoma undercut it. <bookmark mark='d'/> A mental test was part of the "
            "evidence: a number, treated as a fact about a person's worth."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(quote), FadeIn(who), FadeIn(rows[1]))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def burt(self):
        head = heading(r"Burt's twins")
        rows = rows_of([
            (r"Cyril Burt reported IQ correlations for identical twins raised apart, \ in samples that grew over the "
             r"years", WHITE),
            (r"the correlation stayed 0.771 to three decimals while the sample size changed: \ Leon Kamin pointed "
             r"out, \ in 1974, \ how unlikely that was", G),
            (r"Leslie Hearnshaw, \ his official biographer, \ concluded in 1979 that Burt had fabricated data; \ "
             r"defenders still dispute parts of the case", HARM),
            (r"later twin studies of their own found high heritability: \ the scandal was about fraud, \ not about "
             r"the answer", VERB),
        ], 12.4, 24, 0.42).move_to([0, -0.3, 0])
        tag = historical_tag(r"Kamin (1974); \ Hearnshaw (1979)")
        with self.voiceover(
            "There's harm inside science too. <bookmark mark='a'/> Cyril Burt reported IQ correlations for "
            "identical twins raised apart, in samples that grew over the years. <bookmark mark='b'/> The correlation "
            "stayed at 0.771, to three decimal places, while the sample size changed. In 1974 Leon Kamin pointed out "
            "how unlikely that was. <bookmark mark='c'/> In 1979 Leslie Hearnshaw, Burt's official biographer, "
            "concluded that Burt had fabricated data; defenders still dispute parts of the case. "
            "<bookmark mark='d'/> Later, independent twin studies found high heritability on their own data. The "
            "scandal was about fraud, not about the answer."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def gould(self):
        head = heading(r"The critic, \ checked")
        rows = rows_of([
            (r"Stephen Jay Gould, \ 1981, \ \emph{The Mismeasure of Man}: \ a history of biased measurement, \ "
             r"including Samuel Morton's nineteenth-century skulls, \ which Gould said Morton had mismeasured to fit "
             r"his prejudices", WHITE),
            (r"Jason Lewis and colleagues, \ 2011: \ remeasured about 300 of Morton's skulls without knowing their "
             r"origin: \ Morton's measurements were mostly accurate, \ and showed no systematic bias", G),
            (r"Gould's own analysis contained errors; \ his history of how the tests were used stands", VERB),
            (r"the lesson runs both ways: \ bias can enter the critic's work as easily as the scientist's, \ and "
             r"both are checked the same way: \ by measuring again", YOU),
        ], 12.4, 23, 0.4).move_to([0, -0.3, 0])
        tag = published_tag(r"Gould (1981); \ Lewis et al.\ (2011)")
        with self.voiceover(
            "And the critics need checking too. <bookmark mark='a'/> In 1981 Stephen Jay Gould's The Mismeasure of "
            "Man told the history of biased measurement, including Samuel Morton's nineteenth-century collection of "
            "skulls, which Gould said Morton had mismeasured to fit his prejudices. <bookmark mark='b'/> In 2011 "
            "Jason Lewis and colleagues remeasured about three hundred of Morton's skulls without knowing where each "
            "came from. Morton's measurements were mostly accurate, with no systematic bias. "
            "<bookmark mark='c'/> Gould's own analysis contained errors, though his history of how the tests were "
            "used stands. <bookmark mark='d'/> The lesson runs both ways. Bias can enter the critic's work as easily "
            "as the scientist's, and both are checked the same way: by measuring again."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
