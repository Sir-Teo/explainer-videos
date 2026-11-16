from __future__ import annotations

from videos.psychology.psych35.common import *  # noqa: F403


class Self(VoiceoverScene):
    def construct(self):
        self.card()
        self.flattering()
        self.consensus()
        self.dk()
        self.noise()

    def card(self):
        card = chapter_card(5, r"The self's illusions", r"How well do people know how good they are?",
                            lit={1977: r"Ross et al.", 1981: r"Svenson", 1999: r"Kruger \& Dunning",
                                 2004: r"Mezulis et al."}, part=PART, scale=("person",), marr=("what",))
        with self.voiceover("Chapter five. The self's illusions."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def flattering(self):
        head = heading(r"Above the median, \ almost all of us")
        A = axes([-0.6, 1.6], [0, 100], x_length=4.4, y_length=3.6, xticks=None, yticks=[0, 50, 100],
                 yfmt=lambda v: f"{v:.0f}\\%", ylabel=r"rated themselves above the median driver",
                 center=[-3.9, -0.3, 0], font_size=15)
        b = bars(A.ax, [0, 1], [93, 69], [PERSON, CROWD], width=0.6)
        half = DashedLine(A.ax.c2p(-0.6, 50), A.ax.c2p(1.6, 50), color=GREY_B, stroke_width=2)
        hl = label(r"at most half", font_size=14, color=GREY_B).next_to(A.ax.c2p(1.6, 50), RIGHT, buff=0.1)
        names = VGroup(label(r"US students", font_size=15, color=PERSON).next_to(A.ax.c2p(0, 0), DOWN, buff=0.15),
                       label(r"Swedish students", font_size=15, color=CROWD).next_to(A.ax.c2p(1, 0), DOWN, buff=0.15))
        rows = rows_of([
            (r"Svenson, \ 1981: \ 93\% of an American sample rated themselves more skilful than the median "
             r"driver; \ about 69\% of a Swedish sample did", WHITE),
            (r"by definition only half can be above the median: \ the better-than-average effect", PERSON),
            (r"a preregistered replication in 2023, \ with 1{,}203 people, \ found the same majority", GOOD),
            (r"Mezulis and colleagues, \ 2004: \ across 266 studies, \ people credit successes to themselves and "
             r"failures to circumstances, \ $d = 0.96$, \ less so with depression and in some cultures", MODEL),
        ], 6.2, 20, 0.34).move_to([3.2, -0.3, 0])
        tag = published_tag(r"Svenson (1981); \ Mezulis et al.\ (2004)")
        with self.voiceover(
            "People read their own minds with a thumb on the scale. <bookmark mark='a'/> In 1981 Ola Svenson asked "
            "students to compare their driving with other drivers in their group. Ninety-three percent of an "
            "American sample rated themselves more skilful than the median driver, and about sixty-nine percent "
            "of a Swedish sample. <bookmark mark='b'/> Only half can be above the median. It's called the "
            "better-than-average effect. <bookmark mark='c'/> A preregistered replication in 2023, with twelve "
            "hundred people, found the same majority. <bookmark mark='d'/> And in 2004 Mezulis and colleagues "
            "pooled two hundred and sixty-six studies: people credit their successes to themselves and their "
            "failures to circumstances, a large effect, weaker in depression and in some cultures."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names), Create(half), FadeIn(hl))
            vo.wait_until("a")
            self.play(GrowFromEdge(b[0], DOWN), GrowFromEdge(b[1], DOWN), FadeIn(rows[0]))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def consensus(self):
        head = heading(r"Most people are like me")
        sign = VGroup(Rectangle(width=2.2, height=1.4, stroke_color=PERSON, fill_color="#1B2029", fill_opacity=1),
                      label(r"EAT AT JOE'S", font_size=24, color=PERSON))
        sign[1].move_to(sign[0])
        sign.move_to([-4.0, 0.8, 0])
        rows = rows_of([
            (r"Ross, \ Greene and House, \ 1977: \ students were asked to walk around campus for half an hour "
             r"wearing a sandwich board saying ``Eat at Joe's''", WHITE),
            (r"those who agreed thought most others would agree; \ those who refused thought most others would "
             r"refuse", PERSON),
            (r"the false consensus effect: \ people take their own choice as evidence of what others would do", CROWD),
            (r"Mullen and colleagues, \ 1985: \ 115 tests, \ an effect of about $r = .3$", MODEL),
            (r"it is not irrational to use your own case as one data point; \ the error is weighting it too much", YOU),
        ], 7.6, 20, 0.34).move_to([2.4, -0.3, 0])
        tag = historical_tag(r"Ross, \ Greene \& House (1977); \ Mullen et al.\ (1985)")
        with self.voiceover(
            "People also assume others are like them. <bookmark mark='a'/> In 1977 Lee Ross and colleagues asked "
            "students to walk around campus for half an hour wearing a sandwich board that said Eat at Joe's. "
            "<bookmark mark='b'/> Those who agreed thought most others would agree. Those who refused thought most "
            "others would refuse. <bookmark mark='c'/> It's called the false consensus effect: people take their "
            "own choice as evidence of what others would do. <bookmark mark='d'/> In 1985 Mullen and colleagues "
            "pooled a hundred and fifteen tests of it and found an effect of about point three. "
            "<bookmark mark='e'/> Using your own case as one data point isn't irrational. The error is weighting it "
            "too much."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(sign))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def dk(self):
        d = load("dk")
        head = heading(r"Unskilled and unaware?")
        A = axes([0.5, 4.5], [0, 100], x_length=5.6, y_length=3.8, xticks=[1, 2, 3, 4], yticks=[0, 25, 50, 75, 100],
                 xfmt=lambda v: ["bottom", "second", "third", "top"][int(v) - 1], yfmt=lambda v: f"{v:.0f}",
                 xlabel=r"quartile of actual score", ylabel=r"percentile", center=[-3.2, -0.4, 0], font_size=15)
        qs = np.arange(1, 5)
        act = VGroup(curve(A.ax, qs, d["actual"], GOOD, stroke_width=4), scatter(A.ax, qs, d["actual"], GOOD, radius=0.07))
        ks = [(1, 12), (1, 62)]
        kd = VGroup(Dot(A.ax.c2p(1, 62), radius=0.1, color=AUTH),
                    label(r"thought 62nd", font_size=16, color=AUTH).next_to(A.ax.c2p(1, 62), UP, buff=0.1),
                    Dot(A.ax.c2p(1, 12), radius=0.1, color=GOOD),
                    label(r"scored 12th", font_size=16, color=GOOD).next_to(A.ax.c2p(1, 12), RIGHT, buff=0.1))
        key = legend([(GOOD, r"actual percentile"), (AUTH, r"self-estimate")], font_size=15).move_to(A.ax.c2p(3.4, 15))
        rows = rows_of([
            (r"Kruger and Dunning, \ 1999: \ students took tests of humour, \ grammar and logic, \ and estimated "
             r"their percentile", WHITE),
            (r"the bottom quarter scored around the 12th percentile and placed themselves around the 62nd", AUTH),
            (r"their reading: \ the skills needed to do well are the skills needed to know you did badly", PERSON),
        ], 5.6, 20, 0.34).move_to([3.6, -0.3, 0])
        tag = published_tag(r"Kruger \& Dunning (1999)")
        with self.voiceover(
            "The most famous illusion of self-knowledge has a name. <bookmark mark='a'/> In 1999 Kruger and "
            "Dunning gave students tests of humour, grammar and logic, and asked them to estimate their "
            "percentile. <bookmark mark='b'/> The bottom quarter scored around the twelfth percentile, and placed "
            "themselves around the sixty-second. <bookmark mark='c'/> Their reading was a double curse: the skills "
            "you need to do well are the skills you need to know you did badly."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(Create(act[0]), FadeIn(act[1]), FadeIn(key), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(kd), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def noise(self):
        d = load("dk")
        head = heading(r"The same picture from noise")
        A = axes([0.5, 4.5], [0, 100], x_length=5.6, y_length=3.8, xticks=[1, 2, 3, 4], yticks=[0, 25, 50, 75, 100],
                 xfmt=lambda v: ["bottom", "second", "third", "top"][int(v) - 1], yfmt=lambda v: f"{v:.0f}",
                 xlabel=r"quartile of actual score", ylabel=r"percentile", center=[-3.2, -0.4, 0], font_size=15)
        qs = np.arange(1, 5)
        act = VGroup(curve(A.ax, qs, d["actual"], GOOD, stroke_width=4), scatter(A.ax, qs, d["actual"], GOOD, radius=0.07))
        noisy = VGroup(curve(A.ax, qs, d["noisy"], AUTH, stroke_width=4), scatter(A.ax, qs, d["noisy"], AUTH, radius=0.07))
        rand = curve(A.ax, qs, d["random"], GREY_B, stroke_width=2)
        key = legend([(GOOD, r"actual"), (AUTH, r"self-estimate: \ $r = 0.3$, \ +15 points"),
                      (GREY_B, r"self-estimate: \ pure noise")], font_size=14).move_to(A.ax.c2p(3.3, 18))
        rows = rows_of([
            (r"Psyche: \ 4{,}000 people whose self-estimates correlate only 0.3 with their scores, \ and who all add "
             r"15 points of better-than-average", MODEL),
            (rf"grouped by actual quartile, \ the bottom quarter estimates the {ordinal(d['noisy'][0])} percentile and "
             rf"the top the {ordinal(d['noisy'][3])}: \ the famous shape, \ with no extra ignorance at the bottom", AUTH),
            (r"a weak correlation pulls every group's estimate toward the middle: \ regression to the mean", PERSON),
            (r"Nuhfer and colleagues, \ 2016 and 2017, \ showed random numbers mimic the graph; \ the pattern "
             r"replicates, \ and how much of it is metacognition is still argued", YOU),
        ], 5.6, 19, 0.32).move_to([3.6, -0.3, 0])
        tag = psyche_tag(r"\texttt{social.dunning\_kruger}")
        with self.voiceover(
            "But the picture can be made from noise. <bookmark mark='a'/> Here are four thousand of Psyche's "
            "people whose self-estimates correlate only point three with their real scores, and who all add "
            "fifteen points of better-than-average. <bookmark mark='b'/> Group them by actual quartile. The "
            f"bottom quarter estimates the {ordinal(d['noisy'][0])} percentile and the top quarter the "
            f"{ordinal(d['noisy'][3])}. It's the famous shape, and there's no extra ignorance at the bottom built in. "
            "<bookmark mark='c'/> A weak correlation pulls every group's estimate toward the middle. It's "
            "regression to the mean. <bookmark mark='d'/> In 2016 and 2017 Nuhfer and "
            "colleagues showed that random numbers mimic the graph. The pattern itself replicates; how much of it "
            "is a failure of self-knowledge, rather than statistics, is still argued."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Create(act[0]), FadeIn(act[1]))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(noisy[0]), FadeIn(noisy[1]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(rand), FadeIn(key), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
