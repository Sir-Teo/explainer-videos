from __future__ import annotations

from videos.psychology.psych30.common import *  # noqa: F403

AGE_COL = [BABY, OBJ, LOOK, NUM]


class Number(VoiceoverScene):
    def construct(self):
        self.card()
        self.wynn()
        self.record()
        self.ratio()
        self.later()

    def card(self):
        card = chapter_card(6, r"Number", r"Can a five-month-old add?",
                            lit={1992: r"Wynn", 2000: r"Xu \& Spelke", 2008: r"Halberda et al.",
                                 2017: r"Christodoulou et al."}, part=PART, scale=("person",), marr=("what", "how"))
        with self.voiceover("Chapter six. Number."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def wynn(self):
        head = heading(r"One plus one")
        stage = Line([-6.0, -1.4, 0], [-1.0, -1.4, 0], color=GREY_B)
        doll = lambda x: VGroup(Circle(radius=0.18, color=BABY, fill_opacity=0.6),  # noqa: E731
                                RoundedRectangle(corner_radius=0.1, width=0.4, height=0.6, color=BABY,
                                                 fill_opacity=0.4).shift(DOWN * 0.45)).move_to([x, -0.9, 0])
        d1 = doll(-4.2)
        d2 = doll(-2.8)
        scr = Rectangle(width=2.6, height=1.6, color=LOOK, fill_color=LOOK, fill_opacity=0.85).move_to([-3.5, -0.6, 0])
        rows = rows_of([
            (r"Karen Wynn, \ 1992: \ a doll is placed on a stage; \ a screen rises; \ a hand adds a second doll "
             r"behind it", WHITE),
            (r"the screen drops to show two dolls \ (possible) \ or one \ (impossible): \ 5-month-olds looked longer "
             r"at one", NUM),
            (r"two minus one, \ and one plus one equals three, \ gave the same pattern", NUM),
            (r"read as: \ infants compute the results of adding and subtracting small numbers of objects", GOOD),
        ], 5.6, 21, 0.32).move_to([3.4, -0.1, 0])
        tag = published_tag(r"Wynn (1992)")
        with self.voiceover(
            "The most famous number study is an addition. <bookmark mark='a'/> In 1992 Karen Wynn placed a doll on "
            "a small stage while a five-month-old watched. A screen rose to hide it, and a hand placed a second doll "
            "behind the screen. <bookmark mark='b'/> Then the screen dropped, to show two dolls, which is possible, "
            "or only one, which is not. Infants looked longer at one. <bookmark mark='c'/> Two minus one, and one "
            "plus one equals three, gave the same pattern. <bookmark mark='d'/> The reading: infants compute the "
            "results of adding and subtracting small numbers of objects."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), Create(stage), FadeIn(d1))
            vo.wait_until("a")
            self.play(FadeIn(scr), FadeIn(rows[0]))
            self.play(FadeIn(d2, shift=DOWN * 0.4))
            self.bring_to_front(scr)
            vo.wait_until("b")
            self.remove(d2)
            self.play(FadeOut(scr), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def record(self):
        head = heading(r"Thirty years of one plus one")
        rows = rows_of([
            (r"Wakeley, \ Rivera and Langer, \ 2000: \ a careful repetition found no reliable "
             r"effect; \ results across studies were inconsistent", LOST),
            (r"Wynn replied that most repetitions had succeeded; \ critics showed that a preference for familiar "
             r"displays could produce the pattern without arithmetic", GREY_A),
            (r"Christodoulou, \ Lac and Moore, \ 2017: \ a meta-analysis of 12 studies, \ 26 samples, \ 550 "
             r"infants: \ $d = 0.34$, \ with signs of publication bias in some tests and not others", NUM),
            (r"the pattern is more likely real than not, \ smaller than first reported; \ whether it is arithmetic "
             r"is contested", OBJ),
        ], 12.2, 25, 0.4).move_to([0, -0.2, 0])
        tag = published_tag(r"Wakeley, \ Rivera \& Langer (2000); \ Christodoulou, \ Lac \& Moore (2017)")
        with self.voiceover(
            "The record is mixed. <bookmark mark='a'/> In 2000 Wakeley, Rivera and Langer "
            "repeated the study carefully and found no reliable effect, and argued that results across studies were "
            "inconsistent. <bookmark mark='b'/> Wynn replied that most repetitions had succeeded. Critics showed "
            "that a preference for familiar displays could produce the same looking pattern without any arithmetic. "
            "<bookmark mark='c'/> In 2017 Christodoulou, Lac and Moore pooled twelve studies, with "
            "twenty-six samples and five hundred and fifty infants. The pooled effect was a d of 0.34, with signs "
            "of publication bias in some tests and not in others. <bookmark mark='d'/> So the pattern is more likely "
            "real than not, and smaller than first reported. Whether it is arithmetic is contested."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def ratio(self):
        d = load("number")
        head = heading(r"Large numbers: \ a ratio, \ sharpening with age")
        A = axes([1, 4], [0.5, 1.0], x_length=5.8, y_length=3.6, xticks=[1, 1.5, 2, 3, 4], yticks=[0.5, 0.75, 1.0],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"ratio of the two numbers",
                 ylabel=r"chance of telling them apart", center=[-3.2, -0.3, 0], font_size=16)
        cvs = VGroup(*[curve(A.ax, d["ratio"], d[f"p{i}"], AGE_COL[i], 3) for i in range(4)])
        ref = DashedLine(A.ax.c2p(1, 0.75), A.ax.c2p(4, 0.75), color=GREY_B, stroke_width=2)
        key = legend([(AGE_COL[i], rf"{a}: \ $w = {d[f'w{i}']:.2f}$") for i, a in enumerate(d["ages"])],
                     font_size=15).move_to(A.ax.c2p(3.2, 0.62))
        rows = rows_of([
            (r"Fei Xu and Elizabeth Spelke, \ 2000: \ 6-month-olds habituated to 8 dots noticed 16, \ but not 12; "
             r"\ size and brightness were controlled", WHITE),
            (r"Weber's law again \ (Part 11): \ numbers are represented with noise that grows with the number, \ so "
             r"what matters is the ratio", NUM),
            (rf"Psyche: \ ratio at 75\% correct: \ {d['thr0']:.2f} at six months, \ {d['thr1']:.2f} at nine, \ "
             rf"{d['thr3']:.2f} in adults \ (Weber fractions illustrative)", MODEL),
            (r"at nine months, \ 2:3 is told apart \ (Lipton \& Spelke, \ 2003); \ the system keeps sharpening into "
             r"adulthood", LOOK),
        ], 5.6, 21, 0.3).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{develop.ans\_correct}")
        with self.voiceover(
            "For larger numbers the evidence is cleaner. <bookmark mark='a'/> In 2000 Fei Xu and Elizabeth Spelke "
            "habituated six-month-olds to displays of eight dots, with size and brightness controlled. Infants "
            "noticed a change to sixteen, but not to twelve. <bookmark mark='b'/> It's Weber's law again, from Part "
            "11. Numbers are represented with noise that grows with the number, so what matters is the ratio. "
            f"<bookmark mark='c'/> In Psyche's version, the ratio told apart three times in four is {d['thr0']:.2f} "
            f"at six months, {d['thr1']:.2f} at nine, and {d['thr3']:.2f} in adults. The Weber fractions here are "
            "illustrative, chosen to match those infant results. <bookmark mark='d'/> At nine months, two to three "
            "is told apart, as Jennifer Lipton and Spelke found in 2003, and the system keeps sharpening into "
            "adulthood."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Create(ref))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(c) for c in cvs], lag_ratio=0.3), FadeIn(key), FadeIn(rows[1]),
                      run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def later(self):
        head = heading(r"Does number sense predict mathematics?")
        rows = rows_of([
            (r"Justin Halberda, \ Mich\`ele Mazzocco and Lisa Feigenson, \ 2008: \ 14-year-olds' acuity at "
             r"comparing dot arrays correlated with their mathematics scores back to kindergarten", WHITE),
            (r"meta-analyses since: \ a real but small correlation, \ around 0.2, \ weaker beyond about age six, "
             r"\ and partly shared with general ability", NUM),
            (r"training the approximate number system to improve school mathematics has not shown reliable "
             r"benefits", LOST),
            (r"the approximate number system is a foundation, \ but exact number words and counting are learned, "
             r"\ slowly, \ between two and four \ (Part 31)", LOOK),
        ], 12.2, 25, 0.4).move_to([0, -0.2, 0])
        tag = published_tag(r"Halberda, \ Mazzocco \& Feigenson (2008); \ Schneider et al.\ (2017)")
        with self.voiceover(
            "Does this number sense matter later? <bookmark mark='a'/> In 2008 Justin Halberda, Michèle Mazzocco "
            "and Lisa Feigenson found that fourteen-year-olds' acuity at comparing dot arrays correlated with their "
            "mathematics scores going back to kindergarten. <bookmark mark='b'/> Meta-analyses since find a real "
            "but small correlation, around 0.2, weaker beyond about age six, and partly shared with general "
            "ability. <bookmark mark='c'/> Training the approximate number system to improve school mathematics has "
            "not shown reliable benefits. <bookmark mark='d'/> The approximate system is a foundation. Exact number "
            "words and counting are learned, slowly, between about two and four, which Part 31 takes up."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
