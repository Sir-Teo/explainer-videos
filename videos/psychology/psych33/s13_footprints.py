from __future__ import annotations

from videos.psychology.psych33.common import *  # noqa: F403


class Footprints(VoiceoverScene):
    def construct(self):
        self.card()
        self.likes()
        self.judges()
        self.targeting()

    def card(self):
        card = chapter_card(12, r"Personality from footprints", r"What can a trail of clicks reveal?",
                            lit={2013: r"Kosinski et al.", 2015: r"Youyou et al.", 2017: r"Matz et al."}, part=PART,
                            scale=("person", "society"), marr=("what",))
        with self.voiceover("Chapter twelve. Personality from footprints."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def likes(self):
        d = load("likes")
        head = heading(r"Likes, \ and what they predict")
        A = axes([0.6, 3.4], [0, 0.85], x_length=6.2, y_length=3.8, xticks=[1, 2, 3], yticks=[0, 0.2, 0.4, 0.6, 0.8],
                 xfmt=lambda v: {1: "10", 2: "100", 3: "1000"}[int(round(v))], yfmt=lambda v: f"{v:g}",
                 xlabel=r"likes used per person \ (log scale)", ylabel=r"accuracy (correlation)",
                 center=[-2.9, -0.4, 0], font_size=15)
        lk = np.log10(d["k"])
        c = VGroup(curve(A.ax, lk, d["r"], O_, stroke_width=4), scatter(A.ax, lk, d["r"], O_, radius=0.06))
        rows = rows_of([
            (r"Michal Kosinski, \ David Stillwell and Thore Graepel, \ 2013: \ 58{,}466 American volunteers who took a "
             r"personality test in a Facebook app and shared their likes", WHITE),
            (r"from likes alone, \ openness was predicted about as accurately as the test agrees with itself on a "
             r"retest; \ the other traits less well", O_),
            (r"Psyche's simulated world: \ each like leans a little on one or two traits; \ a ridge regression learns "
             r"the leanings from thousands of people", MODEL),
            (r"no single like says much; \ hundreds together say a lot: \ chapter six's aggregation again", YOU),
        ], 5.6, 20, 0.34).move_to([3.6, -0.3, 0])
        tag = published_tag(r"Kosinski et al.\ (2013); \ simulated: \ \texttt{personality.likes\_accuracy}")
        with self.voiceover(
            "The newest way to measure personality doesn't ask any questions. <bookmark mark='a'/> In 2013 Michal "
            "Kosinski, David Stillwell and Thore Graepel studied fifty-eight thousand, four hundred and sixty-six "
            "American volunteers who'd taken a personality test in a Facebook app and shared what they liked. "
            "<bookmark mark='b'/> From likes alone, openness was predicted about as accurately as the test agrees "
            "with itself on a retest, and the other traits less well. <bookmark mark='c'/> Psyche builds a "
            "simulated world in which each like leans a little on one or two traits, and a ridge regression learns "
            "the leanings from thousands of people. <bookmark mark='d'/> No single like says much. Hundreds together "
            "say a lot. It's chapter six's aggregation again, applied to clicks."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(c[0]), FadeIn(c[1]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def judges(self):
        head = heading(r"Who knows you best?")
        A = axes([0.6, 3.3], [0, 5.0], x_length=6.0, y_length=3.6, xticks=[1, 2, 3], yticks=None,
                 xfmt=lambda v: {1: "10", 2: "100", 3: "1000"}[int(round(v))], xlabel=r"likes the computer needed \ (log scale)",
                 center=[-2.9, -0.4, 0], font_size=15)
        judges = [(10, r"a colleague", GREY_A), (70, r"a friend or roommate", A_), (150, r"a family member", C_),
                  (300, r"a spouse", N_)]
        marks = VGroup()
        for i, (n, who, col) in enumerate(judges):
            x = np.log10(n)
            y = 0.9 + 1.0 * i
            marks.add(VGroup(Dot(A.ax.c2p(x, y), radius=0.1, color=col),
                             label(rf"{n}: \ {who}", font_size=18, color=col).next_to(A.ax.c2p(x, y), RIGHT, buff=0.15)))
        rows = rows_of([
            (r"Wu Youyou, \ Michal Kosinski and David Stillwell, \ 2015: \ compare the computer's estimate and people's "
             r"ratings of a friend against the person's own test", WHITE),
            (r"with 10 likes the computer beat a colleague; \ 70, \ a friend or roommate; \ 150, \ a family member; "
             r"\ 300, \ a spouse", YOU),
            (r"across the five traits, \ the computer's estimates agreed with self-reports at .56, \ friends' at .49",
             O_),
            (r"Danny Azucar and colleagues' meta-analysis, \ 2018: \ footprints on social media predict the five at "
             r"about .3 to .4", MODEL),
        ], 5.6, 20, 0.34).move_to([3.6, -0.3, 0])
        tag = published_tag(r"Youyou et al.\ (2015); \ Azucar et al.\ (2018)")
        with self.voiceover(
            "How good is that? <bookmark mark='a'/> In 2015 Wu Youyou, Michal Kosinski and David Stillwell compared "
            "the computer's estimate, and people's ratings of their friends, against each person's own test. "
            "<bookmark mark='b'/> With ten likes, the computer beat a work colleague. With seventy, a friend or "
            "roommate. With a hundred and fifty, a family member. With three hundred, a spouse. "
            "<bookmark mark='c'/> Across the five traits the computer's estimates agreed with self-reports at point "
            "five six, and friends' at point four nine. <bookmark mark='d'/> A 2018 meta-analysis by Danny Azucar "
            "and colleagues put the accuracy of social-media footprints at about point three to point four."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m_, shift=UP * 0.1) for m_ in marks], lag_ratio=0.5), FadeIn(rows[1]))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def targeting(self):
        head = heading(r"From measuring to persuading")
        rows = rows_of([
            (r"2018: \ a researcher's personality-quiz app, \ taken by about 270{,}000 people, \ had also collected "
             r"their Facebook friends' data: \ up to 87 million people, \ by Facebook's estimate, \ ended up with the "
             r"political consultancy Cambridge Analytica", WHITE),
            (r"the story said elections had been swung by personality profiling; \ how much the data were used, \ and "
             r"to what effect, \ was never shown", LOST),
            (r"Sandra Matz, \ Michal Kosinski, \ Gideon Nave and David Stillwell, \ 2017: \ field experiments reaching "
             r"over 3.5 million people: \ ads matched to extraversion or openness drew up to 40\% more clicks and up "
             r"to 50\% more purchases", O_),
            (r"Dean Eckles and colleagues replied: \ people were not randomly assigned to ads, \ and the platform's "
             r"ad delivery alone could produce differences that size", A_),
            (r"so: \ traits can be read from footprints; \ how much they move behaviour when used to target is "
             r"contested", YOU),
        ], 12.4, 21, 0.32).move_to([0, -0.3, 0])
        tag = published_tag(r"Matz et al.\ (2017); \ Eckles et al.\ (2018)")
        with self.voiceover(
            "Measuring led quickly to persuading. <bookmark mark='a'/> In 2018 it emerged that a researcher's "
            "personality-quiz app, taken by about two hundred and seventy thousand people, had also collected data "
            "on their Facebook friends. Up to eighty-seven million people's data, by Facebook's own estimate, ended "
            "up with the political consultancy Cambridge Analytica. <bookmark mark='b'/> The story was told as "
            "elections swung by personality profiling. How much the data were actually used, and with what effect, "
            "was never shown. <bookmark mark='c'/> The best evidence on targeting comes from a 2017 study by Sandra "
            "Matz, Kosinski, Gideon Nave and Stillwell. Field experiments reaching over three and a half million "
            "people found that ads matched to a person's extraversion or openness drew up to forty percent more "
            "clicks and up to fifty percent more purchases. <bookmark mark='d'/> Dean Eckles and colleagues replied "
            "that people weren't randomly assigned to the ads, and the platform's own ad delivery could produce "
            "differences of that size. <bookmark mark='e'/> So traits can be read from footprints. How much they "
            "move behaviour when used to target people is contested."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
